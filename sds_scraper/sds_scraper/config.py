from injector import singleton


@singleton
class Configuration(object):
    DATA_DIR = 'sds_data'
