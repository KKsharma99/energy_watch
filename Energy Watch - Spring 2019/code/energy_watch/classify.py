# Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from sklearn.preprocessing import StandardScaler
import pickle
from . import tools


class Classify:

    # Classify Object Classify's the Data in the Data Object
    # Classifications of Building Consumption Behavior Include
    # -1 - Below Threshold -> Energy Consumption is Very Low
    #  0 - Cocentric       -> Consumption is relatively uniform
    #  1 - People          -> Building has higher consumption during work hours
    #  2 - Scheduler       -> Building that Operates With a Scheduler
    #  3 - Reverse         -> Energy Usage is Greater During Work Hours
    #  4 - Random          -> Abnormal Energy Behavior, Can't be Classified
    # 
    # self.data   = Original Consumption
    # self.thresh = Threshold Level to Classify as Below Threshold (kwH)
    # self.classifications = [ bldgnames(arr), dates(arr), classifications(2d arr)]
    def __init__(self, data, thresh):
        self.data = data.data
        self.thresh = thresh
        self.classifications = self.gen_classifications()
     
    # Get Classifications for All Buildings for Every Day in the Data Object
    def gen_classifications(self):
        energy_data = self.reshape_data()
        original_len = len(energy_data)
        
        energy_y = []
        for i in range(len(energy_data)): energy_y.append(i)
        energy_y = pd.DataFrame(energy_y)

        energy_data, energy_y = self.remove_small(pd.DataFrame(energy_data), energy_y)
        energy_y = energy_y.iloc[:, 0]
        
        sc = StandardScaler()
        energy_data = sc.fit_transform(energy_data)

        # Get List of Buildings
        buildings = list(self.data)[1:]

        # Get List of dates
        dates = pd.DataFrame(self.data.iloc[:,0])
        dates = self.group_df(df=dates, method="mean", interval='day')
        for i in range(dates.shape[0]): dates.iloc[i, 0] = dates.iloc[i, 0].split()[0]
        dates = list(dates.iloc[:, 0])

        classifications = self.classify(energy_data)

        # Create building_type Array
        building_type = []
        for i in range(original_len): building_type.append(-1)
        for i in range(len(energy_y)): building_type[energy_y[i]] = classifications[i]

        # Create Classification df Date, Building Type
        dates = dates * 134
        updated_bldg = [] 
        for i in buildings: updated_bldg += [i] * 237

        # Create List of Day Types
        day_type = tools.Tools.classify_day_type(dates)

        #Create Building Classification Dataframe
        arrays = [day_type, dates, updated_bldg, building_type]
        labels = ['Day_Type', 'Date', 'Building', 'Type']
        bldg_classes = tools.Tools.arrays_to_df(arrays, labels)
        
        # Remove Weekends and Holidays from the Dataset
        wkday_bldg = bldg_classes[bldg_classes['Day_Type'] > 0].reset_index()

        return self.table_bldg_classes(wkday_bldg)


    # Create Dataframe with the Columns: 'Building', 'Data', 'Type'
    # param bldg_df (dataframe): dataframe with the building data
    # return bldg_classes [bldg label (arr), dates (arr), types(arr)]
    def table_bldg_classes(self, bldg_df):
        counter = 0
        # Arrays for Dataframe Creation
        bldgs_labels = []
        dates_arr = []
        types_arr = []
        # Arrays Collect Information for Each Building then Reset for next Building
        prev_bldg = bldg_df['Building'][0]
        dates = []
        bldg_type = []

        for i in range(len(bldg_df)):    
            curr_bldg = bldg_df['Building'][i]
            # Graph Old Building if Current Bldg is New or Last Bldg
            if (curr_bldg != prev_bldg) or (i == len(bldg_df) - 1):
                counter += 1
                bldgs_labels.append(prev_bldg)
                dates_arr.append(dates)
                types_arr.append(bldg_type)
                dates = []
                bldg_type = []
                prev_bldg = curr_bldg
            else:
                dates.append(bldg_df['Date'][i])
                bldg_type.append(bldg_df['Type'][i])

        return [bldgs_labels, dates_arr, types_arr]

    # Remove Instances With Energy Usage Below thresh kwH
    def remove_small(self, X, y):
        final_X, final_y = pd.DataFrame(), pd.DataFrame()
        y_list = list(y.iloc[:, 0])
        new_df = []
        new_y = []
        for i in range(0, X.shape[0]):
            if X.iloc[i, :].mean() > self.thresh*4:
                new_df.append(X.iloc[i, :].values)
                new_y.append(y_list[i])
        final_X = pd.concat([final_X, pd.DataFrame(new_df)])
        final_y = pd.concat([final_y, pd.DataFrame(new_y)])
        return final_X, final_y


    # Classify incoming data
    # param (data) - Data to classify
    def classify(self, data):
        filename = 'building_classification_model.p'
        loaded_model = pickle.load(open(filename, 'rb'))
        return loaded_model.predict(data)
    
    # Group By Interval with some Method
    # Methods: Sum, Mean, Min, or Max
    # Returns a df of grouped data
    def group_df(self, df, method="mean", interval='day', has_time_col=True):
        interval = tools.Tools.time_to_row(interval)
        grouped_df = pd.DataFrame()
        for i in range(0,len(df)//interval):
            if has_time_col: start_date = df['time'][i*interval]
            block = df.iloc[ i*interval:(i+1)*interval, : ]
            #####if(i == 223): print(block)
            # Perform Computation on Row
            if method == "sum": block = block.sum(axis=0)
            elif method == "mean": block = block.mean(axis=0)
            elif method == "min": block = block.min(axis=0)
            elif method == "max": block = block.max(axis=0)
            else:
                print("Invalid Method Entry")
                return
            # Add the Start Date Label
            if has_time_col:
                if method == "mean": block = pd.Series([start_date]).append(block)  
                else: block[0] = start_date
            block = block.to_frame().transpose()
            grouped_df = grouped_df.append(block)
        if method == "mean" and has_time_col: grouped_df = grouped_df.rename(columns={ grouped_df.columns[0]: "time" })
        return grouped_df
        
    # Reshape Training Data
    # Formats it for Classification Model
    def reshape_data(self, has_time_col=True, agg_interval="0:15", time_interval="day"):
        X = self.data
        if has_time_col: X = X.drop(columns=['time'])
        # Determine Shape of New Dataframe and Reshape
        new_col_ct = int(tools.Tools.time_to_row(time_interval)/tools.Tools.time_to_row(agg_interval))
        rows_per_instance = int(X.shape[0]/new_col_ct)
        X = X.T.values.reshape(X.shape[1] * rows_per_instance, new_col_ct)
        return X

    # Create a Bar Graph Summarizing Classification Type Frequency
    def graph_bar_summary(self):
        type_labels = ["Below Threshold", "Cocentric", "People", "Scheduler", "Reverse", "Random"]
        counts = [0, 0, 0, 0, 0, 0]
        for classifications in self.classifications[2]:
            for classified in classifications:
                counts[classified + 1] += 1

        print("Classification Type Frequency")
        for i in range(len(counts)): print(type_labels[i] + ": " + str(counts[i]))

        plt.title("Classification Type Frequency")
        plt.bar(x=[0,1,2,3,4,5], height=counts, tick_label=type_labels)
        plt.xticks(rotation='vertical')
        plt.show()