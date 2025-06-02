import streamlit as st
import os
import base64

# ✅ Function to Convert Image to Base64
def get_base64_image(image_path):
    """Encodes an image in Base64 format for embedding in HTML."""
    if not os.path.exists(image_path):
        return None  # Return None if image is missing
    
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
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(page_bg_css, unsafe_allow_html=True)

# ✅ Function to Display Header with Logo for About Us
def about_us_header():
    """Displays the About Us logo in the header."""
    logo_path = os.path.join("images", "aboutuslogo.jpg")  # Ensure correct path
    logo_base64 = get_base64_image(logo_path)

    if logo_base64:
        st.markdown(f"""
            <style>
                .about-header {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    background-color: rgb(5, 1, 1);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 5px rgba(252, 252, 252, 0.86);
                }}
                .about-header img {{
                    height: 60px;
                    width: auto;
                    border-radius: 5px;
                }}
                .about-header h1 {{
                    color: white;
                    font-size: 26px;
                    font-weight: bold;
                    margin: 0;
                }}
            </style>
            <div class="about-header">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="About Us Logo">
                <h1>About Us - Food Flow</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.title("📌 About Us - Food Flow")  # Fallback if logo is missing

# ✅ Load Team Member Images
team_images = {
    "Rizwan Yousaf": get_base64_image("images/istructor.jpg"),
    "Zaib Un Nisa": get_base64_image("images/zaib.jpg"),
    "Rao Muhammad Zubair": get_base64_image("images/zubair.jpg"),
    "Huzaifa Jahangir": get_base64_image("images/huzaifa.jpg"),
    "Jannat Chochan": get_base64_image("images/jannat.jpg"),
    "Farhan Ashraf": get_base64_image("images/farhan.jpg"),
}

# ✅ About Us Page Function
def about_us_page():
    # ✅ Set Background Image
    set_background("images/flas.jpg")

    # ✅ Display About Us Header with Logo
    about_us_header()
    st.markdown("")
    st.markdown("")

    # ✅ Expandable About Us Section
    with st.expander("📌 About Us - Food Flow", expanded=False):
        st.write("""
        🚀 **As 4th-semester Software Engineering students**, our **ICAT project** serves multiple purposes:
        - Developing a **real-world software project**.
        - Enhancing **UI/UX & database** skills.
        - Making **Halal food more accessible**.
        - Gaining **job-ready experience**.
        """)

    # ✅ Expandable Purpose Section
    with st.expander("🎯 Purpose of Our Project - Food Flow", expanded=False):
        st.write("""
        ### **1️⃣ Real-World Software Development Experience**  
        ✅ Apply **full-stack development** skills.  
        ✅ Work with **databases, APIs, and UI design**.  

        ### **2️⃣ Improving Halal Food Accessibility**  
        ✅ Provide an **easy platform** for Halal food.  
        ✅ Ensure **authentic and accessible** Halal meals.  

        ### **3️⃣ Learning Software Engineering Principles**  
        ✅ Implement **agile development & team collaboration**.  
        ✅ Work on **payment integration, security, and APIs**.  

        ### **4️⃣ Building a Strong Portfolio for Jobs**  
        ✅ Gain experience in **Python, Streamlit, and UI/UX**.  
        ✅ Demonstrate **problem-solving & teamwork**.  

        ### **5️⃣ ICAT Project Evaluation & Academic Success**  
        ✅ Deliver a **fully functional food-ordering system**.  
        ✅ Learn **software optimization and debugging**.  
        """)

    # Team Members Section
    st.markdown("## 🌟 Our Dedicated Team") 
    st.markdown("<style>.fade-in {{ animation: fadeIn 1s; }}</style>", unsafe_allow_html=True)  # Motion UI effect 
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)  # Start fade-in effect

    
    # Improved CSS for Proper Image Display and Vertical Spacing
    st.markdown("""
        <style>
        .team-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 50px;  /* Increased spacing between cards */
            padding: 20px;
        }
        .team-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            background: rgba(255, 255, 255, 0.85);
            padding: 25px;  /* Increased padding */
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            width: 300px;
            text-align: center;
            margin-bottom: 30px;  /* More vertical spacing */
            transition: transform 0.3s; /* Animation for card */
        }
        .team-card:hover {
            transform: scale(1.05); /* Slightly increase size on hover */
            box-shadow: 0 8px 16px rgba(0,0,0,0.4); /* Enhanced shadow on hover */
        }
        .team-card img {
            width: 150px;  /* Bigger images */
            height: 150px;
            border-radius: 50%;
            object-fit: cover;  /* Ensures the full image is displayed */
            margin-bottom: 20px; /* Increased spacing */
            border: 3px solid white;
        }
        .team-card h3 {
            font-size: 20px;
            color: #333;
            margin: 8px 0;
        }
        .team-card p {
            font-size: 15px;
            color: #555;
            margin: 5px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="team-container">', unsafe_allow_html=True)

    members = [
        ("Rizwan Yousaf", "Supervisor", "📧 rizwan@gmail.com"),
        ("Zaib Un Nisa", "Lead Full-Stack Developer", "📧 zaibnisa112002@gmail.com"),
        ("Rao Muhammad Zubair", "Database & API Management", "📧 raozubair@gmail.com"),
        ("Huzaifa Jahangir", "Frontend & UI Designer", "📧 huzaifajahangir@gmail.com"),
        ("Jannat Chochan", "Testing & Content Writer", "📧 jannatchochan@gmail.com"),
        ("Farhan Ashraf", "Deployment & Hosting Expert", "📧 farhanashraf@gmail.com"),
    ]

    # Display members in rows with proper spacing
    cols = st.columns(3)
    for index, (name, role, email) in enumerate(members):
        img_src = f"data:image/jpeg;base64,{team_images[name]}" if team_images[name] else "https://via.placeholder.com/140"

        with cols[index % 3]:  
            st.markdown(f"""
                <div class="team-card">
                    <img src="{img_src}" alt="{name}">
                    <h3>{name}</h3>
                    <p><strong>{role}</strong></p>
                    <p>{email}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # End fade-in effect


    st.markdown("---")

    # Contact Information
    st.markdown(""" 
        ### 📩 Want to Connect? 
        📧 **Contact Us:** foodflow@team.com  
        🌐 **Follow Us:** [📸 Instagram](#) | [🐦 Twitter](#) | [🔗 LinkedIn](#)  
        🔥 **Thank you for supporting our journey!** 🔥 

    """)