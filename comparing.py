from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import pandas as pd

def extract_secondary_structure_from_cif(cif_file):
    mmcif_dict = MMCIF2Dict(cif_file)
    
    columns_of_interest = [
        '_dssp_struct_summary.label_seq_id', 
        '_dssp_struct_summary.label_comp_id', 
        '_dssp_struct_summary.secondary_structure'
    ]
    
    data = {col: mmcif_dict[col] for col in columns_of_interest if col in mmcif_dict}
    
    df = pd.DataFrame(data)
    
    return df

def extract_secondary_structure_from_ss2(ss2_file):
    df2 = pd.read_excel(ss2_file, header=None)
    df2 = df2.iloc[:, 0:3]
    return df2

def comparing(cif, ss2):
    matches = []
    for i in range(len(cif)):
        for j in range(len(ss2)):
            
            if cif.iloc[i, 0] == ss2.iloc[j, 0]:
                
                if cif.iloc[i, 2] in helix and ss2.iloc[j, 2] in helix:
                    matches.append(1)
                elif cif.iloc[i, 2] in coil and ss2.iloc[j, 2] in coil:
                    matches.append(1)
                elif cif.iloc[i, 2] in esheet and ss2.iloc[j, 2] in esheet:
                    matches.append(1)
                else:
                    matches.append(0)
            else:
                continue
    return matches

cif_file = "/Users/julialemanska/Desktop/studia/bio strukturalna/lab2/4ywo.cif"
df_cif = extract_secondary_structure_from_cif(cif_file)

ss2_file = "/Users/julialemanska/Desktop/studia/bio strukturalna/lab2/bios.xlsx"
df_ss2 = extract_secondary_structure_from_ss2(ss2_file)

helix = ["H", "G", "I", "P"]
coil = ["T", "S", "C", "."]
esheet = ["B", "E"]

df_ss2 = df_ss2.iloc[10:]
df_ss2.columns = ['id','aa_s','ss_ss2']
df_cif.columns = ['id','aa_n', 'ss_cif']

df_ss2['id'] = df_ss2['id'].astype(int)
df_cif['id'] = df_cif['id'].astype(int)

comparison = comparing(df_cif, df_ss2)

suma = sum(comparison)
size = len(comparison)

res = round(suma/size, 4)

print("Result:")
print("Comparing length of predicted structure: SSI=" + str(res))