# Deployment Guide - Mutual Funds Recommendation System

## Quick Start - Streamlit Cloud Deployment (Recommended)

This guide provides step-by-step instructions to deploy your Mutual Funds Recommendation System to Streamlit Cloud.

---

## Prerequisites

- GitHub account
- Groq API Key: Get from https://console.groq.com/keys
- Project code pushed to GitHub

---

## Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git

```bash
cd d:\Recommendation_Systems
git init
git add .
git commit -m "Initial commit: Mutual Funds Recommendation System"
```

### 1.2 Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New" to create a new repository
3. Name it: `recommendation-system` or similar
4. Initialize with README (optional)
5. Click "Create repository"

### 1.3 Push Code to GitHub

```bash
git remote add origin https://github.com/yourusername/recommendation-system.git
git branch -M main
git push -u origin main
```

**Replace `yourusername` with your actual GitHub username.**

### 1.3b Set Environment Variable

Before pushing, update your `.env` file:

```bash
# Get your Groq API key from: https://console.groq.com/keys
GROQ_API_KEY="your-actual-groq-api-key"
```

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Visit Streamlit Cloud Dashboard

1. Go to [Streamlit Cloud Dashboard](https://share.streamlit.io/)
2. Sign in or create an account using GitHub
3. Click "New app"

### 2.2 Connect Repository

1. In the "Deploy an app" form:
   - **Repository**: Select your GitHub repository
   - **Branch**: Select `main`
   - **Main file path**: Enter `ui/app.py`

2. Click "Deploy!"

Streamlit will start deploying your app. This may take 1-2 minutes.

### 2.3 Add Secrets

Once deployed, you'll see your app with a "Manage app" link in the top-right.

1. Click "Manage app"
2. Go to "Settings" tab
3. Click "Secrets" section (or scroll down)
4. Paste your secrets in TOML format:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

5. Save and restart the app

### 2.4 Get Your Public URL

After deployment, your app will be available at:
```
https://share.streamlit.io/yourusername/recommendation-system/main/ui/app.py
```

You can also find it on your Streamlit Cloud Dashboard.

---

## Step 3: Update Code to Use Secrets

Update `ui/app.py` to use Streamlit secrets:

```python
# Replace this line:
# GROQ_API_KEY = "your-groq-api-key"

# With this:
import streamlit as st
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "your-groq-api-key")
```

---

## Optional: Alternative Deployment Methods

### Deploy to Heroku

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Steps

1. **Login to Heroku:**
```bash
heroku login
```

2. **Create Heroku App:**
```bash
heroku create your-app-name
```

3. **Set Environment Variables:**
```bash
heroku config:set GROQ_API_KEY="your-groq-api-key-here"
```

4. **Deploy:**
```bash
git push heroku main
```

5. **Open App:**
```bash
heroku open
```

Your app will be available at: `https://your-app-name.herokuapp.com`

### Deploy to Render

1. Go to [Render.com](https://render.com/)
2. Sign up and create new Web Service
3. Connect your GitHub repository
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run ui/app.py`
5. Add environment variables in settings
6. Deploy

### Deploy to PythonAnywhere

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com/)
2. Create account and upload files via Web interface
3. Create new Streamlit web app
4. Set up WSGI configuration
5. Enable and run the web app

---

## Troubleshooting Deployment

### Issue: "requirements.txt not found"

**Solution:** Ensure `requirements.txt` is in the root directory and committed to Git.

```bash
git add requirements.txt
git commit -m "Add requirements.txt"
git push origin main
```

### Issue: "ModuleNotFoundError: No module named 'groq'"

**Solution:** Update `requirements.txt` to include all dependencies:

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push origin main
```

### Issue: "API key not found" or "GROQ_API_KEY is missing"

**Solution:** Add secrets through Streamlit Cloud dashboard:
1. Go to your app's Manage page
2. Click Settings → Secrets
3. Add your GROQ_API_KEY
4. Restart the app

### Issue: App is very slow or timing out

**Solution:** 
- Optimize data loading by caching functions with `@st.cache_data`
- Reduce the number of mutual funds shown initially
- Implement pagination for fund listings

### Issue: "Connection refused" when trying to access API

**Solution:**
- FastAPI backend is only available locally
- For production, deploy both frontend (Streamlit) and backend (FastAPI) separately
- Or embed FastAPI directly in Streamlit (current setup)

---

## Sharing Your App

Once deployed on Streamlit Cloud, you can share your app:

### Method 1: Direct Link
```
https://share.streamlit.io/yourusername/recommendation-system/main/ui/app.py
```

### Method 2: QR Code
- Go to your Streamlit Cloud Dashboard
- Click on your app
- A QR code will be available to share

### Method 3: Share Settings
- Click "Share" button in your app (top right)
- Choose sharing preferences

---

## Production Checklist

Before sharing with your manager:

- [ ] **API Key**: Securely set in Streamlit Cloud secrets
- [ ] **.gitignore**: Ensure `.env` file is not committed
- [ ] **Error Handling**: Test error scenarios
- [ ] **Performance**: Check app load times
- [ ] **UI/UX**: Test all features work as expected
- [ ] **Mobile**: Test on mobile devices
- [ ] **Documentation**: Keep README updated
- [ ] **Monitoring**: Set up monitoring for uptime

---

## Configuration for Production

### Update `.streamlit/config.toml` for Production:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#31333F"
font = "sans serif"

[client]
showErrorDetails = false
toolbarMode = "viewer"

[logger]
level = "warning"

[server]
port = 8501
headless = true
enableXsrfProtection = true
maxUploadSize = 200
runOnSave = false
```

---

## Monitoring and Maintenance

### View Logs
- **Streamlit Cloud**: Check logs in your app's settings
- **Heroku**: `heroku logs --tail`
- **Render**: View in dashboard

### Update Application
1. Make changes locally
2. Commit to Git: `git add . && git commit -m "message"`
3. Push to GitHub: `git push origin main`
4. Deployment will update automatically (usually within 1-2 minutes)

### Enable Auto-Deploy
In Streamlit Cloud settings, ensure "Auto-deploy" is enabled.

---

## Security Best Practices

1. **Never commit API keys** to Git
2. **Use Streamlit Secrets** for sensitive data
3. **Enable 2FA** on GitHub account
4. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`
5. **Review deployed code** regularly
6. **Monitor API usage** to detect unusual activity
7. **Use environment-specific configurations**

---

## Support and Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud/)
- [Groq Documentation](https://console.groq.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## Final Steps to Send to Manager

1. **Get your public URL** from Streamlit Cloud
2. **Test the application thoroughly**
3. **Send the URL** to your manager with context:
   ```
   Subject: Mutual Funds Recommendation System - Live Demo
   
   Hi [Manager Name],
   
   I've deployed the Mutual Funds Recommendation System to:
   [YOUR_STREAMLIT_CLOUD_URL]
   
   Features:
   - AI-powered mutual fund recommendations
   - Real fund data with performance metrics
   - Interactive chat with AI advisor
   - Fund comparison tools
   - Complete analytics
   
   Please let me know if you have any questions or feedback.
   
   Best regards,
   [Your Name]
   ```

4. **Share GitHub repository** if needed:
   ```
   https://github.com/yourusername/recommendation-system
   ```

---

## Version Control for Future Updates

After deployment, keep updating your app:

```bash
# Make changes
git add .
git commit -m "Feature: Add new mutual funds"
git push origin main

# Streamlit Cloud will auto-deploy within 1-2 minutes
```

---

**Deployment Date**: [Current Date]  
**Status**: Ready for Production  
**Support Contact**: [Your Contact Info]

Good luck with your deployment! 🚀
