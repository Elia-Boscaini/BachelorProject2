import numpy
from metric import Metric


class DirectlyFollowsMetric(Metric):
    def __init__(self, database, order_matters):
        self.database = database
        self.order_matters = order_matters

    def get_name(self) -> str:
        return f"Direclty Follows Order={self.order_matters}"

    def get_metric(self) -> numpy.ndarray:

        rawdata = self.database.get_latest_log()
        set_of_actions = self.database.get_actions()

        directly_followed_sum = numpy.zeros(
            (len(set_of_actions), len(set_of_actions)))

        # Depends on whether the traces start from index 0 or index 1
        for trace in self.database.get_traces():
            previous_action = None
            for event in rawdata[rawdata[rawdata.columns[self.database.get_trace_column()]] == trace].values:
                current_action = event[self.database.get_action_column()]
                if previous_action != None:
                    if (not(self.order_matters)):
                        directly_followed_sum[set_of_actions.index(
                            current_action)][set_of_actions.index(previous_action)] += 1
                    directly_followed_sum[set_of_actions.index(
                        previous_action)][set_of_actions.index(current_action)] += 1

                previous_action = current_action

        directly_followed_sum = directly_followed_sum / \
            numpy.maximum(directly_followed_sum.sum(axis=0), 1.0e-8)
        # if (not(self.order_matters)):
        #   directly_followed_sum *= 2

        directly_followed_sum = 1 - directly_followed_sum

        return directly_followed_sum
