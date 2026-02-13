from __future__ import annotations
import logging
import os


def get_variable_bool(name: str, default_value: bool | None = None) -> bool:
    # original from https://stackoverflow.com/questions/63116419/evaluate-boolean-environment-variable-in-python
    true_ = ('true', '1', 't')  # Add more entries if you want, like: `y`, `yes`, `on`, ...
    false_ = ('false', '0', 'f')  # Add more entries if you want, like: `n`, `no`, `off`, ...
    value: str | None = os.getenv(name, None)
    if value is None:
        if default_value is None:
            raise ValueError(f'Variable `{name}` not set!')
        else:
            value = str(default_value)
    value = value.strip("\"").strip('\'')
    if value.lower() not in true_ + false_:
        raise ValueError(f'Invalid value `{value}` for variable `{name}`')
    return value.lower() in true_


def get_variable_str(name: str, default_value: str | None = None) -> str:
    # original from https://stackoverflow.com/questions/63116419/evaluate-boolean-environment-variable-in-python
    value: str | None = os.getenv(name, None)
    if value is None:
        if default_value is None:
            raise ValueError(f'Variable `{name}` not set!')
        else:
            value = str(default_value)

    return value.strip("\"").strip('\'')


def get_variable_loglevel(name: str, default_value: str | None = None) -> int:
    # original from https://stackoverflow.com/questions/63116419/evaluate-boolean-environment-variable-in-python
    debug_ = ('debug', 'debugging', 'd')
    warn_ = ('warn', 'warning', 'w')
    error_ = ('error', 'critical', 'e')
    value: str | None = os.getenv(name, None)
    if value is None:
        if default_value is None:
            raise ValueError(f'Variable `{name}` not set!')
        else:
            value = str(default_value)
    value = value.strip("\"").strip('\'')
    if value.lower() not in debug_ + warn_ + error_:
        raise ValueError(f'Invalid value `{value}` for variable `{name}`')
    if value.lower() in debug_:
        return logging.DEBUG
    if value.lower() in warn_:
        return logging.WARN
    return logging.ERROR


def get_variable_int(name: str, default_value: int | None = None) -> int:
    # original from https://stackoverflow.com/questions/63116419/evaluate-boolean-environment-variable-in-python
    value: str | None = os.getenv(name, None)
    if value is None:
        if default_value is None:
            raise ValueError(f'Variable `{name}` not set!')
        else:
            value = str(default_value)
    value = value.strip("\"").strip('\'')
    try:
        value_int = int(value)
    except:
        raise ValueError(f'Invalid value `{value}` for variable `{name}`')
    return value_int



class RedisSessionManagerSettings:
    host = get_variable_str("REDISSESSIONMANAGERSETTINGS_HOST")
    port = get_variable_int("REDISSESSIONMANAGERSETTINGS_PORT", 6379)
    db = get_variable_int("REDISSESSIONMANAGERSETTINGS_DB", 0)

class DatabaseSettings:
    sqlalchemy_database_server_name = get_variable_str("DATABASESETTINGS_SQLALCHEMY_DATABASE_SERVER_NAME")
    sqlalchemy_database_server_port = get_variable_int("DATABASESETTINGS_SQLALCHEMY_DATABASE_SERVER_PORT")
    sqlalchemy_database_server_user = get_variable_str("DATABASESETTINGS_SQLALCHEMY_DATABASE_SERVER_USER")
    sqlalchemy_database_server_password = get_variable_str("DATABASESETTINGS_SQLALCHEMY_DATABASE_SERVER_PASSWORD")
    sqlalchemy_database_server_database = get_variable_str("DATABASESETTINGS_SQLALCHEMY_DATABASE_SERVER_DATABASE")

class ProducerSettings:
    smartland_username = get_variable_str("SMARTLAND_USERNAME")
    smartland_password = get_variable_str("SMARTLAND_PASSWORD")

class AppRoutesSettings:
    login_url = "/api/auth/login"
    logout_url = "/api/auth/logout"
    root_url = "/"
    landing_page = "/api/home/"
    error_page = "/api/fail"
    error_page_frontend = "https://consumer.tenant.lan:8443/error"
    login_page_frontend = "https://consumer.tenant.lan:8443/"
    home_url = "https://consumer.tenant.lan:8443/home"