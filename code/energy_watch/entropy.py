# Importing the libraries
import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sc
import matplotlib.pyplot as plt
import copy
from . import classify
from . import tools

class Entropy:

    # Entropy Object calculates the entropy of the classifications from a Classify Object
    # self.classifications = Classifications from Classify Object
    # self.bldgs = List of Buildings
    # self.entropy = List of Entropy Corresponding to the Index in Self.bldgs
    def __init__(self, classify_obj):
        self.classifications = classify_obj.classifications
        self.bldgs = self.classifications[0]
        self.entropy = self.entropy_list(self.classifications[2])


    # Calculate Entropy (Uses Boltzmann's Entropy)
    # data (arr or series) - Pandas series to calculate entropy 
    def entropy_calc(self, data):
        from sklearn.preprocessing import StandardScaler
        data = pd.Series(data)
        p_data= data.value_counts()/len(data) # calculates the probabilities
        entropy= sc.stats.entropy(p_data)  # input probabilities to get the entropy 
        return entropy
    
    # Calculate Entropy of a 2D Array
    # data  (2d arr) - Bldg Classification Arrays
    # returns (arr) - Entropy Scores
    def entropy_list(self, data):
        scores = []
        for bldg_types in data:
            data_series = pd.Series(bldg_types)
            scores.append(self.entropy_calc(data_series))
        return scores
    
    # Graph Entropy Scores
    # param scores (arr) - List of Entropy Scores
    def graph_entr(self):
        plt.figure(figsize=(25,5))
        plt.title('Entropy of Building Classifications')
        plt.xlabel('Bldgs')
        labels = self.bldgs
        ticks = [i for i in range(1, len(labels) + 1)]
        plt.xticks(ticks, labels, rotation='vertical')
        plt.ylabel('Entropy')
        plt.plot(self.entropy)
        plt.show()
        
    # Heatmap of Entropy Scores
    # param scores (arr) - List of Entropy Scores
    def heatmap_entr(self):
        self.create_heatmap(entropy=self.entropy, ylabels=self.bldgs)

    # General function to create heatmap
    # param entropy (2D arr) - List of Entropy Scores
    # param title (str) - Title of Plot
    # param xlabels (arr) - List with Labels for X Axis
    # param ylabels (arr) - List with Labels for Y Axis
    def create_heatmap(self, entropy, title="Entropy Heatmap", xlabels=False, ylabels=False):
        plt.figure(figsize=(120,64))
        plt.title(title)
        ax = sns.heatmap(pd.DataFrame(entropy), yticklabels=ylabels, xticklabels=xlabels)
        plt.show()
  
    # Sort Building by Entropy 
    # Sorts self.entropy and the associated labels in self.bldgs
    def entropy_sort(self):
        bldgs, entr = self.bldgs, self.entropy
        if(len(bldgs) != len(entr)):
            print('Building and Entropy Array Must be The Same Length')
            return
        for passnum in range(len(entr)-1,0,-1):
            for i in range(passnum):
                if entr[i]>entr[i+1]:
                    # Swap Entropy Scores in Array
                    temp_entr = entr[i]
                    entr[i] = entr[i+1]
                    entr[i+1] = temp_entr
                    # Swap Bldg Names in Array
                    temp_bldg = bldgs[i]
                    bldgs[i] = bldgs[i+1]
                    bldgs[i+1] = temp_bldg
        return
    
    # Calculate Cumulative Entropy of Building Classifications Over Time
    # returns (arr) Associated Building Names
    # returns (2d Arr) Entropy Calculations over Time
    def calc_cum_entropy(self):
        bldg_names = self.classifications[0]
        classifications = self.classifications[2]
        return self.calc_cum_entropy_helper(bldg_names, classifications)

    # Calculate Cumulative Entropy Helper Function
    # returns (arr) Associated Building Names
    # returns (2d Arr) Entropy Calculations over Time
    def calc_cum_entropy_helper(self, bldg_names, classifications):
        bldg_entr_over_t = []
        for i in range(0, len(bldg_names)):
            entr_over_t = []
            for j in range(1, len(classifications[0])):
                entr = self.entropy_calc(pd.Series(classifications[i][:j]))
                entr_over_t.append(entr)
            bldg_entr_over_t.append(entr_over_t)
        return bldg_names, bldg_entr_over_t


    # Create A Heatmap of the Cumulative Entropy of Buildings Over Time
    def graph_cum_entropy(self):
        y_labels, entropy = self.calc_cum_entropy()
        x_labels = [i for i in range(len(entropy[0]))]
        title = "Cumulative Entropy Heatmap"
        self.create_heatmap(entropy, title=title, xlabels=x_labels, ylabels=y_labels)

    # Calculate Sliding Window Entropy of Building Classifications Over Time
    # param window (int) - Size of Window (Number of Days)
    # returns (arr) Associated Building Names
    # returns (2d Arr) Entropy Calculations over Time
    def calc_sliding_entropy(self, window=21):
        bldg_entr_over_t = []
        bldg_names = self.classifications[0]
        for i in range(0, len(bldg_names)):
            entr_over_t = []
            for j in range(1, len(self.classifications[2][0]) - window):
                entr = self.entropy_calc(pd.Series(self.classifications[2][i][j:j + window]))
                entr_over_t.append(entr)
            bldg_entr_over_t.append(entr_over_t)
        return bldg_names, bldg_entr_over_t

    # Create A Heatmap of the Cumulative Entropy of Buildings Over Time
    def graph_sliding_entropy(self, window=21):
        y_labels, entropy = self.calc_sliding_entropy(window=window)
        x_labels = [i for i in range(len(entropy))]
        title = "Sliding-Window Entropy Heatmap. Window Size: " + str(window) + " days."
        self.create_heatmap(entropy, title=title, xlabels=x_labels, ylabels=y_labels)