# ChangeMatchers

ChangeMatchers is an AI-powered platform that analyzes ESG/CRSD reports and matches companies with local sustainability opportunities, including research projects, startups, and initiatives.

## Features
- **AI-Powered Analysis**: Utilizes Google's Gemini AI to analyze ESG/CRSD reports
- **Smart Matching**: Automatically matches reports with relevant local opportunities
- **Location-Based**: Filters opportunities by city and industry
- **Detailed Analysis**: Provides match scores, alignment points, potential impact, and implementation timeline
- **User-Friendly Interface**: Built with Streamlit for easy interaction

## Prerequisites
- Python 3.x
- Google Cloud Platform account with Gemini API access
- Valid Gemini API key

## Installation
```bash
git clone https://github.com/yourusername/changematchers.git
cd changematchers
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
1. Create a `.env` file in the root directory
2. Add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Running the Application
1. Ensure you're in your virtual environment:
```bash
# On Unix/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

2. Start the Streamlit application:
```bash
streamlit run app.py
```

3. The application will open in your default web browser at `http://localhost:8501`

Note: If you're running the application remotely, you can access it using the Network URL provided in the terminal output.

## Usage
1. Select your city and industry from the sidebar dropdowns
2. Enter the URL of your ESG/CRSD report (PDF format)
3. Click "Find Matching Opportunities"
4. Review the AI-generated matches and analysis

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.