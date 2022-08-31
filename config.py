from log_classes import log_generator

# log details
log_folder_name = 'logs'
log = log_generator.generate_log(log_folder_name)
log.configure_log()

# CSV details
csv_folder_name = 'CSVs'
csv_file_name = 'webpages_to_crawl.csv'

# report details
report_folder_name = 'reports'

# savedwebsite details
download_folder_name = 'savedwebsites'
specials_file_name = 'specials.html'
source_file_name = 'sales-original-source.html'
saved_websites_find_cheap_url = 'http://savedwebsites.findcheap.com.au/'

# ftp details
ftp_server = '192.168.20.106'
ftp_user = 'savedwebsites@findcheap.com.au'
ftp_password = '12345'
ftp_allow_upload = True
