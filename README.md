Daftar Isi

1. [Persiapan Environment](#persiapan-environment)
2. [Struktur Project](#struktur-project)
3. [Install Dependencies](#install-dependencies)
4. [Script Utama](#script-utama)
5. [Konfigurasi](#konfigurasi)
6. [Menjalankan Simulation](#menjalankan-simulation)
7. [Hasil dan Analisis](#hasil-dan-analisis)

### Persiapan Environment

#### Sistem Requirements:

- Python 3.8+
- Ubuntu/Linux (recommended) atau WSL2 di Windows
- Minimal 8GB RAM
- 5GB disk space

#### Software yang Dibutuhkan:

```bash
# Install sistem dependencies

# Pastikan Homebrew sudah terinstall
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Update brew
brew update

# Install Python + pip + venv
brew install python

# Build tools
brew install cmake boost

# Chemistry tools
brew install open-babel
brew install autodock-vina
```

Struktur Project

```
egfr_docking_project/
├── main.py                 # Script utama
├── config.py              # Konfigurasi
├── requirements.txt       # Dependencies Python
├── setup.sh              # Setup script
├── data/                 # Folder untuk data
│   ├── proteins/         # File protein
│   ├── ligands/          # File ligan
│   └── results/          # Hasil docking
├── scripts/              # Script utilities
│   ├── protein_prep.py   # Preparasi protein
│   ├── ligand_prep.py    # Preparasi ligan
│   ├── docking.py        # Proses docking
│   └── visualization.py  # Visualisasi
└── notebooks/            # Jupyter notebooks
    └── analysis.ipynb    # Analisis hasil
```

### Install Dependencies

#### 1. Buat Virtual Environment:

```bash
python3 -m venv egfr_docking_env
source egfr_docking_env/bin/activate
```

#### 2. Install Python Packages:

```bash
pip install -r requirements.txt
```


### Menjalankan Simulation

#### 1. Setup Project:

```bash
# Clone atau buat direktori project
git clone https://github.com/ryanakmalpasya/egfr_docking_project.git
```
or

```bash
# Clone atau buat direktori project
cd egfr_docking_project

# Copy semua file script ke direktori ini
# Jalankan setup
chmod +x setup.sh
./setup.sh
```
or

```bash
sh setup.sh
```

#### 2. Activate Environment dan Run:

```bash
source egfr_docking_env/bin/activate
python main.py
```

#### 3. Monitor Progress:

Script akan menampilkan progress real-time dan menyimpan log detail di `data/results/`.


### Hasil dan Analisis

Setelah selesai, Anda akan mendapatkan:

#### File Output:

- **docking_results.xlsx** - Hasil lengkap dalam Excel
- **binding_affinity_chart.png** - Chart perbandingan affinity
- **interaction_analysis.png** - Analisis distribusi dan interaksi
- **docking_visualization.html** - Visualisasi 3D interaktif
- **analysis_report.pdf** - Laporan analisis lengkap

#### Interpretasi Hasil:

- **Binding Affinity < -8.0 kcal/mol**: Binding sangat kuat
- **-8.0 to -6.0 kcal/mol**: Binding kuat
- **-6.0 to -4.0 kcal/mol**: Binding sedang
- **> -4.0 kcal/mol**: Binding lemah

#### Analisis Lanjutan:

1. **Buka visualization HTML** untuk melihat struktur 3D
2. **Review Excel report** untuk data numerik
3. **Analisis interaction plots** untuk distribusi binding
4. **Baca PDF report** untuk summary lengkap

### Troubleshooting

#### Common Issues dan Solutions:

**1. AutoDock Vina tidak terinstall:**

```bash
sudo apt install autodock-vina
# atau compile dari source jika perlu
```

**2. OpenBabel error:**

```bash
sudo apt install openbabel libopenbabel-dev
pip install openbabel
```

**3. Memory issues:**

```bash
# Kurangi exhaustiveness di config.py
DOCKING_CONFIG['exhaustiveness'] = 16  # dari 32
```

**4. Network timeout saat download PDB:**

```bash
# Script akan otomatis coba backup PDB IDs
# atau download manual dan letakkan di data/proteins/
```

**5. Permission denied:**

```bash
chmod +x main.py setup.sh
sudo chown -R $USER:$USER egfr_docking_project/
```

### Kustomisasi

#### Mengganti Target Protein:

```python
# Di config.py
EGFR_PDB_ID = '3POZ'  # Ganti dengan PDB ID lain
```

#### Menambah Ligand Baru:

```python
# Di config.py, tambahkan ke TARGET_LIGANDS
'new_ligand': 'SMILES_string_here'
```

#### Mengubah Parameter Docking:

```python
# Di config.py, modify DOCKING_CONFIG
DOCKING_CONFIG = {
    'center_x': -10.0,  # Sesuaikan binding site
    'center_y': 2.0,
    'center_z': 60.0,
    'size_x': 30,       # Perbesar grid box
    'exhaustiveness': 64  # Tingkatkan akurasi
}
```

Referensi dan Resources

#### Software yang Digunakan:

- **AutoDock Vina**: Molecular docking
- **OpenBabel**: Format conversion
- **RDKit**: Cheminformatics
- **BioPython**: Struktur protein
- **3Dmol.js**: Visualisasi 3D

#### Database:

- **RCSB PDB**: Struktur protein
- **ChEMBL**: Data bioaktivitas
- **PubChem**: Struktur kimia

#### Publikasi Terkait:

- Trott, O. & Olson, A.J. (2010) AutoDock Vina
- EGFR inhibitor studies in drug discovery
- Molecular docking best practices