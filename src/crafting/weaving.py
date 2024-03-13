import streamlit as st
import pandas as pd

MARKET_TAX_COMPENSATOR = 1.0417

st.session_state["qtd_craft"] = 1


# Dados fornecidos
def load_weaving_crafting_data():
    # Tenta carregar o DataFrame do CSV
    df = pd.read_csv('./data/weaving_crafting_info.csv')
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
    return st.session_state["df_crafting_info"].round(0)


def run_weaving_crafting_table():
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