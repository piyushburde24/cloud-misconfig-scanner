from config.config import Config

if Config.GEMINI_API_KEY:
    print("✅ Gemini API Key Loaded Successfully")
else:
    print("❌ API Key Not Found")
