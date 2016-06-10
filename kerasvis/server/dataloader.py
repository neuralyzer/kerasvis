import json

import pandas as pd
import os


class LogDataLoader:
    def __init__(self, path=None):
        if path is None:
            path = "sqlite:///" + os.path.join(os.environ["HOME"], "tmp", "keras_logs.db")
        try:
            self.logs = pd.read_sql_table("log", path)
            self.runs = pd.read_sql_table("run", path).rename(columns={"id": "runid"}).sort_values("runid", ascending=False)
            self.df = self.logs.merge(self.runs)
        except ValueError:
            self.runs = pd.DataFrame({"runid":[], "comment":[], "user":[]})

    def id_exists(self, id):
        return id in self.runs.runind

    def get_overview(self):
        return self.runs.runid, self.runs.comment, self.runs.user

    def get_data(self, id):
        df = self.df[self.df.runid == id]
        df = df.sort_values("id")
        df["epoch"] = list(range(len(df)))
        return df

    def get_config(self, id):
        return self.runs[self.runs.runid == id].iloc[0]["config"]

    def id_exists(self, id):
        return (self.runs.runid == id).any()

    def get_last_update_time(self, id):
        try:
            return self.get_data(id).iloc[-1]["time"]
        except IndexError:
            return None

    def get_comment(self, id):
        return self.runs[self.runs.runid == id]["comment"].iloc[0]



def to_dict(config_string):
    """
    Convert ill formatted JSON like string to JSON decodable format.
    """
    if config_string is not None:
        try:
            return json.loads(config_string)
        except json.decoder.JSONDecodeError:
            sanitized_string = (config_string.replace("'", '"')
                  .replace("(", "[").replace(")", "]")
                  .replace("True", "true").replace("False", "false")
                  .replace("None", "\"None\""))
            return json.loads(sanitized_string)
    return {"layers": (), "optimizer": {"name": "None"}}
