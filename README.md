AI Text Summarizer 🤖
A production-ready AI-powered text summarization service built with FastAPI, OpenAI GPT, and deployed on Google Cloud Run with automated CI/CD.
🚀 Live Demo

Web App: https://vertexai-summarization-kpqtxt7dijchuzpd3tba3t.streamlit.app/
API Documentation: https://vertex-ai-summarizer-1055382643810.us-central1.run.app/docs
Health Check: https://vertex-ai-summarizer-1055382643810.us-central1.run.app/health

✨ Features

Real AI Summarization - Powered by OpenAI GPT-3.5-turbo
Production-Ready API - FastAPI with automatic OpenAPI documentation
Beautiful Web Interface - Streamlit frontend for easy interaction
Automated Deployment - CI/CD pipeline with GitHub Actions
Cloud-Native - Containerized and deployed on Google Cloud Run
Cost Protection - Built-in budget limits to prevent runaway costs
Scalable Architecture - Auto-scaling based on demand

🛠️ Tech Stack

Backend: FastAPI, Python 3.9
AI/ML: OpenAI GPT-3.5-turbo API
Frontend: Streamlit
Containerization: Docker
Cloud Platform: Google Cloud Run
CI/CD: GitHub Actions
Authentication: Google Cloud IAM

🏗️ Architecture
User → Streamlit UI → FastAPI Backend → OpenAI API → AI Summary
                            ↓
                    Google Cloud Run (Auto-scaling)
                            ↓
                    GitHub Actions (CI/CD)
🚀 Quick Start
Prerequisites

Python 3.9+
OpenAI API key
Google Cloud account (for deployment)

Local Development

Clone the repository
git clone https://github.com/nehagovekar/vertexAI-summarization.git
cd vertexAI-summarization

Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Set up environment variables
# Create .env file
echo "OPENAI_API_KEY=your-openai-key-here" > .env
echo "PROJECT_ID=your-project-id" >> .env

Run the API
python src/server/main.py

Run the Streamlit app
streamlit run streamlit_app.py


📝 API Usage
Summarize Text
curl -X POST "https://vertex-ai-summarizer-1055382643810.us-central1.run.app/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "max_length": 100
  }'
Check API Health
curl https://vertex-ai-summarizer-1055382643810.us-central1.run.app/health
Budget Status
curl https://vertex-ai-summarizer-1055382643810.us-central1.run.app/budget
🔧 Configuration
Environment Variables

OPENAI_API_KEY - Your OpenAI API key
PROJECT_ID - Google Cloud project ID
LOCATION - Google Cloud region (default: us-central1)

Budget Limits
The API includes built-in cost protection:

OpenAI Account Limit: $5.00/month (set in OpenAI dashboard)
Request Tracking: Monitors usage and estimated costs
Automatic Cutoff: Stops API when budget is reached

🚀 Deployment
Automatic Deployment
Every push to main triggers automatic deployment via GitHub Actions:
git add .
git commit -m "Your changes"
git push origin main
Manual Deployment
# Build and deploy to Google Cloud Run
gcloud run deploy vertex-ai-summarizer \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
  
📊 Monitoring

API Logs: Google Cloud Console → Cloud Run → Logs
Usage Tracking: /budget endpoint
Health Monitoring: /health endpoint
OpenAI Usage: OpenAI Dashboard → Usage

🔒 Security

API Keys: Stored securely in GitHub Secrets
Service Accounts: Google Cloud IAM with minimal permissions
Rate Limiting: Built-in request throttling
Input Validation: Comprehensive request validation

💰 Cost Optimization

Serverless: Pay only for actual usage
Auto-scaling: Scales to zero when not in use
Budget Limits: Automatic cost protection
Efficient API: Optimized for minimal OpenAI token usage

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

