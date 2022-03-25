from time_distance import TimeDistance
import numpy as np
import statistics as stat



class TimeDistanceVariance(TimeDistance):

    def get_name(self) -> str:
        return "Variance"
    

    def get_metric(self):
        all_times = super().get_time_between_events()
        medians = np.zeros((len(super.set_of_actions), len(super.set_of_actions)))
        for a1 in range(len(super.set_of_actions)):
            for a2 in range(len(super.set_of_actions)):
                
                medians[a1, a2] = stat.stdev(super.all_times[a1][a2]) if len(
                    super.all_times[a1][a2]) > 0 else np.inf
        return medians
