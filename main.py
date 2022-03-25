from csv_reader import CSVReader
from database import Database
from log_processor import LogProcessor
from predictor import Predictor
from time_distance_median import TimeDistanceMedian
from time_distance_stdev import TimeDistanceStdev

def ask_user(event1, event2, distance):
    print("Do you want to abstract:")
    print(event1 + "-" + event2)
    print("The time distance between them is:")
    print(distance)
    return input(" Type Yes or No or Stop")


if __name__ == "__main__":

    #Read in csv
    csv_reader = CSVReader()
    data = csv_reader.read_data("Data.csv","%Y-%m-%dT%H:%M:%S.%f", 6, 8114, ";", 3)

    #Store data on database
    database = Database(5,0,3)
    database.update_latest_log(data)

    #Delete repetitions
    log_processor = LogProcessor(database)
    log_processor.delete_repetitions()

    time_distance_stdev = TimeDistanceStdev(database)
    time_distance_median = TimeDistanceMedian(database)
    metrics = [time_distance_median, time_distance_stdev]
    predictor = Predictor(metrics, database)
    
    #Main Loop
    for level_of_abstraction in range(1, 16):
        stop_abstracting = False
        predictor.predict_sum()
        sorted_pair_array, sorted_pair_labels = predictor.sort_results()

        for i in range(len(sorted_pair_array)):
            set_of_actions = database.get_actions()
            e1 = set_of_actions[sorted_pair_labels[0, i]]
            e2 = set_of_actions[sorted_pair_labels[1, i]]
            answer = ask_user(e1, e2, sorted_pair_array[i])

            if answer == "Yes":

                """tree_string = build_abstraction_tree(
                    e1, e2, level_of_abstraction, tree_string)"""

                nr_events_abstracted = log_processor.abstract_log(e1,e2,e1+e2)
                log_processor.delete_repetitions()
                #rawdata, nr_events_abstracted, set_of_actions = abstract_log(e1, e2, e1 + e2, rawdata)

                print("Abstracted {} Events".format(nr_events_abstracted))
                print(f"Now you only have {len(database.get_actions())} actions")
                print(f"{database.events_deleted_last_abstraction} have been deleted")

                #rawdata = delete_repetitions(rawdata)
                #save_process_as_png(rawdata, level_of_abstraction)
                #save_abstraction_as_csv(rawdata, level_of_abstraction)

                #generate_tree(tree_string)
                break
            elif answer == "Stop":
                stop_abstracting = True
                break
            elif answer == "No":
                continue
        if stop_abstracting:
            break
