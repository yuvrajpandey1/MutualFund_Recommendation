⚠️ **IMPORTANT: Configure Groq API Key Before Running**

This project requires a Groq API key to function. Follow these steps:

## Step 1: Get Your Groq API Key

1. Visit: https://console.groq.com/keys
2. Sign up or log in with your Groq account
3. Create a new API key
4. Copy the key (starts with `gsk_`)

## Step 2: Configure Local Environment

Create a `.env` file in the project root with your API key:

```bash
GROQ_API_KEY=your-actual-groq-api-key-here
```

**DO NOT commit this file to Git!** It's already in `.gitignore`

## Step 3: For Streamlit Cloud Deployment

When deploying to Streamlit Cloud:

1. Go to your app's **Settings** → **Secrets**
2. Add:
   ```toml
   GROQ_API_KEY = "your-actual-groq-api-key-here"
   ```
3. Save and restart the app

## Step 4: Run the Application

```bash
# Activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run ui/app.py
```

The app will open at: http://localhost:8501

---

**⚠️ Security Note:** Never share your API key. Never commit `.env` to version control.

For detailed setup instructions, see [README.md](README.md) and [QUICK_START.md](QUICK_START.md)
