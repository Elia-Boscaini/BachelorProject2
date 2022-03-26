from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.util import constants

class HeuristicMiner():

    def __init__(self,database):
        self.database = database
        self.case_id_key = database.get_latest_log().columns[database.get_trace_column()]
        self.action_key = database.get_latest_log().columns[database.get_action_column()]
        self.timestamp_key = database.get_latest_log().columns[database.get_timestamp_column()]

    def save_process_as_png(self, level_of_abstraction):
        parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: self.case_id_key,
                      constants.PARAMETER_CONSTANT_ACTIVITY_KEY: self.action_key,
                      constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: self.timestamp_key}
        event_log = log_converter.apply(
            self.database.get_latest_log(), parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)
        heu_net = heuristics_miner.apply_heu(event_log, parameters=parameters)
        gviz = hn_visualizer.apply(heu_net)
        hn_visualizer.save(gviz, "abstractions_process_models/Abstraction" +
                           str(level_of_abstraction) + ".png")