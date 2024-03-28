import streamlit as st
import pandas as pd


def load_tradepack_materials_data():
    # Tenta carregar o DataFrame do CSV
    df = pd.read_csv('./data/tradepack_materials.csv')
    return df

def on_click_save_tradepack_data():
    st.session_state["tradepack_materials"].to_csv('./data/tradepack_materials.csv', index=False)

def run_tradepack_materials_table():

    st.session_state["tradepack_materials"] = load_tradepack_materials_data()

    tradepack_material_data_column_config={
            "material": st.column_config.ImageColumn(
                "material"
            )
        }

    st.caption("Set price material here to update tradepack table")
    edit_df = st.data_editor(st.session_state["tradepack_materials"],hide_index=True,column_config=tradepack_material_data_column_config, use_container_width=True, disabled=["material", "name"])
    if edit_df is not None:
        st.session_state["tradepack_materials"] = edit_df
    st.button("Save prices", on_click=on_click_save_tradepack_data, use_container_width=True)