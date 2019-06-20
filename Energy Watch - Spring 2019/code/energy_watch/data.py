# Importing the libraries
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler

class Data:

    # Data Object That Holds the Energy Consumption Data
    # Object has tools to select sections of the original data
    def __init__(self, data='../data/year_data/2018-01-01_2018-08-30.csv'):
        self.data = pd.read_csv(data)
        self.bldgs = list(self.data.columns)[1:]

    # Returns a Json Dict of building energy consumption totals from Jan 1, Aug 30
    # 'columns' - Building Names
    # 'data' - Building Energy Consumption Totals
    def get_bldg_totals(self):
        bldg_tot = self.data.sum()[1:]
        bldg_tot = bldg_tot.divide(4)
        bldg_tot = pd.DataFrame(bldg_tot).transpose().to_json(orient='split')
        bldg_tot = json.loads(bldg_tot)
        bldg_tot['data'] = bldg_tot['data'][0]
        return bldg_tot

    # Get the Starting and Ending Indexes Between Two Months
    # param start (int) - Number representing the Month
    # param end (int) - Number representing the Ending Month
    # Returns (dataframe) - Sliced Dataframe of Selected Data 
    def slice_by_month(self, start, end=None):
        start_idx = self.get_month_start(start)
        end_idx = 0
        if end == None:
            if start == 12: end_idx = len(self.data)
            else: end_idx = self.get_month_start(start + 1)
        else:
            if end == 12: end_idx = len(self.data)
            else: end_idx = self.get_month_start(end + 1)
                
        print(start_idx)
        print(end_idx)
        return self.get_slice(start_idx, end_idx)
    
    # Get the First Index of the Dataframe of the Given Month
    # param month (int) - Number of the Month (eg. Feb = 2)
    # returns index where the month starts in the dataframe
    def get_month_start(self, month):
        for i in range(len(self.data)):
            if(self.data['time'][i].split('/')[0] == str(month) 
              and self.data['time'][i].split('/')[1] == '1'
              and self.data['time'][i].split('/')[2].split()[1] == '0:00'):
                return i
   
    # Get Consumption Data for the Last Number of Days
    # param 'days' - Number of Days to Select
    # Returns Sliced Dataframe
    def get_last(self, days):
        end = len(self.data)
        start = end - 96*days
        return self.get_slice(start, end)
    
    # Get Consumption Data for a Defined Slice
    # param 'start' - Starting Index
    # param 'end' - Ending Index
    # Returns Sliced Dataframe
    def get_slice(self, start, end):
        return self.data.iloc[start:end, :]
    
    # Replace Nan's with 0
    def replace_nan_0(self):
        for i in range(1, self.data.shape[1]):
            self.data.iloc[1:, i] = self.data.iloc[1:, i].fillna(0)