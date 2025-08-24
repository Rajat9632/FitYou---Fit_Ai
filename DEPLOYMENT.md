# FitAI - Render Deployment Guide

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has the following files:
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration
- `exercises.csv` - Exercise database
- `diet_data.csv` - Diet plan data
- `runtime.txt` - Python version specification

### 2. Set Up Environment Variables

**Required Environment Variables:**
- `GEMINI_API_KEY`: Your Google Gemini API key

**Optional Environment Variables:**
- `PYTHON_VERSION`: 3.12.3 (already configured)

### 3. Deploy to Render

#### Method A: Using GitHub Integration (Recommended)

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your repository
5. Render will automatically detect the `render.yaml` configuration
6. Configure environment variables in the Render dashboard

#### Method B: Manual Configuration

If not using `render.yaml`, configure manually:
- **Name**: fitai-backend
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
- **Plan**: Free

### 4. Set Environment Variables in Render

1. In your Render dashboard, go to your service
2. Click "Environment" tab
3. Add the following environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: Your actual Gemini API key
   - Mark as "Secret" if desired

### 5. Verify Deployment

After deployment, test your application:

1. **Health Check**: Visit `https://your-service-name.onrender.com/health`
2. **Main Application**: Visit `https://your-service-name.onrender.com/`
3. **AI Chatbot**: Test the chatbot functionality

## Local Development

### Running Locally

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
set GEMINI_API_KEY=your_api_key_here  # Windows
export GEMINI_API_KEY=your_api_key_here  # macOS/Linux

# Run the application
python app.py
```

### Testing Production Configuration

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn (production mode)
gunicorn app:app --bind 0.0.0.0:5000 --workers 2 --threads 4 --timeout 120
```

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check `requirements.txt` for correct package versions
   - Ensure Python version in `runtime.txt` is supported

2. **Application Crashes**:
   - Check Render logs for error messages
   - Verify environment variables are set correctly

3. **API Key Issues**:
   - Ensure `GEMINI_API_KEY` is set in Render environment variables
   - Check the API key is valid and has sufficient quota

4. **Static Files Not Loading**:
   - Verify file paths in templates are correct
   - Check that static files are included in repository

### Monitoring

- **Health Check**: `/health` endpoint returns application status
- **Logs**: View application logs in Render dashboard
- **Metrics**: Monitor CPU, memory, and response times in Render

## File Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── runtime.txt           # Python version specification
├── exercises.csv         # Exercise database
├── diet_data.csv         # Diet plan data
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML templates
│   ├── index.html
│   ├── diet.html
│   ├── chatbot.html
│   └── ...
└── DEPLOYMENT.md         # This file
```

## Support

If you encounter issues:
1. Check Render deployment logs
2. Verify all required files are in repository
3. Ensure environment variables are set correctly
4. Test locally with production configuration

For Render-specific issues, refer to [Render Documentation](https://render.com/docs).
