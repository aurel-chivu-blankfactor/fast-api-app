import logging
from colorama import Fore, Style


class CustomFormatter(logging.Formatter):

    def format(self, record) -> str:
        if record.levelname == "INFO":
            record.levelname = f"{Fore.GREEN}{record.levelname}{Style.RESET_ALL}"
        elif record.levelname == "WARNING":
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        elif record.levelname == "ERROR":
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        elif record.levelname == "DEBUG":
            record.msg = f"{Fore.BLUE}{record.msg}{Style.RESET_ALL}"

        record.msg = f"    {record.msg}"

        return super().format(record)


formatter = CustomFormatter("%(levelname)s: %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = [handler]
