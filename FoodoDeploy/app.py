import streamlit as st
import pandas as pd
import base64
import os

# ✅ Set Page Configuration
st.set_page_config(page_title="Food Flow", layout="wide")

# ✅ Import Pages
from homepage import homepage
from order import order_page
from progress import progress_page
from review import review_page
from vendors import vendor_page
from about_us import about_us_page  # ✅ Import About Us Page

# ✅ Function to Convert Image to Base64
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return None  # Return None if image is missing
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ✅ Load Header Logo
logo_path = "images/headlogo.jpg"  # Make sure the path is correct
logo_base64 = get_base64_image(logo_path)

# ✅ Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("food_data.csv", encoding="utf-8")
    df.columns = df.columns.str.strip().str.lower()  # Standardize column names
    return df

df = load_data()  # Load dataset

# ✅ Enhanced Navigation Bar with Bigger Logo
st.markdown(f'''
    <style>
    /* ✅ Header Styling */
    .header {{
        background: #ffffff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        position: sticky;
        top: 0;
        z-index: 100;
        border-radius: 8px;
    }}
    
    /* ✅ Logo Styling - Increased Size */
    .header .logo img {{
        height: 55px;  /* Adjusted to match buttons */
        width: auto;
        object-fit: contain;
    }}

    /* ✅ Navigation Buttons */
    .header .menu {{
        display: flex;
        gap: 15px;
    }}

    .header .menu a {{
        background: #111;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 22px;
        border-radius: 6px;
        text-decoration: none;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}

    .header .menu a:hover {{
        background: #333;
        transform: scale(1.05);
    }}

    /* ✅ Footer Styling */
    .footer {{
        text-align: center;
        padding: 15px;
        background: #333;
        color: yellow;
        width: 100%;
        font-size: 14px;
        margin-top: 50px;
        border-radius: 8px;
    }}

    .footer a {{
        color: #ffffff;
        text-decoration: none;
        font-weight: bold;
        padding: 0 10px;
    }}

    .footer a:hover {{
        text-decoration: underline;
    }}
    </style>

    <div class="header">
        <div class="logo">
            <img src="data:image/jpeg;base64,{logo_base64}" alt="Food Flow Logo">
        </div>
        <div class="menu">
            <a href="/?page=Homepage">🏠 Home</a>
            <a href="/?page=Order">🛒 Order</a>
            <a href="/?page=Progress">📦 Progress</a>
            <a href="/?page=Review">⭐ Review</a>
            <a href="/?page=Vendor">🏪 Vendor</a>
            <a href="/?page=AboutUs">ℹ️ About Us</a>  <!-- ✅ Added About Us -->
        </div>
    </div>
''', unsafe_allow_html=True)

# ✅ Initialize session state for cart and order tracking
if "cart" not in st.session_state:
    st.session_state.cart = []
if "order_status" not in st.session_state:
    st.session_state.order_status = 0  # Reset order tracking

# ✅ Navigation Logic with Query Parameters
query_params = st.query_params
page = query_params.get("page", "Homepage")  # Ensure correct data type handling

# ✅ Page Rendering Based on URL Query Parameters
if page == "Homepage":
    homepage(df)
elif page == "Order":
    order_page()
elif page == "Progress":
    progress_page()
elif page == "Review":
    review_page()
elif page == "Vendor":
    vendor_page()
elif page == "AboutUs":  # ✅ Load About Us Page
    about_us_page()

# ✅ Footer with "About Us" Link
st.markdown('''
    <div class="footer">
        <p><strong>&copy; 2025 Food Flow.</strong> All Rights Reserved | 
        <a href="/?page=AboutUs">About Us</a> | 
        <a href="#">Privacy Policy</a> | 
        <a href="#">Terms & Conditions</a></p>
    </div>
''', unsafe_allow_html=True)
