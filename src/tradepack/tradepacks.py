import streamlit as st
import pandas as pd
import src.tradepack.constants as constants


def load_tradepacks():
    return constants.tradepacks

# def calculate_total_cost(tradepack):
#     total_cost = 0
#     for material, quantity in tradepack.items():
#         material_price = st.session_state["tradepack_materials"].loc[st.session_state["tradepack_materials"]['name'] == material, 'price'].values[0]
#         total_cost += material_price * quantity
#     return total_cost



def run_tradepack_calculator_tab():
    st.session_state["tradepacks_df"] = {}
    tradepacks = load_tradepacks()
    for tradepack_name, tradepack_materials in tradepacks.items():
        tradepack_df = pd.DataFrame(tradepack_materials.items(), columns=['material', 'quantity'])
        tradepack_df['material_price'] = tradepack_df['material'].map(st.session_state["tradepack_materials"].set_index('name')['price'])
        tradepack_df['total_cost'] = tradepack_df['quantity'] * tradepack_df['material_price']
        # total_cost = calculate_total_cost(tradepack_materials)
        # tradepack_df.loc[len(tradepack_df)] = total_cost
        st.session_state["tradepacks_df"][tradepack_name] = tradepack_df

    sorted_tradepacks_dfs = {k: v for k, v in sorted(st.session_state["tradepacks_df"].items(), key=lambda item: item[1]['total_cost'].sum(), reverse=False)}

    # st.container(border=True)
    col1, col2, col3 = st.columns(3)
 
    for i, (tradepack_name, tradepack_df) in enumerate(sorted_tradepacks_dfs.items()):
        if i % 3 == 0:
            col1.markdown(f"*{tradepack_name}*.  **Total Cost: { tradepack_df.total_cost.sum()}**")
            col1.dataframe(tradepack_df, hide_index=True)
        elif i % 3 == 1:
            col2.markdown(f"*{tradepack_name}*.  **Total Cost: { tradepack_df.total_cost.sum()}**")
            col2.dataframe(tradepack_df, hide_index=True)
        else:
            col3.markdown(f"*{tradepack_name}*.  **Total Cost: { tradepack_df.total_cost.sum()}**")
            col3.dataframe(tradepack_df, hide_index=True)
            # st.container(border=True)
            col1, col2, col3 = st.columns(3)