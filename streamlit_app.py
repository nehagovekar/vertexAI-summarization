import streamlit as st
import requests
import json

# Configure the page
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Your API URL
#API_URL = "http://localhost:8000"
API_URL = "https://vertex-ai-summarizer-1055382643810.us-central1.run.app"

# Title and description
st.title("🤖 AI Text Summarizer")
st.markdown("### Powered by OpenAI GPT")
st.markdown("Transform long text into concise, meaningful summaries with the power of AI!")

# Sidebar for settings
st.sidebar.header("⚙️ Settings")
max_length = st.sidebar.slider(
    "Maximum Summary Length (words)",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

# API status check
with st.sidebar:
    st.markdown("---")
    if st.button("🔍 Check API Status"):
        try:
            response = requests.get(f"{API_URL}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ API is online!")
                st.info(f"AI Mode: {data.get('ai', 'unknown')}")
            else:
                st.error("❌ API is having issues")
        except Exception as e:
            st.error(f"❌ Cannot reach API: {str(e)}")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input Text")
    
    # Text input options
    input_method = st.radio(
        "Choose input method:",
        ["Type/Paste Text", "Sample Document", "Sample Achievement Summary"]
    )
    
    if input_method == "Type/Paste Text":
        user_text = st.text_area(
            "Enter your text to summarize:",
            height=300,
            placeholder="Paste your article, document, or any long text here...\n\nMinimum 50 characters required.",
            help="Enter at least 50 characters for the AI to generate a meaningful summary."
        )
    elif input_method == "Sample Document":
        # Sample document
        sample_text = """Media playback is not supported on this device. The QPR striker scored on his home debut to boost his hopes of making the squad for the Euro 2016 finals. "Conor has strength, power and composure - he looks like he is going to be an asset for us," said O'Neill. "It's a great achievement to go unbeaten in 10 games and now we just want to build on it." Washington struck his first goal for Northern Ireland before the break, while Roy Carroll kept out Milivoje Novakovic's penalty in the second half. The team showed excellent defensive organization throughout the match and created several scoring opportunities. The manager praised the team's work ethic and commitment to the tactical plan. This victory continues their impressive unbeaten streak and builds momentum for upcoming fixtures."""
        
        user_text = st.text_area(
            "Sample document (you can edit this):",
            value=sample_text,
            height=300
        )
    else:
        # Your project achievement summary
        achievement_text = """My Vertex AI Summarizer Project represents a complete learning journey in modern cloud-native development. I successfully built and deployed a production-ready AI-powered text summarization service using cloud technologies, containerization, and automated deployment pipelines. This project transformed me from someone struggling with deployment issues to confidently managing enterprise-level applications. I mastered FastAPI for building REST APIs with automatic documentation, integrated AI services for natural language processing, implemented Docker containerization for application portability, deployed on Google Cloud Platform including Cloud Run and Container Registry, created automated GitHub Actions CI/CD pipelines, managed service accounts and authentication systems, and developed both backend APIs and frontend interfaces. The technical achievements include building a complete FastAPI application with multiple endpoints, implementing proper error handling and input validation, creating RESTful API design with clear request/response models, successfully deploying to Google Cloud Run serverless platform, configuring auto-scaling and resource allocation, integrating multiple AI services including OpenAI and Google AI, creating automated build and deployment workflows, managing secrets and credentials securely across environments, and solving complex debugging problems including authentication failures, container startup issues, and API integration challenges. This project taught me essential skills in cloud computing fundamentals, modern API development best practices, DevOps workflows and automation, project management and systematic problem-solving, and prepared me for advanced roles in AI and cloud development. The learning methodology included mastering error analysis and debugging techniques, developing effective research and documentation skills, building confidence to experiment with new technologies, and learning to distinguish between temporary fixes and proper architectural solutions. This complete system demonstrates real-world production deployment expertise and prepares me for career advancement in modern technology companies working on cloud-native AI applications."""
        
        user_text = st.text_area(
            "Your project achievement summary (you can edit this):",
            value=achievement_text,
            height=300
        )
    
    # Character count
    if user_text:
        char_count = len(user_text)
        word_count = len(user_text.split())
        if char_count < 50:
            st.warning(f"⚠️ Text is too short ({char_count} characters). Need at least 50 characters.")
        else:
            st.info(f"✅ Ready to summarize ({char_count} characters, ~{word_count} words)")

with col2:
    st.header("🎯 AI Summary")
    
    # Summarize button
    if st.button("✨ Generate Summary", type="primary", use_container_width=True):
        if not user_text:
            st.error("❌ Please enter some text to summarize!")
        elif len(user_text.strip()) < 50:
            st.error("❌ Text is too short! Please enter at least 50 characters.")
        else:
            # Show loading spinner
            with st.spinner("🤖 AI is analyzing your text..."):
                try:
                    # Make API call
                    payload = {
                        "text": user_text.strip(),
                        "max_length": max_length
                    }
                    
                    response = requests.post(
                        f"{API_URL}/summarize",
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display success metrics
                        original_length = len(user_text)
                        original_words = len(user_text.split())
                        summary_length = len(result["summary"])
                        summary_words = len(result["summary"].split())
                        compression_ratio = (1 - summary_length/original_length) * 100
                        
                        # Metrics
                        col_metric1, col_metric2, col_metric3 = st.columns(3)
                        with col_metric1:
                            st.metric("Original", f"{original_words} words")
                        with col_metric2:
                            st.metric("Summary", f"{summary_words} words")
                        with col_metric3:
                            st.metric("Compressed", f"{compression_ratio:.1f}%")
                        
                        # Summary result
                        st.success("✅ Summary generated successfully!")
                        st.markdown("### 📄 AI Summary:")
                        
                        # Display summary in a nice box
                        st.markdown(f"""
                        <div style="
                            background-color: #f0f2f6;
                            padding: 20px;
                            border-radius: 10px;
                            border-left: 5px solid #4CAF50;
                            margin: 10px 0;
                        ">
                            <p style="margin: 0; font-size: 16px; line-height: 1.6;">
                                {result['summary']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Additional info
                        ai_source = result.get('summary_source', 'unknown')
                        if ai_source == 'openai':
                            st.info("🚀 Powered by OpenAI GPT")
                        elif ai_source == 'mock':
                            st.warning("⚠️ Demo mode - using mock responses")
                        else:
                            st.info(f"🔧 Source: {ai_source}")
                        
                        # Download option
                        summary_text = f"""AI TEXT SUMMARIZER RESULTS
{'='*50}

ORIGINAL TEXT ({original_words} words):
{user_text}

{'='*50}

AI SUMMARY ({summary_words} words):
{result['summary']}

{'='*50}
Compression: {compression_ratio:.1f}%
AI Source: {ai_source}
Generated: {st.session_state.get('timestamp', 'Unknown')}
"""
                        
                        st.download_button(
                            label="📥 Download Summary",
                            data=summary_text,
                            file_name="ai_summary.txt",
                            mime="text/plain"
                        )
                        
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"❌ API Error: {error_detail}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏰ Request timed out. The text might be too long or the API is busy.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to the API. Please check if the service is running.")
                except Exception as e:
                    st.error(f"💥 Unexpected error: {str(e)}")

# Footer section
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("### 🚀 Quick Actions")
    if st.button("🔄 Clear All"):
        st.rerun()

with col_footer2:
    st.markdown("### 📊 API Resources")
    st.markdown(f"[View API Documentation]({API_URL}/docs)")
    st.markdown(f"[Health Check]({API_URL}/health)")

with col_footer3:
    st.markdown("### ℹ️ About")
    st.markdown("Built with FastAPI + OpenAI + Streamlit")
    st.markdown("Deployed on Google Cloud Run")

# Usage instructions in expandable section
with st.expander("📖 How to Use This App"):
    st.markdown("""
    ### 🎯 Getting Started
    1. **Choose Input Method**: Select how you want to provide text
        - Type/paste your own text
        - Use the sample sports document
        - Try your project achievement summary
    
    2. **Adjust Settings**: Use the sidebar to set summary length (10-500 words)
    
    3. **Generate Summary**: Click the "Generate Summary" button
    
    4. **Review Results**: See compression metrics and AI-generated summary
    
    5. **Download**: Save your results as a text file
    
    ### 💡 Tips for Best Results
    - **Longer texts** (200+ words) generally produce better summaries
    - **Structured content** like articles work better than random text
    - **Try different summary lengths** to find what works best for your use case
    - **Check API status** if you encounter issues
    
    ### 🔧 Technical Details
    - **AI Model**: OpenAI GPT-3.5-turbo
    - **Cost**: ~$0.002 per 1000 words
    - **Response Time**: Usually 2-5 seconds
    - **Max Input**: No hard limit, but longer texts take more time
    """)

# Add custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.25);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    
    .stExpander {
        border: 1px solid #e1e5e9;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)