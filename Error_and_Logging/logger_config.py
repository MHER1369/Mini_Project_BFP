import logging
import sys
from pathlib import Path


def setup_logger():
    """لاگر مشترک پروژه را برای ثبت در فایل و نمایش در کنسول آماده می‌کند."""
    logger = logging.getLogger("bioforge")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # فراخوانی دوباره، خروجی‌های تکراری ایجاد نمی‌کند.
    if logger.handlers:
        return logger

    # مسیر فایل به محل اجرای برنامه وابسته نیست.
    log_path = Path(__file__).resolve().parent.parent / "Output" / "bioforge.log"
    formatter = logging.Formatter("%(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
