import logging
import os
import sys


def setup_logger(output_dir=None):
    if output_dir is None:
        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        output_dir = os.path.join(project_dir, "output")

    os.makedirs(output_dir, exist_ok=True)

    log_path = os.path.join(
        output_dir,
        "bioforge.log"
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
