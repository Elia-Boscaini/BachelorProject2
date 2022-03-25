import pandas as pd

class Database:

    def __init__(self, action_column, trace_column, timestamp_column):
        self.latest_log = None
        self.level_of_abstraction = 0
        self.action_column = action_column
        self.trace_column = trace_column
        self.timestamp_column = timestamp_column
    
    def update_latest_log(self,data):
        data.to_csv(f"abstractions/Abstraction {self.level_of_abstraction}.csv")
        self.latest_log = data
        self.level_of_abstraction += 1

    def get_latest_log(self):
        return self.latest_log
    
    def get_actions(self):
        return list(self.data[self.action_column].unique())
    
    def get_action_column(self):
        return self.action_column

    def get_timestamp_column(self):
        return self.timestamp_column

    def get_trace_column(self):
        return self.trace_column

    def get_number_of_traces(self):
        return self.latest_log.at(-1, self.trace_column)