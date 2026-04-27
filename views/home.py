"""Home page — hero banner and top-10 GitHub Copilot features."""

import streamlit as st

FEATURES_PER_COLUMN = 5

FEATURES = [
    (
        "Code Completions",
        "Real-time, context-aware code suggestions as you type — spanning single lines to entire functions.",
    ),
    (
        "Chat Assistance",
        "Ask Copilot questions in natural language and get explanations, refactors, or new code right in your editor.",
    ),
    (
        "Inline Chat",
        "Highlight code and invoke Copilot inline to fix bugs, add features, or refactor without leaving context.",
    ),
    (
        "Multi-Language Support",
        "Works across Python, JavaScript, TypeScript, Java, C#, Go, Ruby, and dozens more languages.",
    ),
    (
        "Test Generation",
        "Automatically generate unit tests for your functions with appropriate assertions and edge-case coverage.",
    ),
    (
        "Documentation Generation",
        "Produce docstrings, JSDoc comments, and README content from your code with a single prompt.",
    ),
    (
        "Code Review (Copilot in PRs)",
        "Get AI-powered review comments on pull requests to catch bugs and suggest improvements.",
    ),
    (
        "Terminal & CLI Assistance",
        "Describe what you need in plain English and Copilot suggests the right shell command.",
    ),
    (
        "Agent Mode",
        "Let Copilot autonomously plan, implement, and iterate on multi-step coding tasks end-to-end.",
    ),
    (
        "Context-Aware Workspace Understanding",
        "Copilot indexes your repository so suggestions respect project conventions, dependencies, and architecture.",
    ),
]


def render() -> None:
    """Render the home page with hero banner and feature cards."""
    # Hero banner
    st.markdown(
        """
        <div class="hero">
            <h1><i class="bi bi-github"></i>&nbsp; GitHub Copilot Features</h1>
            <p class="lead">
                Your AI pair-programmer — explore the top capabilities that make
                GitHub Copilot an essential developer tool.
            </p>
            <span class="badge rounded-pill text-bg-primary px-3 py-2"
                  style="font-size:.95rem;">
                <i class="bi bi-stars"></i>&nbsp; Powered by AI
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top-10 features in two columns
    col1, col2 = st.columns(2)
    for idx, (title, desc) in enumerate(FEATURES, 1):
        target = col1 if idx <= FEATURES_PER_COLUMN else col2
        with target:
            st.markdown(
                f"""
                <div class="feature-card d-flex flex-column">
                    <div class="d-flex align-items-center">
                        <span class="feature-num">{idx}</span>
                        <span class="feature-title">{title}</span>
                    </div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
