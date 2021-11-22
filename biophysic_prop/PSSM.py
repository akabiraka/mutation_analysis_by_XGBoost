import sys
sys.path.append("../mutation_analysis_by_XGBoost")

import os
import pandas as pd
import numpy as np
from scipy.special import softmax
from Bio.Blast.Applications import NcbipsiblastCommandline

class PSSM(object):
    """PSSM stands for position-specific socring-matrix
    """
    def __init__(self, db=None, output_dir=None) -> None:
        super().__init__()
        # self.db = "3rd_party_items/swissprot_db/swissprot" if db is None else db
        self.db = "3rd_party_items/rp_req_15/rp_req_15"
        self.output_dir = "data/pssms/" if output_dir is None else output_dir
        self.psiblast_exe = "3rd_party_items/ncbi-blast-2.12.0+/bin/psiblast"
        self.pdb_id = None

        
    def set_up(self, fasta_file, force=False):
        """This blast run the query sequence 3 iterations against a db using psiblast program,
        and save the output file in pssms directory. 

        Args:
            fasta_file (str): file path
            force (bool): whether to enforce PSSM set up from start
        """
        pdbid = fasta_file.split("/")[2].split(".")[0]
        output_file_path = self.output_dir + pdbid +".pssm"
        self.pdb_id = pdbid 

        if os.path.exists(output_file_path) and force==False: 
            print("PSSM is already set up for {}. To set-up again, set force=True.".format(pdbid))
            return
        else:
            print("Computing PSSM for {} using psi-blast ... ...".format(pdbid))    
            E_VALUE_TRESH = 10
            cline = NcbipsiblastCommandline(cmd=self.psiblast_exe, db=self.db, query=fasta_file,\
                                            evalue=E_VALUE_TRESH, outfmt=5, num_iterations=3,\
                                            save_pssm_after_last_round=True, out_ascii_pssm=output_file_path)# 
                                            # out = out_xml, out_pssm=out_pssm, out_ascii_pssm=output_file_path)
            cline()
        

    def __get_pssm_file(self):
        return self.output_dir + self.pdb_id + ".pssm"
    
    def __parse_pssm_output_file(self, pssm_file):
        """Parse PSSM raw file generated by PSI-BLAST.

        Args:
            pssm_file (str): a pssm file path

        Returns:
            dataframe: raw result as dataframe
        """
        # delim_whitespace=True,
        col_names = pd.read_csv(pssm_file, delim_whitespace=True, header=None, skiprows=[0, 1], nrows=1)
        col_names = col_names.loc[0, 0:19].tolist()
        residue_dict = {key: i for i, key in enumerate(col_names)}
        # print(residue_dict)
        # col_names.insert(0, "index")
        # col_names.insert(1, "name")
        # col_names.append("dont_know_1")
        # col_names.append("dont_know_2")
        # col_names = pd.DataFrame([col_names])
        # print(col_names)

        df = pd.read_csv(pssm_file, delim_whitespace=True, header=None, skiprows=[0, 1, 2]) # skipping 1st 2 rows
        df = df.head(-5) # removing last 5 rows
        # df = pd.concat([col_names, df]).reset_index(drop=True)
        
        return df, residue_dict
    
   
    def of_a_residue(self, residue_index, type="softmax"):
        """Compute a PSSM for a given residue number.

        Args:
            pssm_file (str): a pssm file path
            residue_index (int): a residue number. Must be 0-based index.
            type (str, optional): If not softmax, it will return raw numpy array.
                Defaults to "softmax".

        Returns:
            nd array: 1x20 dimensional array 
        """
        pssm_file = self.__get_pssm_file()
        if os.path.exists(pssm_file)==False:
            print("No pssm file is found for ", pssm_file)
            return np.array([0.0])
        df, residue_dict = self.__parse_pssm_output_file(pssm_file)
        pssm = np.array(df.loc[residue_index, 2:21], dtype=np.float32)
        # print(pssm)
        if type=="softmax": 
            pssm = softmax(pssm)
            # print("should be 1: ", pssm.sum())
        pssm_score = pssm[residue_dict[df.loc[residue_index, 1]]]
        return np.array([pssm_score])
    
    
   

# fasta_file = "data/fastas/2ptlA_T_19_A.fasta"

# # sample usage
# pssm = PSSM()
# pssm.set_up(fasta_file)

# result = pssm.of_a_residue(19) # check boundary value
# print(result)
# result = pssm.of_a_residue(35, type="softmax") # check boundary value

# result = pssm.of_some_residues(from_residue=0, n_residues=None, type="softmax") # getting pssm for all residues
# result = pssm.of_some_residues(from_residue=0, n_residues=5, type="softmax")
# print(result.shape)
# print(result.sum(axis=1)) # n_residues 1s 
# result = pssm.of_some_residues(from_residue=235, n_residues=100, type="softmax") # getting pssm upto last residue
