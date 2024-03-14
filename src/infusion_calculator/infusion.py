import streamlit as st
import pandas as pd

def load_infusion_data():
    df = pd.read_csv(f'./data/infusions_price.csv')
    return df

def calculate_infusion_cost(initial_grade, final_grade, tier, df):
        initial_grade_index = df[df["Grade"] == initial_grade].index[0]
        final_grade_index = df[df["Grade"] == final_grade].index[0]
        total_sum = df.loc[initial_grade_index:final_grade_index, tier ].sum()
        ratio = st.session_state["infusion_data"]['xp'] / st.session_state["infusion_data"]['price']
        infusion = st.session_state["infusion_data"]
        best_infusion = st.session_state["infusion_data"].loc[ratio.idxmax()]
        infusion_qty = total_sum/best_infusion["xp"]
        cost = (total_sum * 2) + infusion_qty*best_infusion["price"]
        data = [best_infusion['name'],infusion_qty, cost ]
        columns = ["Infusion to Buy", "Infusion Quantity", "Infusion Total Cost"]
        return pd.DataFrame(data= [data], columns = columns).round(0)


def on_click_save_infusion_data():
    st.session_state["infusion_data"].to_csv('./data/infusions_price.csv', index=False)


infusion_group_types = {
    'Armors, Helmets, Legs, Boots and Fishing items': 'armor_and_fishing_infusions',
    'One Handed Weapons': 'one_handed_weapons_infusions',
    'Two Handed Weapons': 'two_handed_weapons_infusions',
    'Profession Gloves and Bracers': 'profession_gloves_bracers_infusions',
    'Profession Equipments': 'profession_equipments_infusions'
}

def run_infusion_tab():

    st.session_state["infusion_data"] = load_infusion_data()    

    infusion_cost_calculator, infusion_price = st.columns(2)
    with infusion_price:
        st.markdown("<h3 style='text-align: center;'>Infusion price table</h3>", unsafe_allow_html=True)
        
        st.caption("Update infusion prices here", unsafe_allow_html=True)
        infusion_data_column_config={
            "infusion": st.column_config.ImageColumn(
                "infusion"
            ),
            "name": st.column_config.Column(
                disabled=True,
            ),
            "xp": st.column_config.Column(
                disabled=True,
            )
        }
        edit_df = st.data_editor(st.session_state["infusion_data"],hide_index=True,column_config=infusion_data_column_config, use_container_width=True, key = "asljkaskd")
        if edit_df is not None:
            st.session_state["infusion_data"] = edit_df
        st.button("Save Infusion Data", on_click=on_click_save_infusion_data, use_container_width=True)

    with infusion_cost_calculator:
        st.caption("Select Item, grade and tier", unsafe_allow_html=True)
        option_selected = st.selectbox("Item group", options= infusion_group_types.keys())
        infusion_group_selected = infusion_group_types[option_selected]
        df_infusion = pd.read_csv(f'./data/{infusion_group_selected}.csv')
        # Get column names starting with "tier"
        tier_columns_names = [col for col in df_infusion.columns if col.startswith('Tier')]
        tier_selected = st.selectbox("Item Tier:", options= tier_columns_names)

        initial_grade_selected = st.selectbox("From Grade:", options= df_infusion["Grade"])
        final_grade_selected = st.selectbox("To Grade:", options= df_infusion["Grade"])
        df_infusion_cost = calculate_infusion_cost(initial_grade=initial_grade_selected, final_grade=final_grade_selected,tier=tier_selected,df = df_infusion)
        st.markdown("**Infusion Needed**")
        st.dataframe(df_infusion_cost, hide_index=True)