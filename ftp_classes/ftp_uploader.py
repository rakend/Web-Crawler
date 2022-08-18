from ftp_classes import get_libraries

class upload_via_ftp:

    def __init__(self, ftp_server, ftp_user, ftp_password):
        self.ftp_server = ftp_server
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password

    def start_ftp_host_connection(self):
        ftp_host = get_libraries.ftputil.FTPHost(self.ftp_server, self.ftp_user, self.ftp_password)
        return ftp_host

    def end_ftp_host_connection(self, ftp_host):
        ftp_host.close()

    def get_new_ftp_host_path(self, ftp_host, new_path_part):
        ftp_host_path = ftp_host.getcwd()
        new_ftp_host_path = get_libraries.os.path.join(ftp_host_path, new_path_part)
        new_ftp_host_path = new_ftp_host_path.replace(get_libraries.os.sep, "/")
        return new_ftp_host_path

    def change_ftp_host_path(self, ftp_host, new_path):
        if not ftp_host.path.isdir(new_path):
            ftp_host.mkdir(new_path)
        ftp_host.chdir(new_path)

    def set_ftp_save_location(self, ftp_host, domain_name, category_name):
        ftp_host_domain_path = self.get_new_ftp_host_path(ftp_host, domain_name)
        self.change_ftp_host_path(ftp_host, ftp_host_domain_path)
        ftp_host_category_path = self.get_new_ftp_host_path(ftp_host, category_name)
        self.change_ftp_host_path(ftp_host, ftp_host_category_path)

    def get_html_file_paths(self, product_page_save_location):
        html_file_paths = []
        directory = get_libraries.os.fsencode(product_page_save_location)
        for file in get_libraries.os.listdir(directory):
            file_name = get_libraries.os.fsdecode(file)
            if file_name.endswith(".html"):
                file_path = get_libraries.os.path.join(product_page_save_location, file_name)
                html_file_paths.append(file_path)
        return html_file_paths

    def save_files_to_server(self, ftp_host, html_file_paths, domain_name, category_name):
        print(f"Uploading files to private server with domain : '{domain_name}' and category : '{category_name}'")
        ftp_host_current_path = ftp_host.getcwd()
        ftp_host.synchronize_times()
        for html_file_path in html_file_paths:
            html_file_name = html_file_path.split('\\')[-1]
            ftp_host_html_file_path = self.get_new_ftp_host_path(ftp_host, html_file_name)
            ftp_host.upload_if_newer(html_file_path, ftp_host_html_file_path)

    def upload_files_to_server(self, product_page_save_location, domain_name, category_name):
        try:
            ftp_host = self.start_ftp_host_connection()
            self.set_ftp_save_location(ftp_host, domain_name, category_name)
            html_file_paths = self.get_html_file_paths(product_page_save_location)
            self.save_files_to_server(ftp_host, html_file_paths, domain_name, category_name)
            self.end_ftp_host_connection(ftp_host)
            print("Successfully uploaded files to private server")
        except Exception as exception:
            print(exception)
        finally:
            print()