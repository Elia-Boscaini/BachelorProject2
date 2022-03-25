from metric import Metric
import numpy

class TimeDistance(Metric):

    def __init__ (self, database):
        self.rawdata = database.get_latest_log()
        self.set_of_actions = database.get_actions()
        self.timestamp_column = database.get_timestamp_column()
        self.action_column = database.get_action_column()
        self.trace_column = database.get_trace_column()
        self.number_of_traces = database.get_number_of_traces()


    def get_time_between_events(self) -> numpy.ndarray:

        time_between_events = [[[] for i in range(len(self.set_of_actions()))]
                 for j in range(len(self.set_of_actions))]

        for trace in range(1, self.number_of_traces + 1): #Depends on whether the traces start from index 0 or index 1
            timestamps_of_previous_events = {}
            for event in self.rawdata[self.rawdata[self.trace_column] == trace].values:
                current_action = event[self.action_column]
                time = event[self.timestamp_column]
                #time = convert_to_seconds(time)

                for action in timestamps_of_previous_events.keys():
                    for p_time in timestamps_of_previous_events[action]:
                        time_between_events[self.set_of_actions.index(action)][self.set_of_actions.index(
                            current_action)].append(abs(time - p_time))

                        time_between_events[self.set_of_actions.index(current_action)][
                            self.set_of_actions.index(action)].append(abs(time - p_time))

                if current_action in timestamps_of_previous_events.keys():
                    previous_occurences = timestamps_of_previous_events[current_action]
                    previous_occurences.append(time)
                    timestamps_of_previous_events[current_action] = previous_occurences
                else:
                    timestamps_of_previous_events[current_action] = [time]
        
        return time_between_events

    def get_name(self) -> str:
        pass