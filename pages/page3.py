# pages/page3.py
import streamlit as st
import pandas as pd
import numpy as np
from utils import display_profile_box
import re

# --- ข้อมูลเบี้ยประกันจำลองสำหรับผลิตภัณฑ์ (Fallback Data) ---
product_details_data = {
    "เมืองไทย เฟล็กซี่ รีไทร์ 90/1 D55": {
        "payment_period": "ชำระเบี้ยประกันครั้งเดียว",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 90 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": 55,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 50, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 55 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 582%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029972.pdf"
    },
    "เมืองไทย เฟล็กซี่ รีไทร์ 90/1 D60": {
        "payment_period": "ชำระเบี้ยประกันครั้งเดียว",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 90 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": 60,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 55, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 60 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 522%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029972.pdf"
    },
    "เมืองไทย เฟล็กซี่ รีไทร์ 90/1 D65": {
        "payment_period": "ชำระเบี้ยประกันครั้งเดียว",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 90 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": 65,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 60, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 65 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 462%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029972.pdf"
    },
    
    "เมืองไทย เฟล็กซี่ รีไทร์ 90/5 D55": {
        "payment_period": "ชำระเบี้ย 5 ปี",
        "coverage_duration": "คุ้มครองถึงอายุ 90 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": 55,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 50, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 55 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 582%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029d50.pdf"
    },
    "เมืองไทย เฟล็กซี่ รีไทร์ 90/5 D60": {
        "payment_period": "ชำระเบี้ย 5 ปี",
        "coverage_duration": "คุ้มครองถึงอายุ 90 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": 60,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 55, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 60 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 522%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029d50.pdf"
    },
    "เมืองไทย เฟล็กซี่ รีไทร์ 90/5 D65": {
        "payment_period": "ชำระเบี้ย 5 ปี",
        "coverage_duration": "คุ้มครองถึงอายุ 90 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": 65,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 55, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 65 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 462%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029d50.pdf"
    },
    
    "เมืองไทย 8501 (บํานาญแบบลดหย่อนได้)": {
        "payment_period": "ชำระเบี้ยประกันครั้งเดียว",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 85 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": None,
        "min_age": 55, # เพิ่มอายุที่รับประกันภัย
        "max_age": 70, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>12% ของจํานวนเงินเอาประกันภัย ณ วันเริ่มสัญญา</li>
                </ul>
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/01b8de.pdf",
    },
    "เมืองไทย 9901 D65 (บำนาญแบบลดหย่อนได้)": {
        "payment_period": "ชำระเบี้ยประกันครั้งเดียว",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 99 ปี",
        "design_payment_type":"จ่ายสั้น",
        "design_retirement_age": 65,
        "min_age": 0, # เพิ่มอายุที่รับประกันภัย
        "max_age": 60, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>12% ของจํานวนเงินเอาประกันภัย ณ วันเริ่มสัญญา</li>
                </ul>
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/020f1d.pdf"
    },
    "เฟล็กซี่ รีไทร์ 9055 (บํานาญแบบลดหย่อนได้)": {
        "payment_period": "ระยะเวลาชําระเบี้ยประกันภัย ครบอายุ 55 ปี",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 90 ปี",
        "design_payment_type":"จ่ายยาว",
        "design_retirement_age": 55,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 50, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 55 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 582%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029cff.pdf",

    },
    "เฟล็กซี่ รีไทร์ 9060 (บํานาญแบบลดหย่อนได้)": {
        "payment_period": "ระยะเวลาชําระเบี้ยประกันภัย ครบอายุ 60 ปี",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 90 ปี",
        "design_payment_type":"จ่ายยาว",
        "design_retirement_age": 60,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 55, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 60 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 522%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029cff.pdf"
    },
    "เฟล็กซี่ รีไทร์ 9065 (บํานาญแบบลดหย่อนได้)": {
        "payment_period": "ระยะเวลาชําระเบี้ยประกันภัย ครบอายุ 65 ปี",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 90 ปี",
        "design_payment_type":"จ่ายยาว",
        "design_retirement_age": 65,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 60, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>อายุ 65 – 70 ปี : 12%</li>
                    <li>อายุ 71 – 75 ปี : 15%</li>
                    <li>อายุ 76 – 80 ปี : 18%</li>
                    <li>อายุ 81 – 85 ปี : 21%</li>
                    <li>อายุ 86 – 90 ปี : 24%</li>
                </ul>
                ผลประโยชน์รวมสูงสุด เมื่ออยู่ครบสัญญา 462%
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/029cff.pdf"
    },
    "เมืองไทย 8555 จี20 (บํานาญแบบลดหย่อนได้)": {
        "payment_period": "ระยะเวลาชําระเบี้ยประกันภัย ครบอายุ 55 ปี",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 85 ปี",
        "design_payment_type":"จ่ายยาว",
        "design_retirement_age": 55,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 50, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>24% ของจํานวนเงินเอาประกันภัย ณ วันเริ่มสัญญา</li><br>
                    <li>การันตีเงินบำนาญ 20 ปี</li>
                </ul>
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/0294b9.pdf"
    },
    "เมืองไทย 8560 จี15 (บํานาญแบบลดหย่อนได้)": {
        "payment_period": "ระยะเวลาชําระเบี้ยประกันภัย ครบอายุ 60 ปี",
        "coverage_duration": "ระยะเวลาความคุ้มครอง ครบอายุ 85 ปี",
        "design_payment_type":"จ่ายยาว",
        "design_retirement_age": 60,
        "min_age": 20, # เพิ่มอายุที่รับประกันภัย
        "max_age": 55, # เพิ่มอายุที่รับประกันภัย
        "pension_benefits_html": """
            <div class="pension-benefits-box">
                <b>ผลประโยชน์เงินบำนาญ (ต่อปี)</b><br>
                <ul>
                    <li>12% ของจํานวนเงินเอาประกันภัย ณ วันเริ่มสัญญา</li><br>
                    <li>การันตีเงินบำนาญ 15 ปี</li>
                </ul>
            </div>
        """,
        "pdf_url": "https://smartweb.muangthai.co.th/stocks/media/0297c5.pdf"
    },
}

def parse_pension_benefits(html_string):
    pension_rates = {}
    matches = re.findall(r'<li>อายุ (\d+) – (\d+) ปี : (\d+)%</li>', html_string)
    for start, end, rate in matches:
        pension_rates[(int(start), int(end))] = float(rate) / 100
    
    # Check for the special case "12% ของจํานวนเงินเอาประกันภัย ณ วันเริ่มสัญญา"
    if not pension_rates:
        matches = re.search(r'(\d+)% ของจํานวนเงินเอาประกันภัย ณ วันเริ่มสัญญา', html_string)
        if matches:
            rate = float(matches.group(1)) / 100
            pension_rates[('all', 'all')] = rate
            
    return pension_rates

def calculate_pv_pension_benefits_per_unit(retirement_age, lifespan, investment_return_rate, inflation_rate, pension_rates):
    """
    คำนวณมูลค่าปัจจุบันของผลประโยชน์บำนาญต่อหน่วยประกันชีวิต โดยใช้อัตราเงินบำนาญเฉพาะสำหรับผลิตภัณฑ์ที่กำหนด
    """
    pv_benefits_per_unit = 0
    if (1 + inflation_rate) == 0:
        real_return_rate = -1 # เป็น -1 เพื่อไม่ให้หารด้วยศูนย์
    else:
        real_return_rate = (1 + investment_return_rate) / (1 + inflation_rate) - 1

    for age in range(int(retirement_age), int(lifespan) + 1):
        annual_payout_rate = 0
        for (start_age, end_age), rate in pension_rates.items():
            if start_age == 'all':
                annual_payout_rate = rate
                break
            elif start_age <= age <= end_age:
                annual_payout_rate = rate
                break
        
        if annual_payout_rate > 0:
            benefit_per_unit = annual_payout_rate
            years_from_retirement = age - retirement_age
            
            if real_return_rate <= 0 and years_from_retirement > 0:
                return 0
            elif years_from_retirement < 0:
                continue
            elif years_from_retirement == 0:
                pv_benefits_per_unit += benefit_per_unit
            else:
                pv_benefits_per_unit += benefit_per_unit / ((1 + real_return_rate) ** years_from_retirement)
    return pv_benefits_per_unit


def calculate_recommended_products(retirement_results, user_profile):
    """
    คำนวณและกรองรายการผลิตภัณฑ์ประกันภัยที่แนะนำโดยอิงตามข้อมูลผู้ใช้และเป้าหมายการเกษียณอายุ
    """
    if retirement_results is None: retirement_results = {}
    if user_profile is None: user_profile = {}

    required_fund = retirement_results.get('required_fund', 0)
    total_prepared_assets = retirement_results.get('total_prepared_assets', 0)
    
    payment_type = st.session_state.retirement_inputs.get("payment_type",0)
    retirement_age = st.session_state.retirement_inputs.get("retirement_age", 0)
    lifespan = st.session_state.retirement_inputs.get("lifespan", 0)
    investment_return_rate = st.session_state.retirement_inputs.get("investment_return_rate", 0) / 100
    inflation_rate = st.session_state.retirement_inputs.get("inflation_rate", 0) / 100

    MIN_LIFE_INSURANCE_AMOUNT = 50_000

    retirement_gap = max(0, required_fund - total_prepared_assets)
    
    recommended_products = []
    
    unique_products = product_details_data.keys()
    
    if retirement_gap > 0 and len(unique_products) > 0:
        for product_name in unique_products:
            product_data = product_details_data.get(product_name, {})
            if not product_data:
                continue
                
            design_retirement_age = product_data.get('design_retirement_age')
            design_payment_type = product_data.get('design_payment_type')
            product_min_age = product_data.get('min_age') # ดึงอายุขั้นต่ำที่รับประกันภัย
            product_max_age = product_data.get('max_age') # ดึงอายุสูงสุดที่รับประกันภัย
            
            is_match = False
            user_age = user_profile.get("age", 0)
            
            # เพิ่มเงื่อนไขตรวจสอบอายุผู้ใช้
            age_is_within_range = (user_age >= product_min_age and user_age <= product_max_age)
            
            if design_retirement_age is not None:
                # ตรวจสอบทั้งอายุเกษียณที่เลือกและอายุผู้ใช้ต้องอยู่ในช่วงที่รับประกันภัย
                is_match = (design_retirement_age == retirement_age) and (age_is_within_range) and (design_payment_type == payment_type)
            elif product_name == "เมืองไทย 8501 (บํานาญแบบลดหย่อนได้)":
                # สำหรับแบบพิเศษนี้ ให้ตรวจสอบเฉพาะอายุผู้ใช้เท่านั้น
                is_match = age_is_within_range
            
            if not is_match:
                continue
                
            pension_rates_data = parse_pension_benefits(product_data.get('pension_benefits_html', ''))

            pv_factor_per_unit = calculate_pv_pension_benefits_per_unit(
                retirement_age, lifespan, investment_return_rate, inflation_rate, pension_rates_data
            )
            
            life_insurance_amount = MIN_LIFE_INSURANCE_AMOUNT
            if pv_factor_per_unit > 0:
                calculated_sum_assured = retirement_gap / pv_factor_per_unit
                life_insurance_amount = max(MIN_LIFE_INSURANCE_AMOUNT, min(calculated_sum_assured, 10_000_000))
            else:
                life_insurance_amount = max(MIN_LIFE_INSURANCE_AMOUNT, min(retirement_gap * 1.2, 10_000_000))

            life_insurance_amount = int(round(life_insurance_amount / 100000) * 100000)

            annual_premium = "ข้อมูลไม่พร้อมใช้งาน"
            total_premium = "ข้อมูลไม่พร้อมใช้งาน"

            recommended_products.append({
                "name": product_name,
                "payment_period": product_data.get('payment_period', ''),
                "coverage_duration": product_data.get('coverage_duration', ''),
                "life_insurance_amount": life_insurance_amount,
                "annual_premium": annual_premium,
                "total_premium": total_premium,
                "pension_benefits_html": product_data.get('pension_benefits_html', '')
            })

    return {
        "recommended_products": recommended_products,
        "required_fund": required_fund,
        "total_prepared_assets": total_prepared_assets,
        "shortfall": retirement_gap,
    }


def app():
    # CSS styling for a more polished look
    st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #007bff;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .stButton>button[data-testid="stFormSubmitButton"] {
            background-color: #E91E63;
        }
        .stButton>button[data-testid="stFormSubmitButton"]:hover {
            background-color: #C2185B;
        }
        .product-card {
            background-color: #F0F2F6;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
        }
        .product-name {
            font-weight: bold;
            color: #E91E63;
            font-size: 1.1em;
            margin-bottom: 5px;
        }
        .product-info {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 3px;
        }
        .pension-benefits-box {
            background-color: #e6e6e6;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 0.85em;
        }
        .bookmark-icon {
            color: #E91E63;
            font-size: 24px;
            margin-left: 10px;
        }
        div[data-testid="stVerticalBlock"] > div:first-child {
            padding-top: 0;
        }
        .stAlert {
            font-weight: bold;
            
        }
    </style>
    """, unsafe_allow_html=True)
    
    display_profile_box()

    st.header("แบบประกันแนะนำ")

    retirement_results_dict = st.session_state.get("retirement_results", {})
    user_profile_dict = st.session_state.get("user_profile", {})

    if not retirement_results_dict or not user_profile_dict:
        st.warning("ไม่พบข้อมูลการคำนวณ โปรดกลับไปที่หน้าแรกเพื่อเริ่มใหม่")
        return
    
    calculated_values = calculate_recommended_products(retirement_results_dict, user_profile_dict)
    
    recommended_products = calculated_values.get('recommended_products', [])
    required_fund = calculated_values.get('required_fund', 0)
    total_prepared_assets = calculated_values.get('total_prepared_assets', 0)
    shortfall = calculated_values.get('shortfall', 0)

    if shortfall > 0:
       st.markdown(f"""
        <div style='
            background-color: #E91E63; 
            color: white; 
            padding: 20px; 
            border-radius: 15px; 
            text-align: center; 
            font-weight: bold;
            font-size: 32px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        '>
            ขาดเงินอีก🚨 {shortfall:,.0f} บาท เพื่อให้บรรลุเป้าหมายเกษียณ
        </div>
    """, unsafe_allow_html=True)
       
    else:
        st.success(f"**คุณมีเงินเตรียมไว้เกินพอ!** จำนวน {abs(shortfall):,.2f} บาท")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="จำนวนเงินที่ต้องเตรียม", value=f"{required_fund:,.2f} บาท")
    with col2:
        st.metric(label="ส่วนที่เตรียมไว้", value=f"{total_prepared_assets:,.2f} บาท")

    st.markdown("---")
    
    if not recommended_products:
        user_retirement_choice = st.session_state.retirement_inputs.get("retirement_age")
        st.warning(f"ขออภัยค่ะ ไม่พบแบบประกันที่เหมาะสมสำหรับผู้ที่ต้องการเกษียณอายุที่ {user_retirement_choice} ปี หรือไม่ตรงกับเงื่อนไขอายุของผู้ใช้")
    else:
        for product in recommended_products:
            with st.container():
                cleaned_benefits_text = re.sub(r'<\/?b>', '', product['pension_benefits_html'])
                cleaned_benefits_text = re.sub(r'<\/?ul>', '', cleaned_benefits_text)
                cleaned_benefits_text = re.sub(r'<\/?li>', '', cleaned_benefits_text)
                cleaned_benefits_text = re.sub(r'<div[^>]*>', '', cleaned_benefits_text)
                cleaned_benefits_text = cleaned_benefits_text.replace('</div>', '')
                
                cleaned_benefits_text = cleaned_benefits_text.replace('<br>', '\n').strip()
                cleaned_benefits_text = '\n'.join([f"- {line.strip()}" if line.strip().startswith('อายุ') else line.strip() for line in cleaned_benefits_text.split('\n')])

                product_name = product['name']
                product_data = product_details_data.get(product_name, {}) # ดึงข้อมูลผลิตภัณฑ์
    
                # ตรวจสอบว่ามี URL ของไฟล์ PDF หรือไม่
                pdf_url = product_data.get('pdf_url')

                st.markdown(f"""
                    <div class="product-card">
                        <div class="product-details">
                            <div class="product-name">{product['name']}</div>
                            <div class="product-info">{product['payment_period']}</div>
                            <div class="product-info">{product['coverage_duration']}</div>
                            <div class="product-info">แนะนำทุนประกันชีวิต {product['life_insurance_amount']:,.0f} บาท</div>
                            <div class="pension-benefits-box">
                                <div class="product-info">
                {cleaned_benefits_text}
                        </div>
                    </div>
                </div>
                <div class="bookmark-icon">🔖</div>
                </div>
                """, unsafe_allow_html=True)
                # เพิ่มโค้ดสร้างปุ่มดาวน์โหลด ถ้ามี URL
                if pdf_url:
                    st.markdown(f"""
                            <a href="{pdf_url}" target="_blank" style="text-decoration: none;">
                                <button style="
                                    background-color: #E91E63;
                                    color: white;
                                    border: none;
                                    padding: 10px 20px;
                                    border-radius: 10px;
                                    font-size: 16px;
                                    cursor: pointer;
                                    width: 100%;
                                ">
                                    ดาวน์โหลดรายละเอียดแผนประกัน
                                </button>
                            </a>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True) # ปิด div ของ product-card


    with st.form("navigation_form"):
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("ย้อนกลับ", type="secondary"):
                st.session_state.current_page = 'page2'
                st.rerun()
        with col2:
            if st.form_submit_button("เริ่มต้นใหม่", type="primary"):
                st.session_state.clear()
                st.session_state.current_page = 'page0'
                st.rerun()