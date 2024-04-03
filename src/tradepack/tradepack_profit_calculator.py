import streamlit as st
import pandas as pd
import numpy as np
import src.tradepack.constants as constants


tradeposts = constants.tradeposts
tradepacks = constants.tradepacks
tradeposts_tiles_df = pd.read_csv('./data/tradeposts_tiles.csv', index_col=0)
def load_tradepack_demands():
    # Tenta carregar o DataFrame do CSV
    df = pd.read_csv('./data/tradepacks_demands.csv', index_col=0)
    return df

def on_click_save_tradepack_demands():
    st.session_state["tradepacks_demands"].to_csv('./data/tradepacks_demands.csv', index=True)


def calculate_tradepack_sell_price(df):
    # Mesclar os dataframes
    df_final = df.merge(st.session_state["tradepacks_demands"], left_on= "Tradepack", right_index=True)

    # Multiplicar os custos totais pelas demandas de cada cidade
    for tradepost in st.session_state["tradepacks_demands"].columns:
        df_final[tradepost + '_sell'] = (10000 + (tradeposts_tiles_df.loc[st.session_state["start_location_selected"],tradepost] * 6)*df_final[tradepost]/100)
    return df_final.drop(columns = st.session_state["tradepacks_demands"].columns)


def run_tradepack_profit_calculator_tab():
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state["start_location_selected"] = st.selectbox("Start Location", options= tradeposts)
            tradepacks_available = tradepacks.copy()
            if "selected_tradepacks" not in st.session_state:
                st.session_state["selected_tradepacks"] = tradepacks_available
            tradepacks_available = st.multiselect("Select Tradepacks", options= tradepacks_available, default=st.session_state["selected_tradepacks"])
        with col2:
            tradeposts_available = tradeposts.copy()
            # tradeposts_available.remove(st.session_state["start_location_selected"])
            if "selected_tradeposts" not in st.session_state:
                st.session_state["selected_tradeposts"] = tradeposts_available
            tradeposts_available = st.multiselect("Select Tradeposts", options= tradeposts_available, default=st.session_state["selected_tradeposts"])

    with st.container(border=True):
        st.session_state["tradepacks_demands"] = load_tradepack_demands()
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            edited_df = st.data_editor(st.session_state["tradepacks_demands"].loc[tradepacks_available,tradeposts_available].sort_index())
            if edited_df is not None:
                st.session_state["tradepacks_demands"] = edited_df.sort_index()
            st.button("Save Demands", on_click=on_click_save_tradepack_demands, use_container_width=True)
        with col2:
            combined_df = pd.concat(st.session_state["tradepacks_df"])
            # Agregue os valores pela chave do dicionário e calcule a soma de 'total_cost'
            result_df = combined_df.groupby(level=0)['total_cost'].sum().reset_index().sort_values("total_cost").rename(columns={"index": "Tradepack"})
            st.dataframe(result_df, hide_index=True)
    
    profit_df = calculate_tradepack_sell_price(result_df)
    st.markdown(f"Profit Table")
    st.dataframe(profit_df, hide_index=True)


    
    
    
