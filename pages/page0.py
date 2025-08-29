# pages/page0.py

import streamlit as st

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
            background-color: #E91E63; /* Pink for "Next" button */
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #C2185B;
        }
        .stTextInput, .stNumberInput, .stSelectbox {
            margin-bottom: 15px;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .stTextInput>label, .stNumberInput>label, .stSelectbox>label {
            font-weight: bold;
            margin-bottom: 5px;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("ข้อมูลส่วนตัว")

    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            gender_options = ["ชาย", "หญิง", "ไม่ระบุ"]
            current_gender = st.session_state.user_profile.get("gender", "ไม่ระบุ")
            gender_index = gender_options.index(current_gender) if current_gender in gender_options else 2
            gender = st.selectbox(
                "เพศ*",
                gender_options,
                key="gender_input",
                index=gender_index
            )
            name = st.text_input(
                "ชื่อ-นามสกุล*",
                key="name_input",
                placeholder="กรุณากรอกชื่อ-นามสกุล",
                value=st.session_state.user_profile.get("name", "")
            )
            occupation = st.text_input(
                "อาชีพ*",
                key="occupation_input",
                placeholder="กรุณากรอกอาชีพ",
                value=st.session_state.user_profile.get("occupation", "")
            )
            

        with col2:
            age = st.number_input(
                "อายุ*",
                min_value=0,
                max_value=120,
                key="age_input",
                value=int(st.session_state.user_profile.get("age", 25))
            )

            nationality = st.text_input(
                "สัญชาติ*",
                key="nationality_input",
                placeholder="กรุณากรอกสัญชาติ",
                value=st.session_state.user_profile.get("nationality", "")
            )
            
            id_card = st.text_input(
                "เลขบัตรประชาชน",
                key="id_card_input",
                placeholder="กรุณากรอกหมายเลขบัตรประชาชน",
                value=st.session_state.user_profile.get("id_card", "")
            )

        if st.form_submit_button("ถัดไป"):
            if not all([gender,nationality,age,occupation,name]):
                st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
            elif age > 70:
                st.warning("ไม่มีแบบประกันที่รองรับตั้งแต่อายุ 71 ปีขึ้นไป")
            else:
                st.session_state.user_profile = {
                    "id_card": id_card,
                    "nationality": nationality,
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "occupation": occupation,
                }
                
                initial_retirement_age = st.session_state.retirement_inputs.get("retirement_age", 60)
                if initial_retirement_age < age:
                    initial_retirement_age = age
                    
                st.session_state.retirement_inputs.update({
                    "retirement_age": initial_retirement_age,
                    "lifespan": st.session_state.retirement_inputs.get("lifespan", 85),
                    "monthly_income": st.session_state.retirement_inputs.get("monthly_income", 0.0),
                    "monthly_expenses": st.session_state.retirement_inputs.get("monthly_expenses", 0.0),
                })
                
                st.session_state.current_page = 'page1'
                st.rerun()