from dataclasses import dataclass
import numpy as np


class LogProcessor:

    def __init__(self, database):
        self.database = database

    def abstract_log(self,set_of_actions1, set_of_actions2, newname):
        nr_events_abstracted = 0
        for n,event in enumerate(self.database.get_latest_log().values):
            if event[5] == set_of_actions1 or event[5] == set_of_actions2:
                nr_events_abstracted += 1
                self.database.change_event(n,self.database.get_action_column(),newname)
        return nr_events_abstracted


    def delete_repetitions(self):
        # keeps the mean time of the 
        rawdata = self.database.get_latest_log()
        ids_to_delete = []
        n = 0
        for trace in range(1, self.database.get_number_of_traces() + 1):
            last_event = []
            average_time = np.array([])
            for event in rawdata[rawdata[rawdata.columns[self.database.get_trace_column()]] == trace].values:
                if len(last_event) > 0 and last_event[5] == event[5]:
                    average_time = np.append(
                        average_time, last_event[3])
                    ids_to_delete.append(n)
                if len(average_time) > 0 and last_event[5] != event[5]:
                    # Maybe keep track also of the other proprieties, not only time
                    self.database.change_event(n - 1, self.database.get_timestamp_column(), average_time.mean())
                    average_time = np.array([])
                last_event = event
                n += 1
        self.database.delete_events(ids_to_delete)