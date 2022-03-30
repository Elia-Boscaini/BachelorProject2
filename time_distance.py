from metric import Metric
import numpy
from database import Database

class TimeDistance(Metric):

    def __init__ (self, database: Database):
        self.database = database

    def get_time_between_events(self) -> numpy.ndarray:
        
        rawdata = self.database.get_latest_log()
        set_of_actions = self.database.get_actions()

        time_between_events = [[[] for i in range(len(set_of_actions))] for j in range(len(set_of_actions))]

        for trace in self.database.get_traces(): 
            timestamps_of_previous_events = {}
            for event in rawdata[rawdata[rawdata.columns[self.database.get_trace_column()]] == trace].values:
                current_action = event[self.database.get_action_column()]
                time = event[self.database.get_timestamp_column()]
                #time = convert_to_seconds(time)

                for action in timestamps_of_previous_events.keys():
                    for p_time in timestamps_of_previous_events[action]:
                        time_between_events[set_of_actions.index(action)][set_of_actions.index(
                            current_action)].append(abs(time - p_time))

                        time_between_events[set_of_actions.index(current_action)][
                            set_of_actions.index(action)].append(abs(time - p_time))

                if current_action in timestamps_of_previous_events.keys():
                    previous_occurences = timestamps_of_previous_events[current_action]
                    previous_occurences.append(time)
                    timestamps_of_previous_events[current_action] = previous_occurences
                else:
                    timestamps_of_previous_events[current_action] = [time]
        
        return time_between_events

    def get_name(self) -> str:
        pass