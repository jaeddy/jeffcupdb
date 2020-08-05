import os


def get_db_uri(user, password, host, port, dbname):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    # return f"mysql://{user}:{password}@{host}:{port}/{dbname}"
    # return f"oracle://{user}:{password}@{host}:{port}/{dbname}"


class Config(object):
    LEAGUE_ID = os.environ.get('LEAGUE_ID')
    CURRENT_YEAR = os.environ.get('CURRENT_YEAR')
    DB_URI = ""
    COOKIES = {
        "swid": os.environ.get('COOKIE_SWID'),
        "espn_s2": os.environ.get('COOKIE_ESPN_S2')
    }

    log_format = "%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s"
    log_interval = 1
    log_base_dir = ""
    console_level = 20
    rootlogger_level = 10
    filelog_level = 20
    log_backup_count = 90
    log_when = "midnight"


class EnvConfig(Config):
    config_dir = os.environ.get('CONFIG_DIR')

    DB_URI = os.environ.get('DB_URI')
    if not DB_URI:
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT')
        dbname = os.environ.get('DB_NAME')

        DB_URI = get_db_uri(user=user, password=password, host=host, port=port, dbname=dbname)

    log_base_dir = os.environ.get('LOG_BASE_DIR')

