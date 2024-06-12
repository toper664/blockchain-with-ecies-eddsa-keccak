from configparser import ConfigParser

from .app import app

# config for flask app
config = ConfigParser()
config.read("config.ini")


if __name__ == "__main__":
    app.run(
        host=config.get("HOST", "host"),
        port=config.getint("HOST", "port"),
        debug=config.getboolean("DEBUG", "debug"),
    )