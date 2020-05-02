import os
from stateGraph import Data, Graph

class State():
    def __init__(self, state_name, date, clean_scale, change_scale):
        self.state_name = str(state_name)
        self.date = str(date)
        self.clean_scale = float(clean_scale)
        self.change_scale = float(change_scale)

date = str(input("From what date do you want to graph? [Input Form: Month-Day-2X]: "))

# Get the data from a specified date
data = Data(date)

states = ["New York", "New Jersey", "Massachusetts", "Rhode Island", "California", "Michigan", "Ohio"]
for i in range(len(states)):
    new_state = State(states[i], date, 1000, 100)
    # Create a state folder
    os.makedirs(os.path.join(data.path, new_state.state_name))
    state_folder = os.path.join(data.path, new_state.state_name)

    # Create the graphs
    os.chdir(state_folder)
    cleanRaw = Graph(new_state.state_name, data, "clean", "raw", "Raw Growth Data", new_state.clean_scale, 3)
    cleanRawLog = Graph(new_state.state_name, data, "clean", "raw", "Log Scale of Raw Growth Data", new_state.clean_scale, 3, True)
    cleanTrend = Graph(new_state.state_name, data, "clean", "trend", "Trend line of Growth Data", new_state.clean_scale, 3)
    changeRaw = Graph(new_state.state_name, data, "change", "raw", "Raw Data of Daily Patient Change", new_state.change_scale)
    changeTrend = Graph(new_state.state_name, data, "change", "trend", "Trend line of Daily Patient Change", new_state.change_scale)