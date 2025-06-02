import streamlit as st
import sqlite3
import os
import base64

# ✅ Function to Convert Image to Base64
def get_base64_image(image_path):
    """Encodes an image in Base64 format for embedding in HTML."""
    if not os.path.exists(image_path):
        return None  # Return None if image not found
    
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ✅ Function to Set a Background Image
def set_background(image_file):
    """Sets a background image in Streamlit using custom CSS."""
    encoded_string = get_base64_image(image_file)
    
    if encoded_string:
        page_bg_css = f"""
        <style>
        .stApp {{
            background: url("data:image/jpeg;base64,{encoded_string}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """
        st.markdown(page_bg_css, unsafe_allow_html=True)
    else:
        st.error(f"⚠️ Background image not found: {image_file}")

# ✅ Function to Display Header with Logo
def header_with_logo():
    """Displays the vendor logo in the header."""
    logo_path = os.path.join("images", "venderslogo.jpeg")  # Ensure correct path
    logo_base64 = get_base64_image(logo_path)

    if logo_base64:
        st.markdown(f"""
            <style>
                .vendor-header {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    background-color: rgb(5, 1, 1);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 5px rgba(252, 252, 252, 0.86);
                }}
                .vendor-header img {{
                    height: 60px;
                    width: auto;
                    border-radius: 5px;
                }}
                .vendor-header h1 {{
                    color: white;
                    font-size: 26px;
                    font-weight: bold;
                    margin: 0;
                }}
            </style>
            <div class="vendor-header">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="Vendor Logo">
                <h1>Vendor Dashboard</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.title("📦 Vendor Dashboard")  # Fallback if logo is missing

# ✅ About Us Page Function
def about_us_page():
    # ✅ Set Background Image
    set_background("images/venback.jpeg")  # ✅ Updated image

# ✅ Connect to SQLite Database
def get_db_connection():
    conn = sqlite3.connect("vendor.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendor_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            item_price REAL NOT NULL,
            FOREIGN KEY (vendor_id) REFERENCES vendor(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    return conn

# ✅ Vendor Page
def vendor_page():
    # ✅ Set Background Image
    set_background("images/flas.jpg")  # ✅ Updated background image

    # ✅ Display Header with Logo
    header_with_logo()
    st.markdown("")
    st.markdown("🔹 Manage your products, track sales, and grow your business!")
    conn = get_db_connection()
    cursor = conn.cursor()

    if "vendor_logged_in" not in st.session_state:
        st.session_state.vendor_logged_in = False
    if "vendor_username" not in st.session_state:
        st.session_state.vendor_username = ""

    # ✅ Vendor Registration
    st.subheader("📝 Vendor Registration")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    if st.button("Register"):
        if new_username and new_password:
            try:
                cursor.execute("INSERT INTO vendor (username, password) VALUES (?, ?)", 
                               (new_username, new_password))
                conn.commit()
                st.success("✅ Account registered successfully! You can now log in.")
            except sqlite3.IntegrityError:
                st.error("❌ Username already exists. Choose a different one.")
        else:
            st.warning("⚠️ Please enter both a username and a password.")

    # ✅ Vendor Login
    st.subheader("🔐 Vendor Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        cursor.execute("SELECT id FROM vendor WHERE username=? AND password=?", 
                       (username, password))
        user = cursor.fetchone()
        if user:
            st.session_state.vendor_logged_in = True
            st.session_state.vendor_username = username
            st.session_state.vendor_id = user[0]
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")

    # ✅ Vendor Dashboard (after login)
    if st.session_state.vendor_logged_in:
        st.success(f"🔓 Logged in as **{st.session_state.vendor_username}**")

        # 🔹 Add New Item
        st.subheader("🛒 Add New Item")
        item_name = st.text_input("Item Name")
        item_price = st.number_input("Price ($)", min_value=1.0, step=0.5)

        if st.button("➕ Add Item"):
            if item_name:
                cursor.execute("INSERT INTO vendor_items (vendor_id, item_name, item_price) VALUES (?, ?, ?)",
                               (st.session_state.vendor_id, item_name, item_price))
                conn.commit()
                st.success(f"✅ Item '{item_name}' added successfully!")
                st.rerun()
            else:
                st.warning("⚠️ Please enter an item name.")

        # 🔹 Display Existing Items
        st.subheader("📋 Manage Your Items")
        cursor.execute("SELECT id, item_name, item_price FROM vendor_items WHERE vendor_id=?", 
                       (st.session_state.vendor_id,))
        items = cursor.fetchall()

        if items:
            for item in items:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"🍽️ **{item[1]}** - 💲{item[2]:.2f}")
                with col2:
                    if st.button(f"❌ Remove {item[1]}", key=item[0]):
                        cursor.execute("DELETE FROM vendor_items WHERE id=?", (item[0],))
                        conn.commit()
                        st.success(f"🚫 {item[1]} removed successfully!")
                        st.rerun()
        else:
            st.info("⚠️ No items added yet.")

        # 🔹 Vendor Analytics
        st.subheader("📊 Sales Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total Items Listed", value=len(items))
        with col2:
            total_value = sum(item[2] for item in items)
            st.metric(label="Total Inventory Value", value=f"${total_value:.2f}")

        # 🔹 Logout
        if st.button("🚪 Logout"):
            st.session_state.vendor_logged_in = False
            st.session_state.vendor_username = ""
            st.rerun()

    conn.close()

# ✅ Run the Page
if __name__ == "__main__":
    vendor_page()
