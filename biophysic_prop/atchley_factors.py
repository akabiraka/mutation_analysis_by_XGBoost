import sys
sys.path.append('../mutation_analysis_by_XGBoost')
import numpy as np
import pandas as pd

class AtchleyFactors(object):
    def __init__(self):
        super(AtchleyFactors, self).__init__()
        atchley_file = "data/static/atchley_factors.txt"
        atchley_df = pd.read_csv(atchley_file, delim_whitespace=True, header=None)
        atchley_df = atchley_df.drop(0)
        self.atchley_df = atchley_df.set_index(0) # setting index to the amino-acid characters
        # print(self.atchley_df.loc['A'])

    def get(self, amino_acid):
        """
        returns atchley factors for given amino-acid character
        """
        result = self.atchley_df.loc[amino_acid]
        return np.array(result, dtype=np.float32)

    def get_all(self, amino_acids):
        """
        Given amino-acids this function computes full atchley-factors.
        This function use get() in itself.
        """ 
        factors_df = []
        for aa in amino_acids:
            factors_df.append(self.get(aa))
        return np.array(factors_df)


# af = AtchleyFactors()
# print(af.get("A"))
# print(af.get_all("VINTFDGV"))