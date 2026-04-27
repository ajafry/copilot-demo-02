"""Text Merge page — combine two lines of text into a single line."""

import streamlit as st

SEPARATOR_DEFAULT = " "


def merge_lines(line1: str, line2: str, separator: str = SEPARATOR_DEFAULT) -> str:
    """Merge two lines of text into a single line joined by *separator*."""
    return f"{line1}{separator}{line2}"


def render() -> None:
    """Render the Text Merge page."""
    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem"><i class="bi bi-text-wrap"></i>&nbsp; Text Merge</h1>
            <p>Enter two lines of text and combine them into a single line.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        line1 = st.text_input("First line", placeholder="Enter the first line of text…")
    with col2:
        line2 = st.text_input("Second line", placeholder="Enter the second line of text…")

    separator = st.text_input(
        "Separator (between the two lines)",
        value=SEPARATOR_DEFAULT,
        help="Character(s) used to join the two lines. Defaults to a single space.",
    )

    if st.button("Merge", type="primary"):
        merged = merge_lines(line1, line2, separator)
        st.success(f"**Merged result:** {merged}")
        st.code(merged, language=None)
