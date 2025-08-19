import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import py3Dmol

class ResultVisualizer:
    def __init__(self, results_dir, logger):
        self.results_dir = results_dir
        self.logger = logger
        plt.style.use('seaborn-v0_8')
    
    def create_binding_affinity_chart(self, docking_results):
        """Buat chart binding affinity"""
        try:
            # Prepare data
            ligands = []
            affinities = []
            
            for ligand_name, result in docking_results.items():
                ligands.append(ligand_name)
                affinities.append(result['best_affinity'])
            
            # Sort by affinity
            sorted_data = sorted(zip(ligands, affinities), key=lambda x: x[1])
            sorted_ligands, sorted_affinities = zip(*sorted_data)
            
            # Create plot
            fig, ax = plt.subplots(figsize=(12, 8))
            
            bars = ax.barh(sorted_ligands, sorted_affinities, 
                          color=plt.cm.RdYlBu_r([abs(x)/max(abs(min(sorted_affinities)), abs(max(sorted_affinities))) 
                                                for x in sorted_affinities]))
            
            ax.set_xlabel('Binding Affinity (kcal/mol)')
            ax.set_title('EGFR Ligand Binding Affinities', fontsize=16, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for i, (bar, affinity) in enumerate(zip(bars, sorted_affinities)):
                ax.text(affinity - 0.5, i, f'{affinity:.2f}', 
                       va='center', ha='right', fontweight='bold')
            
            plt.tight_layout()
            
            # Save plot
            chart_file = os.path.join(self.results_dir, 'binding_affinity_chart.png')
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Binding affinity chart saved: {chart_file}")
            
        except Exception as e:
            self.logger.error(f"Error creating binding affinity chart: {str(e)}")
    
    def create_interaction_plots(self, docking_results):
        """Buat plot interaksi dan distribusi"""
        try:
            # Prepare data for all poses
            all_data = []
            for ligand_name, result in docking_results.items():
                for i, affinity in enumerate(result['binding_affinities']):
                    all_data.append({
                        'Ligand': ligand_name,
                        'Pose': i + 1,
                        'Binding_Affinity': affinity
                    })
            
            df = pd.DataFrame(all_data)
            
            # Create subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            
            # 1. Box plot
            sns.boxplot(data=df, x='Ligand', y='Binding_Affinity', ax=axes[0,0])
            axes[0,0].set_title('Binding Affinity Distribution by Ligand')
            axes[0,0].tick_params(axis='x', rotation=45)
            
            # 2. Violin plot
            sns.violinplot(data=df, x='Ligand', y='Binding_Affinity', ax=axes[0,1])
            axes[0,1].set_title('Binding Affinity Distribution (Violin Plot)')
            axes[0,1].tick_params(axis='x', rotation=45)
            
            # 3. Histogram of all affinities
            axes[1,0].hist(df['Binding_Affinity'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            axes[1,0].set_xlabel('Binding Affinity (kcal/mol)')
            axes[1,0].set_ylabel('Frequency')
            axes[1,0].set_title('Overall Binding Affinity Distribution')
            axes[1,0].grid(alpha=0.3)
            
            # 4. Best pose comparison
            best_poses = df.groupby('Ligand')['Binding_Affinity'].min().reset_index()
            best_poses = best_poses.sort_values('Binding_Affinity')
            
            axes[1,1].bar(range(len(best_poses)), best_poses['Binding_Affinity'], 
                         color=plt.cm.viridis(range(len(best_poses))))
            axes[1,1].set_xticks(range(len(best_poses)))
            axes[1,1].set_xticklabels(best_poses['Ligand'], rotation=45)
            axes[1,1].set_ylabel('Best Binding Affinity (kcal/mol)')
            axes[1,1].set_title('Best Pose Comparison')
            axes[1,1].grid(alpha=0.3)
            
            plt.tight_layout()
            
            # Save plot
            interaction_file = os.path.join(self.results_dir, 'interaction_analysis.png')
            plt.savefig(interaction_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Interaction plots saved: {interaction_file}")
            
        except Exception as e:
            self.logger.error(f"Error creating interaction plots: {str(e)}")
    
    def create_3d_visualization(self, protein_file, docking_results):
        """Buat visualisasi 3D interaktif"""
        try:
            # Ambil ligan dengan binding affinity terbaik
            best_ligand = min(docking_results.items(), key=lambda x: x[1]['best_affinity'])
            ligand_name, ligand_result = best_ligand
            
            # Read protein structure
            with open(protein_file, 'r') as f:
                protein_pdb = f.read()
            
            # Read best ligand pose
            if os.path.exists(ligand_result['output_file']):
                with open(ligand_result['output_file'], 'r') as f:
                    ligand_pdbqt = f.read()
                
                # Convert PDBQT to PDB format for visualization
                ligand_pdb = self.pdbqt_to_pdb_string(ligand_pdbqt)
            else:
                ligand_pdb = ""
            
            # Create 3D visualization HTML
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>EGFR-{ligand_name} Docking Visualization</title>
    <script src="https://3dmol.org/build/3Dmol-min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        #container {{ width: 100%; height: 600px; position: relative; }}
        #info {{ margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px; }}
        .controls {{ margin-bottom: 20px; }}
        button {{ margin: 5px; padding: 10px; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>EGFR-{ligand_name} Molecular Docking Visualization</h1>
    
    <div class="controls">
        <button onclick="showProtein()">Show Protein</button>
        <button onclick="showLigand()">Show Ligand</button>
        <button onclick="showBoth()">Show Both</button>
        <button onclick="showSurface()">Show Surface</button>
        <button onclick="resetView()">Reset View</button>
    </div>
    
    <div id="container"></div>
    
    <div id="info">
        <h3>Docking Results Summary:</h3>
        <p><strong>Best Ligand:</strong> {ligand_name}</p>
        <p><strong>Binding Affinity:</strong> {ligand_result['best_affinity']:.2f} kcal/mol</p>
        <p><strong>Number of Poses:</strong> {len(ligand_result['binding_affinities'])}</p>
        
        <h3>All Ligand Results:</h3>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr><th>Ligand</th><th>Best Affinity (kcal/mol)</th><th>Poses</th></tr>"""
            
            # Add results table
            for name, result in sorted(docking_results.items(), key=lambda x: x[1]['best_affinity']):
                html_content += f"""
            <tr>
                <td>{name}</td>
                <td>{result['best_affinity']:.2f}</td>
                <td>{len(result['binding_affinities'])}</td>
            </tr>"""
            
            html_content += f"""
        </table>
    </div>

    <script>
        let viewer = null;
        
        function initViewer() {{
            let element = document.getElementById('container');
            let config = {{ backgroundColor: 'white' }};
            viewer = $3Dmol.createViewer(element, config);
            
            // Add protein
            viewer.addModel(`{protein_pdb}`, "pdb");
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum'}}}});
            
            // Add ligand if available
            if (`{ligand_pdb}`.length > 0) {{
                viewer.addModel(`{ligand_pdb}`, "pdb");
                viewer.setStyle({{model: 1}}, {{stick: {{colorscheme: 'greenCarbon', radius: 0.2}}}});
            }}
            
            viewer.zoomTo();
            viewer.render();
        }}
        
        function showProtein() {{
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum'}}}});
            viewer.setStyle({{model: 1}}, {{}});
            viewer.render();
        }}
        
        function showLigand() {{
            viewer.setStyle({{}}, {{}});
            viewer.setStyle({{model: 1}}, {{stick: {{colorscheme: 'greenCarbon', radius: 0.2}}}});
            viewer.render();
        }}
        
        function showBoth() {{
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum', opacity: 0.8}}}});
            viewer.setStyle({{model: 1}}, {{stick: {{colorscheme: 'greenCarbon', radius: 0.2}}}});
            viewer.render();
        }}
        
        function showSurface() {{
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum'}}}});
            viewer.addSurface($3Dmol.SurfaceType.VDW, {{opacity: 0.3, color: 'white'}});
            viewer.setStyle({{model: 1}}, {{stick: {{colorscheme: 'greenCarbon', radius: 0.2}}}});
            viewer.render();
        }}
        
        function resetView() {{
            viewer.clear();
            initViewer();
        }}
        
        // Initialize viewer when page loads
        window.onload = function() {{
            initViewer();
        }};
    </script>
</body>
</html>"""
            
            # Save HTML file
            html_file = os.path.join(self.results_dir, 'docking_visualization.html')
            with open(html_file, 'w') as f:
                f.write(html_content)
            
            self.logger.info(f"3D visualization saved: {html_file}")
            
        except Exception as e:
            self.logger.error(f"Error creating 3D visualization: {str(e)}")
    
    def pdbqt_to_pdb_string(self, pdbqt_content):
        """Convert PDBQT content to PDB format for visualization"""
        try:
            pdb_lines = []
            for line in pdbqt_content.split('\n'):
                if line.startswith(('ATOM', 'HETATM')):
                    # Convert PDBQT line to PDB format (remove extra columns)
                    pdb_line = line[:66] + '  1.00  0.00' + line[66:78] if len(line) > 78 else line[:66] + '  1.00  0.00'
                    pdb_lines.append(pdb_line)
                elif line.startswith(('MODEL', 'ENDMDL', 'END')):
                    pdb_lines.append(line)
            
            return '\n'.join(pdb_lines[:100])  # Limit lines for web display
        except:
            return ""
    
    def generate_analysis_report(self, docking_results):
        """Generate comprehensive analysis report"""
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            
            pdf_file = os.path.join(self.results_dir, 'analysis_report.pdf')
            
            with PdfPages(pdf_file) as pdf:
                # Page 1: Summary
                fig, ax = plt.subplots(figsize=(8, 11))
                ax.axis('off')
                
                report_text = "EGFR MOLECULAR DOCKING ANALYSIS REPORT\n\n"
                report_text += "="*50 + "\n\n"
                
                # Summary statistics
                all_affinities = []
                for result in docking_results.values():
                    all_affinities.extend(result['binding_affinities'])
                
                report_text += f"SUMMARY STATISTICS:\n"
                report_text += f"- Number of ligands tested: {len(docking_results)}\n"
                report_text += f"- Total poses generated: {len(all_affinities)}\n"
                report_text += f"- Best binding affinity: {min(all_affinities):.2f} kcal/mol\n"
                report_text += f"- Average binding affinity: {sum(all_affinities)/len(all_affinities):.2f} kcal/mol\n"
                report_text += f"- Standard deviation: {pd.Series(all_affinities).std():.2f} kcal/mol\n\n"
                
                # Top 3 ligands
                sorted_ligands = sorted(docking_results.items(), key=lambda x: x[1]['best_affinity'])
                report_text += "TOP 3 LIGANDS:\n"
                for i, (name, result) in enumerate(sorted_ligands[:3], 1):
                    report_text += f"{i}. {name}: {result['best_affinity']:.2f} kcal/mol\n"
                
                report_text += "\n" + "="*50 + "\n\n"
                
                # Detailed results
                report_text += "DETAILED RESULTS:\n\n"
                for name, result in sorted_ligands:
                    report_text += f"{name}:\n"
                    report_text += f"  Best Affinity: {result['best_affinity']:.2f} kcal/mol\n"
                    report_text += f"  Number of Poses: {len(result['binding_affinities'])}\n"
                    report_text += f"  All Affinities: {', '.join([f'{a:.2f}' for a in result['binding_affinities'][:5]])}"
                    if len(result['binding_affinities']) > 5:
                        report_text += " ..."
                    report_text += "\n\n"
                
                ax.text(0.05, 0.95, report_text, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', fontfamily='monospace')
                
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
                
                # Page 2: Binding affinity chart
                self.create_binding_affinity_chart(docking_results)
                fig = plt.figure(figsize=(8, 11))
                img = plt.imread(os.path.join(self.results_dir, 'binding_affinity_chart.png'))
                plt.imshow(img)
                plt.axis('off')
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
            
            self.logger.info(f"Analysis report saved: {pdf_file}")
            
        except Exception as e:
            self.logger.error(f"Error generating analysis report: {str(e)}")