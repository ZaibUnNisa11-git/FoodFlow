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
    """Displays the order tracking logo in the header."""
    logo_path = os.path.join("images", "progresslogo.jpg")  # Ensure correct path
    logo_base64 = get_base64_image(logo_path)

    if logo_base64:
        st.markdown(f"""
            <style>
                .progress-header {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    background-color: rgb(5, 1, 1);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 5px rgba(252, 252, 252, 0.86);
                }}
                .progress-header img {{
                    height: 60px;
                    width: auto;
                    border-radius: 5px;
                }}
                .progress-header h1 {{
                    color: white;
                    font-size: 26px;
                    font-weight: bold;
                    margin: 0;
                }}
            </style>
            <div class="progress-header">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="Order Tracking Logo">
                <h1>Order Tracking</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.title("📦 Order Tracking")  # Fallback if logo is missing

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

# ✅ Progress Page Function
def progress_page():
    # ✅ Set Background Image
    image_path = os.path.join(os.path.dirname(__file__), "images", "flas.jpg")
    if os.path.exists(image_path):
        set_background(image_path)

    # ✅ Display Header with Logo
    header_with_logo()

    if "order_status" not in st.session_state:
        st.session_state.order_status = 0  

    status_messages = [
        "🛒 Order Received",
        "🍳 Preparing Your Food",
        "🚴 Out for Delivery",
        "✅ Delivered!"
    ]

    # ✅ Prevent tracking if order has not started
    st.markdown("")
    st.markdown("")
    if st.session_state.order_status == 0:
        st.warning("🚨 No active order found! Please place an order first.")
        return

    # ✅ Show Progress Bar and Status
    st.progress(st.session_state.order_status / 3)
    st.write(f"### {status_messages[st.session_state.order_status]}")

    # ✅ Move to next step when "Next Step" is clicked
    if st.session_state.order_status < 3:
        if st.button("Next Step ➡️"):
            st.session_state.order_status += 1
            st.rerun()

    # ✅ Show "Reset Tracking" when order is delivered
    if st.session_state.order_status == 3:
        st.success("🎉 Your order has been delivered!")
        if st.button("🔄 Reset Tracking"):
            st.session_state.order_status = 0
            st.session_state.show_track_button = False  # ✅ Hide "Track Order" button after delivery
            st.rerun()

# ✅ Run the Page
if __name__ == "__main__":
    progress_page()
