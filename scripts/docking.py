import os
import subprocess
import tempfile
import pandas as pd
from collections import defaultdict

class AutoDockVina:
    def __init__(self, results_dir, logger):
        self.results_dir = results_dir
        self.logger = logger
    
    def create_config_file(self, protein_file, ligand_file, output_file, docking_config):
        """Buat file konfigurasi untuk Vina"""
        config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        
        config_content = f"""receptor = {protein_file}
ligand = {ligand_file}
out = {output_file}

center_x = {docking_config['center_x']}
center_y = {docking_config['center_y']}
center_z = {docking_config['center_z']}

size_x = {docking_config['size_x']}
size_y = {docking_config['size_y']}
size_z = {docking_config['size_z']}

exhaustiveness = {docking_config['exhaustiveness']}
num_modes = {docking_config['num_modes']}
"""
        
        config_file.write(config_content)
        config_file.close()
        
        return config_file.name
    
    def run_vina_docking(self, protein_file, ligand_file, ligand_name, docking_config):
        """Jalankan docking dengan AutoDock Vina"""
        try:
            output_file = os.path.join(self.results_dir, f"{ligand_name}_docked.pdbqt")
            log_file = os.path.join(self.results_dir, f"{ligand_name}_docking.log")
            
            # Create config file
            config_file = self.create_config_file(protein_file, ligand_file, output_file, docking_config)
            
            # Run Vina
            cmd = [
                'vina',
                '--config', config_file,
                '--log', log_file
            ]
            
            self.logger.info(f"Running docking for {ligand_name}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            # Clean up config file
            os.unlink(config_file)
            
            if result.returncode == 0 and os.path.exists(output_file):
                # Parse results
                binding_affinities = self.parse_vina_output(log_file)
                self.logger.info(f"Docking completed for {ligand_name} - Best affinity: {binding_affinities[0]:.2f} kcal/mol")
                
                return {
                    'output_file': output_file,
                    'log_file': log_file,
                    'binding_affinities': binding_affinities,
                    'best_affinity': binding_affinities[0] if binding_affinities else None
                }
            else:
                self.logger.error(f"Vina docking failed for {ligand_name}: {result.stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in Vina docking for {ligand_name}: {str(e)}")
            return None
    
    def parse_vina_output(self, log_file):
        """Parse hasil binding affinity dari log Vina"""
        affinities = []
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            parsing = False
            for line in lines:
                if "-----+------------+----------+----------" in line:
                    parsing = True
                    continue
                elif parsing and line.strip() == "":
                    break
                elif parsing and len(line.split()) >= 2:
                    try:
                        affinity = float(line.split()[1])
                        affinities.append(affinity)
                    except (ValueError, IndexError):
                        continue
                        
        except Exception as e:
            self.logger.error(f"Error parsing Vina output: {str(e)}")
        
        return affinities
    
    def run_docking_batch(self, protein_file, ligand_files, docking_config):
        """Jalankan batch docking untuk semua ligan"""
        self.logger.info(f"Starting batch docking for {len(ligand_files)} ligands...")
        
        results = {}
        
        for ligand_name, ligand_file in ligand_files.items():
            result = self.run_vina_docking(protein_file, ligand_file, ligand_name, docking_config)
            if result:
                results[ligand_name] = result
        
        # Save results to Excel
        self.save_results_to_excel(results)
        
        self.logger.info(f"Batch docking completed. {len(results)} successful dockings.")
        return results
    
    def save_results_to_excel(self, results):
        """Simpan hasil ke Excel"""
        try:
            data = []
            for ligand_name, result in results.items():
                for i, affinity in enumerate(result['binding_affinities']):
                    data.append({
                        'Ligand': ligand_name,
                        'Pose': i + 1,
                        'Binding_Affinity_kcal_mol': affinity,
                        'Output_File': result['output_file']
                    })
            
            df = pd.DataFrame(data)
            excel_file = os.path.join(self.results_dir, 'docking_results.xlsx')
            
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='All_Results', index=False)
                
                # Summary sheet
                summary_data = []
                for ligand_name, result in results.items():
                    summary_data.append({
                        'Ligand': ligand_name,
                        'Best_Binding_Affinity': result['best_affinity'],
                        'Number_of_Poses': len(result['binding_affinities'])
                    })
                
                summary_df = pd.DataFrame(summary_data)
                summary_df = summary_df.sort_values('Best_Binding_Affinity')
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            self.logger.info(f"Results saved to Excel: {excel_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving results to Excel: {str(e)}")