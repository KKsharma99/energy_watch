# # Energy_Watch Library, Documentation and Demo

# #### Areospace Design Lab, Georgia Institute of Technology. 
# ##### Dr. Lewe, Last Updated: 4/17/2019

# This purpose of this library is to help researchers or faculty at the Georgia Institute of Technology analyze their building consumption data. Specifically, this library allows you to classify the daily "Consumption Behavior" of buildings. You can then explore the entropy/change of these classifications to quickly identify buildings that may likely need closer inspection. The goal is to identify and fix buildings with electrical issues or energy consumption waste.

# ## Documentation (Classes and Methods)

# ### Data.py

#     # Data Object That Holds the Energy Consumption Data
#     # Object has tools to select sections of the original data
#     # class Data:
#         def __init__(self, data=<path to csv>): 
#             # self.data - Dataframe with Consumption Data
#             # self.bldgs - Building Names
#     
#     # Returns a Json Dict of building energy consumption totals from Jan 1, Aug 30
#     # 'columns' - Building Names
#     # 'data' - Building Energy Consumption Totals
#     def get_bldg_totals(self):
#     
#     # Get the Starting and Ending Indexes Between Two Months
#     # param start (int) - Number representing the Month
#     # param end (int) - Number representing the Ending Month
#     # Returns (dataframe) - Sliced Dataframe of Selected Data 
#     def slice_by_month(self, start, end=None):
#     
#     # Get the First Index of the Dataframe of the Given Month
#     # param month (int) - Number of the Month (eg. Feb = 2)
#     # returns index where the month starts in the dataframe
#     def get_month_start(self, month):
# 
#     # Get Consumption Data for the Last Number of Days
#     # param 'days' - Number of Days to Select
#     # Returns Sliced Dataframe
#     def get_last(self, days):
#     
#     # Get Consumption Data for a Defined Slice
#     # param 'start' - Starting Index
#     # param 'end' - Ending Index
#     # Returns Sliced Dataframe
#     def get_slice(self, start, end):
#     
#     # Replace Nan's with 0
#     def replace_nan_0(self):

# ### Classify.py

#     # Classify Object classify's the data in the Data Object
#     # Classifications of Building Consumption Behavior Include
#     # -1 - Below Threshold -> Energy Consumption is Very Low
#     #  0 - Cocentric       -> Consumption is relatively uniform
#     #  1 - People          -> Building has higher consumption during work hours
#     #  2 - Scheduler       -> Building that Operates With a Scheduler
#     #  3 - Reverse         -> Energy Usage is Greater During Work Hours
#     #  4 - Random          -> Abnormal Energy Behavior, Can't be Classified 
#     class Classify:
#         def __init__(self, data, thresh):
#         self.data   = A Data Class object
#         self.thresh = Threshold Level to Classify as Below Threshold (kwH)
#         self.classifications = [bldgnames(arr), dates(arr), classifications(2d arr)]
#     
#     # INTERNAL CLASS FUNCTION
#     # Function executed during object creation
#     # Get Classifications for All Buildings for Every Day in the Data Object
#     def gen_classifications(self):
#     
#     # INTERNAL CLASS FUNCTION
#     # Create Dataframe with the Columns: 'Building', 'Data', 'Type'
#     # param bldg_df (dataframe): dataframe with the building data
#     # return bldg_classes [bldg label (arr), dates (arr), types(arr)]
#     def table_bldg_classes(self, bldg_df):
#     
#     # INTERNAL CLASS FUNCTION
#     # Remove Instances With Energy Usage Below thresh kwH
#     def remove_small(self, X, y):
#     
#     # INTERNAL CLASS FUNCTION
#     # Classify incoming data
#     # param (data) - Data to classify
#     def classify(self, data):
#     
#     # INTERNAL CLASS FUNCTION
#     # Group By Interval with some Method
#     # Methods: Sum, Mean, Min, or Max
#     # Returns a df of grouped data
#     def group_df(self, df, method="mean", interval='day', has_time_col=True):
#     
#     # INTERNAL CLASS FUNCTION
#     # Reshape Training Data
#     # Formats it for Classification Model
#     def reshape_data(self, has_time_col=True, agg_interval="0:15", time_interval="day"): 
#     
#     # Create a Bar Graph Summarizing Classification Type Frequency
#     def graph_bar_summary(self):

# ### Entropy.py

#     # Entropy Object calculates the entropy of the classifications from a Classify Object
#     
#     class Entropy:
#     def __init__(self, classify_obj):
#         self.classifications = Classifications from Classify Object
#         self.bldgs = List of Buildings
#         self.entropy = List of Entropy Corresponding to the Index in Self.bldgs
#         
#     # Calculate Entropy (Uses Boltzmann's Entropy)
#     # data (arr or series) - Pandas series to calculate entropy 
#     def entropy_calc(self, data):
#     
#     # Calculate Entropy of a 2D Array
#     # data  (2d arr) - Bldg Classification Arrays
#     # returns (arr) - Entropy Scores
#     def entropy_list(self, data):
#     
#     # Graph Entropy Scores
#     # param scores (2d arr) - List of Entropy Scores
#     def graph_entr(self):
#     
#     # Heatmap of Entropy Scores
#     # param scores (arr) - List of Entropy Scores
#     def heatmap_entr(self):
#     
#     # INTERNAL FUNCTION
#     # General function to create heatmap
#     # param entropy (2D arr) - List of Entropy Scores
#     # param title (str) - Title of Plot
#     # param xlabels (arr) - List with Labels for X Axis
#     # param ylabels (arr) - List with Labels for Y Axis
#     def create_heatmap(self, entropy, title="Entropy Heatmap", xlabels=False, ylabels=False):
#     
#     # Sort Building by Entropy 
#     # Sorts self.entropy and the associated labels in self.bldgs
#     def entropy_sort(self):
#     
#     # Calculate Cumulative Entropy of Building Classifications Over Time
#     # Returns (2d Arr) Entropy Calculations over Time
#     def calc_cum_entropy(self):
#     
#     # Create A Heatmap of the Cumulative Entropy of Buildings Over Time
#     def graph_cum_entropy(self):
#     
#     # Calculate Sliding Window Entropy of Building Classifications Over Time
#     # param window (int) - Size of Window (Number of Days)
#     # Returns (2d Arr) Entropy Calculations over Time
#     # def calc_sliding_entropy(self, window=21):
#     
#     # Create A Heatmap of the Cumulative Entropy of Buildings Over Time
#     # param window (int) - Size of Window (Number of Days)
#     def graph_sliding_entropy(self, window=21):

# ### Tools.py

#     # Class with useful function for the rest of the library
#     # class Tools:
#     def __init__(self):
#         pass
# 
#     # Convert a time interval into the correct number of rows
#     # Interval: "3:15", "hour", day", "week", "month", "year" 
#     def time_to_row(interval):
#     
#     # param arrays (arr) An array of arrays (data for each column)
#     # param labels (arr) An array of associated labels (str)
#     # return df final dataframe
#     def arrays_to_df(arrays, labels):
# 
#     # Get List of Day Types. 1-5: M-F, -1: Weekend, -2: Holiday
#     # Param dates: List of Dates in 'MM/DD/YYYY' Format
#     # Param holidays: List of Holidays in 'MM/DD/YY' Format
#     def classify_day_type(dates):

# ## Demo

# In[1]:


# Keep the energy_watch folder in your currently directory and import as shown below
from energy_watch import data, classify, entropy, tools


# ### Data.py

# In[2]:


# Create Data Object
bldg_data = data.Data()


# In[3]:


# Replace Nan Values with Zero
bldg_data.replace_nan_0()


# In[4]:


bldg_data.get_bldg_totals()


# In[5]:


bldg_data.slice_by_month(2,6)


# In[6]:


# Get the Index Where a Month (1,2...12) Starts 
bldg_data.get_month_start(5)


# In[7]:


# Get the last X Days in your Data
bldg_data.get_last(15)


# In[8]:


# Get the selected Slice
bldg_data.get_slice(15, 450)


# ### Classify.py

# In[9]:


# Create Classify Object
bldg_classify = classify.Classify(bldg_data, thresh=30)


# In[10]:


# Bar Graph Summary
bldg_classify.graph_bar_summary()


# ### Entropy.py

# In[11]:


# Create Entropy Object
bldg_entr = entropy.Entropy(bldg_classify)


# In[12]:


# Graph the Entropy of All Buildings
bldg_entr.graph_entr()


# In[13]:


# Create a Heatmap of Building Entropy
bldg_entr.heatmap_entr()


# In[14]:


# Sort the Entropy Values
bldg_entr.entropy_sort()


# In[15]:


# Graph the Sorted Entropy
bldg_entr.graph_entr()


# In[16]:


# Create a Heatmap of Sorted Entropy
bldg_entr.heatmap_entr()


# In[17]:


# Calculate Cumulative Entropy
bldg_entr.calc_cum_entropy()


# In[18]:


# Graph Cumulative Entropy
bldg_entr.graph_cum_entropy()


# In[19]:


# Calculate Sliding Entropy
bldg_entr.calc_sliding_entropy()


# In[21]:


# Graph Sliding Entropy
bldg_entr.graph_sliding_entropy()

