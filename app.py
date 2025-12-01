import streamlit as st
import pandas as pd
from nltk.stem import PorterStemmer
import string
from nltk.corpus import stopwords
import pickle

# Set page config
st.set_page_config(page_title=" Spam Detector", page_icon="📧", layout="wide")

# Load resources
stop = stopwords.words("english")
with open("spam.pkl", 'rb') as obj1:
    dict1 = pickle.load(obj1)

def preprocess(text):
    data = ''.join([i for i in text.lower() if i not in string.punctuation])
    stemmer = PorterStemmer()
    data = [stemmer.stem(i) for i in data.split() if i not in stop]
    return " ".join(data)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    /* Global Reset */
    .stApp {
        background-color: #F6F8FC !important;
        font-family: 'Roboto', sans-serif !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F6F8FC !important;
        border-right: none !important;
    }
    .sidebar-item {
        padding: 10px 20px;
        border-radius: 5px 10px 10px 5px;
        color: #202124;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .sidebar-item:hover {
        background-color: #E8EAED;
    }
    .sidebar-item.active {
        background-color: #FCE8E6;
        color: #D93025;
    }

    /* Header */
    .header {
        display: flex;
        align-items: center;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    .logo {
        width: 32px;
        margin-right: 10px;
    }
    .header-title {
        font-size: 22px;
        color: #5f6368;
        font-weight: 400;
    }

    /* Compose Area (Main Card) */
    .compose-card {
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 1px 3px 0 rgba(60,64,67,0.3);
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border: none !important;
        border-bottom: 1px solid #E0E0E0 !important;
        border-radius: 0 !important;
        padding: 10px 0 !important;
        font-size: 16px !important;
        background-color: transparent !important;
    }
    .stTextInput > div > div > input:focus {
        border-bottom: 2px solid #1A73E8 !important;
        box-shadow: none !important;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #1A73E8 !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 8px 24px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-top: 20px !important;
    }
    .stButton > button:hover {
        background-color: #1557B0 !important;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15) !important;
    }

    /* Result Badge */
    .result-badge {
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        display: inline-block;
        margin-top: 10px;
    }
    .spam {
        background-color: #FCE8E6;
        color: #D93025;
    }
    .ham {
        background-color: #E6F4EA;
        color: #137333;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Layout
with st.sidebar:
    st.image("https://ssl.gstatic.com/ui/v1/icons/mail/rfr/logo_gmail_lockup_default_1x_r5.png", width=100)
    
    # Navigation
    selected_page = st.radio(
        "Navigation", 
        ["Demo", "Dataset info", "Explanation"], 
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div style="margin-top: 20px;">
        <a href="#" target="_blank" style="text-decoration: none;">
            <div class="sidebar-item">GitHub Repo</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Main Content
col1, col2 = st.columns([1, 8])

with col2:
    if selected_page == "Demo":
        # Header
        st.markdown("""
        <div class="header">
            <div class="header-title">Search in mail</div>
        </div>
        """, unsafe_allow_html=True)

        # Compose Interface
        st.markdown("### New Message")
        
        text = st.text_area("Message", height=200, placeholder="Type your message here...")
        
        col_actions, col_space = st.columns([1, 5])
        with col_actions:
            button = st.button("Send & Check")
        
        if button and text:
            clean = preprocess(text)
            vector = dict1['vectorizer'].transform([clean])
            res = dict1['model'].predict(vector)[0]

            if res == 'spam':
                st.error("Spam Detected")
                
                # Vibration logic
                st.markdown("""
                <script>
                    if (window.navigator && window.navigator.vibrate) {
                        window.navigator.vibrate(200);
                    }
                </script>
                """, unsafe_allow_html=True)
                
            else:
                st.success("Not Spam")
                
        elif button and not text:
            st.warning("Please enter a message body.")
            
    elif selected_page == "Dataset info":
        st.markdown("## SMS Spam Collection v.1")
        
        st.markdown("""
        ### 1. DESCRIPTION
        The SMS Spam Collection v.1 (hereafter the corpus) is a set of SMS tagged messages that have been collected for SMS Spam research. It contains one set of SMS messages in English of 5,574 messages, tagged acording being ham (legitimate) or spam.

        #### 1.1. Compilation
        This corpus has been collected from free or free for research sources at the Web:
        - A collection of between 425 SMS spam messages extracted manually from the Grumbletext Web site.
        - A list of 450 SMS ham messages collected from Caroline Tag's PhD Theses.
        - A subset of 3,375 SMS ham messages of the NUS SMS Corpus (NSC).
        - The amount of 1,002 SMS ham messages and 322 spam messages extracted from the SMS Spam Corpus v.0.1 Big.

        #### 1.2. Statistics
        There is one collection:
        - The SMS Spam Collection v.1 has a total of 4,827 SMS legitimate messages (86.6%) and a total of 747 (13.4%) spam messages.

        #### 1.3. Format
        The files contain one message per line. Each line is composed by two columns: one with label (ham or spam) and other with the raw text.
        """)
        
        # Display first 10 rows of dataset
        st.markdown("### First 10 Lines of Dataset")
        try:
            df = pd.read_csv("spam.csv", encoding='latin-1')
            st.table(df.head(10))
        except Exception as e:
            st.error(f"Error loading dataset: {e}")

        st.markdown("""
        ### 2. USAGE
        We offer a comprehensive study of this corpus in the following paper that is under review. This work presents a number of statistics, studies and baseline results for several machine learning methods.
        
        [1] Almeida, T.A., Gómez Hidalgo, J.M., Yamakami, A. Contributions to the study of SMS Spam Filtering: New Collection and Results. Proceedings of the 2011 ACM Symposium on Document Engineering (ACM DOCENG'11), Mountain View, CA, USA, 2011. (Under review)

        ### 3. ABOUT
        The corpus has been collected by Tiago Agostinho de Almeida and José María Gómez Hidalgo.
        We would like to thank Dr. Min-Yen Kan and his team for making the NUS SMS Corpus available.

        ### 4. LICENSE/DISCLAIMER
        The SMS Spam Collection v.1 is provided for free and with no limitations excepting:
        1. Tiago Agostinho de Almeida and José María Gómez Hidalgo hold the copyrigth (c) for the SMS Spam Collection v.1.
        2. No Warranty/Use At Your Risk.
        3. Limitation of Liability.
        """)
        
    elif selected_page == "Explanation":
        st.markdown("## How it Works")
        st.markdown("""
        This application uses a Machine Learning model to classify SMS messages as either **Spam** or **Ham** (Legitimate).
        
        ### The Process
        
        1.  **Preprocessing**:
            - The input text is converted to lowercase.
            - Punctuation is removed.
            - Stopwords (common words like "the", "is", "in") are removed.
            - Words are reduced to their root form using **Porter Stemmer** (e.g., "running" -> "run").
            
        2.  **Vectorization**:
            - The cleaned text is converted into a numerical format that the model can understand.
            
        3.  **Classification**:
            - A pre-trained Machine Learning model (loaded from `spam.pkl`) predicts whether the numerical vector represents a spam or ham message.
        """)
        
    st.markdown('</div>', unsafe_allow_html=True)