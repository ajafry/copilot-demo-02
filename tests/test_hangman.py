"""Tests for the hangman module — "Are you not entertained?" — Maximus Decimus Meridius."""

import pytest

from views.hangman import (
    HINT_PORTAL_THRESHOLD,
    MORDOR_WRONG_GUESS_LIMIT,
    THE_ONE_RING_WORD_BANK,
    build_display_word,
    check_win,
    get_gallows_stage,
    get_hint_letter,
    pick_secret_word,
    process_guess,
    validate_guess,
)


# ── Word Bank & Constants ──────────────────────────────────────────────


class TestWordBankAndConstants:
    """Verify the word bank and game constants are configured correctly."""

    def test_word_bank_has_at_least_thirty_words(self) -> None:
        assert len(THE_ONE_RING_WORD_BANK) >= 30

    def test_word_bank_contains_only_strings(self) -> None:
        for word in THE_ONE_RING_WORD_BANK:
            assert isinstance(word, str)

    def test_word_bank_has_no_empty_strings(self) -> None:
        for word in THE_ONE_RING_WORD_BANK:
            assert word.strip() != ""

    def test_mordor_wrong_guess_limit_is_six(self) -> None:
        assert MORDOR_WRONG_GUESS_LIMIT == 6

    def test_hint_portal_threshold_is_three(self) -> None:
        assert HINT_PORTAL_THRESHOLD == 3


# ── pick_secret_word ───────────────────────────────────────────────────


class TestPickSecretWord:
    """Tests for the random word picker."""

    def test_returns_string(self) -> None:
        word = pick_secret_word()
        assert isinstance(word, str)

    def test_returns_lowercase(self) -> None:
        word = pick_secret_word()
        assert word == word.lower()

    def test_returns_word_from_bank(self) -> None:
        bank = ["fellowship", "jedi", "pikachu"]
        word = pick_secret_word(bank)
        assert word in bank

    def test_custom_word_bank(self) -> None:
        bank = ["triforce"]
        assert pick_secret_word(bank) == "triforce"


# ── build_display_word ─────────────────────────────────────────────────


class TestBuildDisplayWord:
    """Tests for masked-word display generation."""

    def test_all_letters_hidden_initially(self) -> None:
        result = build_display_word("hobbit", set())
        assert result == "_ _ _ _ _ _"

    def test_correct_guess_revealed(self) -> None:
        result = build_display_word("hobbit", {"h"})
        assert result.startswith("h")

    def test_fully_guessed_word(self) -> None:
        result = build_display_word("jedi", set("jedi"))
        assert result == "j e d i"

    def test_partial_reveal(self) -> None:
        result = build_display_word("force", {"f", "e"})
        # f revealed, o/r/c hidden, e revealed
        assert result == "f _ _ _ e"

    def test_single_letter_word(self) -> None:
        assert build_display_word("a", {"a"}) == "a"
        assert build_display_word("a", set()) == "_"

    def test_repeated_letters_all_revealed(self) -> None:
        result = build_display_word("hobbit", {"b"})
        # 'b' appears at index 2 and 3 (h-o-b-b-i-t)
        parts = result.split()
        assert parts[2] == "b"
        assert parts[3] == "b"


# ── get_gallows_stage ──────────────────────────────────────────────────


class TestGetGallowsStage:
    """Tests for gallows ASCII art stage selection."""

    def test_seven_unique_stages(self) -> None:
        stages = [get_gallows_stage(i) for i in range(7)]
        assert len(set(stages)) == 7

    def test_stage_zero_is_empty_gallows(self) -> None:
        stage = get_gallows_stage(0)
        # Stage 0 should not contain a head
        assert "O" not in stage

    def test_final_stage_has_full_figure(self) -> None:
        stage = get_gallows_stage(6)
        assert "O" in stage  # head
        assert "|" in stage  # body

    def test_clamps_to_zero_for_negative(self) -> None:
        assert get_gallows_stage(-1) == get_gallows_stage(0)

    def test_clamps_to_max_for_overflow(self) -> None:
        assert get_gallows_stage(99) == get_gallows_stage(MORDOR_WRONG_GUESS_LIMIT)

    def test_all_stages_are_strings(self) -> None:
        for i in range(7):
            assert isinstance(get_gallows_stage(i), str)


# ── check_win ──────────────────────────────────────────────────────────


class TestCheckWin:
    """Tests for win-condition detection."""

    def test_win_when_all_letters_guessed(self) -> None:
        assert check_win("jedi", set("jedi")) is True

    def test_no_win_with_partial_guesses(self) -> None:
        assert check_win("jedi", {"j", "e"}) is False

    def test_no_win_with_empty_guesses(self) -> None:
        assert check_win("force", set()) is False

    def test_extra_guesses_do_not_prevent_win(self) -> None:
        # Guessing extra wrong letters shouldn't block the win
        assert check_win("elf", {"e", "l", "f", "z", "x"}) is True

    def test_single_letter_word_win(self) -> None:
        assert check_win("a", {"a"}) is True


# ── get_hint_letter ────────────────────────────────────────────────────


class TestGetHintLetter:
    """Tests for the Doctor Strange hint system."""

    def test_returns_unguessed_letter(self) -> None:
        hint = get_hint_letter("force", set())
        assert hint in "force"

    def test_returns_none_when_all_guessed(self) -> None:
        assert get_hint_letter("jedi", set("jedi")) is None

    def test_hint_not_in_guessed_set(self) -> None:
        hint = get_hint_letter("dragon", {"d", "r"})
        assert hint not in {"d", "r"}
        assert hint in "dragon"

    def test_single_remaining_letter(self) -> None:
        hint = get_hint_letter("hobbit", set("hobit"))
        # Only 'b' (second b) remains unguessed? Actually 'b' repeated —
        # with 'h','o','b','i','t' guessed, the second 'b' position is still 'b'
        # so all of hobbit's unique chars are guessed → should be None
        assert hint is None

    def test_hint_is_string_when_available(self) -> None:
        hint = get_hint_letter("fellowship", set())
        assert isinstance(hint, str)
        assert len(hint) == 1


# ── validate_guess ─────────────────────────────────────────────────────


class TestValidateGuess:
    """Tests for single-letter input validation — "I'll be back." — Terminator (after fixing input)."""

    def test_valid_single_letter(self) -> None:
        ok, msg = validate_guess("a", set())
        assert ok is True
        assert msg == ""

    def test_valid_uppercase_normalised(self) -> None:
        # Uppercase input for a letter not yet guessed should be valid
        ok, msg = validate_guess("A", set())
        assert ok is True

    def test_empty_input_invalid(self) -> None:
        ok, msg = validate_guess("", set())
        assert ok is False
        assert msg != ""

    def test_whitespace_only_invalid(self) -> None:
        ok, msg = validate_guess("   ", set())
        assert ok is False

    def test_multiple_letters_invalid(self) -> None:
        ok, msg = validate_guess("ab", set())
        assert ok is False
        assert msg != ""

    def test_digit_invalid(self) -> None:
        ok, msg = validate_guess("3", set())
        assert ok is False

    def test_special_char_invalid(self) -> None:
        ok, msg = validate_guess("!", set())
        assert ok is False

    def test_already_guessed_invalid(self) -> None:
        ok, msg = validate_guess("a", {"a"})
        assert ok is False
        assert "a" in msg.lower() or "already" in msg.lower()

    def test_whitespace_around_valid_letter(self) -> None:
        # A letter surrounded by whitespace should still be valid (stripped)
        ok, msg = validate_guess(" b ", set())
        assert ok is True
        assert msg == ""


# ── process_guess ──────────────────────────────────────────────────────


class TestProcessGuess:
    """Tests for the full guess-processing pipeline."""

    def test_correct_guess_does_not_increment_wrong_count(self) -> None:
        _, wrong, _, _ = process_guess("f", "force", set(), 0)
        assert wrong == 0

    def test_wrong_guess_increments_wrong_count(self) -> None:
        _, wrong, _, _ = process_guess("z", "force", set(), 0)
        assert wrong == 1

    def test_correct_guess_added_to_guessed(self) -> None:
        guessed, _, _, _ = process_guess("f", "force", set(), 0)
        assert "f" in guessed

    def test_wrong_guess_added_to_guessed(self) -> None:
        guessed, _, _, _ = process_guess("z", "force", set(), 0)
        assert "z" in guessed

    def test_win_detected(self) -> None:
        # Only 'e' left to guess
        _, _, won, _ = process_guess("e", "elf", {"e", "l"}, 2)
        # 'elf' needs e, l, f — only 'f' would win
        _, _, won, _ = process_guess("f", "elf", {"e", "l"}, 2)
        assert won is True

    def test_loss_detected_at_limit(self) -> None:
        _, _, _, lost = process_guess("z", "force", set(), MORDOR_WRONG_GUESS_LIMIT - 1)
        assert lost is True

    def test_game_not_over_below_limit(self) -> None:
        _, _, _, lost = process_guess("z", "force", set(), 0)
        assert lost is False

    def test_existing_guesses_preserved(self) -> None:
        existing = {"a", "b"}
        guessed, _, _, _ = process_guess("c", "force", existing, 0)
        assert "a" in guessed
        assert "b" in guessed
        assert "c" in guessed
