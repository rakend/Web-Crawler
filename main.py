import os
import csv
import time

import config

from config import log
from ftp_classes import ftp_uploader
from report_classes import report_generator
from browser_classes import browser_manager
from crawler_classes import url_extractor
from crawler_classes import product_page_storer

main_logger = log.get_logger(__name__)

def make_tuple(*arguments):
    return tuple(arguments)

def process_product_listing_page(product_listing_page_info, chrome_driver_info):
    product_listing_page_link = product_listing_page_info[0]
    product_listing_page_link_xpath = product_listing_page_info[1]
    load_more_products = product_listing_page_info[2]
    plp_download_number = product_listing_page_info[3]
    chrome_driver = chrome_driver_info[0]
    products = url_extractor.extract_source_links_and_html(
        product_listing_page_link,
        product_listing_page_link_xpath,
        load_more_products,
        plp_download_number,
        chrome_driver
    )
    product_links, product_listing_page_source = products.get_links_and_html()
    return product_links, product_listing_page_source

def process_product_listing_page_source_and_product_links(product_listing_page_info, product_page_info, chrome_driver_info):
    product_listing_page_link = product_listing_page_info[0]
    product_listing_page_source = product_listing_page_info[1]
    product_links = product_page_info[0]
    review_xpath_1 = product_page_info[1]
    review_xpath_2 = product_page_info[2]
    review_xpath_3 = product_page_info[3]
    chrome_driver = chrome_driver_info[0]
    local_files = product_page_storer.store_product_pages(
        config.download_folder_name,
        config.specials_file_name,
        config.source_file_name,
        config.saved_websites_find_cheap_url
    )
    product_page_save_location = local_files.save_html_files(
        product_listing_page_link,
        product_listing_page_source,
        product_links,
        review_xpath_1,
        review_xpath_2,
        review_xpath_3,
        chrome_driver
    )
    status = local_files.get_status()
    return product_page_save_location, status

def process_report(statistics):
    report = report_generator.generate_report(statistics, config.report_folder_name)
    report.make_report()

def main():
    main_logger.debug(f"start of program")
    statistics = []
    main_logger.debug(f"'statistics' value set to : {statistics}")
    project_folder_path = os.path.dirname(os.path.realpath(__file__))
    csv_folder_path = os.path.join(project_folder_path, config.csv_folder_name)
    csv_file_path = os.path.join(csv_folder_path, config.csv_file_name)
    with open(csv_file_path) as csv_file, browser_manager.chrome_manager() as chrome_handler:
        csvReader = csv.DictReader(csv_file)
        main_logger.info(f"opened csv file from function : '{open.__qualname__}'")
        web_list = [dict(row) for row in csvReader]
        main_logger.debug(f"csv file contents stored in 'web_list' as list of dictionaries")
        chrome_driver = chrome_handler.get_chrome_driver()
        main_logger.info(f"'chrome_driver' set from method : '{chrome_handler.get_chrome_driver.__qualname__}'")
        print(os.linesep.join(['Read and loop through csv', '']))
        for row in web_list:
            if not row['url'] or not row['url_xpath']:
                main_logger.warning(f"url or url_xpath not found in 'row', skipped 'row' in 'web_list'")
                continue
            print(f"Processing product listing page (plp) : '{row['url']}'")
            main_logger.debug(f"'row' value set to : '{row}'")
            product_listing_page_info = make_tuple(row['url'], row['url_xpath'], row['load_more_products'], row['plp_download_number'])
            chrome_driver_info = make_tuple(chrome_driver)
            main_logger.debug(f"made tuple of 'product_listing_page_info' and 'chrome_driver_info'")
            product_links, product_listing_page_source = process_product_listing_page(product_listing_page_info, chrome_driver_info)
            main_logger.info(f"values returned from function : '{process_product_listing_page.__qualname__}'")
            product_listing_page_info = make_tuple(row['url'], product_listing_page_source)
            product_page_info = make_tuple(product_links, row['review_xpath_1'], row['review_xpath_2'], row['review_xpath_3'])
            main_logger.debug(f"made tuple of 'product_listing_page_info' and 'product_page_info'")
            product_page_save_location, status = process_product_listing_page_source_and_product_links(
                product_listing_page_info, product_page_info, chrome_driver_info)
            main_logger.debug(f"'status' value set to : '{status}'")
            main_logger.info(f"values returned from function : '{process_product_listing_page_source_and_product_links.__qualname__}'")
            statistics.append(status)
            main_logger.debug(f"'status' appended to 'statistics'")
            if config.ftp_allow_upload and product_page_save_location:
                ftp = ftp_uploader.upload_via_ftp(config.ftp_server, config.ftp_user, config.ftp_password)
                ftp.upload_files_to_server(product_page_save_location, status['domain_name'], status['category_name'])
                main_logger.info(f"uploading files to server completed from method : '{ftp.upload_files_to_server.__qualname__}'")
        print('Loop through CSV file completed')
        main_logger.debug(f"loop through CSV file completed")
        process_report(statistics)
        print('Report has been generated')
        main_logger.info(f"report generated from function : '{process_report.__qualname__}'")
        main_logger.debug(f"end of program")

if __name__ == '__main__':
    main()