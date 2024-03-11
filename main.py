import streamlit as st
import pandas as pd
import numpy as np

MARKET_TAX_COMPENSATOR = 1.0417
st.set_page_config(layout='wide')

st.header('Calculadora de Crafting')

st.session_state["qtd_craft"] = 1
# Dados fornecidos
def load_weaving_data():
    # Tenta carregar o DataFrame do CSV
    df = pd.read_csv('weaving_materials.csv')
    return df

# Dados fornecidos
def load_weaving_crafting_data():
    # Tenta carregar o DataFrame do CSV
    df = pd.read_csv('weaving_crafting_info.csv')
    df['qtd_material_1'] = df['qtd_material_1'].fillna(0) * st.session_state["qtd_craft"]
    df['qtd_material_2'] = df['qtd_material_2'].fillna(0) * st.session_state["qtd_craft"]
    df['qtd_material_3'] = df['qtd_material_3'].fillna(0) * st.session_state["qtd_craft"]
    df['qtd_material_4'] = df['qtd_material_4'].fillna(0) * st.session_state["qtd_craft"]
    df['tax'] = df['tax'] * st.session_state["qtd_craft"]
    df['xp'] = df['xp'] * st.session_state["qtd_craft"]
    df['cost'] = (
    df['tax'] +
    df['material_1'].map(st.session_state["weaving_materials"].set_index('name')['price']).fillna(0) * df['qtd_material_1'].fillna(0) +
    df['material_2'].map(st.session_state["weaving_materials"].set_index('name')['price']).fillna(0) * df['qtd_material_2'].fillna(0) +
    df['material_3'].map(st.session_state["weaving_materials"].set_index('name')['price']).fillna(0) * df['qtd_material_3'].fillna(0) +
    df['material_4'].map(st.session_state["weaving_materials"].set_index('name')['price']).fillna(0) * df['qtd_material_4'].fillna(0)
)
    df['lucro'] = (st.session_state["weaving_materials"].set_index('name').loc[df['craft']]['price'].values) *  st.session_state["qtd_craft"] - df['cost']
    df['lucro/xp'] = df['lucro'] / df['xp']
    df['breakeven'] = df['cost'] /  st.session_state["qtd_craft"] * MARKET_TAX_COMPENSATOR
    col_order = ["craft","cost", "lucro","lucro/xp","breakeven", "xp", "material_1","qtd_material_1", "material_2","qtd_material_2", "material_3","qtd_material_3", "material_4","qtd_material_4"]
    st.session_state["df_crafting_info"] = df[col_order]
    return st.session_state["df_crafting_info"]


def on_click_save_data():
    st.session_state["weaving_materials"].to_csv('weaving_materials.csv', index=False)

# Criar ou carregar o DataFrame
st.session_state["weaving_materials"] = load_weaving_data()
df_crafting_info = load_weaving_crafting_data()


with st.sidebar:
    weaving_material_tab, tab2 = st.tabs(["Weaving Material", "tab2"])
    with weaving_material_tab:
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
            # edit_df.to_csv('weaving_materials.csv', index=False)
            st.session_state["weaving_materials"] = edit_df
        st.button("Save data", on_click=on_click_save_data, use_container_width=True)



weaving_crafting_tab, blacksmithing_crafting_tab = st.tabs(["Weaving", "Blacksmith"])
with weaving_crafting_tab:
    st.session_state["qtd_craft"] = st.number_input("quantidade a ser craftado", format='%d', value = 1, min_value=1)
    # Criar ou carregar o DataFrame

    df_crafting_info = load_weaving_crafting_data()
    # Filtrar os tipos únicos de df_weaving_materials
    weaving_types = st.session_state["weaving_materials"].loc[st.session_state["weaving_materials"]['type'] != "Materials"]['type'].unique()

    df_weaving_types = {}
    for weaving_type in weaving_types:
        # Obter as linhas correspondentes com base no tipo
        df_crafting_filtered = df_crafting_info[df_crafting_info['craft'].isin(st.session_state["weaving_materials"][st.session_state["weaving_materials"]['type'] == weaving_type]['name'])]
        
        # Armazenar o DataFrame filtrado no dicionário
        df_weaving_types[weaving_type] = df_crafting_filtered

    # Exibindo o resultado
    for weaving_type, df_crafting_filtered in df_weaving_types.items():
        st.subheader(weaving_type)
        st.dataframe(df_crafting_filtered.sort_values(by='lucro', ascending=False),hide_index=True)