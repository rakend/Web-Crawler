from config import log
from crawler_classes import get_libraries

product_page_extractor_logger = log.get_logger(__name__)

class extract_page_html:

    def __init__(self, product_link, review_xpath_1, review_xpath_2, review_xpath_3, chrome_driver):
        self.delay = 5
        self.timeout = 30
        self.product_link = product_link
        self.review_xpath_1 = review_xpath_1
        self.review_xpath_2 = review_xpath_2
        self.review_xpath_3 = review_xpath_3
        self.chrome_driver = chrome_driver

    def open_product_link(self):
        self.chrome_driver.set_page_load_timeout(self.timeout)
        self.chrome_driver.get(self.product_link)
        get_libraries.time.sleep(self.delay)

    def scroll_to_end_of_page(self):
        self.chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        get_libraries.time.sleep(self.delay)

    def separate_xpath_and_clicks(self, xpath):
        splitat = len(xpath) - 3
        xpath, clicks = xpath[:splitat], xpath[splitat + 1:splitat + 2]
        clicks = int(clicks)
        return xpath, clicks

    def scroll_element_into_center(self, element):
        self.chrome_driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", element)

    def click_review_xpath(self, xpath):
        if not len(xpath):
            return None
        xpath, clicks = self.separate_xpath_and_clicks(xpath)
        for max_clicks in range(clicks):
            try:
                review_element = get_libraries.WebDriverWait(self.chrome_driver, self.delay).until(
                    get_libraries.expected_conditions.presence_of_element_located(
                        (get_libraries.By.XPATH, xpath)
                    )
                )
                get_libraries.time.sleep(self.delay)
                self.scroll_element_into_center(review_element)
                get_libraries.time.sleep(self.delay)
                review_element.click()
                get_libraries.time.sleep(self.delay)
            except:
                product_page_extractor_logger.warning(f"could not find product page xpath : {xpath}")

    def get_page_source(self):
        html = self.chrome_driver.page_source
        get_libraries.time.sleep(self.delay)
        return html

    def get_domain_name(self):
        url_results = get_libraries.extract(self.product_link)
        domain_name = url_results.domain
        return domain_name

    def get_deal_link(self):
        gotodeal_element = get_libraries.WebDriverWait(self.chrome_driver, self.delay).until(
            get_libraries.expected_conditions.presence_of_element_located(
                (get_libraries.By.XPATH, "//div[@class='gotodeal']/a")
            )
        )
        self.scroll_element_into_center(gotodeal_element)
        get_libraries.time.sleep(self.delay)
        deal_link = gotodeal_element.get_attribute('href')
        return deal_link

    def get_redirect_link(self, deal_link):
        user_agent = self.chrome_driver.execute_script("return navigator.userAgent;")
        request = get_libraries.Request(deal_link, headers={'User-Agent': user_agent})
        response = get_libraries.urlopen(request)
        redirect_link = response.geturl()
        return redirect_link

    def insert_source_url_into_html(self, redirect_link, html):
        sourceurl_tag = "<h2><a id='sourceURL' href='" + redirect_link + "' >sourceURL:" + redirect_link + "</a></h2>"
        html = sourceurl_tag + html
        return html

    def process_ozbargain_product(self, html):
        domain_name = self.get_domain_name()
        if domain_name == 'ozbargain':
            deal_link = self.get_deal_link()
            redirect_link = self.get_redirect_link(deal_link)
            html = self.insert_source_url_into_html(redirect_link, html)
        return html

    def get_html(self):
        self.open_product_link()
        product_page_extractor_logger.info(f"product link has been opened from {self.open_product_link}")
        self.scroll_to_end_of_page()
        product_page_extractor_logger.info(f"{self.scroll_to_end_of_page} has been called")
        self.click_review_xpath(self.review_xpath_1)
        product_page_extractor_logger.info(f"{self.click_review_xpath} has been called for review_xpath_1 : {self.review_xpath_1}")
        self.click_review_xpath(self.review_xpath_2)
        product_page_extractor_logger.info(f"{self.click_review_xpath} has been called for review_xpath_2 : {self.review_xpath_2}")
        self.click_review_xpath(self.review_xpath_3)
        product_page_extractor_logger.info(f"{self.click_review_xpath} has been called for review_xpath_3 : {self.review_xpath_3}")
        html = self.get_page_source()
        product_page_extractor_logger.info(f"product page source has been set from {self.get_page_source}")
        html = self.process_ozbargain_product(html)
        product_page_extractor_logger.info(f"if ozbargain product page then source has been set from {self.process_ozbargain_product}")
        return html