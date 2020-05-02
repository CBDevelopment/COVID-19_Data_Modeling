import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import math

class Data():
    def __init__(self, date):
        self.clean_data = []
        self.change_data = []
        self.date = date
        self.dates = []
        for i in range(1, 31):
            self.dates.append(i)
        self.path = os.path.join("E:/Projects/COVID-19_Data_Modeling/finished/", self.date)
        self.import_clean_data()
        self.import_change_data()

    def read_csv(self, csv_path, call):
        with open(os.path.join(self.path, csv_path), 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                call.append(line)

    def import_clean_data(self):
        self.read_csv("clean_COVID-19_data_" + self.date + ".csv", self.clean_data)
    
    def import_change_data(self):
        self.read_csv("daily_change_COVID-19_data_" + self.date + ".csv", self.change_data)

class Graph():
    def __init__(self, state, data, clean_or_change, trend_or_raw, title, scale, degree=2, log=False):
        self.data = data
        self.clean_or_change = clean_or_change # Growth data or daily patient data
        self.trend_or_raw = trend_or_raw
        self.log = log
        self.state = state
        self.title = title + " in " + self.state
        self.scale = float(scale)
        self.degree = degree

        self.x = self.get_x_values()
        self.y = self.get_y_values(self.clean_or_change, self.scale)
        self.create_graph(self.trend_or_raw)

    def get_x_values(self):
        return self.data.dates

    def get_y_values(self, clean_or_change, scale):
        y_vals = []
        if clean_or_change == "clean":
            for i in range(len(self.data.clean_data)):
                if self.data.clean_data[i][0] == self.state:
                    for j in range(len(self.data.clean_data[i]) - 30, len(self.data.clean_data[i])):
                        y_vals.append(float(self.data.clean_data[i][j]) / scale)
        elif clean_or_change == "change":
            for i in range(len(self.data.change_data)):
                if self.data.change_data[i][0] == self.state:
                    for j in range(len(self.data.change_data[i]) - 30, len(self.data.change_data[i])):
                        y_vals.append(float(self.data.change_data[i][j]) / scale)
        return y_vals

    def set_graph_init(self):
        plt.title(self.title)
        plt.xlabel("Past 30 Days")
        plt.ylabel("Cases in " + str(self.scale) + "s")
        plt.grid(axis="y")
        plt.rc('font', size=8)
        if self.log:
            plt.yscale('log')
        else:
            plt.ylim(0, (max(self.y) + (math.sqrt(int(self.scale)) / 10)))

    def create_graph(self, trend_or_raw):
        if trend_or_raw == "trend":
            self.set_graph_init()
            fitted = np.polyfit(self.x, self.y, self.degree)
            x_space = np.linspace(min(self.x), max(self.x))
            y_space = np.polyval(fitted, x_space)
            plt.plot(x_space, y_space)
            plt.savefig(self.clean_or_change + "_" + trend_or_raw + ".png",bbox_inches='tight', pad_inches=0.75, dpi=300)
            plt.close()
        elif trend_or_raw == "raw":
            self.set_graph_init()
            plt.scatter(self.x, self.y, s=10)

            if self.clean_or_change == "change":
                plt.grid(axis="x")
            if self.log:
                plt.savefig("log_" + self.clean_or_change + "_" + trend_or_raw + ".png",bbox_inches='tight', pad_inches=0.75, dpi=300)
            else:
                plt.savefig(self.clean_or_change + "_" + trend_or_raw + ".png",bbox_inches='tight', pad_inches=0.75, dpi=300)
            plt.close()

# state_name = str(input("Which state would you like to graph?: "))
# date = str(input("From what date do you want to graph? [Input Form: Month-Day-2X]: "))
# clean_scale = float(input("What should the clean data scale be?: "))
# change_scale = float(input("What should the change data scale be?: "))

# # Get the data from a specified date
# data = Data(date)

# # Create a state folder
# os.makedirs(os.path.join(data.path, state_name))
# state_folder = os.path.join(data.path, state_name)

# # Create the graphs
# os.chdir(state_folder)
# cleanRaw = Graph(data, "clean", "raw", "Raw Growth Data", clean_scale, 3)
# cleanTrend = Graph(data, "clean", "trend", "Trend line of Growth Data", clean_scale, 3)
# changeRaw = Graph(data, "change", "raw", "Raw Data of Daily Patient Change", change_scale)
# changeTrend = Graph(data, "change", "trend", "Trend line of Daily Patient Change", change_scale)
