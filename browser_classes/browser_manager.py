from config import log
from browser_classes import get_libraries

browser_manager_logger = log.get_logger(__name__)

class chrome_manager:

    def __init__(self):
        self.chrome_driver = None
        self.chrome_options = None
        self.implicit_wait_time = 10

    def set_chrome_options(self):
        self.chrome_options = get_libraries.webdriver.ChromeOptions()
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    def set_chrome_driver(self):
        self.set_chrome_options()
        self.chrome_driver = get_libraries.webdriver.Chrome(
            service = get_libraries.ChromeService(get_libraries.ChromeDriverManager().install()),
            options = self.chrome_options
        )
        self.chrome_driver.implicitly_wait(self.implicit_wait_time)

    def get_chrome_driver(self):
        return self.chrome_driver

    def quit_chrome_driver(self):
        self.chrome_driver.quit()

    def __enter__(self):
        self.set_chrome_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit_chrome_driver()