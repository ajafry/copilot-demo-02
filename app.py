import streamlit as st

from views import calculator, codegen_lab, home, password_generator, text_merge
from views.styles import inject_styles, render_footer

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="GitHub Copilot Demo",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Shared styles
# ---------------------------------------------------------------------------
inject_styles()

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
PAGE_HOME = "🏠 Home"
PAGE_CALCULATOR = "🧮 Calculator"
PAGE_CODEGEN = "💡 Code Generation Lab"
PAGE_TEXT_MERGE = "🔗 Text Merge"
PAGE_PASSWORD = "🔑 Password Generator"

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:1rem 0 .5rem">
            <span style="font-size:2.2rem;">✈️</span>
            <h3 style="margin:.25rem 0 0;font-weight:700;
                        background:linear-gradient(90deg,#58a6ff,#7d5fff);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                Copilot Demo
            </h3>
        </div>
        <hr style="border-color:#30363d">
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigate",
        [PAGE_HOME, PAGE_CALCULATOR, PAGE_CODEGEN, PAGE_TEXT_MERGE, PAGE_PASSWORD],
        label_visibility="collapsed",
    )

# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------
if page == PAGE_HOME:
    home.render()
elif page == PAGE_CALCULATOR:
    calculator.render()
elif page == PAGE_CODEGEN:
    codegen_lab.render()
elif page == PAGE_TEXT_MERGE:
    text_merge.render()
elif page == PAGE_PASSWORD:
    password_generator.render()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
render_footer()
