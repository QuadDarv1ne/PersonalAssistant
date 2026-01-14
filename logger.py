import logging
import os
from config import DEFAULT_THEME

# Настройка логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_FILE = os.getenv('LOG_FILE', 'assistant.log')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('PersonalAssistant')

# Цвета для консоли
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

def log_with_color(level: str, message: str, color: str = Colors.RESET):
    """Логировать с цветом в консоль"""
    if level == 'INFO':
        logger.info(message)
        print(f"{color}{message}{Colors.RESET}")
    elif level == 'ERROR':
        logger.error(message)
        print(f"{Colors.RED}{message}{Colors.RESET}")
    elif level == 'WARNING':
        logger.warning(message)
        print(f"{Colors.YELLOW}{message}{Colors.RESET}")
    elif level == 'DEBUG':
        logger.debug(message)
        if LOG_LEVEL == 'DEBUG':
            print(f"{Colors.BLUE}{message}{Colors.RESET}")