import streamlit as st
import pandas as pd


def load_weaving_data():
    # Tenta carregar o DataFrame do CSV
    df = pd.read_csv('./data/weaving_materials.csv')
    return df

def on_click_save_data():
    st.session_state["weaving_materials"].to_csv('weaving_materials.csv', index=False)

def run_weaving_materials_table():

    st.session_state["weaving_materials"] = load_weaving_data()

    weaving_material_column_config={
        "name": st.column_config.Column(
            disabled=True,
        ),
        "type": st.column_config.Column(
            disabled=False,
        )
    }

    edit_df = st.data_editor(st.session_state["weaving_materials"],hide_index=True,column_config=weaving_material_column_config, use_container_width=True)
    if edit_df is not None:
        st.session_state["weaving_materials"] = edit_df
    st.button("Save data", on_click=on_click_save_data, use_container_width=True)