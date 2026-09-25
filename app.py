import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# FAQ KNOWLEDGE BASE
# =========================================================

faq_data = {

    "codealpha": {
        "questions": [
            "What is CodeAlpha?",
            "Tell me about CodeAlpha",
            "What does CodeAlpha do?",
            "What is Code Alpha?",
            "Tell me about Code Alpha"
        ],
        "answer":
            "CodeAlpha is a technology company that provides "
            "internship and learning opportunities for students "
            "and aspiring developers."
    },

    "artificial_intelligence": {
        "questions": [
            "What is artificial intelligence?",
            "What is AI?",
            "Explain AI",
            "Explain artificial intelligence",
            "Tell me about artificial intelligence",
            "What does AI mean?",
            "Define AI"
        ],
        "answer":
            "Artificial Intelligence (AI) is a field of computer "
            "science that enables machines to perform tasks that "
            "normally require human intelligence."
    },

    "machine_learning": {
        "questions": [
            "What is machine learning?",
            "What is ML?",
            "Explain machine learning",
            "Explain ML",
            "Tell me about machine learning",
            "How does machine learning work?",
            "Define machine learning"
        ],
        "answer":
            "Machine Learning is a branch of Artificial Intelligence "
            "that allows computers to learn patterns from data and "
            "make predictions or decisions."
    },

    "python": {
        "questions": [
            "What is Python?",
            "What is Python programming?",
            "Tell me about Python",
            "Explain Python",
            "Why is Python used?",
            "What is Python language?",
            "Define Python"
        ],
        "answer":
            "Python is a popular high-level programming language "
            "known for its simple syntax and wide range of uses "
            "including web development, automation, data science "
            "and artificial intelligence."
    },

    "streamlit": {
        "questions": [
            "What is Streamlit?",
            "What is Streamlit used for?",
            "Explain Streamlit",
            "Tell me about Streamlit",
            "Why use Streamlit?",
            "How does Streamlit work?"
        ],
        "answer":
            "Streamlit is a Python framework used to quickly "
            "create interactive web applications, especially "
            "for data science and machine learning projects."
    },

    "chatbot": {
        "questions": [
            "What is a chatbot?",
            "What is chatbot?",
            "Explain chatbot",
            "Tell me about chatbots",
            "How does a chatbot work?",
            "What does chatbot mean?"
        ],
        "answer":
            "A chatbot is a software application that communicates "
            "with users through text or voice and provides automated "
            "responses."
    },

    "api": {
        "questions": [
            "What is an API?",
            "What does API mean?",
            "Explain API",
            "What is an application programming interface?",
            "How does an API work?",
            "Why are APIs used?"
        ],
        "answer":
            "API stands for Application Programming Interface. "
            "It allows different software applications to "
            "communicate and exchange data with each other."
    },

    "nlp": {
        "questions": [
            "What is natural language processing?",
            "What is NLP?",
            "Explain NLP",
            "What does NLP mean?",
            "Tell me about natural language processing",
            "How does NLP work?"
        ],
        "answer":
            "Natural Language Processing (NLP) is a field of "
            "Artificial Intelligence that enables computers to "
            "understand, process and analyze human language."
    },

    "deep_learning": {
        "questions": [
            "What is deep learning?",
            "Explain deep learning",
            "What is deep learning in AI?",
            "Tell me about deep learning",
            "How does deep learning work?",
            "What does deep learning mean?"
        ],
        "answer":
            "Deep Learning is a subset of Machine Learning that "
            "uses neural networks with multiple layers to learn "
            "complex patterns from large amounts of data."
    },

    "data_science": {
        "questions": [
            "What is data science?",
            "Explain data science",
            "What does data science mean?",
            "Tell me about data science",
            "What is data science used for?",
            "Define data science"
        ],
        "answer":
            "Data Science combines programming, statistics, "
            "mathematics and domain knowledge to extract useful "
            "insights from data."
    },

    "computer_vision": {
        "questions": [
            "What is computer vision?",
            "Explain computer vision",
            "What is CV in AI?",
            "Tell me about computer vision",
            "How does computer vision work?",
            "What does computer vision mean?"
        ],
        "answer":
            "Computer Vision is a field of Artificial Intelligence "
            "that enables computers to interpret and understand "
            "information from images and videos."
    },

    "learn_ai": {
        "questions": [
            "How can I learn artificial intelligence?",
            "How can I learn AI?",
            "How do I learn AI?",
            "How should I start learning AI?",
            "What should I study to learn AI?",
            "How can I become an AI developer?"
        ],
        "answer":
            "You can learn AI by starting with Python, mathematics, "
            "data processing and machine learning. After that, "
            "study neural networks and build practical AI projects."
    }
}


# =========================================================
# PREPARE QUESTIONS
# =========================================================

all_questions = []
question_to_topic = {}

for topic, data in faq_data.items():

    for question in data["questions"]:

        all_questions.append(question)

        question_to_topic[question] = topic


# =========================================================
# CREATE TF-IDF MODEL
# =========================================================

@st.cache_resource
def create_vectorizer():

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(all_questions)

    return vectorizer, vectors


vectorizer, question_vectors = create_vectorizer()


# =========================================================
# FIND BEST ANSWER
# =========================================================

def get_answer(user_question):

    user_question = user_question.lower().strip()

    if not user_question:
        return None, 0

    # Convert user question into TF-IDF vector
    user_vector = vectorizer.transform([user_question])

    # Calculate similarity
    similarities = cosine_similarity(
        user_vector,
        question_vectors
    )[0]

    # Get best matching question
    best_index = similarities.argmax()

    best_score = similarities[best_index]

    best_question = all_questions[best_index]

    best_topic = question_to_topic[best_question]

    # -----------------------------------------------------
    # EXTRA KEYWORD MATCHING
    # -----------------------------------------------------

    keyword_groups = {

        "artificial_intelligence": [
            "ai",
            "artificial intelligence"
        ],

        "machine_learning": [
            "machine learning",
            "ml"
        ],

        "deep_learning": [
            "deep learning"
        ],

        "python": [
            "python"
        ],

        "streamlit": [
            "streamlit"
        ],

        "chatbot": [
            "chatbot",
            "chat bot"
        ],

        "api": [
            "api",
            "application programming interface"
        ],

        "nlp": [
            "nlp",
            "natural language processing"
        ],

        "data_science": [
            "data science"
        ],

        "computer_vision": [
            "computer vision"
        ],

        "codealpha": [
            "codealpha",
            "code alpha"
        ]
    }

    # Check strong keyword matches
    for topic, keywords in keyword_groups.items():

        for keyword in keywords:

            if keyword in user_question:

                best_topic = topic
                best_score = max(best_score, 0.80)

                break


    # -----------------------------------------------------
    # CONFIDENCE CHECK
    # -----------------------------------------------------

    if best_score < 0.18:

        return (
            "Sorry 😕 I couldn't understand your question.\n\n"
            "Try asking about:\n"
            "• Artificial Intelligence\n"
            "• Machine Learning\n"
            "• Python\n"
            "• Streamlit\n"
            "• Chatbots\n"
            "• APIs\n"
            "• NLP\n"
            "• Deep Learning\n"
            "• Data Science\n"
            "• Computer Vision",
            best_score
        )

    return faq_data[best_topic]["answer"], best_score


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    color: #2563eb;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 17px;
    margin-bottom: 25px;
}

.user-message {
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border-radius: 18px;
    margin: 10px 0 10px 20%;
}

.bot-message {
    background: white;
    color: #1e293b;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 20% 10px 0;
    border: 1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">🤖 AI FAQ Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions and get answers using NLP, '
    'TF-IDF and Cosine Similarity'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 FAQ Topics")

    st.write("Try one of these questions:")

    selected_question = st.selectbox(
        "Select a question",
        ["Choose a question"] + all_questions
    )

    if st.button(
        "Ask Selected Question",
        use_container_width=True
    ):

        if selected_question != "Choose a question":

            answer, score = get_answer(
                selected_question
            )

            st.session_state.messages.append({
                "role": "user",
                "content": selected_question
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "score": score
            })

            st.rerun()

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                👤 <b>You</b><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="bot-message">
                🤖 <b>Bot</b><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# USER INPUT
# =========================================================

st.subheader("💬 Ask Your Question")

user_question = st.text_input(
    "Enter your question",
    placeholder="Example: Can you explain AI?"
)


# =========================================================
# ANSWER BUTTON
# =========================================================

if st.button(
    "🤖 Get Answer",
    type="primary",
    use_container_width=True
):

    if not user_question.strip():

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        with st.spinner(
            "🔍 Finding the best answer..."
        ):

            answer, score = get_answer(
                user_question
            )

        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "score": score
        })

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Built with Python • Streamlit • scikit-learn • "
    "TF-IDF • Cosine Similarity"
)