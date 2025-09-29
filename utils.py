# utils.py
import streamlit as st

def display_profile_box():
    """
    แสดงข้อมูลโปรไฟล์ผู้ใช้ในรูปแบบกล่องสวยงาม
    """
    # ตรวจสอบว่ามีข้อมูลโปรไฟล์หรือไม่
    if "user_profile" in st.session_state and st.session_state.user_profile.get('name'):
        profile = st.session_state.user_profile

        name = profile.get('name', '')
        age = profile.get('age', '')
        gender = profile.get('gender', '')
        occupation = profile.get('occupation', '')

        # ตรวจสอบว่ามีข้อมูลเพียงพอที่จะแสดงหรือไม่
        if name and age and gender and occupation:
            st.markdown(f"""
                <style>
                    .profile-box {{
                        background-color: #F0F2F6;
                        border-left: 5px solid #E91E63;
                        padding: 15px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                        display: flex;
                        align-items: center;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    .profile-icon {{
                        font-size: 2.5em;
                        color: #E91E63;
                        margin-right: 15px;
                    }}
                    .profile-details {{
                        line-height: 1.4;
                    }}
                    .profile-name {{
                        font-weight: bold;
                        color: #E91E63;
                        font-size: 1.2em;
                    }}
                    .profile-info {{
                        font-size: 0.9em;
                        color: #555;
                    }}
                </style>
                <div class="profile-box">
                    <span class="profile-icon">👨</span>
                    <div class="profile-details">
                        <div class="profile-name">คุณ{name}</div>
                        <div class="profile-info">อายุ {age} ปี เพศ {gender} อาชีพ {occupation}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )