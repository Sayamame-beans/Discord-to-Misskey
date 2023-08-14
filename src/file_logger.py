#imports
import logging
import logging.handlers
from datetime import datetime

#logger_Formatter class
class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = (datetime.fromtimestamp(record.created)).strftime("[%Y-%m-%d %H:%M:%S]")
        return f"{timestamp}{record.levelname}: {record.getMessage()}"

#Create Logger
def get_logger(filename: str) -> logging.Logger:
    logger = logging.getLogger("FileLogger")
    logger.setLevel(logging.INFO)
    log_handler = logging.handlers.RotatingFileHandler(filename, "a", maxBytes=1048576, backupCount=8, encoding="utf_8")
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(Formatter())
    logger.addHandler(log_handler)
    return logger
