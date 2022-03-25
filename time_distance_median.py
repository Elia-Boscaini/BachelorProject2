from time_distance import TimeDistance
import numpy as np
import statistics as stat




class TimeDistanceMedian(TimeDistance):

    def __init__(self, database):
        super().__init__(database)

    def get_name(self) -> str:
        return "Median"
    
    def get_metric(self):
        all_times = self.get_time_between_events()
        actions = self.database.get_actions()
        medians = np.zeros((len(actions), len(actions)))
        for a1 in range(len(actions)):
            for a2 in range(len(actions)):
                
                medians[a1, a2] = stat.median(all_times[a1][a2]) if len(
                    all_times[a1][a2]) > 0 else np.inf
        return medians