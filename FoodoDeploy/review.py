import streamlit as st
import pandas as pd
import plotly.express as px  # ✅ Using Plotly for interactive visualizations
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
    """Displays the review logo in the header."""
    logo_path = os.path.join("images", "reviewlogo.jpg")  # Ensure correct path
    logo_base64 = get_base64_image(logo_path)

    if logo_base64:
        st.markdown(f"""
            <style>
                .review-header {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    background-color: rgb(5, 1, 1);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 5px rgba(252, 252, 252, 0.86);
                }}
                .review-header img {{
                    height: 60px;
                    width: auto;
                    border-radius: 5px;
                }}
                .review-header h1 {{
                    color: white;
                    font-size: 26px;
                    font-weight: bold;
                    margin: 0;
                }}
            </style>
            <div class="review-header">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="Review Logo">
                <h1>Food Reviews & Ratings</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.title("⭐ Food Reviews & Ratings")  # Fallback if logo is missing

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

# ✅ Load food dataset
@st.cache_data
def load_data():
    df = pd.read_csv("food_data.csv", encoding="utf-8")
    df.columns = df.columns.str.strip().str.lower()  # Standardize column names
    return df

df = load_data()

def review_page():
    # ✅ Set Background Image
    image_path = os.path.join(os.path.dirname(__file__), "images", "flas.jpg")
    if os.path.exists(image_path):
        set_background(image_path)

    # ✅ Display Header with Logo
    header_with_logo()
    st.markdown("")
    st.markdown("")
    # ✅ Select a category for histogram
    categories = df["category"].unique().tolist()
    st.markdown("")
    selected_category = st.selectbox("📌 Choose a category:", categories)

    # ✅ Filter data for selected category
    filtered_df = df[df["category"] == selected_category]

    # ✅ Show Bar Chart for Reviews
    if not filtered_df.empty:
        fig = px.bar(filtered_df,
                     x="name",  # ✅ Use 'name' for food items
                     y="review",
                     labels={"name": "Food Item", "review": "Review Ratings"},
                     title=f"📊 Review Distribution for {selected_category}",
                     color="review",
                     color_continuous_scale="Sunset")
        st.plotly_chart(fig)

    # ✅ Collect User Reviews
    st.subheader("📝 Share Your Feedback")

    if "reviews" not in st.session_state:
        st.session_state.reviews = []

    name = st.text_input("Your Name")
    food_item = st.selectbox("Select the Food Item", filtered_df["name"].unique().tolist() if not filtered_df.empty else [])
    rating = st.slider("Rate Your Experience", 1, 5, 3)
    comment = st.text_area("Leave a Comment")

    if st.button("Submit Review"):
        if name.strip() and comment.strip() and food_item:
            review = {"name": name, "food": food_item, "rating": rating, "comment": comment}
            st.session_state.reviews.append(review)
            st.success("Thank you for your feedback!")
            st.rerun()
        else:
            st.warning("Please fill out all fields before submitting.")

    # ✅ Show User Submitted Reviews
    if st.session_state.reviews:
        st.subheader("📢 User Reviews")
        for review in st.session_state.reviews:
            st.markdown(f"""
                **Review by {review['name']} on {review['food']}**  
                ⭐ Rating: {review['rating']}/5  
                💬 Comment: {review['comment']}
            """)
            st.divider()

if __name__ == "__main__":
    review_page()
