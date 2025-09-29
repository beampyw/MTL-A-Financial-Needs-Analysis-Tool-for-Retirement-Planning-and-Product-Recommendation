# main_app.py

import streamlit as st

st.set_page_config(
    page_title="A Financial Needs Analysis Tool for Retirement Planning and Product Recommendation",
    page_icon="https://www.muangthai.co.th/assets/c7141db6-903c-4e5e-91c6-1c609f5acea9?width=360&height=453",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
            
</style>
""", unsafe_allow_html=True)

from pages import page0, page1, page2, page3
from utils import display_profile_box

def load_page(page_name):
    st.session_state.current_page = page_name

    if page_name == 'page0':
        page0.app()
    elif page_name == 'page1':
        page1.app()
    elif page_name == 'page2':
        page2.app()
    elif page_name == 'page3':
        page3.app()

def main():
     # ตรวจสอบและกำหนดค่าเริ่มต้นให้ session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = 'page0'
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "name": "",
            "age": 0,
            "gender": "",
            "occupation": "",
            "id_card": "",
            "nationality": ""
        }

    if "retirement_inputs" not in st.session_state:
        st.session_state.retirement_inputs = {
            "payment_type":"โปรดระบุ",
            "retirement_age": 60,
            "lifespan": 85,
            "monthly_income": 0.0,
            "income_increase_rate": 0.0,
            "monthly_expenses": 0.0,
            "expense_increase_rate": 0.0,
            "inflation_rate": 3.0,
            "investment_return_rate": 5.0,
        }
    
    if "retirement_results" not in st.session_state or not isinstance(st.session_state.retirement_results, dict):
        st.session_state.retirement_results = {
            "expense_at_retirement": 0.0,
            "years_in_retirement": 0,
            "required_fund": 0.0,
            "total_prepared_assets": 0.0,
            "shortfall": 0.0,
            "Total_Monthly_Retirement_expenses":0.0,
            "RawSum_Monthly_Retirement_Expenses":0.0
        }
        
    if "existing_savings" not in st.session_state:
        st.session_state.existing_savings = 0.0
    if "mtl_connect_savings" not in st.session_state:
        st.session_state.mtl_connect_savings = 0.0
    if "other_insurance_savings" not in st.session_state:
        st.session_state.other_insurance_savings = 0.0

    load_page(st.session_state.current_page)
    
if __name__ == "__main__":
    main()
