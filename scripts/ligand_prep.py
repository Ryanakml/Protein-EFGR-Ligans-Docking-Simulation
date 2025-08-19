import os
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import tempfile

class LigandPreparator:
    def __init__(self, ligand_dir, logger):
        self.ligand_dir = ligand_dir
        self.logger = logger
    
    def smiles_to_3d_mol(self, smiles, name):
        """Convert SMILES ke molekul 3D"""
        try:
            # Parse SMILES
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                self.logger.error(f"Invalid SMILES for {name}: {smiles}")
                return None
            
            # Add hydrogens
            mol = Chem.AddHs(mol)
            
            # Generate 3D coordinates
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol)
            
            # Calculate drug-like properties
            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = Descriptors.NumHDonors(mol)
            hba = Descriptors.NumHAcceptors(mol)
            
            self.logger.info(f"Ligand {name} properties - MW: {mw:.2f}, LogP: {logp:.2f}, HBD: {hbd}, HBA: {hba}")
            
            return mol
            
        except Exception as e:
            self.logger.error(f"Error generating 3D structure for {name}: {str(e)}")
            return None
    
    def mol_to_pdbqt(self, mol, name):
        """Convert RDKit mol ke PDBQT"""
        try:
            # Save as SDF first
            sdf_file = os.path.join(self.ligand_dir, f"{name}.sdf")
            writer = Chem.SDWriter(sdf_file)
            writer.write(mol)
            writer.close()
            
            # Convert SDF to PDBQT using obabel
            pdbqt_file = os.path.join(self.ligand_dir, f"{name}.pdbqt")
            
            cmd = [
                'obabel',
                '-isdf', sdf_file,
                '-opdbqt', pdbqt_file,
                '--gen3d'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(pdbqt_file):
                self.logger.info(f"Generated PDBQT for {name}: {pdbqt_file}")
                # Clean up SDF file
                os.remove(sdf_file)
                return pdbqt_file
            else:
                self.logger.error(f"PDBQT generation failed for {name}: {result.stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error converting {name} to PDBQT: {str(e)}")
            return None
    
    def prepare_ligands(self, ligand_dict):
        """Preparasi batch ligands"""
        self.logger.info(f"Preparing {len(ligand_dict)} ligands...")
        
        prepared_ligands = {}
        
        for name, smiles in ligand_dict.items():
            self.logger.info(f"Preparing ligand: {name}")
            
            # Generate 3D structure
            mol = self.smiles_to_3d_mol(smiles, name)
            if not mol:
                continue
            
            # Convert to PDBQT
            pdbqt_file = self.mol_to_pdbqt(mol, name)
            if pdbqt_file:
                prepared_ligands[name] = pdbqt_file
        
        self.logger.info(f"Successfully prepared {len(prepared_ligands)} ligands")
        return prepared_ligands