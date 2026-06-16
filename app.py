import streamlit as st

st.title("🧬 Molecular Docking Portal")
st.write("Welcome to the docking interface. The engine is currently being optimized.")

col1, col2 = st.columns(2)
with col1:
    st.header("Input Files")
    receptor = st.file_uploader("Upload Receptor", type=["pdbqt"])
    ligand = st.file_uploader("Upload Ligand", type=["pdbqt"])

with col2:
    st.header("Results")
    if st.button("Run Docking"):
        if receptor and ligand:
            st.info("Simulation initialized. This demo portal is connected and ready for backend integration.")
        else:
            st.warning("Please upload files to proceed.")
