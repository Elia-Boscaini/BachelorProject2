import datetime
import pandas as pd

class CSVReader:
    
        
    def read_data(self, filename, time_string, number_columns, number_rows, separator, timestamp_column):
        data = pd.read_csv(filename, separator, usecols=range(number_columns), nrows=number_rows)
        for n, event in enumerate(data.values):
            data.at[n,data.columns[timestamp_column]] = self.convert_to_seconds(event[timestamp_column], time_string)
        return data


    def convert_to_seconds(self, time, time_string):
        return datetime.datetime.strptime(
            time[0:26], time_string).timestamp()


    def convert_to_datatime(self, time, time_string):
        return datetime.datetime.fromtimestamp(time).strftime(time_string)