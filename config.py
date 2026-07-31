import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # AI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    
    # App Configuration
    APP_TITLE = "AI Content Creator Assistant for Myanmar"
    APP_ICON = "🎬"
    APP_DESCRIPTION = "သင့်အတွက် ဆိုရှယ်မီဒီယာ ကွန်တင့် ဖန်တီးရန် အကူအညီ"
    
    # Available options
    PLATFORMS = ["TikTok", "Facebook", "YouTube", "All Platforms"]
    STYLES = ["Funny", "Educational", "Selling", "Storytelling", "Casual"]
    LANGUAGES = ["Myanmar", "English", "Both"]
    
    # Default settings
    DEFAULT_PLATFORM = "Facebook"
    DEFAULT_STYLE = "Casual"
    DEFAULT_LANGUAGE = "Myanmar"

config = Config()
