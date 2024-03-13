import streamlit as st
import pandas as pd
import src.infusion_calculator.infusion as infusion
import src.crafting.weaving_materials as weaving_materials
import src.crafting.weaving as weaving_craft

st.set_page_config(layout='wide')
st.markdown("<h2 style='text-align: center;'>Ravendawn Calculators</h2>", unsafe_allow_html=True)

with st.sidebar:
    weaving_material_tab, tab2 = st.tabs(["Weaving Material", "tab2"])
    with weaving_material_tab:
        weaving_materials.run_weaving_materials_table()


crafting_tab, infusion_tab = st.tabs(["Crafting Calculator", "Infusion Calculator"])
with crafting_tab:
    weaving_crafting_tab, blacksmithing_crafting_tab = st.tabs(["Weaving", "Blacksmith"])
    with weaving_crafting_tab:
        weaving_craft.run_weaving_crafting_table()
with infusion_tab:
    infusion.run_infusion_tab()
    