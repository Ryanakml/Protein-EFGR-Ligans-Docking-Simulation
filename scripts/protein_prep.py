import os
import subprocess
import requests
import tempfile
from Bio.PDB import PDBParser, PDBIO, Select
from Bio.PDB.PDBList import PDBList

class ProteinPreparator:
    def __init__(self, protein_dir, logger):
        self.protein_dir = protein_dir
        self.logger = logger
        self.pdb_parser = PDBParser(QUIET=True)
        self.pdb_io = PDBIO()
    
    def download_pdb(self, pdb_id):
        """Download struktur protein dari PDB"""
        try:
            output_file = os.path.join(self.protein_dir, f"{pdb_id}.pdb")
            
            # Check if file already exists
            if os.path.exists(output_file):
                self.logger.info(f"PDB file {pdb_id}.pdb already exists")
                return output_file
            
            # Download using BioPython's PDBList
            pdbl = PDBList()
            pdbl.retrieve_pdb_file(pdb_id, pdir=self.protein_dir, file_format="pdb")
            
            # BioPython downloads as pdb{id}.ent, rename to {id}.pdb
            ent_file = os.path.join(self.protein_dir, f"pdb{pdb_id.lower()}.ent")
            if os.path.exists(ent_file):
                os.rename(ent_file, output_file)
                self.logger.info(f"Downloaded and renamed PDB file for {pdb_id}")
                return output_file
            else:
                self.logger.error(f"Failed to download PDB file for {pdb_id}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error downloading PDB {pdb_id}: {str(e)}")
            return None
    
    def clean_pdb(self, pdb_file):
        """Membersihkan file PDB (menghapus air, ligand, dll)"""
        try:
            # Parse PDB file
            structure_id = os.path.basename(pdb_file).split('.')[0]
            structure = self.pdb_parser.get_structure(structure_id, pdb_file)
            
            # Create output file name
            output_file = os.path.join(self.protein_dir, f"{structure_id}_clean.pdb")
            
            # Define a selector to keep only protein atoms
            class ProteinSelect(Select):
                def accept_residue(self, residue):
                    # Keep only standard amino acids
                    return residue.get_resname() in ["ALA", "ARG", "ASN", "ASP", "CYS", 
                                                   "GLN", "GLU", "GLY", "HIS", "ILE", 
                                                   "LEU", "LYS", "MET", "PHE", "PRO", 
                                                   "SER", "THR", "TRP", "TYR", "VAL"]
            
            # Save only protein atoms
            self.pdb_io.set_structure(structure)
            self.pdb_io.save(output_file, ProteinSelect())
            
            self.logger.info(f"Cleaned PDB file saved as {output_file}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error cleaning PDB file {pdb_file}: {str(e)}")
            return None
    
    def pdb_to_pdbqt(self, pdb_file):
        """Convert PDB ke PDBQT menggunakan MGLTools"""
        try:
            # Create output file name
            base_name = os.path.basename(pdb_file).split('.')[0]
            output_file = os.path.join(self.protein_dir, f"{base_name}.pdbqt")
            
            # Use MGLTools' prepare_receptor4.py via subprocess
            # Assuming MGLTools is installed and in PATH
            cmd = f"prepare_receptor4.py -r {pdb_file} -o {output_file} -A hydrogens"
            
            # Alternative: use Open Babel if MGLTools not available
            # cmd = f"obabel {pdb_file} -O {output_file} -xr"
            
            self.logger.info(f"Running command: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.logger.error(f"Error converting PDB to PDBQT: {stderr.decode()}")
                # Fallback to Open Babel if MGLTools fails
                cmd = f"obabel {pdb_file} -O {output_file} -xr"
                self.logger.info(f"Trying fallback with Open Babel: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    self.logger.error(f"Fallback also failed: {stderr.decode()}")
                    return None
            
            if os.path.exists(output_file):
                self.logger.info(f"Successfully converted to PDBQT: {output_file}")
                return output_file
            else:
                self.logger.error(f"PDBQT file was not created")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in PDB to PDBQT conversion: {str(e)}")
            return None
    
    def prepare_protein(self, pdb_id):
        """Pipeline lengkap untuk persiapan protein"""
        self.logger.info(f"Starting protein preparation for {pdb_id}")
        
        # Download PDB
        pdb_file = self.download_pdb(pdb_id)
        if not pdb_file:
            self.logger.error(f"Failed to download PDB {pdb_id}")
            return None
        
        # Clean PDB
        clean_pdb = self.clean_pdb(pdb_file)
        if not clean_pdb:
            self.logger.error(f"Failed to clean PDB {pdb_id}")
            return None
        
        # Convert to PDBQT
        pdbqt_file = self.pdb_to_pdbqt(clean_pdb)
        if not pdbqt_file:
            self.logger.error(f"Failed to convert PDB to PDBQT for {pdb_id}")
            return None
        
        self.logger.info(f"Protein preparation complete for {pdb_id}")
        return pdbqt_file