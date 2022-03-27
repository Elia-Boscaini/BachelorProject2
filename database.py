import pandas as pd
from neo4j import GraphDatabase


class Database:

    def __init__(self, action_column, trace_column, timestamp_column, uri, user, password):
        self.latest_log = None
        self.level_of_abstraction = -1
        self.action_column = action_column
        self.trace_column = trace_column
        self.timestamp_column = timestamp_column
        self.events_deleted_last_abstraction = 0
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def update_latest_log(self, data):
        if self.level_of_abstraction >= 0:
            data.to_csv(
                f"abstractions/Abstraction{self.level_of_abstraction}.csv")
        self.latest_log = data
        self.level_of_abstraction += 1

    def get_latest_log(self):
        return self.latest_log

    def get_actions(self):
        return list(self.latest_log[self.latest_log.columns[self.action_column]].unique())

    def get_action_column(self):
        return self.action_column

    def get_timestamp_column(self):
        return self.timestamp_column

    def get_trace_column(self):
        return self.trace_column

    def get_number_of_traces(self):
        n_t = self.latest_log.iloc[-1, self.trace_column]
        return n_t

    def change_event(self, row_number, column_number, new_value):
        self.latest_log.at[row_number,
                           self.latest_log.columns[column_number]] = new_value

    def delete_events(self, ids_to_delete):
        self.latest_log = self.latest_log.drop(labels=ids_to_delete, axis=0)
        self.latest_log = self.latest_log.reset_index(drop=True)
        self.events_deleted_last_abstraction = len(ids_to_delete)
        self.update_latest_log(self.latest_log)

    def initiate_tree(self):
        with self.driver.session() as session:
            for action in self.get_actions():
                session.run("Create (e:Action{name: \""+action+"\"})")
        self.driver.close()

    def update_tree(self, e1, e2, enew):
        with self.driver.session() as session:
            session.run("Create (e:Action{name: \""+enew+"\"})")
            session.run("MATCH(a:Action),(b:Action),(c:Action) WHERE a.name = \""+e1+"\" AND b.name = \"" +
                        e2+"\" AND c.name = \""+enew+"\" CREATE (c)-[r:ABSTRACTS]->(a) CREATE (c)-[r2:ABSTRACTS]->(b) ")
        self.driver.close()
