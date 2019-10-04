def get_db_uri(user, password, host, port, dbname):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    # return f"mysql://{user}:{password}@{host}:{port}/{dbname}"
    # return f"oracle://{user}:{password}@{host}:{port}/{dbname}"


class Config(object):
    LEAGUE_ID = 123456
    CURRENT_YEAR = 2019
    DB_URI = ""
    COOKIES = {
        "swid": "{your_swid}",
        "espn_s2": "your_espn_s2"
    }

    log_format = "%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s"
    log_interval = 1
    log_base_dir = ""
    console_level = 20
    rootlogger_level = 10
    filelog_level = 20
    log_backup_count = 90
    log_when = "midnight"


class DevConfig(Config):
    config_dir = "conf"

    user = "your_dev_user"
    password = "your_dev_pw"
    host = "localhost"
    port = "5432"
    dbname = "your_dev_db"

    log_base_dir = "log"
    # console_level = 10

    DB_URI = get_db_uri(user=user, password=password, host=host, port=port, dbname=dbname)


class ProdConfig(Config):
    config_dir = "/etc/opt/espn-ffb"

    user = "your_prod_user"
    password = "your_prod_pw"
    host = "localhost"
    port = "5432"
    dbname = "your_prod_db"

    log_base_dir = "/var/log/espn-ffb"

    DB_URI = get_db_uri(user=user, password=password, host=host, port=port, dbname=dbname)
