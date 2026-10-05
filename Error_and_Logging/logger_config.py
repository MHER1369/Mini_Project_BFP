import logging
import sys
from pathlib import Path


def setup_logger():
    log_path = Path(__file__).resolve().parent.parent / "Output" / "bioforge.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                log_path,
                mode="a",
                encoding="utf-8"
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger()
