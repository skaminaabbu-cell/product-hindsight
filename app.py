import os
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from groq import Groq

from hindsight_connection import client
from github_client import get_issues


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing. Please add it to your .env file.")
    st.stop()

groq = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="ProductHindsight",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "demo_memory" not in st.session_state:
    st.session_state["demo_memory"] = ""

if "demo_question" not in st.session_state:
    st.session_state["demo_question"] = ""


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #080d1a;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    h1 {
        font-size: 46px !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 650 !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.07),
            rgba(255,255,255,0.025)
        );
        padding: 22px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }

    [data-testid="stMetricLabel"] {
        font-size: 14px;
    }

    [data-testid="stMetricValue"] {
        font-size: 30px;
        font-weight: 750;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 650;
        min-height: 45px;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .hero-card {
        padding: 28px;
        border-radius: 20px;
        background:
        linear-gradient(
            135deg,
            rgba(92,124,250,0.16),
            rgba(255,255,255,0.035)
        );
        border: 1px solid rgba(255,255,255,0.09);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 25px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .hero-text {
        font-size: 16px;
        opacity: 0.82;
        line-height: 1.6;
    }

    .memory-card {
        padding: 22px;
        border-radius: 18px;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        min-height: 130px;
    }

    .memory-title {
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .memory-text {
        opacity: 0.75;
        line-height: 1.5;
    }

    .learning-box {
        padding: 25px;
        border-radius: 18px;
        background: rgba(92,124,250,0.10);
        border: 1px solid rgba(92,124,250,0.25);
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_github_issues():
    """Safely retrieve GitHub issues."""
    try:
        issues = get_issues()

        if issues is None:
            return []

        return issues

    except Exception as e:
        st.error(f"GitHub connection error: {e}")
        return []


def recall_memory(query):
    """Safely retrieve information from Hindsight."""
    try:
        return client.recall(
            bank_id="product-hindsight",
            query=query
        )

    except Exception as e:
        st.error(f"Hindsight error: {e}")
        return None


def save_memory(content):
    """Safely save information to Hindsight."""
    try:
        client.retain(
            bank_id="product-hindsight",
            content=content
        )
        return True

    except Exception as e:
        st.error(f"Could not save memory: {e}")
        return False


def ask_groq(question, memory):
    """Send remembered evidence to Groq."""
    prompt = f"""
You are ProductHindsight, an AI product investigator.

Use ONLY the Hindsight memories provided below.

USER QUESTION:
{question}

HINDSIGHT MEMORIES:
{memory}

Provide:

1. Main findings
2. Repeated problems
3. Evidence from the memories
4. Possible patterns
5. What should be investigated next

Important rules:

- Do not invent facts.
- Only use information present in the memories.
- Clearly distinguish evidence from interpretation.
- Do not claim causation unless the evidence clearly supports it.
"""

    try:
        response = groq.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Groq error: {e}")
        return None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧠 ProductHindsight")

st.sidebar.caption(
    "AI product intelligence powered by persistent memory"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Hindsight Memory",
        "AI Investigator",
        "Memory Evolution",
        "🧠 Learning Demo"
    ]
)

st.sidebar.divider()

st.sidebar.caption("SYSTEM STATUS")

st.sidebar.success("GitHub Connected")
st.sidebar.success("Hindsight Connected")
st.sidebar.success("Groq AI Connected")


# =========================================================
# PAGE 1 — OVERVIEW
# =========================================================

if page == "Overview":

    st.title("🧠 ProductHindsight")

    st.markdown(
        """
        <div class="hero-card">

        <div class="hero-title">
        AI that learns from product history
        </div>

        <div class="hero-text">

        ProductHindsight transforms scattered product feedback
        into persistent organizational memory.

        It doesn't just answer:
        <b>"What is happening now?"</b>

        It also asks:

        <b>"Have we seen this before, what did we learn,
        and what happened afterwards?"</b>

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    issues = get_github_issues()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🐙 GitHub Issues",
            len(issues)
        )

    with col2:
        st.metric(
            "🧠 Memory",
            "ACTIVE"
        )

    with col3:
        st.metric(
            "🤖 AI Investigator",
            "ONLINE"
        )

    with col4:
        st.metric(
            "🔄 Learning",
            "ENABLED"
        )

    st.divider()

    st.subheader("💡 Why ProductHindsight?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="memory-card">

            <div class="memory-title">
            🧠 Persistent Memory
            </div>

            <div class="memory-text">
            ProductHindsight stores product knowledge
            beyond a single conversation.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="memory-card">

            <div class="memory-title">
            🔍 Historical Context
            </div>

            <div class="memory-text">
            New investigations can be compared
            against previously remembered evidence.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="memory-card">

            <div class="memory-title">
            🔄 Continuous Learning
            </div>

            <div class="memory-text">
            Investigation outcomes become knowledge
            that can be recalled later.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("🔄 Product Intelligence Pipeline")

    pipeline = pd.DataFrame(
        {
            "Stage": [
                "🐙 GitHub",
                "🧠 Hindsight",
                "🔍 Investigator",
                "💾 Memory",
                "🔄 Future Query"
            ],
            "What happens": [
                "Collect real product feedback",
                "Store persistent product knowledge",
                "Analyze problems with AI",
                "Remember investigation outcomes",
                "Use history for future investigations"
            ],
            "Status": [
                "CONNECTED",
                "ACTIVE",
                "ONLINE",
                "ACTIVE",
                "READY"
            ]
        }
    )

    st.dataframe(
        pipeline,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🐙 Recent Hyperswitch Issues")

    if issues:

        issue_data = []

        for issue in issues[:10]:

            issue_data.append(
                {
                    "Issue": issue.get(
                        "number",
                        issue.get("id", "N/A")
                    ),

                    "Title": issue.get(
                        "title",
                        "N/A"
                    ),

                    "Created": issue.get(
                        "created_at",
                        "N/A"
                    ),

                    "Updated": issue.get(
                        "updated_at",
                        "N/A"
                    )
                }
            )

        issue_df = pd.DataFrame(issue_data)

        st.dataframe(
            issue_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No GitHub issues were retrieved."
        )


# =========================================================
# PAGE 2 — HINDSIGHT MEMORY
# =========================================================

elif page == "Hindsight Memory":

    st.title("🧠 Hindsight Memory")

    st.markdown(
        """
        Search ProductHindsight's persistent memory.

        Ask questions about previous developer experiences,
        product problems, and investigation history.
        """
    )

    st.divider()

    query = st.text_input(
        "What should ProductHindsight remember?",
        "What problems have developers reported before?"
    )

    if st.button("🔍 Recall Memory"):

        if not query.strip():
            st.warning("Please enter a question.")
        else:

            with st.spinner(
                "Searching Hindsight memory..."
            ):

                memory = recall_memory(query)

            if memory is not None:

                st.success("Memory retrieved!")

                st.markdown(
                    "### 📚 Retrieved Product Knowledge"
                )

                st.write(memory)


# =========================================================
# PAGE 3 — AI INVESTIGATOR
# =========================================================

elif page == "AI Investigator":

    st.title("🔍 AI Product Investigator")

    st.markdown(
        """
        Ask a product question.

        ProductHindsight first retrieves relevant memory,
        then Groq analyzes that remembered evidence.
        """
    )

    st.divider()

    question = st.text_area(
        "What do you want to investigate?",
        "What problems are developers struggling with?"
    )

    if st.button("🚀 Investigate"):

        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner(
            "Searching product history..."
        ):

            memory = recall_memory(question)

        if memory is None:
            st.stop()

        with st.spinner(
            "AI is analyzing remembered evidence..."
        ):

            investigation_text = ask_groq(
                question,
                memory
            )

        if investigation_text is None:
            st.stop()

        st.success("Investigation complete!")

        st.markdown(
            "### 🧠 Investigation Result"
        )

        st.markdown(
            investigation_text
        )

        saved = save_memory(
            f"""
ProductHindsight Investigation

Question:
{question}

Findings:
{investigation_text}

This investigation was saved as product knowledge
for future investigations.
"""
        )

        if saved:
            st.success(
                "💾 Investigation saved to Hindsight memory!"
            )


# =========================================================
# PAGE 4 — MEMORY EVOLUTION
# =========================================================

elif page == "Memory Evolution":

    st.title("🧠 Memory Evolution")

    st.markdown(
        """
        Compare new product questions with knowledge
        remembered from previous investigations.
        """
    )

    st.divider()

    st.subheader("1️⃣ What did we learn before?")

    old_question = st.text_input(
        "Previous investigation",
        "What problems have developers reported in Hyperswitch?"
    )

    if st.button("🔎 Recall Previous Learning"):

        if not old_question.strip():
            st.warning("Please enter a question.")
        else:

            with st.spinner(
                "Searching Hindsight..."
            ):

                old_memory = recall_memory(
                    old_question
                )

            if old_memory is not None:

                st.success(
                    "Previous knowledge recalled!"
                )

                st.markdown(
                    "### 📚 Previous Knowledge"
                )

                st.write(old_memory)

    st.divider()

    st.subheader("2️⃣ Ask a new question")

    new_question = st.text_input(
        "New investigation",
        "Have we seen similar developer problems before?"
    )

    if st.button("🔄 Compare With Memory"):

        if not new_question.strip():
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner(
            "Comparing with product history..."
        ):

            memory = recall_memory(
                new_question
            )

        if memory is None:
            st.stop()

        with st.spinner(
            "AI is comparing remembered evidence..."
        ):

            prompt = f"""
You are ProductHindsight.

Compare the new investigation with
the knowledge stored in Hindsight.

NEW QUESTION:

{new_question}

PAST MEMORY:

{memory}

Explain:

1. What is already known
2. What appears similar
3. What appears different
4. What evidence supports the comparison
5. What should be investigated next

Important:

- Do not invent facts.
- Do not claim causation without evidence.
- Clearly separate evidence from interpretation.
"""

            try:

                response = groq.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                comparison = (
                    response
                    .choices[0]
                    .message
                    .content
                )

            except Exception as e:

                st.error(
                    f"Groq error: {e}"
                )

                st.stop()

        st.success(
            "Memory comparison complete!"
        )

        st.markdown(
            "### 🔄 Comparison Result"
        )

        st.markdown(comparison)

        st.info(
            """
            🧠 **Hindsight Learning**

            This investigation used remembered
            information from previous product history.
            """
        )


# =========================================================
# PAGE 5 — LEARNING DEMO
# =========================================================

elif page == "🧠 Learning Demo":

    st.title("🧠 ProductHindsight Learning Demo")

    st.markdown(
        """
        ### Watch the agent learn

        This page demonstrates the most important part
        of ProductHindsight: persistent memory.
        """
    )

    st.divider()

    st.subheader("1️⃣ Observe & Investigate")

    demo_question = st.text_input(
        "Investigation question",
        "What developer problems have appeared in Hyperswitch?"
    )

    if st.button("🔍 Run Investigation"):

        if not demo_question.strip():
            st.warning("Please enter a question.")
        else:

            with st.spinner(
                "Searching Hindsight memory..."
            ):

                memory = recall_memory(
                    demo_question
                )

            if memory is not None:

                st.success(
                    "Evidence retrieved from Hindsight!"
                )

                st.markdown("### 📚 Evidence")

                st.write(memory)

                st.session_state["demo_memory"] = str(
                    memory
                )

                st.session_state["demo_question"] = (
                    demo_question
                )

    st.divider()

    st.subheader("2️⃣ Remember What We Learned")

    if st.button("💾 Remember This Investigation"):

        investigation_text = st.session_state.get(
            "demo_memory",
            ""
        )

        saved_question = st.session_state.get(
            "demo_question",
            demo_question
        )

        if investigation_text:

            saved = save_memory(
                f"""
ProductHindsight Investigation

Question:
{saved_question}

Investigation Evidence:
{investigation_text}

Learning:
ProductHindsight stored this investigation
so future investigations can compare new
problems with previous product knowledge.
"""
            )

            if saved:

                st.success(
                    "🧠 Investigation saved to Hindsight memory!"
                )

        else:

            st.warning(
                "Run the investigation first."
            )

    st.divider()

    st.subheader("3️⃣ New Problem → Recall History")

    future_question = st.text_input(
        "Future investigation",
        "Have we seen this type of developer problem before?"
    )

    if st.button("🔄 Check Product History"):

        if not future_question.strip():
            st.warning("Please enter a question.")
        else:

            with st.spinner(
                "Checking what ProductHindsight remembers..."
            ):

                remembered = recall_memory(
                    future_question
                )

            if remembered is not None:

                st.success(
                    "Previous product knowledge found!"
                )

                st.markdown(
                    "### 🧠 What ProductHindsight Remembers"
                )

                st.write(remembered)

    st.divider()

    st.subheader("🔄 The Hindsight Learning Loop")

    learning_flow = pd.DataFrame(
        {
            "Step": [
                "1. Observe",
                "2. Investigate",
                "3. Remember",
                "4. New Problem",
                "5. Recall"
            ],

            "ProductHindsight": [
                "Collect real GitHub evidence",
                "AI analyzes the evidence",
                "Store the investigation in Hindsight",
                "A future product question appears",
                "Retrieve relevant historical knowledge"
            ]
        }
    )

    st.dataframe(
        learning_flow,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        <div class="learning-box">

        <b>🎯 Observe → Investigate → Remember → New Problem → Recall</b>

        <br><br>

        ProductHindsight carries product knowledge forward
        instead of treating every investigation as a completely
        new conversation.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "ProductHindsight • GitHub + Hindsight + Groq + Streamlit"
)
