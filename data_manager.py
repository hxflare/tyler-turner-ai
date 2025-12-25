import json


class Config:
    def __init__(self):
        with open("config.json") as f:
            self.json=json.load(f)
            self.ai_filename=self.json["ai-filename"]
            self.persistence_filename=self.json["persistence-filename"]
            self.bot_token=self.json["bot-token"]
            self.cache_dir=self.json["cache-dir"]
            self.bot_names=self.json["bot-names"]
            self.prompt=self.json["prompt"]