# AI Text Summarizer

A production-ready AI-powered text summarization service built with FastAPI, OpenAI GPT, and deployed on Google Cloud Run with automated CI/CD.

## Live Demo

- **Web App**: https://streamlit-app-[your-hash].us-central1.run.app
- **API Documentation**: https://vertex-ai-summarizer-1055382643810.us-central1.run.app/docs
- **Health Check**: https://vertex-ai-summarizer-1055382643810.us-central1.run.app/health

## Features

- **Real AI Summarization** - Powered by OpenAI GPT-3.5-turbo
- **Full-Stack GCP Deployment** - Both frontend and backend on Google Cloud Run
- **Production-Ready API** - FastAPI with automatic OpenAPI documentation
- **Interactive Web Interface** - Streamlit frontend deployed on GCP
- **Automated CI/CD** - GitHub Actions pipeline for both services
- **Serverless Architecture** - Auto-scaling with pay-per-use pricing
- **Cost Protection** - Built-in budget limits ($5/month)

## Tech Stack

- **Backend**: FastAPI, Python 3.9, OpenAI GPT-3.5-turbo
- **Frontend**: Streamlit (deployed on GCP Cloud Run)
- **Containerization**: Docker (multi-service deployment)
- **Cloud Platform**: Google Cloud Platform (Cloud Run, Container Registry, IAM)
- **CI/CD**: GitHub Actions with automated deployment
- **Monitoring**: Google Cloud Logging and monitoring

## GCP Services Used

- **Cloud Run** - Serverless containers for both API and frontend
- **Container Registry** - Docker image storage and versioning  
- **Cloud Build** - Integration with GitHub Actions
- **IAM** - Service account authentication and security
- **Cloud Logging** - Centralized monitoring across services

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- Google Cloud account
