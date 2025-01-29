import pandas as pd
import numpy as np

class Data():
    def __init__(self):
        self.data = pd.read_csv("2016-mlb-homeruns.csv")
        self.data_1 = pd.read_csv("2017-mlb-homeruns.csv")
        self.data_2 = pd.read_csv("2024-mlb-homeruns.csv")

    def call_data(self):
        return self.data, self.data_1, self.data_2