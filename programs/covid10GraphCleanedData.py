# from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import webbrowser
from time import sleep

os.chdir("E:\Projects\COVID-19_Data_Modeling\working\programs")

# Create a data class to take in a csv file and do things with that data
class Data:
    def __init__(self, csv, date):
        self.csv = csv
        self.date = date
        self.path = os.path.join("E:\Projects\COVID-19_Data_Modeling\working\COVID-19-master_" + self.date + "\csse_covid_19_data\csse_covid_19_time_series", self.csv)

    def organize_data(self):
        states_and_data = []
        dates = []
        with open(self.path, 'r', newline='') as file:
            reader = csv.reader(file)
            counter = 0
            for line in reader:
                # State name is index 6(Province_State); Dates start at index 11
                if counter == 0:
                    dates = line[11:]
                    counter += 1
                else:
                    temp_line = []  # holds the state in [0] and the data for each day in [1:]
                    temp_line.append(line[6])
                    temp_line.append(line[11:])
                    states_and_data.append(temp_line)
                    counter += 1
            # print(counter)
        
        clean_states_and_data = []
        for town in states_and_data:
            inClean = False
            for state in clean_states_and_data:
                if town[0] == state[0]:
                    inClean = True
                    for i in range(len(town[1])):
                        state[1][i] = int(state[1][i]) + int(town[1][i])
            if not(inClean):
                clean_states_and_data.append(town)
        return [dates, clean_states_and_data]  # output[0] is dates, output[1][i][0] is state name, output[1][i][1] is data


fileDate = str(input("What is the last date in the time_series_covid19_confirmed_US.csv file? [Input Form: Month-Day-202X]: "))
data = Data('time_series_covid19_confirmed_US.csv', fileDate)
xy = data.organize_data()

dates = xy[0] # x-axis labels
date = str(dates[-1]).replace('/', '-') # current date
path = os.path.join("E:/Projects/COVID-19_Data_Modeling/finished/" + date)
os.makedirs(path)

dates = dates[-30:] # last 30 days

def outputCsv():
    with open('E:/Projects/COVID-19_Data_Modeling/finished/' + date + '/clean_COVID-19_data_' + date + '.csv', mode='w', newline='') as cleaned:
        csv_writer = csv.writer(cleaned)
        for i in range(len(xy[1])):
            row = [xy[1][i][0]] # name of state
            for j in range(len(xy[1][i][1])): # appending the daily data from the daily data list
                row.append(xy[1][i][1][j])
            csv_writer.writerow(row)
    print("Saved CSV file as clean_COVID-19_data_" + date + ".csv")
    with open('E:/Projects/COVID-19_Data_Modeling/finished/' + date + '/daily_change_COVID-19_data_' + date + '.csv', mode='w', newline='') as change:
        csv_writer = csv.writer(change)
        for i in range(len(xy[1])):
            row = [xy[1][i][0]] # name of state
            for j in range(len(xy[1][i][1])):
                if j == 0:
                    row.append(xy[1][i][1][j])
                else:
                    change = int(xy[1][i][1][j]) - int(xy[1][i][1][j - 1])
                    row.append(change)
            csv_writer.writerow(row)
    print("Saved CSV file as daily_change_COVID-19_data_" + date + ".csv")
outputCsv()

for i in range(len(xy[1])):
    tempL = xy[1][i][1]
    for i in range(len(tempL)):
        tempL[i] = float(tempL[i]) / 1000.0 # scale down by 1000

def sortArray(dataSet):
    for row in range(1, len(dataSet)):
        current = dataSet[row]
        position = row

        while position > 0 and float(dataSet[position - 1][-1]) < float(current[-1]):
            dataSet[position] = dataSet[position - 1]
            position -= 1

        dataSet[position] = current

xyStatesFormat = []
for i in range(len(xy[1])):
    row = []
    row.append(xy[1][i][0])
    for j in range(len(xy[1][i][1])):
        row.append(xy[1][i][1][j])
    xyStatesFormat.append(row)

sortArray(xyStatesFormat) # last 10 indices are the top 10

highestList1 = xyStatesFormat[:10]
highestList = []
for i in range(len(highestList1)): # re-instituting the Data class format for graphing
    row = []
    row.append(highestList1[i][0]) # name of state
    vals = []
    for j in range(len(highestList1[i]) - 30, len(highestList1[i])):
        vals.append(highestList1[i][j])
    row.append(vals)
    highestList.append(row)

for i in range(len(highestList)):
    plt.plot(dates, highestList[i][1])

statesLabel = []
for i in range(len(highestList)):
    statesLabel.append(highestList[i][0])

# Plot top 10
plt.legend(statesLabel, loc='upper left')
# plt.yscale('log')
plt.title("Current Top 10 State Coronavirus Totals as of " + date)
plt.xticks(rotation=90)
plt.xlabel("Past 30 Days")
plt.ylabel("Cases in Thousands")
plt.grid(axis="y")
plt.ylim(0, highestList[0][1][-1] + 10.0)
plt.rc('font', size=8)
for i in range(3):
    plt.text(dates[-1], highestList[i][1][-1], highestList[i][0], horizontalalignment="right")
# plt.show()
plt.savefig("E:/Projects/COVID-19_Data_Modeling/finished/" + date + "/COVID-19_Top_10_" + date + ".png",bbox_inches='tight', pad_inches=0.75, dpi=300)
print("Saved graph as COVID-19_Top_10_" + date + ".png")
plt.close()

for i in range(len(highestList)):
    Xs = []
    for j in range(len(dates)):
        Xs.append(j)
    fitted = np.polyfit(Xs, highestList[i][1], 3)
    print("(Terciary) " + highestList[i][0] + ": " + str(fitted))
    x = np.linspace(min(Xs), max(Xs))
    y = np.polyval(fitted, x)
    plt.plot(x, y)


# Plot top 10 trendline
plt.legend(statesLabel, loc='upper left')
# plt.yscale('log')
plt.title("TRENDLINE Current Top 10 State Coronavirus Totals as of " + date)
plt.xticks(rotation=90)
plt.xlabel("Past 30 Days")
plt.ylabel("Cases in Thousands")
plt.grid(axis="y")
plt.ylim(0, highestList[0][1][-1] + 10.0)
plt.rc('font', size=8)
for i in range(3):
    plt.text(Xs[-1], highestList[i][1][-1], highestList[i][0], horizontalalignment="right")
# plt.show()
plt.savefig("E:/Projects/COVID-19_Data_Modeling/finished/" + date + "/TRENDLINE_COVID-19_Top_10_" + date + ".png",bbox_inches='tight', pad_inches=0.75, dpi=300)
print("Saved graph as TRENDLINE_COVID-19_Top_10_" + date + ".png")
plt.close()

# Plot Changes Trendline
changes = []
with open('E:/Projects/COVID-19_Data_Modeling/finished/' + date + '/daily_change_COVID-19_data_' + date + '.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for line in reader:
        changes.append(line)

sortArray(changes)

highestChange = changes[:10]

legend = []
for i in range(len(highestChange)):
    legend.append(highestChange[i][0])

scale = 10.0
for i in range(len(highestChange)):
    yVals = []
    for j in range(len(highestChange[i]) - 30, len(highestChange[i])):
        yVals.append(float(highestChange[i][j]) / scale)
    xs = []
    for k in range(len(dates)):
        xs.append(k)
    fitted2 = np.polyfit(xs, yVals, 2)
    print("(Parabolic) " + highestChange[i][0] + ": " + str(fitted2))
    x = np.linspace(min(xs), max(xs))
    y = np.polyval(fitted2, x)
    plt.plot(x, y)

plt.legend(legend, loc='upper left')
plt.title("TRENDLINE Current Top 10 State Coronavirus Count Changes Day-to-Day as of " + date)
plt.xticks(rotation=90)
plt.xlabel("Past 30 Days")
plt.ylabel("Cases in 10s")
plt.grid(axis="y")
dayTotals = []
for i in range(len(highestChange)):
    for j in range(1, len(highestChange[i])):
        dayTotals.append(float(highestChange[i][j]))

plt.ylim(0, (max(dayTotals) / scale) + 100.0)
plt.rc('font', size=8)
for i in range(3):
    plt.text(xs[-1], float(highestChange[i][-1]) / scale, highestChange[i][0], horizontalalignment="right")
# plt.show()
plt.savefig("E:/Projects/COVID-19_Data_Modeling/finished/" + date + "/TRENDLINE_COVID-19_Top_10_Count_Changes_Day-to-Day_" + date + ".png", bbox_inches='tight', pad_inches=0.75, dpi=300)
print("Saved graph as TRENDLINE_COVID-19_Top_10_Count_Changes_Day-to-Day_" + date + ".png")
plt.close()


# Plot Changes

for i in range(len(highestChange)):
    yVals = []
    for j in range(len(highestChange[i]) - 30, len(highestChange[i])):
        yVals.append(float(highestChange[i][j]) / scale)
    plt.plot(dates, yVals)

plt.legend(legend, loc='upper left')
plt.title("Current Top 10 State Coronavirus Count Changes Day-to-Day as of " + date)
plt.xticks(rotation=90)
plt.xlabel("Past 30 Days")
plt.ylabel("Cases in 10s")
plt.grid(axis="y")
dayTotals = []
for i in range(len(highestChange)):
    for j in range(1, len(highestChange[i])):
        dayTotals.append(float(highestChange[i][j]))

plt.ylim(0, (max(dayTotals) / scale) + 100.0)
plt.rc('font', size=8)
for i in range(3):
    plt.text(xs[-1], float(highestChange[i][-1]) / scale, highestChange[i][0], horizontalalignment="right")
# plt.show()
plt.savefig("E:/Projects/COVID-19_Data_Modeling/finished/" + date + "/COVID-19_Top_10_Count_Changes_Day-to-Day_" + date + ".png", bbox_inches='tight', pad_inches=0.75, dpi=300)
print("Saved graph as COVID-19_Top_10_Count_Changes_Day-to-Day_" + date + ".png")
plt.close()


webbrowser.open("https://docs.google.com/spreadsheets/d/1qPrc0bip3NbSMB_U3NZ2re_3t59oMOdrqsbTByApk3w/edit#gid=2145933813") # daily_change_COVID-19_data
webbrowser.open("https://docs.google.com/spreadsheets/d/1v33wqc3dM4zUbyIVDKVsMb-jcujsV0c7PswpIP3WzXk/edit#gid=1706192871") # clean_COVID-19_data

sleep(10000)