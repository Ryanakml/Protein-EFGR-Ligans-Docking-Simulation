#!/usr/bin/env python3
"""
EGFR Docking Simulation - Script Utama
Automasi penuh dari download data hingga analisis
"""

import os
import sys
import logging
import traceback
from datetime import datetime
from config import *
from scripts.protein_prep import ProteinPreparator
from scripts.ligand_prep import LigandPreparator
from scripts.docking import AutoDockVina
from scripts.visualization import ResultVisualizer

def setup_logging():
    """Setup logging untuk tracking proses"""
    log_file = os.path.join(RESULTS_DIR, f'docking_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def create_directories():
    """Buat folder-folder yang dibutuhkan"""
    directories = [DATA_DIR, PROTEIN_DIR, LIGAND_DIR, RESULTS_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory created/exists: {directory}")

def main():
    """Fungsi utama untuk menjalankan docking simulation"""
    print("🧬 EGFR Docking Simulation Started")
    print("=" * 50)
    
    # Setup
    logger = setup_logging()
    create_directories()
    
    try:
        # Step 1: Preparasi Protein
        print("\n📥 Step 1: Downloading and Preparing EGFR Protein...")
        protein_prep = ProteinPreparator(PROTEIN_DIR, logger)
        protein_file = protein_prep.prepare_egfr_protein(EGFR_PDB_ID, BACKUP_PDB_IDS)
        if not protein_file:
            raise Exception("Failed to prepare protein")
        print(f"✓ Protein prepared: {protein_file}")
        
        # Step 2: Preparasi Ligand
        print("\n🧪 Step 2: Preparing Ligands...")
        ligand_prep = LigandPreparator(LIGAND_DIR, logger)
        ligand_files = ligand_prep.prepare_ligands(TARGET_LIGANDS)
        if not ligand_files:
            raise Exception("Failed to prepare ligands")
        print(f"✓ {len(ligand_files)} ligands prepared")
        
        # Step 3: Molecular Docking
        print("\n🔬 Step 3: Running Molecular Docking...")
        docker = AutoDockVina(RESULTS_DIR, logger)
        docking_results = docker.run_docking_batch(
            protein_file, 
            ligand_files, 
            DOCKING_CONFIG
        )
        if not docking_results:
            raise Exception("Docking failed")
        print(f"✓ Docking completed for {len(docking_results)} ligands")
        
        # Step 4: Visualisasi dan Analisis
        print("\n📊 Step 4: Generating Visualization and Analysis...")
        visualizer = ResultVisualizer(RESULTS_DIR, logger)
        
        # Generate visualizations
        visualizer.create_interaction_plots(docking_results)
        visualizer.create_binding_affinity_chart(docking_results)
        visualizer.create_3d_visualization(protein_file, docking_results)
        visualizer.generate_analysis_report(docking_results)
        
        print("✓ Analysis and visualization completed")
        
        # Step 5: Summary
        print("\n📋 Step 5: Results Summary")
        print("=" * 30)
        
        # Sort by binding affinity
        sorted_results = sorted(docking_results.items(), 
                              key=lambda x: float(x[1]['best_affinity']))
        
        print("🏆 Best Binding Affinities:")
        for i, (ligand, result) in enumerate(sorted_results[:3], 1):
            print(f"{i}. {ligand}: {result['best_affinity']} kcal/mol")
        
        print(f"\n📁 All results saved in: {RESULTS_DIR}")
        print("📝 Check the following files:")
        print(f"   - Excel report: {os.path.join(RESULTS_DIR, OUTPUT_FILES['docking_results'])}")
        print(f"   - 3D visualization: {os.path.join(RESULTS_DIR, OUTPUT_FILES['visualization_html'])}")
        print(f"   - Analysis report: {os.path.join(RESULTS_DIR, OUTPUT_FILES['analysis_report'])}")
        
        print("\n🎉 EGFR Docking Simulation Completed Successfully!")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"\n❌ Error occurred: {str(e)}")
        print("Check the log file for detailed error information")
        sys.exit(1)

if __name__ == "__main__":
    main()