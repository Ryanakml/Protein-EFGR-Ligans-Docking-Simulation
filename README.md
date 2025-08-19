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

or

# Clone atau buat direktori project
cd egfr_docking_project

# Copy semua file script ke direktori ini
# Jalankan setup
chmod +x setup.sh
./setup.sh
```

#### 2. Activate Environment dan Run:

```bash
source egfr_docking_env/bin/activate
python main.py
```

#### 3. Monitor Progress:

Script akan menampilkan progress real-time dan menyimpan log detail di `data/results/`.