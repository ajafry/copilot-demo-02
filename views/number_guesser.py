"""Number-guessing game page — "The answer is out there, Neo, and it's looking for you."

A configurable number-guessing game powered by Streamlit session state.
The oracle picks a secret integer; the player has a configurable number of
attempts to find it, guided by higher/lower hints after each wrong guess.
"""

import random

import streamlit as st

# ── Game Defaults ──────────────────────────────────────────────────────
# "These are not the defaults you're looking for." — Obi-Wan Kenobi

MATRIX_DEFAULT_MIN: int = 1          # There is no spoon, but there is a floor
MATRIX_DEFAULT_MAX: int = 100        # The One True Ceiling
YODA_DEFAULT_MAX_GUESSES: int = 10   # "Ten guesses, you have. Waste them, do not."
THANOS_ABSOLUTE_MIN_GUESSES: int = 1  # Perfectly balanced — as all things should be
GANDALF_ABSOLUTE_MIN_RANGE: int = 2   # You shall not have a range smaller than this

# ── Session State Keys ─────────────────────────────────────────────────

_SK_SECRET: str = "ng_secret_number"
_SK_MIN: str = "ng_range_min"
_SK_MAX: str = "ng_range_max"
_SK_MAX_GUESSES: str = "ng_max_guesses"
_SK_GUESSES_REMAINING: str = "ng_guesses_remaining"
_SK_GAME_OVER: str = "ng_game_over"
_SK_WIN: str = "ng_win"
_SK_HISTORY: str = "ng_guess_history"   # list of (guess, feedback) tuples
_SK_ERROR: str = "ng_input_error"
_SK_CONFIGURED: str = "ng_configured"   # True once the player locks in settings


# ── Result Literals ────────────────────────────────────────────────────

RESULT_CORRECT: str = "correct"   # "I am Iron Man." — Tony Stark
RESULT_TOO_HIGH: str = "too_high"  # "The eagle flies too high, Sam."
RESULT_TOO_LOW: str = "too_low"   # "Going deeper, Inception-style."


# ── Pure Logic (testable without Streamlit) ────────────────────────────


def conjure_the_number(range_min: int, range_max: int) -> int:
    """Pick a random secret integer between range_min and range_max (inclusive).

    Like the Sorting Hat — it knows the answer before you've even started guessing.

    Raises:
        ValueError: If range_min >= range_max (even Dumbledore needs a valid range).
    """
    if range_min >= range_max:
        raise ValueError(
            f"You shall not pass a range where min ({range_min}) >= max ({range_max})!"
        )
    return random.randint(range_min, range_max)  # noqa: S311 — not cryptographic


def evaluate_guess(player_guess: int, secret_number: int) -> str:
    """Compare the player's guess to the secret number and return a result string.

    Returns RESULT_CORRECT, RESULT_TOO_HIGH, or RESULT_TOO_LOW.
    "Do. Or do not. There is no 'close enough.'" — Yoda
    """
    if player_guess == secret_number:
        return RESULT_CORRECT
    if player_guess > secret_number:
        return RESULT_TOO_HIGH
    return RESULT_TOO_LOW


def validate_guess_input(
    raw_input: str,
    range_min: int,
    range_max: int,
) -> tuple[bool, str, int]:
    """Validate and parse the player's raw guess input.

    Returns (is_valid, error_message, parsed_int).
    The parsed_int is 0 when is_valid is False — handle accordingly, like Batman handles criminals.

    Args:
        raw_input: The raw string entered by the user.
        range_min: The inclusive lower bound of the valid range.
        range_max: The inclusive upper bound of the valid range.
    """
    stripped = raw_input.strip()
    if not stripped:
        return False, "You entered nothing. Even Thanos had a plan.", 0

    try:
        parsed = int(stripped)
    except ValueError:
        return False, f"'{stripped}' is not a number. This isn't The Price is Right.", 0

    if parsed < range_min or parsed > range_max:
        return (
            False,
            f"Out of range! Stick between {range_min} and {range_max}. "
            f"Even Icarus knew his limits (eventually).",
            0,
        )

    return True, "", parsed


def validate_game_config(
    range_min: int,
    range_max: int,
    max_guesses: int,
) -> tuple[bool, str]:
    """Validate the user-supplied game configuration before starting.

    Returns (is_valid, error_message).
    "With great configuration comes great responsibility." — Uncle Ben (probably)

    Args:
        range_min: Desired minimum of the number range.
        range_max: Desired maximum of the number range.
        max_guesses: Desired number of guesses allowed.
    """
    range_size = range_max - range_min
    if range_size < GANDALF_ABSOLUTE_MIN_RANGE:
        return (
            False,
            f"Range too small! Max must be at least {GANDALF_ABSOLUTE_MIN_RANGE} "
            f"above min. You shall not have a trivial range!",
        )
    if max_guesses < THANOS_ABSOLUTE_MIN_GUESSES:
        return (
            False,
            f"At least {THANOS_ABSOLUTE_MIN_GUESSES} guess required. "
            f"Even Thanos snapped once.",
        )
    return True, ""


def build_progress_emoji(guesses_remaining: int, max_guesses: int) -> str:
    """Return a visual health-bar of remaining guesses using emoji.

    Like Mario's lives counter — every one matters.
    """
    filled = guesses_remaining
    empty = max_guesses - guesses_remaining
    return "❤️" * filled + "🖤" * empty


# ── Session-State Helpers ──────────────────────────────────────────────


def _start_new_game(
    range_min: int,
    range_max: int,
    max_guesses: int,
) -> None:
    """Initialise session state for a brand-new game round.

    "Press START — insert coin." — Every arcade cabinet ever.
    """
    st.session_state[_SK_SECRET] = conjure_the_number(range_min, range_max)
    st.session_state[_SK_MIN] = range_min
    st.session_state[_SK_MAX] = range_max
    st.session_state[_SK_MAX_GUESSES] = max_guesses
    st.session_state[_SK_GUESSES_REMAINING] = max_guesses
    st.session_state[_SK_GAME_OVER] = False
    st.session_state[_SK_WIN] = False
    st.session_state[_SK_HISTORY] = []
    st.session_state[_SK_ERROR] = ""
    st.session_state[_SK_CONFIGURED] = True


def _reset_to_config() -> None:
    """Return to the configuration screen — "Let's start from the top." — Every heist movie."""
    st.session_state[_SK_CONFIGURED] = False
    st.session_state[_SK_GAME_OVER] = False
    st.session_state[_SK_WIN] = False
    st.session_state[_SK_HISTORY] = []
    st.session_state[_SK_ERROR] = ""


def _ensure_session_defaults() -> None:
    """Seed session keys that must exist before the config screen renders."""
    st.session_state.setdefault(_SK_CONFIGURED, False)
    st.session_state.setdefault(_SK_ERROR, "")
    st.session_state.setdefault(_SK_HISTORY, [])
    st.session_state.setdefault(_SK_GAME_OVER, False)
    st.session_state.setdefault(_SK_WIN, False)


def _handle_guess_submission() -> None:
    """Callback: validate and process the number submitted via the text input.

    "Every action has a consequence." — Morpheus (and also Newton)
    """
    raw = st.session_state.get("ng_guess_input", "")
    range_min: int = st.session_state[_SK_MIN]
    range_max: int = st.session_state[_SK_MAX]
    secret: int = st.session_state[_SK_SECRET]
    guesses_remaining: int = st.session_state[_SK_GUESSES_REMAINING]
    history: list[tuple[int, str]] = st.session_state[_SK_HISTORY]

    valid, error_msg, parsed_guess = validate_guess_input(raw, range_min, range_max)
    if not valid:
        st.session_state[_SK_ERROR] = error_msg
        st.session_state["ng_guess_input"] = ""
        return

    result = evaluate_guess(parsed_guess, secret)
    new_remaining = guesses_remaining - 1
    history.append((parsed_guess, result))

    st.session_state[_SK_HISTORY] = history
    st.session_state[_SK_GUESSES_REMAINING] = new_remaining
    st.session_state[_SK_ERROR] = ""
    st.session_state["ng_guess_input"] = ""

    if result == RESULT_CORRECT:
        st.session_state[_SK_WIN] = True
        st.session_state[_SK_GAME_OVER] = True
    elif new_remaining <= 0:
        st.session_state[_SK_GAME_OVER] = True


# ── Streamlit Render ───────────────────────────────────────────────────


def _render_config_screen() -> None:
    """Render the game configuration form.

    "Every great game starts with a settings screen." — Every gamer ever
    """
    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem">🔢&nbsp; Number Guesser</h1>
            <p>Configure your quest. The Oracle has chosen a number — can you find it
            before your guesses run out? "The answer is out there, Neo." — Morpheus</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("⚙️ Game Settings")
    st.caption("Set your range and guess limit, then let the games begin!")

    col1, col2, col3 = st.columns(3)

    with col1:
        range_min = st.number_input(
            "Minimum number",
            value=MATRIX_DEFAULT_MIN,
            step=1,
            key="ng_cfg_min",
            help="The floor. Even Frodo had a starting point.",
        )

    with col2:
        range_max = st.number_input(
            "Maximum number",
            value=MATRIX_DEFAULT_MAX,
            step=1,
            key="ng_cfg_max",
            help="The ceiling. The One True Upper Bound.",
        )

    with col3:
        max_guesses = st.number_input(
            "Number of guesses",
            value=YODA_DEFAULT_MAX_GUESSES,
            min_value=THANOS_ABSOLUTE_MIN_GUESSES,
            step=1,
            key="ng_cfg_guesses",
            help="How many attempts you get. Choose wisely, young Padawan.",
        )

    error_msg = st.session_state.get(_SK_ERROR, "")
    if error_msg:
        st.error(error_msg)

    if st.button("🚀 Start Game", type="primary"):
        valid, cfg_error = validate_game_config(
            int(range_min), int(range_max), int(max_guesses)
        )
        if not valid:
            st.session_state[_SK_ERROR] = cfg_error
            st.rerun()
        else:
            st.session_state[_SK_ERROR] = ""
            _start_new_game(int(range_min), int(range_max), int(max_guesses))
            st.rerun()


def _render_game_screen() -> None:
    """Render the active guessing game UI.

    "Let's get down to business." — Mulan (the General, obviously)
    """
    range_min: int = st.session_state[_SK_MIN]
    range_max: int = st.session_state[_SK_MAX]
    max_guesses: int = st.session_state[_SK_MAX_GUESSES]
    guesses_remaining: int = st.session_state[_SK_GUESSES_REMAINING]
    game_over: bool = st.session_state[_SK_GAME_OVER]
    player_won: bool = st.session_state[_SK_WIN]
    history: list[tuple[int, str]] = st.session_state[_SK_HISTORY]
    error_msg: str = st.session_state[_SK_ERROR]
    secret: int = st.session_state[_SK_SECRET]

    st.markdown(
        f"""
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem">🔢&nbsp; Number Guesser</h1>
            <p>Guess the number between <strong>{range_min}</strong> and
            <strong>{range_max}</strong>.
            You have <strong>{max_guesses}</strong> guesses total.
            "May the odds be ever in your favour." — Effie Trinket</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown("### 💗 Lives Remaining")
        st.markdown(build_progress_emoji(guesses_remaining, max_guesses))
        st.markdown(f"**{guesses_remaining} / {max_guesses} guesses left**")
        st.markdown(f"**Range:** `{range_min}` – `{range_max}`")

    with right_col:
        # ── End states ─────────────────────────────────────────────────
        if game_over:
            if player_won:
                guesses_used = max_guesses - guesses_remaining
                st.success(
                    f"🎉 **YOU FOUND IT!** The number was **{secret}**. "
                    f"You needed {guesses_used} guess(es). "
                    f"'You're a wizard, Harry!' — Hagrid"
                )
            else:
                st.error(
                    f"💀 **GAME OVER.** The number was **{secret}**. "
                    f"'Winter is coming' — and so was this loss. Better luck next time!"
                )

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("▶️ Play Again (same settings)", type="primary", key="ng_play_again"):
                    _start_new_game(range_min, range_max, max_guesses)
                    st.rerun()
            with btn_col2:
                if st.button("⚙️ Change Settings", key="ng_change_settings"):
                    _reset_to_config()
                    st.rerun()

        else:
            # ── Active game input ───────────────────────────────────────
            if error_msg:
                st.warning(error_msg)

            st.text_input(
                f"Enter your guess ({range_min}–{range_max}):",
                key="ng_guess_input",
                on_change=_handle_guess_submission,
                placeholder=f"A number between {range_min} and {range_max}, not Schrödinger's cat",
            )

        # ── Guess history ───────────────────────────────────────────────
        if history:
            st.markdown("### 📜 Guess History")
            # Show most-recent guess first — "Previously, on Lost…"
            for past_guess, result in reversed(history):
                if result == RESULT_CORRECT:
                    st.markdown(f"✅ **{past_guess}** — Correct! The Force is strong with you.")
                elif result == RESULT_TOO_HIGH:
                    st.markdown(f"⬇️ **{past_guess}** — Too high! Come back down, Icarus.")
                else:
                    st.markdown(f"⬆️ **{past_guess}** — Too low! Keep climbing, Mario.")


def render() -> None:
    """Render the Number Guesser game page.

    Routes to the config screen or the active game depending on session state.
    "Roads? Where we're going, we don't need roads." — Doc Brown
    (We do need session state though.)
    """
    _ensure_session_defaults()

    if not st.session_state.get(_SK_CONFIGURED, False):
        _render_config_screen()
    else:
        _render_game_screen()
