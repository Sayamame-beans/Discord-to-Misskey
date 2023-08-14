import datetime
import json
import logging
import os
import traceback
from collections import deque

import file_logger
from d2m_discord import d2mDiscord
from d2m_exception import d2mConfigLoadError
from d2m_misskey import d2mMisskey
from d2m_config_dataclass import *
from d2m_misskey_dataclass import *

class DiscordToMisskey:
    CONFIG_STRUCTURE = d2mConfig(d2mConfigDiscord("", [d2mConfigDiscordChannel()]), [d2mConfigMisskey()])
    VERSION = "0.0.0"

    def __init__(self, config_path: str, logger: logging.Logger = file_logger.get_logger("d2m_log.txt")) -> None:
        self.logger = logger
        self.config_path = os.path.abspath(config_path)

        self.config = self.config_load()

        for mi in self.config.misskey:
            self.d2mMisskey = d2mMisskey(mi.host_url, mi.token)

    def config_load(self) -> d2mConfig:
        temp = None
        result = None

        try:
            with open(self.config_path, "r", encoding="utf_8", errors="ignore") as f:
                temp = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as err:
            self.logger.warning("Please confirm the config file with referring to the template.")
            with open(os.path.dirname(self.config_path) + "/d2m_config.template", "w", encoding="utf_8", errors="ignore") as f:
                json.dump(dataclasses.asdict(self.CONFIG_STRUCTURE), f, ensure_ascii=False)
            raise d2mConfigLoadError(path=self.config_path) from err

        if temp:
            try:
                result = d2mConfig.from_dict(temp)
            except (KeyError, TypeError) as err:
                self.logger.error("Exception occured when loading config!\n\n" + traceback.format_exc())
                self.logger.warning("Please confirm the config file with referring to the template.")
                with open(os.path.dirname(self.config_path) + "/d2m_config.template", "w", encoding="utf_8", errors="ignore") as f:
                    json.dump(dataclasses.asdict(self.CONFIG_STRUCTURE), f, ensure_ascii=False, indent=2)
                raise d2mConfigLoadError(path=self.config_path) from err

        self.logger.info("Config loaded.")

        return result

    def config_save(self) -> None:
        with open(self.config_path, "w", encoding="utf_8", errors="ignore") as f:
            json.dump(dataclasses.asdict(self.config), f, ensure_ascii=False, indent=2)
        self.logger.info("Config saved.")
