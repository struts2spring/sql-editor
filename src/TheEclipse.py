
import logging.config

from src.view.constants import LOG_SETTINGS
from src.view.EditorSplash import MyApp


logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)

def main():
    app = MyApp(False)
    app.MainLoop()

if __name__ == '__main__':
    main()
