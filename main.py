import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="Customer Satisfaction Predictor",
    page_icon="⭐",
    layout="wide"
)

# Enhanced CSS with MASSIVE fonts
st.markdown("""
<style>
    .main-title {

        font-size: 12rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0;
        font-weight: 900;
        padding: 0.5rem 0;
        letter-spacing: 5px;
        line-height: 0.9;
        text-shadow: 5px 5px 10px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #1E3A8A 0%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: -1rem;
    }
    .subtitle {
        font-size: 4.5rem;
        color: #444;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        padding-top: 0;
        background: linear-gradient(135deg, #666 0%, #333 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .result-percentage {
        font-size: 6rem;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f2ff 100%);
        border-radius: 20px;
        border: 3px solid #1E3A8A;
    }
    .prediction-label {
        font-size: 2rem;
        color: #444;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1E3A8A 0%, #2c5282 100%);
        color: white;
        border: none;
        padding: 1.5rem 4rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1.5rem;
        width: 100%;
        margin: 1rem 0;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .input-label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .stNumberInput > div > div > input {
        font-size: 1.2rem;
        padding: 0.8rem;
    }
    .stSelectbox > div > div > select {
        font-size: 1.2rem;
        padding: 0.8rem;
    }
    .stSlider > div > div > div {
        font-size: 1.2rem;
    }
    
    /* Make sure everything fits on the screen */
    @media (max-width: 1200px) {
        .main-title {
            font-size: 10rem;
        }
        .subtitle {
            font-size: 3.5rem;
        }
    }
    
    @media (max-width: 992px) {
        .main-title {
            font-size: 8rem;
        }
        .subtitle {
            font-size: 2.8rem;
        }
    }
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 6rem;
            letter-spacing: 3px;
        }
        .subtitle {
            font-size: 2.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Big Title - NOW EXTREMELY MASSIVE
st.markdown('<p class="main-title">⭐ CLIENT SATISFACTION PREDICTOR</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter freelancer details to predict satisfaction percentage</p>', unsafe_allow_html=True)

# ============================================
# 1. LOAD MODEL
# ============================================

@st.cache_resource
def load_model():
    """Load your trained model"""
    try:
        # Try different paths
        possible_paths = [
            r"C:\Users\SCS\Downloads\Streamlit_files\best_linear_regression_model.sav",
            "best_linear_regression_model.sav",
            "./best_linear_regression_model.sav"
        ]
        
        for model_path in possible_paths:
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                return model, True
        
        return None, False
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, False

# Load model
model, loaded = load_model()

if not loaded:
    st.error("Model file not found. Please make sure 'best_linear_regression_model.sav' is in the correct location.")
    st.stop()

# ============================================
# 2. INPUT FORM - ALL FIELDS START BLANK
# ============================================

st.markdown("---")
st.markdown('<p class="prediction-label">📝 ENTER FREELANCER DETAILS</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<p class="input-label">👤 Personal Information</p>', unsafe_allow_html=True)
    age = st.number_input("Age", 18, 80, None, key="age_input", placeholder="Enter age")
    gender = st.selectbox("Gender", ["Select gender", "Male", "Female"], key="gender_select")
    country = st.selectbox("Country", ["Select country", "USA", "UK", "Germany", "Australia", "India", "Canada", "France", "Spain"], key="country_select")

with col2:
    st.markdown('<p class="input-label">💼 Professional Information</p>', unsafe_allow_html=True)
    language = st.selectbox("Primary Language", ["Select language", "English", "Spanish", "German", "French", "Hindi", "Chinese", "Arabic"], key="language_select")
    skill = st.selectbox("Primary Skill", ["Select skill", "Web Development", "Graphic Design", "Data Analysis", "Content Writing", "Digital Marketing", "Mobile Development", "UI/UX Design"], key="skill_select")
    experience = st.number_input("Years Experience", 0, 50, None, key="exp_input", placeholder="Enter years")

with col3:
    st.markdown('<p class="input-label">⭐ Performance Metrics</p>', unsafe_allow_html=True)
    hourly_rate = st.number_input("Hourly Rate ($)", 10, 500, None, key="rate_input", placeholder="Enter rate")
    rating = st.slider("Client Rating", 0.0, 5.0, 0.0, 0.1, key="rating_slider")
    active = st.radio("Currently Active?", ["Select option", "✅ Yes", "❌ No"], horizontal=True, key="active_radio")

# ============================================
# 3. CREATE INPUT FOR MODEL
# ============================================

def create_input():
    """Create input for the model"""
    # Check if all fields are filled
    if (age is None or gender == "Select gender" or country == "Select country" or 
        language == "Select language" or skill == "Select skill" or experience is None or 
        hourly_rate is None or active == "Select option"):
        st.error("⚠️ Please fill in all fields before predicting!")
        return None
    
    # Create base dictionary
    input_dict = {}
    
    # Numeric features
    input_dict['age'] = float(age)
    input_dict['years_of_experience'] = float(experience)
    input_dict['hourly_rate (USD)'] = float(hourly_rate)
    input_dict['rating'] = float(rating)
    input_dict['is_active'] = 1 if "Yes" in active else 0
    
    # Create dummy variables
    # Gender
    input_dict['gender_Female'] = 1 if gender == "Female" else 0
    
    # Countries (USA as reference)
    countries = ["USA", "UK", "Germany", "Australia", "India", "Canada", "France", "Spain"]
    for c in countries[1:]:
        input_dict[f'country_{c}'] = 1 if country == c else 0
    
    # Languages (English as reference)
    languages = ["English", "Spanish", "German", "French", "Hindi", "Chinese", "Arabic"]
    for l in languages[1:]:
        input_dict[f'language_{l}'] = 1 if language == l else 0
    
    # Skills (Web Development as reference)
    skills = ["Web Development", "Graphic Design", "Data Analysis", "Content Writing", "Digital Marketing", "Mobile Development", "UI/UX Design"]
    for s in skills[1:]:
        input_dict[f'primary_skill_{s}'] = 1 if skill == s else 0
    
    # Create DataFrame
    df = pd.DataFrame([input_dict])
    
    # Add any missing columns with zeros
    if hasattr(model, 'feature_names_in_'):
        for feature in model.feature_names_in_:
            if feature not in df.columns:
                df[feature] = 0
        df = df[model.feature_names_in_]
    
    return df

# ============================================
# 4. PREDICTION BUTTON AND RESULTS
# ============================================

st.markdown("---")
st.markdown('<p class="prediction-label">🎯 GET PREDICTION</p>', unsafe_allow_html=True)

# Center the button
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button("🚀 PREDICT CUSTOMER SATISFACTION", type="primary", use_container_width=True)

if predict_button:
    with st.spinner("Calculating prediction..."):
        try:
            # Create input
            input_df = create_input()
            
            if input_df is None:
                st.stop()
            
            # Make prediction
            prediction = model.predict(input_df)[0]
            prediction = max(0, min(100, prediction))
            
            # Display BIG percentage result
            st.markdown(f'<div class="result-percentage">{prediction:.1f}%</div>', unsafe_allow_html=True)
            
            # Simple interpretation with emojis
            st.markdown("---")
            if prediction >= 80:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); 
                         color: white; border-radius: 15px; margin: 1rem 0;">
                    <h2 style="font-size: 2.5rem; margin: 0;">🏆 EXCELLENT SATISFACTION</h2>
                    <p style="font-size: 1.5rem; margin: 0.5rem 0;">High client satisfaction expected!</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                
            elif prediction >= 65:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #2196F3 0%, #0D47A1 100%); 
                         color: white; border-radius: 15px; margin: 1rem 0;">
                    <h2 style="font-size: 2.5rem; margin: 0;">👍 GOOD SATISFACTION</h2>
                    <p style="font-size: 1.5rem; margin: 0.5rem 0;">Above average expected performance</p>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FF9800 0%, #EF6C00 100%); 
                         color: white; border-radius: 15px; margin: 1rem 0;">
                    <h2 style="font-size: 2.5rem; margin: 0;">⚠️ AVERAGE SATISFACTION</h2>
                    <p style="font-size: 1.5rem; margin: 0.5rem 0;">Room for improvement</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Quick summary of inputs
            with st.expander("📋 View Details Entered"):
                col_sum1, col_sum2 = st.columns(2)
                with col_sum1:
                    st.write("**Personal Info:**")
                    st.write(f"- Age: {age}")
                    st.write(f"- Gender: {gender}")
                    st.write(f"- Country: {country}")
                    st.write(f"- Language: {language}")
                
                with col_sum2:
                    st.write("**Professional Info:**")
                    st.write(f"- Skill: {skill}")
                    st.write(f"- Experience: {experience} years")
                    st.write(f"- Rate: ${hourly_rate}/hr")
                    st.write(f"- Rating: {rating}/5")
                    st.write(f"- Active: {active}")
                    
        except Exception as e:
            # Fallback if model prediction fails
            st.error(f"⚠️ Model error: {str(e)}")
            
            # Simple calculation
            base = 65.0
            estimate = base + (rating * 8) + (experience * 0.5) - (hourly_rate * 0.1)
            if "Yes" in active:
                estimate += 5
            estimate = max(0, min(100, estimate))
            
            # Display BIG percentage result
            st.markdown(f'<div class="result-percentage">{estimate:.1f}%</div>', unsafe_allow_html=True)
            
            # Simple interpretation
            st.markdown("---")
            if estimate >= 80:
                st.success("**HIGH SATISFACTION** - Likely excellent performance")
            elif estimate >= 65:
                st.info("**GOOD SATISFACTION** - Above average expected")
            else:
                st.warning("**AVERAGE SATISFACTION** - May need improvements")

# ============================================
# 5. SIMPLE SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2> ABOUT</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Purpose:**
    Predict customer satisfaction percentage for freelancers
    
    **How to use:**
    1. Fill in all details
    2. Click PREDICT button
    3. View satisfaction percentage
    
    **Features considered:**
    - Age & experience
    - Skills & rates
    - Ratings & activity
    - Location & language
    """)
    
    st.markdown("---")
    
    if loaded:
        st.success("✅ Model loaded successfully")
        if hasattr(model, 'coef_'):
            st.write(f"Model coefficients: {len(model.coef_)}")
    
    st.caption("Customer Satisfaction Prediction Tool")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 2rem; font-size: 1.1rem;">
        <strong>CUSTOMER SATISFACTION PREDICTOR</strong> | 
        By: GROUP 2 A251 Predictive Analytics : 
        - Rieza, Akma, Mas, Aufa

    </div>
    """, 
    unsafe_allow_html=True
)


