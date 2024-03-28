import streamlit as st
import pandas as pd
import src.infusion_calculator.infusion as infusion
import src.crafting.weaving_materials as weaving_materials
import src.crafting.weaving as weaving_craft
import src.tradepack.tradepack_material as tradepack_material
import src.tradepack.tradepacks as tradepacks_calculator
import src.tradepack.tradepack_profit_calculator as tradepacks_profit

st.set_page_config(layout='wide')
st.markdown("<h2 style='text-align: center;'>Ravendawn Calculators</h2>", unsafe_allow_html=True)

with st.sidebar:
    weaving_material_tab, tradepack_material_tab = st.tabs(["Weaving Material", "Tradepack Material"])
    with weaving_material_tab:
        weaving_materials.run_weaving_materials_table()
    with tradepack_material_tab:
        tradepack_material.run_tradepack_materials_table()


crafting_tab, tradepack_tab, infusion_tab = st.tabs(["Crafting Calculator", "Tradepack Calculator", "Infusion Calculator"])
with crafting_tab:
    weaving_crafting_tab, blacksmithing_crafting_tab = st.tabs(["Weaving", "Blacksmith"])
    with weaving_crafting_tab:
        weaving_craft.run_weaving_crafting_table()
with tradepack_tab:
    all_tradepacks_tab, profit_tab = st.tabs(["Tradepacks Overview", "Profit Table"])
    with all_tradepacks_tab:
        tradepacks_calculator.run_tradepack_calculator_tab()

    with profit_tab:
        tradepacks_profit.run_tradepack_profit_calculator_tab()
with infusion_tab:
    infusion.run_infusion_tab()
    