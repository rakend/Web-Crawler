from config import log
from report_classes import get_libraries

report_generator_logger = log.get_logger(__name__)

class generate_report:

    def __init__(self, statistics, report_folder_name):
        self.statistics = statistics
        self.report_folder_name = report_folder_name
        self.statistics_html = None
        self.report_html = None
        self.report_folder_path = None
        self.report_save_location = None

    def get_status_html(self, status):
        status_html = f"""
            <tr>
                <td>
                    {status['domain_name']}
                </td>
                <td>
                    {status['category_name']}
                </td>
                <td>
                    {status['plp_status_code']}
                </td>
                <td>
                    {status['total_pages']}
                </td>
                <td>
                    {status['new_pages']}
                </td>
                <td>
                    {status['updated_pages']}
                </td>
                <td>
                    {status['failed_pages']}
                </td>
            </tr>
        """
        return status_html

    def set_statistics_html(self):
        self.statistics_html = ''
        for status in self.statistics:
            status_html = self.get_status_html(status)
            self.statistics_html = self.statistics_html + status_html

    def set_report_html(self):
        self.report_html = f"""
            <html>
                <head>
                    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" rel="stylesheet"/>
                </head>
                <body>
                    <table class="table">
                        <thead class="thead-dark">
                            <tr>
                                <th scope="col">
                                    Domain
                                </th>
                                <th scope="col">
                                    Category
                                </th>
                                <th scope="col">
                                    PLP Status Code
                                </th>
                                <th scope="col">
                                    Total Pages
                                </th>
                                <th scope="col">
                                    New Pages
                                </th>
                                <th scope="col">
                                    Updated Pages
                                </th>
                                <th scope="col">
                                    Failed Pages
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {self.statistics_html}
                        </tbody>
                    </table>
                </body>
            </html>
        """

    def prettify_report_html(self):
        parsed_html_soup_object = get_libraries.BeautifulSoup(self.report_html, 'html.parser')
        self.report_html = parsed_html_soup_object.prettify()

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

    def get_report_folder_path(self, project_folder_path):
        self.report_folder_path = self.get_sub_folder_path(project_folder_path, self.report_folder_name)
        return self.report_folder_path

    def get_current_date(self):
        time_stamp = get_libraries.datetime.now()
        current_date = time_stamp.strftime('%d-%m-%Y')
        return current_date

    def get_current_date_folder_path(self, report_folder_path):
        current_date_folder_name = self.get_current_date()
        current_date_folder_path = self.get_sub_folder_path(report_folder_path, current_date_folder_name)
        return current_date_folder_path

    def get_report_save_location(self):
        current_folder_path = self.get_current_folder_path()
        project_folder_path = self.get_project_folder_path(current_folder_path)
        report_folder_path = self.get_report_folder_path(project_folder_path)
        current_date_folder_path = self.get_current_date_folder_path(report_folder_path)
        return current_date_folder_path

    def set_report_save_location(self):
        self.report_save_location = self.get_report_save_location()

    def get_current_time(self):
        time_stamp = get_libraries.datetime.now()
        current_time = time_stamp.strftime('%H-%M-%S')
        return current_time

    def add_html_file_extension(self, file):
        html_file = file + '.html'
        return html_file

    def get_report_file_name(self):
        current_time = self.get_current_time()
        report_file_name = self.add_html_file_extension(current_time)
        return report_file_name

    def join_path_components(self, component_one, component_two):
        combined_component = get_libraries.os.path.join(component_one, component_two)
        return combined_component

    def get_report_file_path(self, report_file_name):
        report_file_path = self.join_path_components(self.report_save_location, report_file_name)
        return report_file_path

    def create_report_file(self):
        report_file_name = self.get_report_file_name()
        report_file_path = self.get_report_file_path(report_file_name)
        file = get_libraries.codecs.open(report_file_path, 'w', 'utf−8')
        file.write(self.report_html)
        file.close()

    def make_report(self):
        self.set_statistics_html()
        report_generator_logger.info(f"statistics html has been set from {self.set_statistics_html}")
        self.set_report_html()
        report_generator_logger.info(f"report html has been set from {self.set_report_html}")
        self.prettify_report_html()
        report_generator_logger.info(f"prettified report html from {self.prettify_report_html}")
        self.set_report_save_location()
        report_generator_logger.info(f"report save location has been set from {self.set_report_save_location}")
        self.create_report_file()
        report_generator_logger.info(f"report file has been created from {self.create_report_file}")