import logging
import sys


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("output/bioforge.log", mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger("bioforge")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(
            log_path,
            mode="a",
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(
            sys.stdout
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
