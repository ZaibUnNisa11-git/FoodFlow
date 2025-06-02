import os
import base64
import streamlit as st
import random

# Function to Convert an Image to Base64 for CSS Embedding
def get_base64_image(image_filename):
    """Encodes an image in Base64 format for embedding in HTML."""
    image_path = os.path.join(os.path.dirname(__file__), "images", image_filename)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"⚠️ Image file '{image_path}' not found. Check the path!")

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert images to Base64
bg_image_base64 = get_base64_image("flas.jpg")  # Background Image
hero_image_base64 = get_base64_image("flside.jpeg")  # Hero Section Image

def homepage(df):
    # Custom CSS for Modern UI
    st.markdown(f"""
        <style>
            /* Full-Page Background */
            .stApp {{
                background: url('data:image/jpg;base64,{bg_image_base64}') no-repeat center center fixed;
                background-size: cover;
            }}

            /* Hero Section */
            .hero-container {{
                width: 100%;
                height: 380px;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: white;
                text-shadow: 3px 3px 10px rgba(0,0,0,0.8);
                background: url('data:image/jpeg;base64,{hero_image_base64}') no-repeat center center;
                background-size: cover;
                border-radius: 15px;
                position: relative;
                box-shadow: 0px 2px 5px rgba(252, 252, 252, 0.86);
            }}

            .hero-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6); /* Dark Overlay */
                border-radius: 15px;
            }}

            .hero-content {{
                position: relative;
                z-index: 2;
            }}

            .hero-content h1 {{
                font-size: 55px;
                font-weight: bold;
                margin-bottom: 15px;
                color: #ffcc00; /* Gold */
            }}

            .hero-content p {{
                font-size: 24px;
                font-weight: 300;
                color: white;
                margin-bottom: 25px;
            }}

            /* Stylish Cards */
            .card {{
                background: #333;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease-in-out;
                color: #ffcc00;
                text-align: center;
                cursor: pointer;
            }}

            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 18px rgba(0, 0, 0, 0.5);
            }}
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown(f"""
        <div class="hero-container">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <h1>🍽️ Welcome to FoodFlow</h1>
                <p>Discover Delicious Food & Get Personalized Recommendations!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Cuisine Selection
    st.markdown("## 🌍 Choose Your Cuisine")
    categories = df["category"].unique().tolist()
    category_cols = st.columns(len(categories))
    selected_category = None

    for i, category in enumerate(categories):
        if category_cols[i].button(f"🍽️ {category}", key=f"cat_{i}"):
            selected_category = category

    if not selected_category:
        selected_category = categories[0]

    st.markdown(f"### 🍛 You Selected: **{selected_category}**")

    # Filter Data
    filtered_df = df[df["category"] == selected_category]

    # Food Search Section
    st.markdown("## 🔍 Find Your Favorite Dish")
    selected_item = st.selectbox("Search for a food item:", ["Select an item"] + filtered_df["name"].tolist())

    if selected_item != "Select an item":
        item_info = filtered_df[filtered_df["name"] == selected_item].iloc[0]
        st.success(f"✅ {selected_item} Selected!")
        st.markdown(f"**🍽️ {item_info['name']}** - **{item_info['price']}**")
        st.markdown(f"_{item_info['desc']}_")

    # Recommendations
    st.markdown("---")
    st.markdown("## 🔥 Curated for You ")
    rec_option = st.radio("Choose recommendation type:", ["Randomized", "Top Rated"])

    recommendations = filtered_df.to_dict(orient="records")

    if rec_option == "Randomized":
        recs = random.sample(recommendations, min(3, len(recommendations)))
    else:
        recs = sorted(recommendations, key=lambda x: float(str(x["price"]).replace("$", "")), reverse=True)[:3]

    cols = st.columns(3)
    for i, item in enumerate(recs):
        with cols[i]:
            st.markdown(f"""
                <div class="card">
                    <h4>🍽️ {item['name']} - {item['price']}</h4>
                    <p>{item['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

    # Food Ordering Section
    st.markdown("---")
    st.markdown("## 🛒 Order Your Favorite Food")
    selected_food = st.selectbox("Choose a food item to order:", ["Select an item"] + filtered_df["name"].tolist())

    if selected_food != "Select an item":
        selected_item = next((item for item in recommendations if item["name"] == selected_food), None)
        if selected_item:
            st.markdown(f"### 🍛 {selected_item['name']} - **{selected_item['price']}**")
            st.markdown(f"_{selected_item['desc']}_")
            if st.button("✅ Add to Cart"):
                if "cart" not in st.session_state:
                    st.session_state.cart = []
                if selected_item in st.session_state.cart:
                    st.warning(f"⚠️ {selected_item['name']} is already in your cart!")
                else:
                    st.session_state.cart.append(selected_item)
                    st.success(f"✅ {selected_item['name']} added to cart!")

    # Go to Order Button
    if st.button("🛒 Go to Order"):
        st.query_params["page"] = "Order"
