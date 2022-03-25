from csv_reader import CSVReader


if __name__ == "__main__":
    csv_reader = CSVReader()
    data = csv_reader.read_data("Data.csv","%Y-%m-%dT%H:%M:%S.%f", 6, 8114, ";", 3)
    print(data.head())