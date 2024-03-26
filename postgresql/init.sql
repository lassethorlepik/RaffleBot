CREATE TABLE IF NOT EXISTS users
(
    telegram_user_id bigint PRIMARY KEY NOT NULL,
    role smallint, -- 1 for admin, 0 for registered user
);

CREATE TABLE IF NOT EXISTS raffle
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    code VARCHAR(16) NOT NULL, -- Codes should all be within 16 characters, they can never be null, that would not make sense
    redeemer_telegram_id bigint -- NULL means it is unredeemed, saves space and makes it simpler, no need to add bool redeemed
    CONSTRAINT raffle_pkey PRIMARY KEY (id)
);