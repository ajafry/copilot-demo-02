"""Shared Bootstrap 5 styles and CSS injection for the application."""

import streamlit as st

BOOTSTRAP_CSS_URL = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
BOOTSTRAP_ICONS_URL = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"


def inject_styles() -> None:
    """Inject Bootstrap 5, Bootstrap Icons, and custom CSS into the page."""
    st.markdown(
        f"""
        <link href="{BOOTSTRAP_CSS_URL}" rel="stylesheet">
        <link href="{BOOTSTRAP_ICONS_URL}" rel="stylesheet">
        <style>
            /* ---- Global overrides ---- */
            .block-container {{ padding-top: 1rem; }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
            }}
            [data-testid="stSidebar"] * {{ color: #c9d1d9 !important; }}
            [data-testid="stSidebar"] .stRadio label:hover {{ color: #58a6ff !important; }}

            /* ---- Hero banner ---- */
            .hero {{
                background: linear-gradient(135deg, #0d1117 0%, #161b22 40%, #1a1e2e 100%);
                border: 1px solid #30363d;
                border-radius: 1rem;
                padding: 3rem 2rem;
                text-align: center;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
            }}
            .hero::before {{
                content: '';
                position: absolute;
                top: -50%; left: -50%;
                width: 200%; height: 200%;
                background: radial-gradient(circle at 30% 50%, rgba(88,166,255,.08) 0%, transparent 50%),
                            radial-gradient(circle at 70% 50%, rgba(125,95,255,.08) 0%, transparent 50%);
                animation: pulse 8s ease-in-out infinite alternate;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: .6; }}
                100% {{ transform: scale(1.1); opacity: 1; }}
            }}
            .hero > * {{ position: relative; z-index: 1; }}
            .hero h1 {{
                font-size: 2.8rem;
                font-weight: 800;
                background: linear-gradient(90deg, #58a6ff, #7d5fff, #ff79c6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .hero p {{ color: #8b949e; font-size: 1.15rem; }}

            /* ---- Feature cards ---- */
            .feature-card {{
                background: #0d1117;
                border: 1px solid #30363d;
                border-radius: .75rem;
                padding: 1.25rem 1.5rem;
                margin-bottom: .85rem;
                transition: transform .2s, border-color .2s;
            }}
            .feature-card:hover {{
                transform: translateY(-2px);
                border-color: #58a6ff;
            }}
            .feature-num {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 32px; height: 32px;
                border-radius: 50%;
                background: linear-gradient(135deg, #58a6ff, #7d5fff);
                color: #fff !important;
                font-weight: 700;
                font-size: .85rem;
                margin-right: .75rem;
                flex-shrink: 0;
            }}
            .feature-title {{ font-weight: 600; color: #e6edf3; font-size: 1.05rem; }}
            .feature-desc  {{ color: #8b949e; font-size: .92rem; margin: .25rem 0 0 2.75rem; }}

            /* ---- Calculator ---- */
            .calc-display {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: .5rem;
                padding: 1rem 1.25rem;
                text-align: right;
                font-family: 'Courier New', monospace;
                font-size: 1.8rem;
                color: #e6edf3;
                margin-bottom: 1rem;
                min-height: 60px;
                overflow-x: auto;
                word-break: break-all;
            }}

            /* ---- Factorial result ---- */
            .fact-result {{
                background: #0d1117;
                border: 1px solid #30363d;
                border-radius: .75rem;
                padding: 1.5rem;
                text-align: center;
            }}
            .fact-result h2 {{ color: #58a6ff; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the shared page footer."""
    st.markdown(
        """
        <hr style="border-color:#30363d;margin-top:3rem">
        <p style="text-align:center;color:#484f58;font-size:.85rem;">
            Built with <span style="color:#f85149;">♥</span> using
            <strong>Streamlit</strong> &amp; <strong>Bootstrap 5</strong> —
            GitHub Copilot Demo &copy; 2026
        </p>
        """,
        unsafe_allow_html=True,
    )
