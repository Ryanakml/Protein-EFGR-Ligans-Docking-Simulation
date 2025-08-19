import os

# Path konfigurasi
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
PROTEIN_DIR = os.path.join(DATA_DIR, 'proteins')
LIGAND_DIR = os.path.join(DATA_DIR, 'ligands')
RESULTS_DIR = os.path.join(DATA_DIR, 'results')

# Protein target
EGFR_PDB_ID = '1M17'  # EGFR kinase domain dengan erlotinib
BACKUP_PDB_IDS = ['3POZ', '4HJO', '5P21']  # Backup jika gagal download

# Ligan yang akan di-test (known EGFR inhibitors)
TARGET_LIGANDS = {
    'erlotinib': 'CC1=C2C=C(C=CC2=NC=N1)OC3=CC=C(C=C3)C#CCN4CCOCC4',
    'gefitinib': 'COC1=C(C=C2C(=C1)N=CN=C2NC3=CC(=C(C=C3)F)Cl)OCCCN4CCOCC4',
    'lapatinib': 'CS(=O)(=O)CCNCC1=CC=C(C=C1)C2=CC3=C(C=C2)N=CN=C3NC4=CC(=C5C=CSC5=C4)Cl',
    'afatinib': 'CN(C)C/C=C/C(=O)NC1=CC(=C2N=CN=C(N2C=C1)NC3=CC=C(C=C3)OC4=CC=CC=C4)OC',
    'osimertinib': 'COC1=C(C=C2C(=C1)N=CN=C2NC3=CC=C(C=C3)NC(=O)C=C)N4CCN(CC4)C'
}

# Parameter docking
DOCKING_CONFIG = {
    'center_x': -9.7,     # Koordinat binding site EGFR
    'center_y': 1.4,
    'center_z': 62.1,
    'size_x': 25,         # Ukuran grid box
    'size_y': 25,
    'size_z': 25,
    'exhaustiveness': 32,  # Tingkat pencarian (semakin tinggi semakin akurat)
    'num_modes': 20       # Jumlah pose yang dihasilkan
}

# Output files
OUTPUT_FILES = {
    'protein_prepared': 'egfr_prepared.pdbqt',
    'docking_results': 'docking_results.xlsx',
    'visualization_html': 'docking_visualization.html',
    'analysis_report': 'analysis_report.pdf'
}