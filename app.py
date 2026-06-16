import streamlit as st
import os
from vina import Vina

st.set_page_config(page_title="BioDock Web Portal", layout="wide")

st.title("🧬 Molecular Docking Web Portal")
st.write("Upload your structural files, define your grid box parameters, and run AutoDock Vina directly from the web.")

# Create two columns for layout: Inputs on the left, Execution on the right
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Upload Inputs (.pdbqt)")
    receptor_file = st.file_uploader("Upload Receptor", type=["pdbqt"])
    ligand_file = st.file_uploader("Upload Ligand", type=["pdbqt"])
    
    st.header("2. Grid Box Configuration")
    st.write("Set the center coordinates and box dimensions (in Angstroms):")
    
    # Grid coordinates input
    cx = st.number_input("Center X", value=0.0)
    cy = st.number_input("Center Y", value=0.0)
    cz = st.number_input("Center Z", value=0.0)
    
    # Box size input
    sx = st.number_input("Size X (Angstroms)", value=20.0, min_value=5.0)
    sy = st.number_input("Size Y (Angstroms)", value=20.0, min_value=5.0)
    sz = st.number_input("Size Z (Angstroms)", value=20.0, min_value=5.0)

with col2:
    st.header("3. Run Simulation")
    exhaustiveness = st.slider("Search Exhaustiveness", min_value=1, max_value=20, value=8)
    
    if st.button("Launch Docking Simulation", type="primary"):
        if receptor_file is not None and ligand_file is not None:
            with st.spinner("Running docking algorithm... Please wait..."):
                try:
                    # Save uploaded files temporarily to disk for Vina to read
                    with open("temp_receptor.pdbqt", "wb") as f:
                        f.write(receptor_file.getbuffer())
                    with open("temp_ligand.pdbqt", "wb") as f:
                        f.write(ligand_file.getbuffer())
                    
                    # Initialize Vina
                    v = Vina(sf_name='vina')
                    v.set_receptor("temp_receptor.pdbqt")
                    v.set_ligand_from_file("temp_ligand.pdbqt")
                    
                    # Compute map based on user input coordinates
                    v.compute_vina_maps(center=[cx, cy, cz], box_size=[sx, sy, sz])
                    
                    # Run Docking
                    v.dock(exhaustiveness=exhaustiveness, n_poses=10)
                    
                    # Save results
                    output_filename = "docked_output.pdbqt"
                    v.write_poses(output_filename, n_poses=10, overwrite=True)
                    
                    st.success("🎉 Docking Completed Successfully!")
                    
                    # Provide Download Button for the results
                    with open(output_filename, "rb") as file:
                        st.download_button(
                            label="📥 Download Docked Poses (.pdbqt)",
                            data=file,
                            file_name="docked_output.pdbqt",
                            mime="text/plain"
                        )
                        
                except Exception as e:
                    st.error(f"An error occurred during simulation: {e}")
        else:
            st.error("⚠️ Please upload both the receptor and ligand files before running.")
          
