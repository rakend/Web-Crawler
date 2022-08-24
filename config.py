from log_classes import log_generator

# local log folder name
log_folder_name = 'logs'

# configure log
log = log_generator.generate_log(log_folder_name)
log.configure_log()

# local report folder name
report_folder_name = 'reports'

# webpages to crawl csv file name
csv_file_name = 'webpages_to_crawl.csv'

# local download folder name
download_folder_name = 'savedwebsites'

# local save file names
specials_file_name = 'specials.html'
source_file_name = 'sales-original-source.html'

# savedwebsites find cheap url
saved_websites_find_cheap_url = 'http://savedwebsites.findcheap.com.au/'

# ftp login details
ftp_server = '192.168.20.106'
ftp_user = 'savedwebsites@findcheap.com.au'
ftp_password = '12345'

# ftp allow upload
ftp_allow_upload = True
