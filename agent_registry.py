import logging
import streamlit as st
import multipage_streamlit as mt
import yaml
from intro import introduction
from playground import chat_bot
from playground import image_inference
from playground import local_rag
from playground import document_inference
from playground import audio_inference
from skills import cran_generation, reply_engine, cran_business_loan
from skills import cheque_inference
from skills import quiz_generator, quizbot
from skills import audio_summarisation
from skills import feedback_classification
from skills import ppt_to_doc
from skills import label_scanner, marketing, compliance_checklist, stock_statements_agri, stock_statements_consumer
from skills import audio_summarisation_nodal
from skills.v2.reply_engine import reply_engine as reply_enginev2
from skills.v2.compliance_checklist import handler as compliance_checklist_v2_handler
from sura import app as sura_app
# from skills.aura.ui import brief_generator


def load_feature_config():
    """Load feature management configuration from YAML file"""
    try:
        with open('feature_config.yml', 'r') as file:
            config = yaml.safe_load(file)
            return config.get('feature_management', {}).get('agents', {})
    except FileNotFoundError:
        st.warning("Feature configuration file not found. All features will be available.")
        return {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing feature configuration: {e}")
        return {}


def get_current_user():
    """Get current user ID - you can modify this based on your authentication system"""
    # For now, using a simple session state approach
    # You can replace this with your actual user authentication logic
    if 'current_user' not in st.session_state:
        st.session_state.current_user = st.sidebar.selectbox(
            "Select User",
            ["user_123", "user_456", "user_789", "user_999"],
            index=0
        )
    return st.session_state.current_user


def is_feature_available_for_user(feature_name, user_id, feature_config):
    """Check if a feature is available for the current user"""
    if not feature_config:
        return True  # If no config, all features are available
    
    # Check if the feature exists in config and user has access
    if feature_name in feature_config:
        return user_id in feature_config[feature_name]
    
    return True  # If feature not in config, it's available to all


def main():
    global_settings()
    customize_styles()
    register_skills()


def register_skills():
    app = mt.Multipage()
    
    # Load feature configuration
    feature_config = load_feature_config()
    current_user = get_current_user()
    
    # Display current user in sidebar
    st.sidebar.markdown(f"**Current User:** {current_user}")
    
    # Always add introduction
    app.add(title="Introduction", introduction.run)
    
    # Add playground features (always available)
    app.add(title="Playground > Chat Bot", chat_bot.run)
    app.add(title="Playground > Document Inference", document_inference.run)
    app.add(title="Playground > Image Inference", image_inference.run)
    app.add(title="Playground > Audio Inference", audio_inference.run)
    app.add(title="Playground > Document QnA (RAG)", local_rag.run)
    
    # Add skills with feature management
    skill_mappings = [
        ("Skill > Cheque Inference", cheque_inference.run),
        ("Skill > Reply Engine(GRD)", reply_engine.run),
        ("Skill > Nodal: Meeting Minutes", audio_summarisation_nodal.run),
        ("Skill > Business Loan CRAN [Sample]", cran_business_loan.run),
        ("Skill > CIBIL Analyser [Sample]", cran_generation.run),
        ("Skill > Quiz Generator!", quiz_generator.run),
        ("Skill > QuizzBot!", quizbot.run),
        ("Skill > Audio: Meeting Minutes", audio_summarisation.run),
        ("Skill > Feedback Classification", feedback_classification.run),
        ("Skill > PPT to Doc", ppt_to_doc.run),
        ("Skill > Labels Scanner [Sample]", label_scanner.run),
        ("Skill > Marketing Pitch [Sample]", marketing.run),
        ("Skill > Compliance", compliance_checklist.run),
        ("Skill > Stocks_statements_Agri", stock_statements_agri.run),
        ("Skill > Stocks_statements_Consumer", stock_statements_consumer.run),
        ("Skill > Reply Engine V2 [Experimental]", reply_enginev2.run),
        ("Skill > Compliance Checklist V2 [Experimental]", compliance_checklist_v2_handler.run),
    ]
    
    for skill_title, skill_function in skill_mappings:
        if is_feature_available_for_user(skill_title, current_user, feature_config):
            app.add(title=skill_title, func=skill_function)
    
    app.run_selectbox()


def global_settings():
    st.set_page_config(page_title="Kotak AI Arena", layout="wide", initial_sidebar_state="expanded")


def customize_styles():
    st.markdown(
        """
        <style>
        .stAppDeployButton {
            display: none;
        }
        .stSelectbox{
            width: 300px;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
main()