from dataclasses import dataclass
import numpy as np


class LogProcessor:

    def __init__(self, database):
        self.database = database
        self.action_column = database.get_action_column()
        self.timestamp_column = database.get_timestamp_column()

    def abstract_log(self,set_of_actions1, set_of_actions2, newname):
        nr_events_abstracted = 0
        for n,event in enumerate(self.database.get_latest_log().values):
            if event[self.action_column] == set_of_actions1 or event[self.action_column] == set_of_actions2:
                nr_events_abstracted += 1
                self.database.change_event(n,self.database.get_action_column(),newname)
        return nr_events_abstracted

    def filter_data_by_trace(self, trace):
        rawdata = self.database.get_latest_log()
        array_of_rows = np.array([], dtype=np.int32)
        for row, event in enumerate(rawdata.values):
            if event[self.database.get_trace_column()] == trace:
                array_of_rows = np.append(array_of_rows, row)
        return array_of_rows

    def delete_repetitions(self):
        # keeps the mean time of the 
        rawdata = self.database.get_latest_log()
        ids_to_delete = []
        rawdata_values = rawdata.values
        for trace in self.database.get_traces():
            #print(len(self.database.get_actions()))
            if (len(self.database.get_actions()) == 277):
                continue

            
            last_event = []
            last_row = None
            average_time = np.array([])
            for row in self.filter_data_by_trace(trace):
                event = rawdata_values[row, :]
                #print(event[self.action_column])
                #print(row)
                if len(last_event) > 0 and last_event[self.action_column] == event[self.action_column]:
                    #print(last_event[self.action_column] + " " + event[self.action_column])
                    average_time = np.append(
                        average_time, last_event[self.timestamp_column])
                    ids_to_delete.append(last_row)
                    
                if len(average_time) > 0 and last_event[self.action_column] != event[self.action_column]:
                    # Maybe keep track also of the other proprieties, not only time
                    self.database.change_event(last_row, self.database.get_timestamp_column(), average_time.mean())
                    average_time = np.array([])
                last_event = event
                last_row = row
                #print("Ids to delete")
                #print(ids_to_delete)
        self.database.delete_events(ids_to_delete)