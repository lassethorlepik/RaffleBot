from typing import Optional
from aiogram.filters.callback_data import CallbackData

class PaginationValues(CallbackData, prefix="pagination"):
    action: str
    page: Optional[int] | None = None

class LogsInfo(CallbackData, prefix="log"):
    action: str
    path: Optional[str] | None = None