import streamlit as st
from config import config
from ai_service import ai_service
from utils import data_manager

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .stApp {
        max-width: 100%;
        padding: 0.5rem;
    }
    
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 1.8rem;
        margin: 0;
    }
    
    .main-header p {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .content-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #f0f0f0;
    }
    
    .result-card {
        background: #f8f9ff;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-left: 4px solid #667eea;
    }
    
    .platform-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    
    /* Fix for mobile input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 16px !important;
        padding: 0.75rem !important;
    }
    
    .stButton > button {
        width: 100%;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Make selects mobile-friendly */
    .stSelectbox > div > div {
        font-size: 16px !important;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Responsive grid for mobile */
    @media (max-width: 640px) {
        .content-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .result-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <h1>{config.APP_ICON} {config.APP_TITLE}</h1>
    <p>{config.APP_DESCRIPTION}</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

# API Key input (sidebar or expander)
with st.expander("⚙️ Settings - API Configuration", expanded=False):
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-...",
        help="Enter your OpenAI API key. Get one from https://platform.openai.com/api-keys"
    )
    if api_key:
        st.session_state.api_key = api_key
        # Update the service with new API key
        ai_service.api_key = api_key
        st.success("✅ API Key set successfully!")

# Main input form
with st.form(key="content_form"):
    st.markdown("### 📝 Content Details")
    
    # Topic input
    topic = st.text_input(
        "Content Topic",
        placeholder="e.g., အိမ်တွင်းလေ့ကျင့်ခန်း / Home workout tips",
        help="What is your content about?"
    )
    
    # Platform selection
    platform = st.selectbox(
        "Platform",
        options=config.PLATFORMS,
        index=config.PLATFORMS.index(config.DEFAULT_PLATFORM)
    )
    
    # Audience input
    audience = st.text_input(
        "Target Audience",
        placeholder="e.g., အိမ်ရှင်မများ / Housewives, ကျောင်းသား/ကျောင်းသူများ / Students",
        help="Who is your target audience?"
    )
    
    # Style selection
    style = st.selectbox(
        "Content Style",
        options=config.STYLES,
        index=config.STYLES.index(config.DEFAULT_STYLE)
    )
    
    # Language selection
    language = st.selectbox(
        "Language",
        options=config.LANGUAGES,
        index=config.LANGUAGES.index(config.DEFAULT_LANGUAGE)
    )
    
    # Generate button
    generate_btn = st.form_submit_button("🚀 Generate Content", use_container_width=True)

# Generate content when form is submitted
if generate_btn and topic:
    with st.spinner("🎬 Generating your content... Please wait."):
        # Generate all content types
        try:
            ideas = ai_service.generate_ideas(topic, platform, audience, style, language)
            hooks = ai_service.generate_hooks(topic, platform, style, language)
            script = ai_service.generate_script(topic, platform, audience, style, language)
            captions = ai_service.generate_captions(topic, platform, style, language)
            hashtags = ai_service.generate_hashtags(topic, platform, language)
            
            # Store in session state
            st.session_state.generated_content = {
                'topic': topic,
                'platform': platform,
                'audience': audience,
                'style': style,
                'language': language,
                'ideas': ideas,
                'hooks': hooks,
                'script': script,
                'captions': captions,
                'hashtags': hashtags
            }
            
            # Save to history
            data_manager.add_entry(st.session_state.generated_content)
            
        except Exception as e:
            st.error(f"❌ Error generating content: {str(e)}")

# Display generated content
if st.session_state.generated_content:
    content = st.session_state.generated_content
    
    # Show current context
    st.markdown(f"""
    <div class="content-card">
        <strong>📌 Current Context:</strong><br>
        Topic: {content['topic']}<br>
        Platform: {content['platform']}<br>
        Audience: {content['audience']}<br>
        Style: {content['style']}<br>
        Language: {content['language']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display results in tabs or accordion
    tabs = st.tabs(["💡 Ideas", "🎣 Hooks", "🎬 Script", "📝 Captions", "🏷️ Hashtags"])
    
    with tabs[0]:
        st.markdown("### 💡 Content Ideas")
        st.markdown(f"""
        <div class="result-card">
            {content['ideas']}
        </div>
        """, unsafe_allow_html=True)
        
        # Copy button
        if st.button("📋 Copy Ideas", key="copy_ideas"):
            st.write("✅ Copied to clipboard!")
            # In Streamlit, we need to use st.write with JavaScript
            st.write(
                f'<script>navigator.clipboard.writeText(`{content["ideas"]}`)</script>',
                unsafe_allow_html=True
            )
    
    with tabs[1]:
        st.markdown("### 🎣 Attention-Grabbing Hooks")
        st.markdown(f"""
        <div class="result-card">
            {content['hooks']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy Hooks", key="copy_hooks"):
            st.write("✅ Copied to clipboard!")
            st.write(
                f'<script>navigator.clipboard.writeText(`{content["hooks"]}`)</script>',
                unsafe_allow_html=True
            )
    
    with tabs[2]:
        st.markdown("### 🎬 Video Script")
        st.markdown(f"""
        <div class="result-card">
            {content['script']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy Script", key="copy_script"):
            st.write("✅ Copied to clipboard!")
            st.write(
                f'<script>navigator.clipboard.writeText(`{content["script"]}`)</script>',
                unsafe_allow_html=True
            )
    
    with tabs[3]:
        st.markdown("### 📝 Captions")
        st.markdown(f"""
        <div class="result-card">
            {content['captions']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy Captions", key="copy_captions"):
            st.write("✅ Copied to clipboard!")
            st.write(
                f'<script>navigator.clipboard.writeText(`{content["captions"]}`)</script>',
                unsafe_allow_html=True
            )
    
    with tabs[4]:
        st.markdown("### 🏷️ Hashtags")
        st.markdown(f"""
        <div class="result-card">
            {content['hashtags']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy Hashtags", key="copy_hashtags"):
            st.write("✅ Copied to clipboard!")
            st.write(
                f'<script>navigator.clipboard.writeText(`{content["hashtags"]}`)</script>',
                unsafe_allow_html=True
            )
    
    # Export buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.generated_content = {}
            st.rerun()
    
    with col2:
        if st.button("📊 View History", use_container_width=True):
            st.session_state.show_history = not st.session_state.get('show_history', False)
    
    with col3:
        if st.button("💾 Save to History", use_container_width=True):
            st.success("✅ Content saved to history!")

# History section
if st.session_state.get('show_history', False):
    st.markdown("---")
    st.markdown("### 📊 Content History")
    
    history = data_manager.get_history(limit=10)
    if history:
        for idx, entry in enumerate(history, 1):
            with st.expander(f"{idx}. {entry.get('topic', 'Untitled')} - {entry.get('timestamp', '')[:10]}"):
                st.markdown(f"**Topic:** {entry.get('topic', 'N/A')}")
                st.markdown(f"**Platform:** {entry.get('platform', 'N/A')}")
                st.markdown(f"**Style:** {entry.get('style', 'N/A')}")
                st.markdown(f"**Language:** {entry.get('language', 'N/A')}")
                if st.button(f"Load #{idx}", key=f"load_{idx}"):
                    st.session_state.generated_content = entry
                    st.rerun()
        
        if st.button("🗑️ Clear History"):
            data_manager.clear_history()
            st.success("History cleared!")
            st.rerun()
    else:
        st.info("No history available. Generate some content to get started!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem 0;">
    <p>Made with ❤️ for Myanmar Content Creators</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        Built with Streamlit | AI Content Creator Assistant
    </p>
</div>
""", unsafe_allow_html=True)
