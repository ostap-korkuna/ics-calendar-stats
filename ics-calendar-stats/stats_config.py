import json


class StatsConfig:
    def __init__(self, config: str):
        self.config = config
        with open(self.config, 'r') as conf_file:
            json_config = json.loads(conf_file.read())
            self.mailbox = json_config['mailbox']
            self.category_keywords = json_config['category_keywords']
