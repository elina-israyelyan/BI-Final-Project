# coding = utf-8
import configparser


def get_sql_config(filename, database):
    cf = configparser.ConfigParser()
    cf.read(filename)  # Read configuration file
    # Read corresponding file parameters
    _driver = cf.get(database, "DRIVER")
    _server = cf.get(database, "Server")
    _database = cf.get(database, "Database")
    _trusted_connection = cf.get(database, "Trusted_Connection")
    _user = cf.get(database, "User")
    _password = cf.get(database, "Password")

    return _driver, _server, _database, _trusted_connection, _user, _password
