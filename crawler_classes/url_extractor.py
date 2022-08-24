from config import log
from crawler_classes import get_libraries

url_extractor_logger = log.get_logger(__name__)

class extract_source_links_and_html:

    def __init__(self, source_link, xpath, load_more_products, plp_download_number, chrome_driver):
        self.delay = 5
        self.timeout = 30
        self.source_link = source_link
        self.xpath = xpath
        self.load_more_products = load_more_products
        self.plp_download_number = plp_download_number
        self.chrome_driver = chrome_driver

    def open_source_link(self):
        self.chrome_driver.set_page_load_timeout(self.timeout)
        self.chrome_driver.get(self.source_link)
        get_libraries.time.sleep(self.delay)

    def set_load_more_products_value(self):
        try:
            self.load_more_products = int(self.load_more_products)
        except:
            self.load_more_products = 0

    def end_of_page(self):
        self.set_load_more_products_value()
        match = False
        end_of_page_count = 0
        len_of_page = self.chrome_driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        while(match == False and end_of_page_count < self.load_more_products):
            end_of_page_count = end_of_page_count + 1
            self.chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            get_libraries.time.sleep(self.delay)
            last_count = len_of_page
            len_of_page = self.chrome_driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if last_count == len_of_page:
                match = True

    def get_elements(self):
        elements = []
        try:
            elements = get_libraries.WebDriverWait(self.chrome_driver, self.delay).until(
                get_libraries.expected_conditions.presence_of_all_elements_located((get_libraries.By.XPATH, self.xpath))
            )
        except:
            elements = []
            url_extractor_logger.warning(f"Could not find product link xpath : {self.xpath}")
        finally:
            return elements

    def get_links_from_elements(self, elements):
        product_links = []
        for link in elements:
            product_links.append(link.get_attribute('href'))
        total_links = str(len(product_links))
        print("Total number of links found : " + total_links)
        return product_links

    def set_plp_download_number(self):
        try:
            self.plp_download_number = int(self.plp_download_number)
        except:
            self.plp_download_number = 1

    def get_links_to_download(self, product_links):
        self.set_plp_download_number()
        product_links = product_links[:self.plp_download_number]
        return product_links

    def get_page_source(self):
        html = self.chrome_driver.page_source
        get_libraries.time.sleep(self.delay)
        return html

    def get_links_and_html(self):
        try:
            self.open_source_link()
            url_extractor_logger.debug(f"source link : '{self.source_link}' opened from method : '{self.open_source_link.__qualname__}'")
            self.end_of_page()
            url_extractor_logger.info(f"scrolled to end of page from method : '{self.end_of_page.__qualname__}'")
            elements = self.get_elements()
            url_extractor_logger.info(f"product link elements returned from method : '{self.get_elements.__qualname__}'")
            product_links = self.get_links_from_elements(elements)
            url_extractor_logger.info(f"product links returned from method : '{self.get_links_from_elements.__qualname__}'")
            product_links = self.get_links_to_download(product_links)
            url_extractor_logger.info(
                f"product_links sliced to plp_download_number : '{self.plp_download_number}' from method : '{self.get_links_to_download.__qualname__}'"
            )
            source_html = self.get_page_source()
            url_extractor_logger.info(f"source link page source returned from method : '{self.get_page_source.__qualname__}'")
            return product_links, source_html
        except Exception as exception:
            print(exception)
            url_extractor_logger.exception(exception)
            return (None, None)