"""Code Generation Lab — live demo of Copilot inline code generation.

Open this file in VS Code and use Copilot to replace each `pass` statement
with a real implementation. Then refresh the Streamlit app to see results.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# Stub functions — let Copilot generate the bodies during the live demo
# ---------------------------------------------------------------------------

def reverse_string(text: str) -> str:
    """Return the reverse of the given string."""
    pass


def is_palindrome(text: str) -> bool:
    """Check if text reads the same forwards and backwards.

    Ignore case and non-alphanumeric characters.
    """
    pass


def fizzbuzz(n: int) -> list[str]:
    """Return a list of FizzBuzz results from 1 to n.

    - Multiples of 3 → 'Fizz'
    - Multiples of 5 → 'Buzz'
    - Multiples of both → 'FizzBuzz'
    - Otherwise → the number as a string
    """
    pass


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    pass


def count_vowels(text: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in the given text.

    Case-insensitive.
    """
    pass


def find_max(numbers: list[int]) -> int:
    """Return the largest number in the list without using the built-in max()."""
    pass


# ---------------------------------------------------------------------------
# Page rendering
# ---------------------------------------------------------------------------

FIZZBUZZ_DEFAULT = 15
CELSIUS_DEFAULT = 100.0


def _try_call(func, *args):
    """Call func and return its result, or an error message if it fails."""
    try:
        result = func(*args)
        if result is None:
            return "⏳ *Not implemented yet — replace `pass` with real code!*"
        return result
    except Exception as exc:
        return f"⚠️ Error: {exc}"


def render() -> None:
    """Render the Code Generation Lab page."""
    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem">
                <i class="bi bi-braces-asterisk"></i>&nbsp; Code Generation Lab
            </h1>
            <p>
                Open <code>views/codegen_lab.py</code> in VS Code, place your cursor
                after each docstring, delete <code>pass</code>, and let
                <strong>GitHub Copilot</strong> generate the implementation.
                Then refresh this page to see the results!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- 1. Reverse a String ----
    st.markdown("### 1. Reverse a String")
    text_input = st.text_input("Enter text to reverse", value="GitHub Copilot")
    st.write("**Result:**", _try_call(reverse_string, text_input))
    st.divider()

    # ---- 2. Palindrome Check ----
    st.markdown("### 2. Palindrome Check")
    pal_input = st.text_input("Enter text to check", value="A man a plan a canal Panama")
    st.write("**Is palindrome:**", _try_call(is_palindrome, pal_input))
    st.divider()

    # ---- 3. FizzBuzz ----
    st.markdown("### 3. FizzBuzz")
    fb_input = st.number_input("Generate FizzBuzz up to n", min_value=1, value=FIZZBUZZ_DEFAULT, step=1)
    result = _try_call(fizzbuzz, int(fb_input))
    if isinstance(result, list):
        st.write("**Result:**", ", ".join(result))
    else:
        st.write("**Result:**", result)
    st.divider()

    # ---- 4. Celsius to Fahrenheit ----
    st.markdown("### 4. Celsius to Fahrenheit")
    c_input = st.number_input("Degrees Celsius", value=CELSIUS_DEFAULT, step=0.1)
    st.write("**Fahrenheit:**", _try_call(celsius_to_fahrenheit, c_input))
    st.divider()

    # ---- 5. Count Vowels ----
    st.markdown("### 5. Count Vowels")
    vowel_input = st.text_input("Enter text to count vowels", value="GitHub Copilot is amazing")
    st.write("**Vowel count:**", _try_call(count_vowels, vowel_input))
    st.divider()

    # ---- 6. Find Max ----
    st.markdown("### 6. Find Max")
    max_input = st.text_input("Enter numbers separated by commas", value="42, 17, 93, 8, 61, 25")
    try:
        nums = [int(x.strip()) for x in max_input.split(",") if x.strip()]
        st.write("**Largest number:**", _try_call(find_max, nums))
    except ValueError:
        st.error("Please enter valid integers separated by commas.")
