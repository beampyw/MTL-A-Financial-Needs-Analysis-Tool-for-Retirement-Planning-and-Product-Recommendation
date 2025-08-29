# pages/page1.py
import streamlit as st
from utils import display_profile_box

def app():
    st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #007bff; /* Blue for primary action */
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .stButton>button[data-testid="stFormSubmitButton"] {
            background-color: #E91E63; /* Pink for "Next" button */
        }
        .stButton>button[data-testid="stFormSubmitButton"]:hover {
            background-color: #C2185B;
        }
        .stNumberInput, .stTextInput {
            margin-bottom: 15px;
        }
        .stNumberInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .stNumberInput>label, .stTextInput>label, .stSelectbox>label {
            font-weight: bold;
            margin-bottom: 5px;
            display: block;
        }
        .stForm {
            border: none;
            padding: 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    display_profile_box()
    
    st.header("การวางแผนการเกษียณ")
    
    with st.form("retirement_planning_form"):
        user_profile = st.session_state.get("user_profile", {})
        retirement_inputs = st.session_state.get("retirement_inputs", {})
        current_age = user_profile.get("age", 0)
        initial_retirement_age = retirement_inputs.get("retirement_age", 60)
        
        age_options = sorted({55,60,65})
        if current_age == 55:
            age_options = sorted({60,65})
        elif current_age == 60:
            age_options = sorted({65})
        elif current_age == 65:
            age_options = {}

        age_options_str = [str(age) for age in age_options]
        age_options_str.insert(0, 'ปีถัดไป')    
        if current_age < 55:
            age_options = sorted({55,60,65})
            age_options_str.remove('ปีถัดไป')
        
        try:
            if isinstance(initial_retirement_age, int):
                default_index = age_options_str.index(str(initial_retirement_age))
            else:
                default_index = age_options_str.index(initial_retirement_age)
        except ValueError:
            default_index = 0

        # Retirement age input
        retirement_age_input = st.selectbox(
            "อายุที่ต้องการเกษียณ (ปี)",
            options=age_options_str,
            index=default_index,
            key="retirement_age_selectbox"
        )
        
        # Lifespan input
        lifespan = st.number_input(
            "อายุขัยที่คาดว่าจะเสียชีวิต (ปี)",
            min_value=int(retirement_age_input) if retirement_age_input != 'ปีถัดไป' else current_age + 1,
            max_value=120,
            value=int(retirement_inputs.get("lifespan", 85)),
            key="lifespan_input"
        )
        
        # Monthly income input
        monthly_income = st.number_input(
            "รายได้ต่อเดือนในปัจจุบัน (บาท)",
            min_value=0.0,
            value=float(retirement_inputs.get("monthly_income", 0.0)),
            key="monthly_income_input",
            step=1000.0,
            format="%.2f"
        )
        
        # Monthly income increase rate input
        income_increase_rate = st.number_input(
            "อัตราการเพิ่มขึ้นของรายได้ (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(retirement_inputs.get("income_increase_rate", 0.0)),
            step=0.1,
            format="%.2f"
        )
        
        # Monthly expenses input
        monthly_expenses = st.number_input(
            "ค่าใช้จ่ายต่อเดือนในปัจจุบัน (บาท)",
            min_value=0.0,
            value=float(retirement_inputs.get("monthly_expenses", 0.0)),
            key="monthly_expenses_input",
            step=1000.0,
            format="%.2f"
        )
        
        # Monthly expense increase rate input
        expense_increase_rate = st.number_input(
            "อัตราการเพิ่มขึ้นของค่าใช้จ่าย (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(retirement_inputs.get("expense_increase_rate", 0.0)),
            step=0.1,
            format="%.2f"
        )
        
        st.subheader("ข้อมูลสมมติฐานเพื่อใช้ในการคำนวณ")
        
        # Inflation rate input
        inflation_rate = st.number_input(
            "อัตราเงินเฟ้อ (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(retirement_inputs.get("inflation_rate", 3.0)),
            step=0.1,
            format="%.2f"
        )
        
        # Investment return rate input
        investment_return_rate = st.number_input(
            "ผลตอบแทนจากการลงทุนเฉลี่ย (%)",
            min_value=0.0,
            value=float(retirement_inputs.get("investment_return_rate", 5.0)),
            step=0.1,
            format="%.2f"
        )
            
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("ย้อนกลับ"):
                st.session_state.current_page = 'page0'
                st.rerun()
        with col2:
            if st.form_submit_button("ถัดไป"):
                if retirement_age_input == 'ปีถัดไป':
                    st.session_state.retirement_inputs.update({
                        "retirement_age": current_age + 1,
                        "lifespan": lifespan,
                        "monthly_income": monthly_income,
                        "income_increase_rate": income_increase_rate,
                        "monthly_expenses": monthly_expenses,
                        "expense_increase_rate": expense_increase_rate,
                        "inflation_rate": inflation_rate,
                        "investment_return_rate": investment_return_rate,
                    })
                    st.session_state.current_page = 'page2' 
                    st.rerun()
                elif lifespan < int(retirement_age_input):
                    st.warning("อายุที่คาดว่าจะเสียชีวิตต้องมากกว่าหรือเท่ากับอายุที่เริ่มเกษียณ")
                elif monthly_income is None or monthly_expenses is None:
                    st.warning("กรุณากรอกข้อมูลรายได้และรายจ่ายให้ครบถ้วนก่อนดำเนินการต่อ")
                else:
                    st.session_state.retirement_inputs.update({
                        "retirement_age": int(retirement_age_input),
                        "lifespan": lifespan,
                        "monthly_income": monthly_income,
                        "income_increase_rate": income_increase_rate,
                        "monthly_expenses": monthly_expenses,
                        "expense_increase_rate": expense_increase_rate,
                        "inflation_rate": inflation_rate,
                        "investment_return_rate": investment_return_rate,
                    })
                    st.session_state.current_page = 'page2' 
                    st.rerun()
