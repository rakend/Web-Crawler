from log_classes import get_libraries

class generate_log:

    def __init__(self, log_folder_name):
        self.log_folder_name = log_folder_name
        self.log_save_location = None
        self.log_folder_path = None
        self.log_formatter = None
        self.initialize_log_file_handler_levels()

    def initialize_log_file_handler_levels(self):
        self.debug_log_file_handler = None
        self.info_log_file_handler = None
        self.warning_log_file_handler = None
        self.error_log_file_handler = None
        self.critical_log_file_handler = None

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

    def get_log_folder_path(self, project_folder_path):
        self.log_folder_path = self.get_sub_folder_path(project_folder_path, self.log_folder_name)
        return self.log_folder_path

    def get_current_date(self):
        time_stamp = get_libraries.datetime.now()
        current_date = time_stamp.strftime('%d-%m-%Y')
        return current_date

    def get_current_date_folder_path(self, log_folder_path):
        current_date_folder_name = self.get_current_date()
        current_date_folder_path = self.get_sub_folder_path(log_folder_path, current_date_folder_name)
        return current_date_folder_path

    def get_current_time(self):
        time_stamp = get_libraries.datetime.now()
        current_time = time_stamp.strftime('%H-%M-%S')
        return current_time

    def get_current_time_folder_path(self, current_date_folder_path):
        current_time_folder_name = self.get_current_time()
        current_time_folder_path = self.get_sub_folder_path(current_date_folder_path, current_time_folder_name)
        return current_time_folder_path

    def get_log_save_location(self):
        current_folder_path = self.get_current_folder_path()
        project_folder_path = self.get_project_folder_path(current_folder_path)
        log_folder_path = self.get_log_folder_path(project_folder_path)
        current_date_folder_path = self.get_current_date_folder_path(log_folder_path)
        current_time_folder_path = self.get_current_time_folder_path(current_date_folder_path)
        return current_time_folder_path

    def set_log_save_location(self):
        self.log_save_location = self.get_log_save_location()

    def set_log_formatter(self):
        self.log_formatter = get_libraries.logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def join_path_components(self, component_one, component_two):
        combined_component = get_libraries.os.path.join(component_one, component_two)
        return combined_component

    def get_log_file_handler(self, log_file_path, log_level):
        log_file_handler = get_libraries.logging.FileHandler(log_file_path, mode = 'w')
        log_file_handler.setLevel(log_level)
        log_file_handler.setFormatter(self.log_formatter)
        return log_file_handler

    def get_debug_log_file_handler(self):
        debug_log_file_path = self.join_path_components(self.log_save_location, 'debug.log')
        debug_log_level = get_libraries.logging.DEBUG
        debug_log_file_handler = self.get_log_file_handler(debug_log_file_path, debug_log_level)
        return debug_log_file_handler

    def get_info_log_file_handler(self):
        info_log_file_path = self.join_path_components(self.log_save_location, 'info.log')
        info_log_level = get_libraries.logging.INFO
        info_log_file_handler = self.get_log_file_handler(info_log_file_path, info_log_level)
        return info_log_file_handler

    def get_warning_log_file_handler(self):
        warning_log_file_path = self.join_path_components(self.log_save_location, 'warning.log')
        warning_log_level = get_libraries.logging.WARNING
        warning_log_file_handler = self.get_log_file_handler(warning_log_file_path, warning_log_level)
        return warning_log_file_handler

    def get_error_log_file_handler(self):
        error_log_file_path = self.join_path_components(self.log_save_location, 'error.log')
        error_log_level = get_libraries.logging.ERROR
        error_log_file_handler = self.get_log_file_handler(error_log_file_path, error_log_level)
        return error_log_file_handler

    def get_critical_log_file_handler(self):
        critical_log_file_path = self.join_path_components(self.log_save_location, 'critical.log')
        critical_log_level = get_libraries.logging.CRITICAL
        critical_log_file_handler = self.get_log_file_handler(critical_log_file_path, critical_log_level)
        return critical_log_file_handler

    def set_log_file_handlers(self):
        self.debug_log_file_handler = self.get_debug_log_file_handler()
        self.info_log_file_handler = self.get_info_log_file_handler()
        self.warning_log_file_handler = self.get_warning_log_file_handler()
        self.error_log_file_handler = self.get_error_log_file_handler()
        self.critical_log_file_handler = self.get_critical_log_file_handler()

    def configure_log(self):
        self.set_log_save_location()
        self.set_log_formatter()
        self.set_log_file_handlers()

    def add_log_file_handlers(self, logger):
        logger.addHandler(self.debug_log_file_handler)
        logger.addHandler(self.info_log_file_handler)
        logger.addHandler(self.warning_log_file_handler)
        logger.addHandler(self.error_log_file_handler)
        logger.addHandler(self.critical_log_file_handler)

    def get_logger(self, logger_name):
        logger = get_libraries.logging.getLogger(logger_name)
        logger.setLevel(get_libraries.logging.DEBUG)
        self.add_log_file_handlers(logger)
        return logger