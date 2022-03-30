import datetime
from matplotlib.pyplot import axes
import pandas as pd

class CSVReader:
    
        
    def read_data(self, filename, time_string, number_columns, number_rows, separator, timestamp_column, number_chars_timestamp):
        data = pd.read_csv(filename, separator, usecols=range(number_columns), nrows=number_rows)
        for n, event in enumerate(data.values):
            data.at[n,data.columns[timestamp_column]] = self.convert_to_seconds(event[timestamp_column], time_string, number_chars_timestamp)
        
        
        return data.sort_values(data.columns[timestamp_column], axis = 0)


    def convert_to_seconds(self, time, time_string, number_chars_timestamp):
        return datetime.datetime.strptime(
            time[0:number_chars_timestamp], time_string).timestamp()



    def convert_to_datatime(self, time, time_string):
        return datetime.datetime.fromtimestamp(time).strftime(time_string)

    def sort_timestamps(self, data, timestamp_column):
        print(data.head())
        data.sort_values(data.columns[timestamp_column], axis = 0)
        return data