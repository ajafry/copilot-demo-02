"""Password Generator page — forge unbreakable passwords like Mjolnir forges thunder.

Uses the ``secrets`` module for cryptographically secure randomness because
``random`` is about as secure as the Death Star's thermal exhaust port.
"""

import secrets
import string

import streamlit as st

# ── Constants ── (a.k.a. The Infinity Stones of password policy) ──────

THANOS_MIN_LENGTH = 8          # Below this, passwords snap out of existence
GANDALF_MAX_LENGTH = 128       # You shall not pass this limit
GOLDILOCKS_DEFAULT_LENGTH = 16 # Just right
AVENGERS_MIN_CHAR_CLASSES = 3  # Assemble at least this many character types

LOWERCASE_SHIRE = string.ascii_lowercase   # Humble but essential
UPPERCASE_ASGARD = string.ascii_uppercase  # Elevated characters
DIGIT_MATRIX = string.digits               # Follow the white rabbit
SYMBOL_BATCAVE = string.punctuation        # Where the special ones hang out

# Characters that look alike and cause confusion — banished like Loki
AMBIGUOUS_EXILES = set("Il1O0")


def generate_password(
    length: int = GOLDILOCKS_DEFAULT_LENGTH,
    *,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """Generate a cryptographically secure password.

    One does not simply use ``random.choice()`` — we use ``secrets`` because
    security is no laughing matter (unlike this docstring).

    Guarantees at least one character from each enabled pool so the password
    meets common policy requirements. The final result is shuffled so
    required chars aren't bunched at the front like fans at a Marvel premiere.
    """
    if length < THANOS_MIN_LENGTH:
        raise ValueError(
            f"Password length must be at least {THANOS_MIN_LENGTH}. "
            "Anything shorter and Thanos snaps it out of existence."
        )
    if length > GANDALF_MAX_LENGTH:
        raise ValueError(
            f"You shall not pass {GANDALF_MAX_LENGTH} characters!"
        )

    pool = LOWERCASE_SHIRE
    required_chars: list[str] = []

    if use_uppercase:
        pool += UPPERCASE_ASGARD
    if use_digits:
        pool += DIGIT_MATRIX
    if use_symbols:
        pool += SYMBOL_BATCAVE

    if exclude_ambiguous:
        pool = "".join(ch for ch in pool if ch not in AMBIGUOUS_EXILES)

    # Guarantee at least one character from each enabled class
    # Like assembling the Avengers — you need at least one of each
    _guarantee_from(LOWERCASE_SHIRE, pool, exclude_ambiguous, required_chars)
    if use_uppercase:
        _guarantee_from(UPPERCASE_ASGARD, pool, exclude_ambiguous, required_chars)
    if use_digits:
        _guarantee_from(DIGIT_MATRIX, pool, exclude_ambiguous, required_chars)
    if use_symbols:
        _guarantee_from(SYMBOL_BATCAVE, pool, exclude_ambiguous, required_chars)

    # Fill the rest of the password — like padding the Hogwarts roster
    remaining = length - len(required_chars)
    filler = [secrets.choice(pool) for _ in range(remaining)]
    assembled = required_chars + filler

    # Shuffle so guaranteed chars aren't always in the opening scene
    secrets.SystemRandom().shuffle(assembled)
    return "".join(assembled)


def _guarantee_from(
    source: str,
    pool: str,
    exclude_ambiguous: bool,
    required_chars: list[str],
) -> None:
    """Pick one character from *source* that also exists in *pool*.

    Filters out ambiguous characters when requested — no imposters allowed,
    this isn't Among Us.
    """
    candidates = source
    if exclude_ambiguous:
        candidates = "".join(ch for ch in source if ch not in AMBIGUOUS_EXILES)
    if candidates:
        required_chars.append(secrets.choice(candidates))


def _password_strength(password: str) -> str:
    """Rate password strength like a Yelp review for your security.

    Returns one of: 'Weak 🟥', 'Fair 🟧', 'Strong 🟩', 'Unbreakable 💎'.
    """
    score = 0
    if len(password) >= THANOS_MIN_LENGTH:
        score += 1
    if len(password) >= GOLDILOCKS_DEFAULT_LENGTH:
        score += 1
    if any(ch in LOWERCASE_SHIRE for ch in password):
        score += 1
    if any(ch in UPPERCASE_ASGARD for ch in password):
        score += 1
    if any(ch in DIGIT_MATRIX for ch in password):
        score += 1
    if any(ch in SYMBOL_BATCAVE for ch in password):
        score += 1

    strength_levels = {
        (0, 2): "Weak 🟥",       # About as secure as a screen door on a submarine
        (3, 4): "Fair 🟧",       # You've seen better, you've seen worse
        (5, 5): "Strong 🟩",     # Now we're cooking with vibranium
        (6, 6): "Unbreakable 💎", # The One Password to rule them all
    }
    for (low, high), label in strength_levels.items():
        if low <= score <= high:
            return label
    return "Weak 🟥"


# ── Streamlit UI ──────────────────────────────────────────────────────


def render() -> None:
    """Render the Password Generator page. It's morphin' time."""
    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem"><i class="bi bi-key"></i>&nbsp; Password Generator</h1>
            <p>Forge cryptographically secure passwords worthy of protecting the Batcave.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_options, col_toggles = st.columns(2)
    with col_options:
        length = st.slider(
            "Password length",
            min_value=THANOS_MIN_LENGTH,
            max_value=GANDALF_MAX_LENGTH,
            value=GOLDILOCKS_DEFAULT_LENGTH,
            help=f"Min {THANOS_MIN_LENGTH}, max {GANDALF_MAX_LENGTH}. "
                 "Choose wisely — like picking a wand at Ollivanders.",
        )
    with col_toggles:
        use_uppercase = st.toggle("Include uppercase (A-Z)", value=True)
        use_digits = st.toggle("Include digits (0-9)", value=True)
        use_symbols = st.toggle("Include symbols (!@#…)", value=True)
        exclude_ambiguous = st.toggle(
            "Exclude ambiguous characters (I, l, 1, O, 0)",
            value=False,
            help="Remove lookalikes — no imposters, this isn't Among Us.",
        )

    if st.button("Generate Password", type="primary"):
        try:
            password = generate_password(
                length,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_ambiguous=exclude_ambiguous,
            )
            strength = _password_strength(password)
            st.success(f"**Strength:** {strength}")
            st.code(password, language=None)
        except ValueError as exc:
            st.error(str(exc))
