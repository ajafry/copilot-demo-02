"""Tests for the number_guesser module — "I'll be back." — The Terminator (after a wrong guess)."""

import pytest

from views.number_guesser import (
    GANDALF_ABSOLUTE_MIN_RANGE,
    MATRIX_DEFAULT_MAX,
    MATRIX_DEFAULT_MIN,
    RESULT_CORRECT,
    RESULT_TOO_HIGH,
    RESULT_TOO_LOW,
    THANOS_ABSOLUTE_MIN_GUESSES,
    YODA_DEFAULT_MAX_GUESSES,
    build_progress_emoji,
    conjure_the_number,
    evaluate_guess,
    validate_game_config,
    validate_guess_input,
)


# ── Constants ──────────────────────────────────────────────────────────


class TestConstants:
    """Verify game constants are set to sensible values."""

    def test_default_min_is_one(self) -> None:
        assert MATRIX_DEFAULT_MIN == 1

    def test_default_max_is_one_hundred(self) -> None:
        assert MATRIX_DEFAULT_MAX == 100

    def test_default_max_greater_than_default_min(self) -> None:
        assert MATRIX_DEFAULT_MAX > MATRIX_DEFAULT_MIN

    def test_yoda_default_guesses_is_ten(self) -> None:
        assert YODA_DEFAULT_MAX_GUESSES == 10

    def test_thanos_min_guesses_is_one(self) -> None:
        assert THANOS_ABSOLUTE_MIN_GUESSES == 1

    def test_gandalf_min_range_is_two(self) -> None:
        assert GANDALF_ABSOLUTE_MIN_RANGE == 2

    def test_result_literals_are_distinct(self) -> None:
        assert len({RESULT_CORRECT, RESULT_TOO_HIGH, RESULT_TOO_LOW}) == 3


# ── conjure_the_number ─────────────────────────────────────────────────


class TestConjureTheNumber:
    """Tests for the random secret-number generator."""

    def test_returns_int(self) -> None:
        result = conjure_the_number(1, 10)
        assert isinstance(result, int)

    def test_result_within_range_inclusive(self) -> None:
        for _ in range(200):
            result = conjure_the_number(5, 15)
            assert 5 <= result <= 15

    def test_smallest_valid_range(self) -> None:
        # min=1, max=2 — only two possible values
        result = conjure_the_number(1, 2)
        assert result in (1, 2)

    def test_negative_range_valid(self) -> None:
        result = conjure_the_number(-50, -1)
        assert -50 <= result <= -1

    def test_equal_min_max_raises(self) -> None:
        with pytest.raises(ValueError, match="shall not pass"):
            conjure_the_number(5, 5)

    def test_min_greater_than_max_raises(self) -> None:
        with pytest.raises(ValueError):
            conjure_the_number(10, 1)


# ── evaluate_guess ─────────────────────────────────────────────────────


class TestEvaluateGuess:
    """Tests for guess evaluation — "Do. Or do not." — Yoda"""

    def test_exact_match_returns_correct(self) -> None:
        assert evaluate_guess(42, 42) == RESULT_CORRECT

    def test_guess_above_secret_returns_too_high(self) -> None:
        assert evaluate_guess(99, 50) == RESULT_TOO_HIGH

    def test_guess_below_secret_returns_too_low(self) -> None:
        assert evaluate_guess(1, 50) == RESULT_TOO_LOW

    def test_one_above_secret(self) -> None:
        assert evaluate_guess(51, 50) == RESULT_TOO_HIGH

    def test_one_below_secret(self) -> None:
        assert evaluate_guess(49, 50) == RESULT_TOO_LOW

    def test_negative_secret_correct(self) -> None:
        assert evaluate_guess(-10, -10) == RESULT_CORRECT

    def test_negative_secret_too_high(self) -> None:
        assert evaluate_guess(-5, -10) == RESULT_TOO_HIGH

    def test_negative_secret_too_low(self) -> None:
        assert evaluate_guess(-15, -10) == RESULT_TOO_LOW


# ── validate_guess_input ───────────────────────────────────────────────


class TestValidateGuessInput:
    """Tests for player input validation — "Garbage in, garbage out." — Every CS professor"""

    def test_valid_integer_within_range(self) -> None:
        ok, msg, parsed = validate_guess_input("50", 1, 100)
        assert ok is True
        assert msg == ""
        assert parsed == 50

    def test_valid_min_boundary(self) -> None:
        ok, _, parsed = validate_guess_input("1", 1, 100)
        assert ok is True
        assert parsed == 1

    def test_valid_max_boundary(self) -> None:
        ok, _, parsed = validate_guess_input("100", 1, 100)
        assert ok is True
        assert parsed == 100

    def test_whitespace_stripped(self) -> None:
        ok, _, parsed = validate_guess_input("  42  ", 1, 100)
        assert ok is True
        assert parsed == 42

    def test_empty_input_invalid(self) -> None:
        ok, msg, parsed = validate_guess_input("", 1, 100)
        assert ok is False
        assert msg != ""
        assert parsed == 0

    def test_whitespace_only_invalid(self) -> None:
        ok, msg, _ = validate_guess_input("   ", 1, 100)
        assert ok is False
        assert msg != ""

    def test_non_numeric_input_invalid(self) -> None:
        ok, msg, _ = validate_guess_input("abc", 1, 100)
        assert ok is False
        assert msg != ""

    def test_float_input_invalid(self) -> None:
        ok, msg, _ = validate_guess_input("3.14", 1, 100)
        assert ok is False
        assert msg != ""

    def test_below_range_invalid(self) -> None:
        ok, msg, _ = validate_guess_input("0", 1, 100)
        assert ok is False
        assert "range" in msg.lower() or "1" in msg

    def test_above_range_invalid(self) -> None:
        ok, msg, _ = validate_guess_input("101", 1, 100)
        assert ok is False
        assert "range" in msg.lower() or "100" in msg

    def test_negative_valid_within_negative_range(self) -> None:
        ok, _, parsed = validate_guess_input("-25", -50, -1)
        assert ok is True
        assert parsed == -25

    def test_special_characters_invalid(self) -> None:
        ok, _, _ = validate_guess_input("!", 1, 100)
        assert ok is False


# ── validate_game_config ───────────────────────────────────────────────


class TestValidateGameConfig:
    """Tests for configuration validation — "With great configuration comes great responsibility." """

    def test_valid_config(self) -> None:
        ok, msg = validate_game_config(1, 100, 10)
        assert ok is True
        assert msg == ""

    def test_range_too_small_exactly_equal(self) -> None:
        ok, msg = validate_game_config(5, 5, 10)
        assert ok is False
        assert msg != ""

    def test_range_too_small_only_one_apart(self) -> None:
        # range_max - range_min = 1, which is < GANDALF_ABSOLUTE_MIN_RANGE (2)
        ok, msg = validate_game_config(5, 6, 10)
        assert ok is False
        assert msg != ""

    def test_minimum_valid_range(self) -> None:
        # range_max - range_min == GANDALF_ABSOLUTE_MIN_RANGE (2)
        ok, _ = validate_game_config(1, 3, 5)
        assert ok is True

    def test_zero_guesses_invalid(self) -> None:
        ok, msg = validate_game_config(1, 100, 0)
        assert ok is False
        assert msg != ""

    def test_negative_guesses_invalid(self) -> None:
        ok, msg = validate_game_config(1, 100, -1)
        assert ok is False
        assert msg != ""

    def test_one_guess_valid(self) -> None:
        ok, _ = validate_game_config(1, 100, 1)
        assert ok is True

    def test_large_range_valid(self) -> None:
        ok, _ = validate_game_config(0, 1_000_000, 20)
        assert ok is True

    def test_negative_range_valid(self) -> None:
        ok, _ = validate_game_config(-100, -1, 5)
        assert ok is True


# ── build_progress_emoji ───────────────────────────────────────────────


class TestBuildProgressEmoji:
    """Tests for the life-bar emoji builder — "It's dangerous to go alone, take these hearts." """

    def test_full_lives(self) -> None:
        result = build_progress_emoji(5, 5)
        assert result == "❤️" * 5

    def test_no_lives_remaining(self) -> None:
        result = build_progress_emoji(0, 5)
        assert result == "🖤" * 5

    def test_partial_lives(self) -> None:
        result = build_progress_emoji(3, 5)
        assert result.count("❤️") == 3
        assert result.count("🖤") == 2

    def test_single_guess_remaining(self) -> None:
        result = build_progress_emoji(1, 10)
        assert result.count("❤️") == 1
        assert result.count("🖤") == 9

    def test_one_guess_total_full(self) -> None:
        result = build_progress_emoji(1, 1)
        assert result == "❤️"

    def test_one_guess_total_empty(self) -> None:
        result = build_progress_emoji(0, 1)
        assert result == "🖤"
