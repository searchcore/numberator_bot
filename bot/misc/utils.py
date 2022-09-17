import configparser

def config_read(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config
