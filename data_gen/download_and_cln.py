import sys
sys.path.append("../mutation_analysis_by_XGBoost")

import pandas as pd
from objects.PDBData import PDBData
from objects.Selector import ChainAndAminoAcidSelect

# configurations
pdb_dir = "data/pdbs/"
pdbs_cln_dir = "data/pdbs_clean/"
fastas_dir = "data/fastas/"
CIF = "mmCif"
input_file_path = "data/dataset_5_train.csv"
# input_file_path = "data/dataset_5_test.csv"
n_rows_to_skip = 0
n_rows_to_evalutate = 20#0000

# object initialization
pdb_data = PDBData(pdb_dir=pdb_dir)

# data generation
dfs = pd.read_csv(input_file_path)

for i, row in dfs.iterrows():
    if i+1 <= n_rows_to_skip: continue
    pdb_id, chain_id, mutation, mutation_site, wild_residue, mutant_residue = row["pdb_id"], row["chain_id"], row["mutation"], int(row["mutation_site"]), row["wild_residue"], row["mutant_residue"]
    
    cln_pdb_file = pdbs_cln_dir+pdb_id+chain_id+".pdb"
    wild_fasta_file = fastas_dir+pdb_id+chain_id+".fasta"
    mutant_fasta_file = fastas_dir+pdb_id+chain_id+"_"+mutation+".fasta"
    
    pdb_data.download_structure(pdb_id=pdb_id)
    pdb_data.clean(pdb_id=pdb_id, chain_id=chain_id, selector=ChainAndAminoAcidSelect(chain_id), clean_pdb_dir=pdbs_cln_dir)
    residue_ids_dict = pdb_data.get_residue_ids_dict(pdb_file=cln_pdb_file, chain_id=chain_id)
    zero_based_mutation_site = residue_ids_dict.get(mutation_site)
    
    wild_seq = pdb_data.generate_fasta_from_pdb(pdb_id, chain_id, cln_pdb_file, save_as_fasta=True, output_fasta_dir=fastas_dir)
    mutant_seq = pdb_data.create_mutant_fasta_file(wild_fasta_file, mutant_fasta_file, zero_based_mutation_site, mutant_residue)
    
    print("Row no:{}->{}{}, mutation:{}, 0_indexed_mutation_site:{}".format(i+1, pdb_id, chain_id, mutation, zero_based_mutation_site))
    print(wild_seq)
    print(mutant_seq)
    
    print()
    if i+1 == n_rows_to_skip+n_rows_to_evalutate: 
        break