from config import log
from crawler_classes import get_libraries
from crawler_classes import product_page_extractor

product_page_storer_logger = log.get_logger(__name__)

class store_product_pages:

    def __init__(self, download_folder_name, specials_file_name, source_file_name, saved_websites_find_cheap_url):
        self.download_folder_name = download_folder_name
        self.specials_file_name = specials_file_name
        self.source_file_name = source_file_name
        self.saved_websites_find_cheap_url = saved_websites_find_cheap_url
        self.initialize_domain_name()
        self.initialize_category_name()
        self.initialize_review_xpath()
        self.initialize_html_base_tag()
        self.initialize_chrome_driver()
        self.initialize_request_headers()
        self.initialize_product_page_save_location()
        self.initialize_status()

    def initialize_domain_name(self):
        self.domain_name = None

    def initialize_category_name(self):
        self.category_name = None

    def initialize_review_xpath(self):
        self.review_xpath_1 = None
        self.review_xpath_2 = None
        self.review_xpath_3 = None

    def initialize_html_base_tag(self):
        self.html_base_tag = None

    def initialize_chrome_driver(self):
        self.chrome_driver = None

    def initialize_product_page_save_location(self):
        self.product_page_save_location = None

    def initialize_status(self):
        self.status = {
            'domain_name': 'None',
            'category_name': 'None',
            'plp_status_code': 'None',
            'total_pages': '0',
            'new_pages': '0',
            'updated_pages': '0',
            'failed_pages': '0'
        }

    def initialize_request_headers(self):
        self.headers = {'user-agent': ''}

    def get_domain_name(self, url):
        url_results = get_libraries.extract(url)
        domain_name = url_results.domain
        return domain_name

    def set_domain_name(self, product_listing_page_link):
        self.domain_name = self.get_domain_name(product_listing_page_link)
        self.status['domain_name'] = self.domain_name

    def get_category_name(self, product_listing_page_link):
        path = get_libraries.urlparse(product_listing_page_link).path
        category_name = path.split('/')[-1]
        if category_name == '':
            category_name = path.split('/')[-2]
        if category_name.endswith('.html'):
            category_name = category_name.strip('.html')
        return category_name

    def set_category_name(self, product_listing_page_link):
        self.category_name = self.get_category_name(product_listing_page_link)
        self.status['category_name'] = self.category_name

    def set_review_xpath(self, review_xpath_1, review_xpath_2, review_xpath_3):
        self.review_xpath_1 = review_xpath_1
        self.review_xpath_2 = review_xpath_2
        self.review_xpath_3 = review_xpath_3

    def set_html_base_tag(self, product_listing_page_link):
        url_scheme, url_netlock = self.get_url_scheme_and_netlock(product_listing_page_link)
        self.html_base_tag = f'<base href="{url_scheme}://{url_netlock}"/>'

    def set_chrome_driver(self, chrome_driver):
        self.chrome_driver = chrome_driver

    def set_request_headers(self):
        user_agent = self.chrome_driver.execute_script("return navigator.userAgent;")
        self.headers['user-agent'] = user_agent

    def set_product_page_save_location(self):
        self.product_page_save_location = self.get_product_page_save_location()

    def get_file_safe_name(self, product_link):
        file_safe_name = ''
        for char in product_link:
            if char.isalnum():
                file_safe_name = file_safe_name + char
            else:
                file_safe_name = file_safe_name + '-'
        return file_safe_name

    def remove_leading_slash(self, url_part):
        return url_part[1:]

    def get_url_path(self, url):
        url_result = get_libraries.urlparse(url)
        url_path = url_result.path
        url_path = self.remove_leading_slash(url_path)
        return url_path

    def get_url_scheme_and_netlock(self, url):
        url_result = get_libraries.urlparse(url)
        url_scheme = url_result.scheme
        url_netlock = url_result.netloc
        return url_scheme, url_netlock

    def get_url_path_query_fragment(self, url):
        url_result = get_libraries.urlparse(url)
        path_query_fragment = ''
        if (url_result.path != ''):
            path_query_fragment = path_query_fragment + url_result.path
        if (url_result.query != ''):
            path_query_fragment = path_query_fragment + '?'
            path_query_fragment = path_query_fragment + url_result.query
        if (url_result.fragment != ''):
            path_query_fragment = path_query_fragment + '#'
            path_query_fragment = path_query_fragment + url_result.fragment
        path_query_fragment = self.remove_leading_slash(path_query_fragment)
        return path_query_fragment

    def get_current_folder_path(self):
        current_folder_path = get_libraries.os.path.dirname(get_libraries.os.path.realpath(__file__))
        return current_folder_path

    def get_project_folder_path(self, current_folder_path):
        project_folder_path = get_libraries.os.path.dirname(current_folder_path)
        return project_folder_path

    def get_sub_folder_path(self, current_folder_path, sub_folder_name):
        sub_folder_path = get_libraries.os.path.join(current_folder_path, sub_folder_name)
        if not get_libraries.os.path.isdir(sub_folder_path):
            get_libraries.os.mkdir(sub_folder_path)
        return sub_folder_path

    def get_download_folder_path(self, project_folder_path):
        save_folder_path = self.get_sub_folder_path(project_folder_path, self.download_folder_name)
        return save_folder_path

    def get_domain_folder_path(self, save_folder_path):
        domain_folder_name = self.domain_name
        domain_folder_path = self.get_sub_folder_path(save_folder_path, domain_folder_name)
        return domain_folder_path

    def get_category_folder_path(self, product_listing_page_link, domain_folder_path):
        unsafe_category_folder_name = self.get_url_path_query_fragment(product_listing_page_link)
        category_folder_name = self.get_file_safe_name(unsafe_category_folder_name)
        category_folder_path = self.get_sub_folder_path(domain_folder_path, category_folder_name)
        return category_folder_path, category_folder_name

    def get_category_folder_path_2(self, domain_folder_path):
        category_folder_name = self.category_name
        category_folder_path = self.get_sub_folder_path(domain_folder_path, category_folder_name)
        return category_folder_path

    def get_product_page_save_location(self):
        current_folder_path = self.get_current_folder_path()
        project_folder_path = self.get_project_folder_path(current_folder_path)
        download_folder_path = self.get_download_folder_path(project_folder_path)
        domain_folder_path = self.get_domain_folder_path(download_folder_path)
        # category_folder_path, category_folder_name = self.get_category_folder_path(product_listing_page_link, domain_folder_path)
        category_folder_path = self.get_category_folder_path_2(domain_folder_path)
        return category_folder_path

    def add_html_file_extension(self, file):
        html_file = file + '.html'
        return html_file

    def join_path_components(self, component_one, component_two):
        combined_component = get_libraries.os.path.join(component_one, component_two)
        return combined_component

    def get_parsed_html(self, html):
        parsed_html_soup_object = get_libraries.BeautifulSoup(html, 'html.parser')
        parsed_html = str(parsed_html_soup_object)
        return parsed_html

    def remove_old_html_file(self, path):
        if get_libraries.os.path.exists(path):
            get_libraries.os.remove(path)
            return True
        return False

    def clean_raw_html(self, raw_html, insert_base_tag):
        html_object = get_libraries.BeautifulSoup(raw_html, 'html.parser')
        if insert_base_tag:
            html_base_tag_object = get_libraries.BeautifulSoup(self.html_base_tag, 'html.parser').base
            html_object.insert(0, html_base_tag_object)
        html = str(html_object)
        return html

    def create_new_html_file(self, path, raw_html, insert_base_tag = True):
        html = self.clean_raw_html(raw_html, insert_base_tag)
        file = get_libraries.codecs.open(path, 'w', 'utf−8')
        file.write(html)
        file.close()

    def save_product_listing_page_file(self, product_listing_page_source):
        product_listing_page_source_path = self.join_path_components(self.product_page_save_location, self.source_file_name)
        self.remove_old_html_file(product_listing_page_source_path)
        self.create_new_html_file(product_listing_page_source_path, product_listing_page_source)

    def get_product_html(self, product_link):
        product_page = product_page_extractor.extract_page_html(product_link, self.review_xpath_1, self.review_xpath_2,
                                                                self.review_xpath_3, self.headers, self.chrome_driver)
        product_page_html = product_page.get_html()
        return product_page_html

    def splitShortenAndCreateFullURL(self, productLink):
        fragmentedProdUrl = get_libraries.furl.furl(productLink)
        splitProdUrl = productLink.split(fragmentedProdUrl.origin)
        if len(splitProdUrl) > 1:
            urlWOSpecialChar = get_libraries.re.sub(r'\W+', r'-', splitProdUrl[1])
            prodPage = urlWOSpecialChar.strip("-")
        else:
            urlWOSpecialChar = get_libraries.re.sub(r'\W+', r'-', splitProdUrl[0])
            prodPage = urlWOSpecialChar.strip("-")
        prodPage = "-".join(prodPage.split("-")[:15])
        return prodPage

    def save_product_file_2(self, product_link):
        product_page_html = self.get_product_html(product_link)
        product_link_path_safe_name = self.splitShortenAndCreateFullURL(product_link)
        product_link_file_name = self.add_html_file_extension(product_link_path_safe_name)
        product_path = self.join_path_components(self.product_page_save_location, product_link_file_name)
        remove_file_flag = self.remove_old_html_file(product_path)
        self.create_new_html_file(product_path, product_page_html)
        if remove_file_flag:
            self.status['updated_pages'] = str(int(self.status['updated_pages']) + 1)
        else:
            self.status['new_pages'] = str(int(self.status['new_pages']) + 1)
        return product_link_file_name

    def save_product_file(self, product_link):
        product_page_html = self.get_product_html(product_link)
        product_link_path = self.get_url_path(product_link)
        product_link_path_safe_name = self.get_file_safe_name(product_link_path)
        product_link_file_name = self.add_html_file_extension(product_link_path_safe_name)
        product_path = self.join_path_components(self.product_page_save_location, product_link_file_name)
        self.remove_old_html_file(product_path)
        self.create_new_html_file(product_path, product_page_html)

    def iterate_over_html_files(self, save_path_location):
        html_file_names = []
        directory = get_libraries.os.fsencode(save_path_location)
        for file in get_libraries.os.listdir(directory):
            file_name = get_libraries.os.fsdecode(file)
            if file_name.endswith('.html'):
                html_file_names.append(file_name)
        return html_file_names

    def get_domain_and_suffix_name(self, save_path_location):
        suffix = get_libraries.Path(save_path_location)
        domain = get_libraries.Path(suffix.parent)
        domain_name = domain.name
        suffix_name = suffix.name
        return domain_name, suffix_name

    def join_url_components(self, url_one, url_two, slash = ''):
        combined_url = get_libraries.urljoin(url_one, url_two) + slash
        return combined_url

    def create_specials_url(self, domain_name, suffix_name, html_file_name):
        specials_url = self.join_url_components(self.saved_websites_find_cheap_url, domain_name, '/')
        specials_url = self.join_url_components(specials_url, suffix_name, '/')
        specials_url = self.join_url_components(specials_url, html_file_name)
        return specials_url

    def get_specials_html(self):
        specials_html = ""
        domain_name, suffix_name = self.get_domain_and_suffix_name(self.product_page_save_location)
        html_file_names = self.iterate_over_html_files(self.product_page_save_location)
        for html_file_name in html_file_names:
            html_elements = ""
            specials_url = self.create_specials_url(domain_name, suffix_name, html_file_name)
            if html_file_name == self.specials_file_name:
                continue
            elif html_file_name == self.source_file_name:
                html_elements = f"<a href='{specials_url}'>{html_file_name}</a><br/>"
            else:
                html_elements = f"<a class ='fc_products' href='{specials_url}'>{html_file_name}</a><br/>"
            specials_html = specials_html + html_elements
        return specials_html

    def save_specials_file(self):
        specials_path = self.join_path_components(self.product_page_save_location, self.specials_file_name)
        specials_html = self.get_specials_html()
        self.remove_old_html_file(specials_path)
        self.create_new_html_file(specials_path, specials_html, False)

    def delay_console_display(self):
        console_display_wait_time = 1
        get_libraries.time.sleep(console_display_wait_time)

    def check_url_status_code(self, url):
        request = get_libraries.requests
        response = request.get(url, headers = self.headers)
        status_code = response.status_code
        self.status['plp_status_code'] = str(status_code)
        if response:
            return True
        return False

    def get_status(self):
        return self.status

    def save_html_files(self, product_listing_page_link, product_listing_page_source, product_links, review_xpath_1,
                        review_xpath_2, review_xpath_3, chrome_driver):
        try:
            self.set_domain_name(product_listing_page_link)
            product_page_storer_logger.info(f"domain name set to : '{self.domain_name}' from method : '{self.set_domain_name.__qualname__}'")
            self.set_category_name(product_listing_page_link)
            product_page_storer_logger.info(f"category name set to : '{self.category_name}' from method : '{self.set_category_name.__qualname__}'")
            self.set_review_xpath(review_xpath_1, review_xpath_2, review_xpath_3)
            product_page_storer_logger.info(
                f"review xpath set to : '{self.review_xpath_1}', '{self.review_xpath_2}', '{self.review_xpath_3}' from method : '{self.set_review_xpath.__qualname__}'"
            )
            self.set_html_base_tag(product_listing_page_link)
            product_page_storer_logger.info(f"html base tag set to : '{self.html_base_tag}' from method : '{self.set_html_base_tag.__qualname__}'")
            self.set_chrome_driver(chrome_driver)
            product_page_storer_logger.info(f"chrome_driver set from method : '{self.set_chrome_driver.__qualname__}'")
            self.set_request_headers()
            product_page_storer_logger.info(f"request header set from method : '{self.set_request_headers.__qualname__}'")
            plp_flag = self.check_url_status_code(product_listing_page_link)
            if not plp_flag:
                product_page_storer_logger.info(f"product listing page http status code failed from method : '{self.check_url_status_code.__qualname__}'")
                return self.product_page_save_location
            self.set_product_page_save_location()
            print(f"Product page save location set to : '{self.product_page_save_location}'")
            product_page_storer_logger.info(
                f"product page save location set to : '{self.product_page_save_location}' from method : '{self.set_product_page_save_location.__qualname__}'"
            )
            self.delay_console_display()
            self.save_product_listing_page_file(product_listing_page_source)
            print(f"Source HTML saved as : '{self.source_file_name}'")
            product_page_storer_logger.info(
                f"Product listing page saved as : '{self.source_file_name}' from method : '{self.save_product_listing_page_file.__qualname__}'"
            )
            print()
            self.delay_console_display()
            self.status['total_pages'] = str(len(product_links))
            print(f"Total number of links to download : {self.status['total_pages']}")
            print()
            self.delay_console_display()
            for product_link in product_links:
                product_page_storer_logger.debug(f"'product_link' value set to : '{product_link}'")
                product_link_flag = self.check_url_status_code(product_link)
                if not product_link_flag:
                    self.status['failed_pages'] = str(int(self.status['failed_pages']) + 1)
                    product_page_storer_logger.info(f"product page http status code failed from method : '{self.check_url_status_code.__qualname__}'")
                    continue
                try:
                    print(f"Fetching data from website : '{product_link}'")
                    # self.save_product_file(product_link)
                    product_link_file_name = self.save_product_file_2(product_link)
                    product_page_storer_logger.info(f"product page saved as : '{product_link_file_name}' from method : '{self.save_product_file_2.__qualname__}'")
                except Exception as exception:
                    self.status['failed_pages'] = str(int(self.status['failed_pages']) + 1)
                    print('Fetching data failed')
                    product_page_storer_logger.exception(exception)
                else:
                    print('Fetching data successful')
                    print('Webpage saved locally')
                finally:
                    print()
                    self.delay_console_display()
            print('Loop thorugh all links completed')
            self.save_specials_file()
            self.delay_console_display()
            print(f"Specials html saved as : '{self.specials_file_name}'")
            product_page_storer_logger.info(f"specials html saved as : '{self.specials_file_name}' from method : '{self.save_specials_file.__qualname__}'")
        except Exception as exception:
            print(exception)
            product_page_storer_logger.exception(exception)
        finally:
            print()
            return self.product_page_save_location