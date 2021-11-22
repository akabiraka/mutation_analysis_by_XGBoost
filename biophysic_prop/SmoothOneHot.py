import sys
sys.path.append('../mutation_analysis_by_XGBoost')
import numpy as np
from Bio.PDB import standard_aa_names, protein_letters_3to1

class SmoothOneHot(object):
    def __init__(self) -> None:
        super().__init__()
        self.amino_acids=""
        for x in standard_aa_names:
            self.amino_acids=self.amino_acids+ protein_letters_3to1.get(x)
        
    def string_vectorizer(self, strng):
        vector = [[0.1 if char != letter else 0.9 for char in self.amino_acids] 
                    for letter in strng]
        return np.array(vector, dtype=np.float32)


# soh = SmoothOneHot()
# print(soh.string_vectorizer("AV"))