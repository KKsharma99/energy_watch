# Importing the libraries
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler
from datetime import date

class Tools:
    # Class with useful function for the rest of the library
    def __init__(self):
        pass
    
    # Convert a time interval into the correct number of rows
    # Interval: "3:15", "hour", day", "week", "month", "year" 
    def time_to_row(interval):
        time_conv = { "year": 35040, "month": 2880, "week": 672, "day": 96, "hour": 4}
        if interval in time_conv: return time_conv[interval]
        elif ":" in interval: return int(interval.split(':')[0])*4 + int(interval.split(':')[1])//15
        else: return

    # param arrays (arr) An array of arrays (data for each column)
    # param labels (arr) An array of associated labels (str)
    # return df final dataframe
    def arrays_to_df(arrays, labels):
        if len(arrays) <= 1:
            print("Array must contain more than one array.")
            return
        # Start with First Column
        final_df = pd.DataFrame()
        # Add Remaining Arrays
        for i in range(0, len(arrays)):
            new_col = pd.DataFrame(arrays[i], columns=[labels[i]])
            final_df = pd.concat([final_df, new_col], axis=1)
        return final_df

    # Get List of Day Types. 1-5: M-F, -1: Weekend, -2: Holiday
    # Param dates: List of Dates in 'MM/DD/YYYY' Format
    # Param holidays: List of Holidays in 'MM/DD/YY' Format
    def classify_day_type(dates):
        holidays = ['1/1/2016', '1/2/2016', '1/18/2016', '3/21/2016', '3/22/2016', '3/23/2016',
            '3/24/2016', '3/25/2016','9/5/2016', '10/10/2016', '10/11/2016', '11/23/2016',
            '11/24/2016', '11/25/2016','12/25/2016', '12/26/2016', '12/27/2016',
            '12/28/2016', '12/29/2016', '12/30/2016','12/31/2016', '1/1/2017', '1/2/2017',
            '1/16/2017', '3/19/2017', '3/20/2017','3/21/2017', '3/22/2017', '3/23/2017',
            '3/24/2017', '5/28/2017', '7/3/2017', '7/4/2017', '9/4/2017', '10/9/2017',
            '10/10/2017', '11/22/2017', '11/23/2017', '11/24/2017', '12/25/2017', '12/27/2017',
            '12/28/2017', '12/29/2017', '12/30/2017','12/31/2017', '1/1/2018', '1/2/2018',
           '1/15/2018', '3/19/2018', '3/20/2018', '3/21/2018', '3/22/2018', '3/23/2018',
           '5/28/2018', '7/3/2018', '7/4/2018', '9/3/2018', '10/8/2018', '10/9/2018',
           '11/21/2018', '11/22/2018', '11/23/2018', '12/24/2018', '12/25/2018',
            '12/26/2018', '12/27/2018', '12/28/2018']
        day_type = []
        for i in dates:
            date_elem = i.split('/')
            day_of_week = date(int(date_elem[2]), int(date_elem[0]), int(date_elem[1])).isoweekday()
            if day_of_week > 5: day_type.append(-1)
            elif i in holidays: day_type.append(-2)
            else: day_type.append(day_of_week)
        return day_type