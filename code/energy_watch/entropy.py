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
    def __init__(self, classify_obj):
        self.classifications = classify_obj.get_classifications()
        self.entropy = [self.classifications[0], self.entropy_list(self.classifications[2])]
 
    # Get Entropy Scores
    # returns Entropy Scores (Dataframe)
    def get_entropy(self):
        return self.entropy
        
    # Get Classification Data
    # returns Classification Data (Dataframe)
    def get_classifications(self):
        return self.classifications
        
    # data (arr or series) - Pandas series to calculate entropy
    # Uses Boltzmann's Entropy
    def entropy_calc(self, data):
        from sklearn.preprocessing import StandardScaler
        data = pd.Series(data)
        p_data= data.value_counts()/len(data) # calculates the probabilities
        entropy= sc.stats.entropy(p_data)  # input probabilities to get the entropy 
        return entropy
    
    # data  (arr) - Bldg Classification Arrays
    # entropy (arr) - Entropy Scores
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
        labels = self.entropy[0]
        ticks = [i for i in range(1, len(labels) + 1)]
        plt.xticks(ticks, labels, rotation='vertical')
        plt.ylabel('Entropy')
        plt.plot(self.entropy[1])
        plt.show()
        
    # Heatmap of Entropy Scores
    # param scores (arr) - List of Entropy Scores
    def heatmap_entr(self):
        # plt.figure(figsize=(120,64))
        # plt.title("Entropy Heatmap")
        # ax = sns.heatmap(pd.DataFrame(self.entropy[1]), yticklabels=self.entropy[0], xticklabels=False)
        # plt.show()
        self.create_heatmap(entropy=self.entropy[1], ylabels=self.entropy[0])


    # General function to create heatmap
    # param entropy (2D Array) - List of Entropy Scores
    # param labels (Array) - List of Building Labels
    def create_heatmap(self, entropy, title="Entropy Heatmap", xlabels=False, ylabels=False):
        plt.figure(figsize=(120,64))
        plt.title(title)
        ax = sns.heatmap(pd.DataFrame(entropy), yticklabels=ylabels, xticklabels=xlabels)
        plt.show()

        
    # Sort Building by Entropy
    # param bldgs (arr) - Building Names
    # param entr (arr) - Associated Entropy Scores
    # return bldgs, entr - Sorted Lists
    def entropy_sort(self):
        bldgs, entr = self.entropy[0], self.entropy[1]
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
        return bldgs, entr
    
    # Calculate Cumulative Entropy of Building Classifications Over Time
    # param bldg_arr (arr): [[bldg_names], [date], [classification]]
    # returns bldg_entr_over_t (arr) Array of Bldg Cumulative Entropy Arrays for each bldg
    def cum_entropy(self, bldg_arr):
        bldg_entr_over_t = []
        for i in range(0, len(bldg_arr[0])):
            entr_over_t = []
            for j in range(1, len(bldg_arr[2][0])):
                entr = entropy_calc(pd.Series(bldg_arr[2][i][:j]))
                entr_over_t.append(entr)
            bldg_entr_over_t.append(entr_over_t)
        return bldg_entr_over_t

    # Calculate Sliding Window Entropy of Building Classifications Over Time
    # param bldg_arr (arr): [[bldg_names], [date], [classification]]
    # param window_size (int): Size of Window
    # returns bldg_entr_over_t (arr) Array of Bldg Cumulative Entropy Arrays for each bldg
    def sliding_entropy(self, bldg_arr, window=14):
        bldg_entr_over_t_slide = []
        for i in range(0, len(wkday_bldg_arr[0])):
            entr_over_t = []
            for j in range(1, len(wkday_bldg_arr[2][0]) - window):
                entr = entropy_calc(pd.Series(wkday_bldg_arr[2][i][j:j + window]))
                entr_over_t.append(entr)
            bldg_entr_over_t_slide.append(entr_over_t)
        return bldg_entr_over_t_slide