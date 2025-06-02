import streamlit as st
import os
import base64

# ✅ Function to Convert Image to Base64
def get_base64_image(image_path):
    """Encodes an image in Base64 format for embedding in HTML."""
    if not os.path.exists(image_path):
        return None  # Return None if image not found

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ✅ Function to Display Header with Logo
def header_with_logo():
    """Displays the order page logo in the header."""
    logo_path = os.path.join("images", "orderlogo.jpeg")  # Ensure correct path
    logo_base64 = get_base64_image(logo_path)

    if logo_base64:
        st.markdown(f"""
            <style>
                .order-header {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    background-color: rgb(5, 1, 1);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 5px rgba(252, 252, 252, 0.86);
                }}
                .order-header img {{
                    height: 60px;
                    width: auto;
                    border-radius: 5px;
                }}
                .order-header h1 {{
                    color: white;
                    font-size: 26px;
                    font-weight: bold;
                    margin: 0;
                }}
            </style>
            <div class="order-header">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="Order Logo">
                <h1>Your Cart</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.title("🛒 Your Cart")  # Fallback if logo is missing

# ✅ Function to Set a Background Image
def set_background(image_file):
    """Sets a background image in Streamlit using custom CSS."""
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    page_bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg_css, unsafe_allow_html=True)

# ✅ Function to Apply Discount
def apply_discount(total, discount_option):
    """Applies discount based on dropdown selection."""
    discounts = {
        "No Discount": 0,
        "HALAL10 (10% off)": 10,
        "FOODIE15 (15% off)": 15,
        "VIP20 (20% off)": 20
    }
    discount_percentage = discounts.get(discount_option, 0)  # Default 0 if invalid
    discount_amount = (discount_percentage / 100) * total
    return total - discount_amount, discount_percentage, discount_amount

# ✅ Order Page Function
def order_page():
    # ✅ Set Background Image
    image_path = os.path.join(os.path.dirname(__file__), "images", "flas.jpg")
    if os.path.exists(image_path):
        set_background(image_path)

    # ✅ Display Header with Logo
    header_with_logo()
    st.markdown("")

    if not st.session_state.get("cart"):
        st.warning("🛒 Your cart is empty. Add items from the homepage!")
    else:
        # ✅ Large, Bold, & Underlined Heading for Cart Items
        st.markdown("""
            <h1 style="color:#ffcc00; text-align:center; font-size:40px; font-weight:bold; text-decoration: underline;">
                🛒 Items in Your Cart
            </h1>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        total = sum(float(item["price"].strip('$')) for item in st.session_state.cart)

        for index, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                st.markdown(f"<h3 style='color:#ffcc00;'>🍽️ {item['name']}</h3>", unsafe_allow_html=True)  # ✅ Larger font
                st.caption(f"{item['desc']}")
            with col2:
                st.markdown(f"<h4 style='color:white;'>💲 {item['price']}</h4>", unsafe_allow_html=True)  # ✅ Larger price
            with col3:
                if st.button(f"❌ Remove {item['name']}", key=f"remove_{index}"):
                    st.session_state.cart.pop(index)
                    st.rerun()  # ✅ UI updates immediately

        st.markdown("---")

        # ✅ Discount Dropdown Section
        st.markdown("### 🎟️ **Apply Discount Code**")
        discount_options = ["No Discount", "HALAL10 (10% off)", "FOODIE15 (15% off)", "VIP20 (20% off)"]
        selected_discount = st.selectbox("Select a discount", discount_options)

        discounted_total, discount_percentage, discount_amount = apply_discount(total, selected_discount)

        if discount_percentage > 0:
            st.success(f"✅ {discount_percentage}% discount applied! You saved **${discount_amount:.2f}** 🎉")

        st.markdown(f"## **Total: ${discounted_total:.2f}**")

        # ✅ Confirm Order Button - Clears Cart & Shows "Track Order"
        if st.button("✅ Confirm Order"):
            st.success(f"🎉 Order placed successfully! Final Amount: **${discounted_total:.2f}**")
            st.session_state.cart.clear()
            st.session_state.order_status = 1  # ✅ Start tracking at "Order Received"
            st.session_state.show_track_button = True  # ✅ Show "Track Order" button
            st.rerun()

    # ✅ Show "Track Order" button after confirming order
    if st.session_state.get("show_track_button", False):
        if st.button("📦 Track Order"):
            st.query_params["page"] = "Progress"  # ✅ Correctly update query params

    if st.button("🔙 Homepage"):
        st.query_params["page"] = "Homepage"  # ✅ Correctly update query params

# ✅ Run the Page
if __name__ == "__main__":
    order_page()
