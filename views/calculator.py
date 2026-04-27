"""Node-style on-screen calculator page."""

import streamlit as st

ALLOWED_CHARS = set("0123456789+-*/.() ")

BUTTON_ROWS = [
    [("C", "clr"), ("⌫", "bksp"), ("(", "num"), (")", "num")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("÷", "op")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("×", "op")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("−", "op")],
    [("0", "num"), (".", "num"), ("=", "eq"), ("+", "op")],
]

OPERATOR_MAP = {"÷": "/", "×": "*", "−": "-"}

COLUMNS_PER_ROW = 4


def _append(val: str) -> None:
    st.session_state.calc_expr += val
    st.session_state.calc_result = ""


def _clear() -> None:
    st.session_state.calc_expr = ""
    st.session_state.calc_result = ""


def _backspace() -> None:
    st.session_state.calc_expr = st.session_state.calc_expr[:-1]
    st.session_state.calc_result = ""


def _evaluate() -> None:
    expr = st.session_state.calc_expr
    if not expr or not all(ch in ALLOWED_CHARS for ch in expr):
        st.session_state.calc_result = "Error"
        return
    try:
        result = eval(expr, {"__builtins__": {}}, {})  # noqa: S307
        st.session_state.calc_result = str(result)
    except Exception:
        st.session_state.calc_result = "Error"


def render() -> None:
    """Render the node-style calculator page."""
    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem"><i class="bi bi-calculator"></i>&nbsp; Node Calculator</h1>
            <p>A clean, node-style calculator built entirely in Streamlit.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Session state init
    if "calc_expr" not in st.session_state:
        st.session_state.calc_expr = ""
    if "calc_result" not in st.session_state:
        st.session_state.calc_result = ""

    # Layout
    _, center, _ = st.columns([1, 2, 1])
    with center:
        display_text = st.session_state.calc_result or st.session_state.calc_expr or "0"
        st.markdown(
            f'<div class="calc-display">{display_text}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.calc_result and st.session_state.calc_expr:
            st.caption(f"Expression: `{st.session_state.calc_expr}`")

        for row in BUTTON_ROWS:
            cols = st.columns(COLUMNS_PER_ROW)
            for col, (label, kind) in zip(cols, row):
                with col:
                    if label == "C":
                        st.button(label, key=f"btn_{label}", on_click=_clear, use_container_width=True)
                    elif label == "⌫":
                        st.button(label, key=f"btn_{label}", on_click=_backspace, use_container_width=True)
                    elif label == "=":
                        st.button(label, key=f"btn_{label}", on_click=_evaluate, type="primary", use_container_width=True)
                    else:
                        actual = OPERATOR_MAP.get(label, label)
                        st.button(label, key=f"btn_{label}", on_click=_append, args=(actual,), use_container_width=True)
