from pathlib import Path
import json
import logging


log = logging.getLogger(__name__)


class ConfigurationError(ValueError):
    pass


class ConfigManager:

    def __init__(self, options):
        self.key_file = None
        self.sheet_id = None
        self.load_config(options)

    def load_config(self, options):
        path = Path(options.config_dir)
        config_file = path.joinpath("config.json")
        if path.joinpath("config.json").is_file():
            log.debug("Found config File")
            with config_file.open("r") as fobj:
                config = json.load(fobj)

            assert type(config.get("keyFile")) == str
            assert type(config.get("googleSheetId")) == str

            self.sheet_id = config.get("googleSheetId")
            self.key_file = path.joinpath(config.get("keyFile"))
        else:
            log.debug("No Valid config.json found")
            raise ConfigurationError("Missing config.json file")
