"""Hangman game page — "It's a trap!" (Admiral Ackbar, probably, when he ran out of guesses).

A self-contained Hangman game powered by Streamlit session state. Features a
curated word bank, 7-stage ASCII gallows, a hint portal that opens after 3
wrong guesses, and single-letter input validation worthy of Hermione Granger.
"""

import random

import streamlit as st

# ── Word Bank ─────────────────────────────────────────────────────────
# 30+ words pulled from across the multiverse

THE_ONE_RING_WORD_BANK: list[str] = [
    # Middle-earth crew
    "wizard",
    "fellowship",
    "hobbit",
    "dragon",
    "elf",
    "dwarf",
    # Avengers assemble
    "vibranium",
    "gauntlet",
    "shield",
    "multiverse",
    "infinity",
    "spider",
    # A long time ago in a galaxy far, far away…
    "lightsaber",
    "jedi",
    "force",
    "hyperdrive",
    "republic",
    "rebellion",
    # Pokémon — gotta catch 'em all
    "pikachu",
    "charizard",
    "evolution",
    "trainer",
    "legendary",
    # The Office — that's what she said
    "pretzel",
    "dundie",
    "beet",
    "salesman",
    "manager",
    "branch",
    # Breaking Bad — say my name
    "chemistry",
    "methamphetamine",
    "cartel",
    "empire",
    # Zelda — it's dangerous to go alone
    "triforce",
    "dungeon",
    "princess",
    "sword",
    "adventure",
]

# ── Gallows ASCII Art ──────────────────────────────────────────────────
# 7 stages: 0 wrong guesses (peaceful) → 6 (R.I.P. — Game Over)

GALLOWS_OF_DOOM: list[str] = [
    # Stage 0 — "I am inevitable." (But not yet.)
    """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
    # Stage 1 — The head appears, like Voldemort on the back of Quirrell
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
    # Stage 2 — A body! "I am Iron Man."
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
    # Stage 3 — Left arm. "Help me, Obi-Wan Kenobi."
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
    # Stage 4 — Both arms. "Why so serious?"
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
""",
    # Stage 5 — Left leg. "This is fine." (It is not fine.)
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
""",
    # Stage 6 — GAME OVER. "You know nothing, Jon Snow."
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
""",
]

# ── Game Constants ─────────────────────────────────────────────────────

MORDOR_WRONG_GUESS_LIMIT = 6         # One does not simply survive more than this
HINT_PORTAL_THRESHOLD = 3            # Doctor Strange opens the portal at this point
SESSION_KEY_WORD = "hm_secret_word"
SESSION_KEY_GUESSED = "hm_guessed_letters"
SESSION_KEY_WRONG_COUNT = "hm_wrong_count"
SESSION_KEY_GAME_OVER = "hm_game_over"
SESSION_KEY_WIN = "hm_win"
SESSION_KEY_HINT_USED = "hm_hint_used"
SESSION_KEY_ERROR = "hm_input_error"


# ── Pure Logic (testable without Streamlit) ────────────────────────────


def pick_secret_word(word_bank: list[str] | None = None) -> str:
    """Pick a random word from the word bank.

    Like the Sorting Hat — completely random, no take-backs.
    """
    bank = word_bank if word_bank is not None else THE_ONE_RING_WORD_BANK
    return random.choice(bank).lower()  # noqa: S311 — not cryptographic


def build_display_word(secret_word: str, guessed_letters: set[str]) -> str:
    """Return the word with unguessed letters masked as underscores.

    "Not all those who wander are lost" — but all unguessed letters are hidden.
    """
    return " ".join(ch if ch in guessed_letters else "_" for ch in secret_word)


def get_gallows_stage(wrong_count: int) -> str:
    """Return the ASCII gallows art for the given wrong-guess count.

    Clamps to valid indices so we never go full Thanos off the edge of the list.
    """
    clamped = max(0, min(wrong_count, MORDOR_WRONG_GUESS_LIMIT))
    return GALLOWS_OF_DOOM[clamped]


def check_win(secret_word: str, guessed_letters: set[str]) -> bool:
    """Return True if every letter in the word has been guessed.

    "The eagle has landed" — mission accomplished.
    """
    return all(ch in guessed_letters for ch in secret_word)


def get_hint_letter(secret_word: str, guessed_letters: set[str]) -> str | None:
    """Return an unguessed letter from the secret word, or None if all are found.

    Doctor Strange has seen 14,000,605 futures and picked this letter for you.
    Returns None when there are no letters left to reveal (you're winning already).
    """
    unguessed = [ch for ch in secret_word if ch not in guessed_letters]
    if not unguessed:
        return None
    return random.choice(unguessed)  # noqa: S311 — not cryptographic


def validate_guess(raw_input: str, guessed_letters: set[str]) -> tuple[bool, str]:
    """Validate a player's raw input before processing it.

    Returns (True, "") on success, or (False, error_message) on failure.
    Input validation is harder than it looks — just ask any Space Shuttle engineer.
    """
    stripped = raw_input.strip().lower()
    if not stripped:
        return False, "You entered nothing. Even Thanos had a plan."
    if len(stripped) != 1:
        return False, "One letter at a time! This isn't Wheel of Fortune."
    if not stripped.isalpha():
        return False, "Letters only, please. Numbers are for math class."
    if stripped in guessed_letters:
        return False, f"You already guessed '{stripped.upper()}'. Pay attention, 007."
    return True, ""


def process_guess(
    letter: str,
    secret_word: str,
    guessed_letters: set[str],
    wrong_count: int,
) -> tuple[set[str], int, bool, bool]:
    """Process a valid letter guess and return updated game state.

    Returns (updated_guessed_letters, updated_wrong_count, is_win, is_game_over).
    Like a turn in D&D — roll the dice and face the consequences.
    """
    new_guessed = guessed_letters | {letter}
    new_wrong_count = wrong_count if letter in secret_word else wrong_count + 1
    won = check_win(secret_word, new_guessed)
    lost = new_wrong_count >= MORDOR_WRONG_GUESS_LIMIT
    return new_guessed, new_wrong_count, won, lost


# ── Session-State Helpers ──────────────────────────────────────────────


def _init_new_game() -> None:
    """Reset session state and start a fresh game. Press Start — player 1 insert coin."""
    st.session_state[SESSION_KEY_WORD] = pick_secret_word()
    st.session_state[SESSION_KEY_GUESSED] = set()
    st.session_state[SESSION_KEY_WRONG_COUNT] = 0
    st.session_state[SESSION_KEY_GAME_OVER] = False
    st.session_state[SESSION_KEY_WIN] = False
    st.session_state[SESSION_KEY_HINT_USED] = False
    st.session_state[SESSION_KEY_ERROR] = ""


def _ensure_game_initialised() -> None:
    """Initialise session state keys if they don't exist yet."""
    if SESSION_KEY_WORD not in st.session_state:
        _init_new_game()


def _handle_guess_submission() -> None:
    """Callback: validate and process the letter submitted via the text input."""
    raw = st.session_state.get("hm_guess_input", "")
    secret = st.session_state[SESSION_KEY_WORD]
    guessed = st.session_state[SESSION_KEY_GUESSED]
    wrong_count = st.session_state[SESSION_KEY_WRONG_COUNT]

    valid, error_msg = validate_guess(raw, guessed)
    if not valid:
        st.session_state[SESSION_KEY_ERROR] = error_msg
        return

    letter = raw.strip().lower()
    new_guessed, new_wrong, won, lost = process_guess(letter, secret, guessed, wrong_count)

    st.session_state[SESSION_KEY_GUESSED] = new_guessed
    st.session_state[SESSION_KEY_WRONG_COUNT] = new_wrong
    st.session_state[SESSION_KEY_WIN] = won
    st.session_state[SESSION_KEY_GAME_OVER] = lost or won
    st.session_state[SESSION_KEY_ERROR] = ""
    # Clear the text box for the next guess
    st.session_state["hm_guess_input"] = ""


def _handle_hint() -> None:
    """Callback: reveal one unguessed letter — the Doctor Strange special."""
    secret = st.session_state[SESSION_KEY_WORD]
    guessed = st.session_state[SESSION_KEY_GUESSED]
    hint = get_hint_letter(secret, guessed)
    if hint:
        new_guessed, new_wrong, won, lost = process_guess(hint, secret, guessed, st.session_state[SESSION_KEY_WRONG_COUNT])
        st.session_state[SESSION_KEY_GUESSED] = new_guessed
        st.session_state[SESSION_KEY_WRONG_COUNT] = new_wrong
        st.session_state[SESSION_KEY_WIN] = won
        st.session_state[SESSION_KEY_GAME_OVER] = lost or won
    st.session_state[SESSION_KEY_HINT_USED] = True


# ── Streamlit Render ───────────────────────────────────────────────────


def render() -> None:
    """Render the Hangman game page.

    "Let's play a game." — Jigsaw (we promise this is more fun than his version).
    """
    _ensure_game_initialised()

    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem">🪢&nbsp; Hangman</h1>
            <p>Guess the word before the gallows claim another soul.
            "It's not about how hard you hit — it's about how hard you can get hit
            and keep guessing." — Rocky Balboa (paraphrased)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    secret: str = st.session_state[SESSION_KEY_WORD]
    guessed: set[str] = st.session_state[SESSION_KEY_GUESSED]
    wrong_count: int = st.session_state[SESSION_KEY_WRONG_COUNT]
    game_over: bool = st.session_state[SESSION_KEY_GAME_OVER]
    player_won: bool = st.session_state[SESSION_KEY_WIN]
    hint_used: bool = st.session_state[SESSION_KEY_HINT_USED]
    error_msg: str = st.session_state[SESSION_KEY_ERROR]

    left_col, right_col = st.columns([1, 2])

    with left_col:
        # Gallows — the grim progress meter
        st.code(get_gallows_stage(wrong_count), language=None)
        st.markdown(f"**Wrong guesses:** {wrong_count} / {MORDOR_WRONG_GUESS_LIMIT}")

    with right_col:
        # Masked word display
        display = build_display_word(secret, guessed)
        st.markdown(
            f'<p style="font-size:2rem;letter-spacing:0.3rem;font-family:monospace;">'
            f"{display}</p>",
            unsafe_allow_html=True,
        )

        # Letters guessed so far
        wrong_letters = sorted(ch for ch in guessed if ch not in secret)
        correct_letters = sorted(ch for ch in guessed if ch in secret)

        if correct_letters:
            st.markdown(
                "✅ **Correct:** " + " ".join(f"`{ch.upper()}`" for ch in correct_letters)
            )
        if wrong_letters:
            st.markdown(
                "❌ **Wrong:** " + " ".join(f"`{ch.upper()}`" for ch in wrong_letters)
            )

        # ── End states ────────────────────────────────────────────────
        if game_over:
            if player_won:
                st.success(
                    f"🎉 **You did it!** The word was **{secret.upper()}**. "
                    "'You're a wizard, Harry!' — Hagrid"
                )
            else:
                st.error(
                    f"💀 **GAME OVER.** The word was **{secret.upper()}**. "
                    "'Winter is coming' — and so was this loss."
                )
            if st.button("▶️ Play Again", type="primary", key="hm_play_again"):
                _init_new_game()
                st.rerun()
            return

        # ── Input ─────────────────────────────────────────────────────
        if error_msg:
            st.warning(error_msg)

        st.text_input(
            "Enter a letter:",
            max_chars=1,
            key="hm_guess_input",
            on_change=_handle_guess_submission,
            placeholder="A single letter, not the entire Hogwarts library",
            disabled=game_over,
        )

        # ── Hint Portal ───────────────────────────────────────────────
        # Opens after HINT_PORTAL_THRESHOLD wrong guesses — one-use only
        hint_available = wrong_count >= HINT_PORTAL_THRESHOLD and not hint_used
        if hint_available:
            st.info(
                "🌀 **Hint portal detected!** Doctor Strange has opened a path — "
                "use it wisely, it only works once."
            )
            st.button(
                "🔮 Reveal a Letter (Hint)",
                key="hm_hint_btn",
                on_click=_handle_hint,
            )
        elif hint_used:
            st.caption("🪄 Hint used — you're on your own now, Frodo.")
