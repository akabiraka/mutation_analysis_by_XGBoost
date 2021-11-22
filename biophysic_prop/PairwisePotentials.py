import sys
sys.path.append('../mutation_analysis_by_XGBoost')
import numpy as np
import pandas as pd

class PairwisePotentials(object):
    def __init__(self):
        super(PairwisePotentials, self).__init__()
        self.brauns_df = pd.read_csv("data/static/brauns_potentials.csv").set_index('aa')
        self.jernigans_df = pd.read_csv("data/static/jernigans_potentials.csv").set_index('aa')
        self.levitts_df = pd.read_csv("data/static/levitts_potentials.csv").set_index('aa')

    def get_brauns_potentials(self, aa1, aa2):
        return np.array(self.brauns_df[aa1][aa2], dtype=np.float32)
         

    def get_jernigans_potentials(self, aa1, aa2):
        return np.array(self.jernigans_df[aa1][aa2], dtype=np.float32)
    

    def get_levitts_potentials(self, aa1, aa2):
        return np.array(self.levitts_df[aa1][aa2], dtype=np.float32)
    
    def get_for_a_seq(self, seq):
        features = []
        for i, y in enumerate(seq[:len(seq)-1]):
            features.append(self.get_brauns_potentials(seq[i], seq[i+1]))
            features.append(self.get_jernigans_potentials(seq[i], seq[i+1]))
            features.append(self.get_levitts_potentials(seq[i], seq[i+1]))
        return np.array(features, dtype=np.float32)

# pp = PairwisePotentials()
# print(pp.get_brauns_potentials('G', 'A'))
# print(pp.get_jernigans_potentials('G', 'A'))
# print(pp.get_levitts_potentials('G', 'A'))
# print(pp.get_for_a_seq("VINT"))