import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import httpx
import io
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()

def load_opportunities_structure():
    """Load the opportunities folder structure"""
    opportunities = {}
    base_path = "opportunities"
    
    for city in os.listdir(base_path):
        city_path = os.path.join(base_path, city)
        if os.path.isdir(city_path):
            opportunities[city] = []
            for industry_file in os.listdir(city_path):
                if industry_file.endswith('.txt'):
                    industry_name = industry_file.replace('.txt', '')
                    opportunities[city].append(industry_name)
    
    return opportunities

def load_opportunity_content(city, industry):
    """Load the content of an opportunity file"""
    file_path = f"opportunities/{city}/{industry}.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.exception(f"Failed to load opportunity file: {file_path}")
        return None

# Initialize opportunities structure
OPPORTUNITIES_STRUCTURE = load_opportunities_structure()
if not OPPORTUNITIES_STRUCTURE:
    st.error("Failed to load opportunities structure. Please check the opportunities folder.")
    st.stop()

# Streamlit App Title
st.image("changemakers-logo.png", width=200)

# API Key input in sidebar
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password", help="Get your API key from Google AI Studio")

if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar to proceed.")
    st.stop()

# Configure the Gemini API with the provided API key
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()

def process_report_and_generate_matches(esg_url, opportunity_content, location_context):
    try:
        # Download ESG report
        esg_data = io.BytesIO(httpx.get(esg_url).content)
        
        # Save ESG data to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(esg_data.getvalue())
            tmp_file_path = tmp_file.name
            
        # Upload ESG report
        esg_pdf = genai.upload_file(tmp_file_path)
        
        # Clean up ESG temp file
        os.unlink(tmp_file_path)
        
        # Construct prompt for analysis
        prompt = f"""
        You are an AI assistant analyzing an ESG/CSRD report and matching it with potential sustainability opportunities.
        
        Location Context:
        - City: {location_context['city']}
        - Industry: {location_context['industry']}
        
        Project Context:
        {project_description if project_description else "No additional project context provided."}
        
        Available Opportunities:
        {opportunity_content}
        
        Based on the ESG report and project context, analyze and rate each opportunity based on:
        1. Match Score (0-100) based on how it will improve the company's ESG metrics and align with project goals
        2. Key Alignment Points (including specific connections to project goals if provided)
        3. Potential Impact for ESG metrics
        4. Mail with a concrete Idea proposal to the startup from the company providing the ESG report. Max 3 sentences asking for a meeting.
        5. Relevant Mail Address
        
        Present the results in a markdown table format, followed by detailed explanations for each opportunity.
        Sort the opportunities by Match Score in descending order.
        Focus on practical, actionable insights and specific connections between:
        - The company's ESG goals
        - The stated project objectives (if provided)
        - The available opportunities
        """
        
        # Generate analysis
        response = model.generate_content([esg_pdf, prompt])
        return response.text
    except Exception as e:
        logger.exception("Failed to process report and generate matches")
        return None

# Main content area
st.header("Find Matching Opportunities")
st.write("""
Provide the URL to your ESG/CSRD report and we'll match you with relevant opportunities 
based on your location and industry.
""")

# Sidebar for Selection
st.sidebar.header("Location and Industry")

# Get available cities and industries
cities = list(OPPORTUNITIES_STRUCTURE.keys())
selected_city = st.sidebar.selectbox("Select City", cities)

# Get industries based on selected city
industries = OPPORTUNITIES_STRUCTURE[selected_city] if selected_city else []
selected_industry = st.sidebar.selectbox("Select Industry", industries)

# URL input for ESG/CSRD report
st.header("Provide Your Report")
esg_report_url = st.text_input(
    "Enter the URL to your ESG/CSRD Report (PDF)",
    placeholder="https://example.com/your-esg-report.pdf"
)

# Add project description text area
project_description = st.text_area(
    "Optional Project Description",
    placeholder="Enter any additional context about your sustainability project or specific goals...",
    help="This information will be used to better match opportunities with your specific needs."
)

# Generate Matches button
if esg_report_url and selected_city and selected_industry:
    if st.button("Find Matching Opportunities"):
        with st.spinner("Analyzing your report and finding matches..."):
            # Load opportunity content
            opportunity_content = load_opportunity_content(selected_city, selected_industry)
            
            if not opportunity_content:
                st.error(f"Failed to load opportunities for {selected_city} - {selected_industry}")
                st.stop()
            
            # Location context for the AI
            location_context = {
                "city": selected_city,
                "industry": selected_industry
            }
            
            # Generate matches
            matches = process_report_and_generate_matches(
                esg_report_url,
                opportunity_content,
                location_context
            )
            
            if matches:
                st.success("Analysis completed!")
                st.markdown("## Matching Opportunities")
                st.markdown(matches)
            else:
                st.error("Failed to generate matches. Please check the URL and try again.")
else:
    st.info("👆 Please provide your ESG/CSRD report URL and select your location and industry to find matching opportunities.")

# Add footer with additional information
st.sidebar.markdown("---")
st.sidebar.markdown("""
### About ChangeMatcher
We help companies find local opportunities to improve sustainability metrics through targeted collaborations with research projects, startups and initiatives.
""")