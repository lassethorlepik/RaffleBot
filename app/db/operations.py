import os
import subprocess
from datetime import datetime
from app.db import database
from app.loader import bot
import secrets
import string

# Configuration
DB_NAME = "postgres"
DB_USER = "root"
DB_HOST = "db"  # or your database host
BACKUP_FOLDER = "/backups"
BACKUP_INTERVAL = 24  # hours
LAST_BACKUP_FILENAME = f"{BACKUP_FOLDER}/last_backup.txt"


async def get_username(user_id: int) -> str:
    "Get username based on telegram id."
    try:
        chat = await bot.get_chat(user_id)
        username = chat.username
        return f"@{username}"
    except Exception as e:
        print("Error while getting username:", e)
        return "@NotFound"


def generate_raffle_code() -> str:
    "Generate a secure and unpredicable code, that is 8-characters long."
    attempt = 0
    max_attempts = 10
    while attempt < max_attempts:
        attempt += 1
        
        # Use only uppercase for readablity
        charset = string.ascii_uppercase + "1234567890!@#$%&*"  # 2887378820390246558653190730940416 Variations for security
        
        # Ensure the code has at least one uppercase letter and one symbol
        # by first selecting one character from each subset
        code = [secrets.choice(string.ascii_uppercase), secrets.choice("!@#$%&*")]
        
        # Fill the rest of the code with random choices from the full charset
        code += [secrets.choice(charset) for _ in range(6 - len(code))]
        
        # Shuffle the selected characters to randomize their order
        secrets.SystemRandom().shuffle(code)
        
        # Join the characters into a single string
        generated_code = "".join(code)
        
        if not code_exists(generated_code):
            return generated_code
        
    raise Exception("Raffle code generation out of attempts.")


async def add_code_to_db(code: str) -> None:
    "Insert a code to database."
    sql = "INSERT INTO raffle (code) VALUES ($1)"
    await sql_run(sql, code, execute=True)


async def redeem_code(code: str, userid: int) -> bool:
    "Mark a code redeemed by the given user, returns True on success."
    if is_redeemed(code):
        return False
    else:
        sql = "UPDATE raffle SET redeemer_telegram_id = $1 WHERE code = $2"
        await sql_run(sql, userid, code, execute=True)
        return True


async def check_user_redeemed(code: str, userid: int) -> bool:
    "Check if given code was redeemed by given user."
    sql = "SELECT EXISTS(SELECT 1 FROM raffle WHERE code = $1 AND redeemer_telegram_id = $2)"
    result = await sql_run(sql, code, userid, fetchval=True)
    return result


async def is_redeemed(code: str) -> bool:
    """Check if given code has been redeemed, returns false if code does not exist."""
    sql = """SELECT EXISTS(SELECT 1 FROM raffle WHERE code = $1 AND redeemer_telegram_id IS NOT NULL)"""
    result = await sql_run(sql, code, fetchval=True)
    return result


async def code_exists(code: str) -> bool:
    """Check if given code exists in database already."""
    sql = """SELECT EXISTS(SELECT 1 FROM raffle WHERE code = $1)"""
    result = await sql_run(sql, code, fetchval=True)
    return result


async def reverse_redeeming(code: str) -> None:
    "Make a code valid again, in case it was redeemed."
    sql = "UPDATE raffle SET redeemer_telegram_id = NULL WHERE code = $1"
    await sql_run(sql, code, execute=True)


async def sql_run(sql, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False, execute: bool = False):
    "Execute SQL, this should be used instead of directly accessing data to run additional functions, for example backup."
    if (execute): # ignore reads
        backupCheck() # every time checks if backup needed? If yes, do backup
    values = []
    result = None
    if fetch:
        result = await database.execute(sql, *args, fetch=True)
        values = [dict(row) for row in result]
    elif fetchval:
        values = await database.execute(sql, *args, fetchval=True)
    elif fetchrow:
        result = await database.execute(sql, *args, fetchrow=True)
        values = dict(result)
    elif execute:
        values = await database.execute(sql, *args, execute=True)
    return values


async def get_user_by_role(role: str):
    "Get users with a specific role."
    if role == "admin":
        role = 1
    elif role == "customer":
        role = 0
    else:
        role = -1
    
    sql = f"SELECT userid FROM users WHERE role >= $1"
    result = await database.execute(sql, role, fetch=True)
    values = []
    for row in result:
        values.extend(iter(row))
    return values


def backup_database() -> None:
    "Run backup procedure for the whole database."
    # Generate a timestamped backup filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{BACKUP_FOLDER}/backup_{timestamp}.sql"

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER, exist_ok=True)

    # Construct the pg_dump command
    os.environ['PGPASSWORD'] = 'password'
    backup_command = f"pg_dump -h {DB_HOST} -U {DB_USER} {DB_NAME} > {backup_filename}"

    # Execute the backup command
    result = subprocess.run(backup_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Backup failed:", result.stderr)
    else:
        print("Backup successful")
        # Update the last backup timestamp
        with open(LAST_BACKUP_FILENAME, 'w') as f:
            f.write(timestamp)


def is_time_for_backup() -> bool:
    "Returns true, if last backup was too long ago."
    if not os.path.exists(LAST_BACKUP_FILENAME):
        return True

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
    with open(LAST_BACKUP_FILENAME, 'r') as f:
        last_backup_timestamp = f.readline().strip()

    # Convert the last backup timestamp to a datetime object
    last_backup_time = datetime.strptime(last_backup_timestamp, "%Y-%m-%d_%H-%M-%S")

    # Calculate the time difference
    now = datetime.now()
    elapsed_time = now - last_backup_time

    return elapsed_time.total_seconds() >= BACKUP_INTERVAL * 3600


def backupCheck() -> None:
    "Check last backup time and make another backup if needed."
    if is_time_for_backup():
        backup_database()
        print("Database backup completed.")
    else:
        print("Backup time not reached yet.")