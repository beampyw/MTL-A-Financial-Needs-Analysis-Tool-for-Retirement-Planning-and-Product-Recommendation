# pages/page2.py
import streamlit as st
import numpy as np
from utils import display_profile_box

def app():
    st.markdown("""
    <style>
    /* Style สำหรับปุ่มทั่วไปที่ไม่มี key */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #007bff; /* สีน้ำเงินสำหรับปุ่มทั่วไป */
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
                /* Style สำหรับปุ่มที่มี key "update_button" (สีน้ำเงิน) */
        button[data-testid="stButton-update_button"] {
            background-color: #007bff;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            width: 100%; /* <-- เพิ่มบรรทัดนี้ */
        }

        /* Style สำหรับปุ่มที่มี key "setdf_button" (สีชมพู) */
        button[data-testid="stButton-setdf_button"] {
            background-color: #E91E63;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            width: 100%; /* <-- เพิ่มบรรทัดนี้ */
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
        .stMetric {
            background-color: #f0f2f5;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .stMetric > label {
            font-weight: bold;
        }
        .stAlert {
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    display_profile_box()

    st.header("ค่าใช้จ่ายที่ต้องการจะเตรียมต่อเดือนหลังเกษียณ")
    st.markdown("""
    <div style="background-color: #e6f7ff; padding: 10px; border-left: 5px solid #0099ff; border-radius: 5px;">
        หากต้องการวางแผนรายจ่ายต่าง ๆ ด้วยตัวเอง สามารถกรอกข้อมูลลงในช่องด้านล่างได้เลย <b>(ไม่บังคับ)</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color: #fff3e6; padding: 10px; border-left: 5px solid #ff9900; border-radius: 5px;">
        แต่ถ้าไม่ต้องการวางแผน สามารถใช้กดที่<b style="color: #ff9900;">ปุ่มใช้โปรแกรมคำนวณ</b>จากแบบสอบถามก่อนหน้าได้เลย
    </div>
    """, unsafe_allow_html=True)

    inputs = st.session_state.retirement_inputs
    current_age = st.session_state.user_profile.get("age", 0)
    retirement_age = inputs.get("retirement_age", 60)
    lifespan = inputs.get("lifespan", 85)
    monthly_expenses_current = inputs.get("monthly_expenses", 0.0)
    expense_increase_rate = inputs.get("expense_increase_rate", 0.0) / 100
    inflation_rate = inputs.get("inflation_rate", 3.0) / 100
    investment_return_rate = inputs.get("investment_return_rate", 5.0) / 100

    # คำนวณจำนวนปีอีกกี่ปีที่จะเกษียณและเกษียนกี่ปี
    years_to_retirement = retirement_age - current_age
    years_in_retirement = lifespan - retirement_age

    Daily_Expenses = st.session_state.get('daily_expenses_input', 0.0)
    Housing = st.session_state.get('housing_input', 0.0)
    Healthcare = st.session_state.get('healthcare_input', 0.0)
    Family_Social = st.session_state.get('Family_Social_input', 0.0)
    Lifestyle = st.session_state.get('Lfiestyle_input', 0.0)
    Special_Expenses = st.session_state.get('Special_Expenses_input', 0.0)
    Estate_Planning = st.session_state.get('Estate_Planning_input', 0.0)

    # คำนวณค่าใช้จ่ายเริ่มต้นเมื่อเกษียณ
    default_expense_at_retirement = monthly_expenses_current * ((1 + expense_increase_rate) ** years_to_retirement) if years_to_retirement > 0 else monthly_expenses_current
    col1, col2 = st.columns(2)
    with col1:
        # ค่าใช้จ่ายประจำวัน (Daily Expenses)
        Daily_Expenses = st.number_input(
            "ค่าใช้จ่ายประจำวันที่คาดหวัง",
            min_value=0.0,
            value=float(st.session_state.get("Daily_Expenses", 0.0)),
            key="Daily_Expenses_input",
            step=1.0,
            format="%.2f"
        )
        # ค่าที่อยู่อาศัย (Housing)
        Housing= st.number_input(
            "ค่าที่อยู่อาศัยที่คาดหวัง",
            min_value=0.0,
            value=float(st.session_state.get("Housing", 0.0)),
            key="Housing_input",
            step=1000.0,
            format="%.2f"
        )
        # ค่ารักษาพยาบาลและสุขภาพ (Healthcare)
        Healthcare= st.number_input(
            "ค่ารักษาพยาบาลและสุขภาพที่คาดหวัง",
            min_value=0.0,
            value=float(st.session_state.get("Healthcare", 0.0)),
            key="Healthcare_input",
            step=1000.0,
            format="%.2f"
        )
        # ค่าใช้จ่ายครอบครัวและสังคม (Family & Social)
        Family_Social= st.number_input(
            "ค่าใช้จ่ายครอบครัวและสังคมที่คาดหวัง",
            min_value=0.0,
            value=float(st.session_state.get("Family_Social", 0.0)),
            key="Family_Social_input",
            step=1000.0,
            format="%.2f"
        )
    with col2:
        # ค่าใช้จ่ายด้านไลฟ์สไตล์ (Lifestyle)
        Lifestyle= st.number_input(
            "ค่าใช้จ่ายด้านไลฟ์สไตล์ที่คาดหวัง",
            min_value=0.0,
            value=float(st.session_state.get("Lifestyle", 0.0)),
            key="Lifestyle_input",
            step=1000.0,
            format="%.2f"
        )
        # ค่าใช้จ่ายเฉพาะกิจ (Special/One-time Expenses)
        Special_Expenses= st.number_input(
            "ค่าใช้จ่ายเฉพาะกิจที่คาดหวัง",
            min_value=0.0,
            value=float(st.session_state.get("Special_Expenses", 0.0)),
            key="Special_Expenses_input",
            step=1000.0,
            format="%.2f"
        )
        # แผนการส่งต่อทรัพย์สิน (Estate Planning)
        Estate_Planning= st.number_input(
            "แผนการส่งต่อทรัพย์สินที่คาดหวัง",
            min_value=0.0,
            value=float(st.session_state.get("Estate_Planning", 0.0)),
            key="Estate_Planning_input",
            step=1000.0,
            format="%.2f"
        )
        RawSum_Monthly_Retirement_Expenses = Daily_Expenses+Housing+Healthcare+Family_Social+Lifestyle+Special_Expenses+Estate_Planning
        st.markdown(f"""
    <div style="
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
    ">
        <div style="
            font-size: 14px;
            color: #555;
            font-weight: bold;
        ">
            จำนวนเงินรวมที่ต้องการจะเตรียม
        </div>
        <div style="
            font-size: 24px;
            font-weight: bold;
            color: #E91E63;
        ">
            {RawSum_Monthly_Retirement_Expenses:,.0f} บาท
        </div>
    </div>
""", unsafe_allow_html=True)

    # ตรวจสอบว่าตัวแปรที่ต้องการคำนวณมีค่าเริ่มต้นหรือไม่
    if 'Total_Monthly_retirement_expenses' not in st.session_state:
        # กำหนดค่าเริ่มต้นถ้ายังไม่มี
        st.session_state['Total_Monthly_retirement_expenses'] = 0.0
    
    Total_Monthly_retirement_expenses = (Daily_Expenses+Housing+Healthcare+Family_Social+Lifestyle+Special_Expenses+Estate_Planning)* ((1 + expense_increase_rate) ** years_to_retirement) if years_to_retirement > 0 else monthly_expenses_current
    
    if 'monthly_retirement_expenses' not in st.session_state:
        st.session_state['monthly_retirement_expenses'] = 0.0
    
    col3,col4 = st.columns(2)
    with col3:
        if st.button("มูลค่าในอนาคตของค่าใช้จ่าย", key="update_button"):
            # เมื่อกดปุ่มนี้ ให้บันทึกค่าที่คำนวณไว้แล้วลงใน session_state
            st.session_state['monthly_retirement_expenses'] = Total_Monthly_retirement_expenses
            st.success("บันทึกค่าใช้จ่ายตามมูลค่าในอนาคตแล้ว!") # เพิ่มข้อความแจ้งเตือน
            st.rerun() # สั่งให้ reruns เพื่ออัปเดตค่าที่แสดงผล

    with col4:
        if st.button("ใช้โปรแกรมคำนวณจากแบบสอบถามก่อนหน้า", key="setdf_button"):
            # เมื่อกดปุ่มนี้ ให้บันทึกค่า Default ลงใน session_state
            st.session_state['monthly_retirement_expenses'] = default_expense_at_retirement
            st.success("บันทึกค่าใช้จ่ายตามแบบสอบถามแล้ว!") # เพิ่มข้อความแจ้งเตือน
            st.rerun() # สั่งให้ reruns เพื่ออัปเดตค่าที่แสดงผล

    # ช่องให้ User กรอกจำนวนเงินที่ต้องการหลังเกษียณ
    monthly_retirement_expenses = st.number_input(
        "รายจ่ายต่อเดือนที่คาดหวังหลังเกษียณ (บาท)*",
        min_value=0.0,
        value=float(st.session_state.get("monthly_retirement_expenses", 0.0)),
        help="โดยทั่วไปค่าใช้จ่ายหลังเกษียณจะอยู่ที่ประมาณ 70-80% ของค่าใช้จ่ายปัจจุบัน",
        step=1.0,
        format="%.2f",
        key="mon_re_ex"
    )

    
    # บันทึกข้อมูลลง session_state
    st.session_state.Daily_Expenses = Daily_Expenses
    st.session_state.Housing = Housing
    st.session_state.Healthcare = Healthcare
    st.session_state.Family_Social = Family_Social
    st.session_state.Lifestyle = Lifestyle
    st.session_state.Special_Expenses = Special_Expenses
    st.session_state.Estate_Planning = Estate_Planning
    st.session_state.Total_Monthly_retirement_expenses = Total_Monthly_retirement_expenses
    st.session_state.monthly_retirement_expenses = monthly_retirement_expenses


    # Calculate the real rate of return
    if 1 + inflation_rate != 0: # ไม่ให้หารด้วย 0
        real_return_rate = ((1 + investment_return_rate) / (1 + inflation_rate)) - 1
    else:
        real_return_rate = investment_return_rate

    # คำนวณเงินทุนทั้งหมดที่จำเป็นโดยใช้สูตรมูลค่าปัจจุบันของเงินบำนาญ
    if real_return_rate != 0: # ไม่ให้หารด้วย 0
        required_fund = (monthly_retirement_expenses * 12) * (1 - (1 + real_return_rate)**-years_in_retirement) / real_return_rate
    else:
        required_fund = (monthly_retirement_expenses * 12) * years_in_retirement
    
    # เช็คและทำให้  required_fund ไม่เป็นค่าลบ
    required_fund = max(0, required_fund)
    
    # บันทึกข้อมูลลง session_state เพื่อนำไปใช้ใน page3
    st.session_state.retirement_results["expense_at_retirement"] = monthly_retirement_expenses
    st.session_state.retirement_results["years_in_retirement"] = years_in_retirement
    st.session_state.retirement_results["required_fund"] = required_fund

    # --- UI elements ---
    st.metric("จำนวนเงินที่ต้องเตรียม", f"{required_fund:,.2f} บาท")
    
    st.subheader("ข้อมูลเงินเก็บ")
    
    # Input เงินเก็บที่มีอยู่แล้ว
    existing_savings = st.number_input(
        "เงินเก็บที่มีอยู่แล้ว (บาท)",
        min_value=0.0,
        value=float(st.session_state.get("existing_savings", 0.0)),
        key="existing_savings_input",
        step=1.0
    )

    # Input MTL Connect
    mtl_connect_savings = st.number_input(
        "ข้อมูลจาก MTL Connect (บาท)",
        min_value=0.0,
        value=float(st.session_state.get("mtl_connect_savings", 0.0)),
        key="mtl_connect_savings_input",
        step=1.0
    )

    # Input ข้อมูลประกันที่ทำกับบริษัทอื่น
    other_insurance_savings = st.number_input(
        "ข้อมูลประกันที่ทำกับบริษัทอื่น (บาท)",
        min_value=0.0,
        value=float(st.session_state.get("other_insurance_savings", 0.0)),
        key="other_insurance_savings_input", 
        step=1.0
    )
    
    # คำนวณสินทรัพย์ทั้งหมดที่เตรียมไว้
    total_prepared_assets = existing_savings + mtl_connect_savings + other_insurance_savings
    
    # แสดงยอดสินทรัพย์ที่เตรียมไว้ทั้งหมด
    st.metric("ส่วนที่เตรียมไว้ทั้งหมด", f"{total_prepared_assets:,.2f} บาท")
    with st.form("navigation_form"):
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("ย้อนกลับ"):
                st.session_state.current_page = 'page1'
                st.rerun()
        with col2:
            if st.form_submit_button("ถัดไป"):
                if not monthly_retirement_expenses:
                    st.warning("โปรดระบุรายจ่ายต่อเดือนที่คาดหวังหลังเกษียณ (บาท)")
                # Save the final values before moving to the next page
                else:
                    st.session_state.existing_savings = existing_savings
                    st.session_state.mtl_connect_savings = mtl_connect_savings
                    st.session_state.other_insurance_savings = other_insurance_savings
                    st.session_state.total_prepared_assets = total_prepared_assets
                    st.session_state.retirement_results["total_prepared_assets"] = total_prepared_assets
                    st.session_state.current_page = 'page3'
                    st.rerun()
    

            