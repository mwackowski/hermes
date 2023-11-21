from configparser import ConfigParser
from os.path import join, dirname, abspath

# TODO - remove after migration to postres
DB_PARENT_DIR = "/home/wladzioo/aidevs"


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(join(dirname(abspath(__file__)), filename))
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    return db
