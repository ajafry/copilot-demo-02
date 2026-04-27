"""Tests for the password generator module.

As Nick Fury once said: 'I still believe in heroes' — and in thorough unit tests.
"""

import string

import pytest

from views.password_generator import (
    AMBIGUOUS_EXILES,
    DIGIT_MATRIX,
    GANDALF_MAX_LENGTH,
    GOLDILOCKS_DEFAULT_LENGTH,
    LOWERCASE_SHIRE,
    SYMBOL_BATCAVE,
    THANOS_MIN_LENGTH,
    UPPERCASE_ASGARD,
    _password_strength,
    generate_password,
)


# ── generate_password ─────────────────────────────────────────────────


class TestGeneratePassword:
    """Test the generate_password function — the Arc Reactor of this module."""

    def test_default_length(self) -> None:
        password = generate_password()
        assert len(password) == GOLDILOCKS_DEFAULT_LENGTH

    def test_custom_length(self) -> None:
        for chosen_length in (THANOS_MIN_LENGTH, 20, 64, GANDALF_MAX_LENGTH):
            password = generate_password(chosen_length)
            assert len(password) == chosen_length

    def test_contains_lowercase_always(self) -> None:
        password = generate_password(
            use_uppercase=False, use_digits=False, use_symbols=False,
        )
        assert any(ch in LOWERCASE_SHIRE for ch in password)

    def test_contains_uppercase_when_enabled(self) -> None:
        password = generate_password(32, use_uppercase=True)
        assert any(ch in UPPERCASE_ASGARD for ch in password)

    def test_contains_digits_when_enabled(self) -> None:
        password = generate_password(32, use_digits=True)
        assert any(ch in DIGIT_MATRIX for ch in password)

    def test_contains_symbols_when_enabled(self) -> None:
        password = generate_password(32, use_symbols=True)
        assert any(ch in SYMBOL_BATCAVE for ch in password)

    def test_no_uppercase_when_disabled(self) -> None:
        password = generate_password(32, use_uppercase=False, use_digits=False, use_symbols=False)
        assert not any(ch in UPPERCASE_ASGARD for ch in password)

    def test_no_digits_when_disabled(self) -> None:
        password = generate_password(32, use_uppercase=False, use_digits=False, use_symbols=False)
        assert not any(ch in DIGIT_MATRIX for ch in password)

    def test_no_symbols_when_disabled(self) -> None:
        password = generate_password(32, use_uppercase=False, use_digits=False, use_symbols=False)
        assert not any(ch in SYMBOL_BATCAVE for ch in password)

    def test_exclude_ambiguous_chars(self) -> None:
        password = generate_password(64, exclude_ambiguous=True)
        assert not any(ch in AMBIGUOUS_EXILES for ch in password)

    def test_too_short_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="Thanos"):
            generate_password(THANOS_MIN_LENGTH - 1)

    def test_too_long_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="shall not pass"):
            generate_password(GANDALF_MAX_LENGTH + 1)

    def test_all_options_enabled(self) -> None:
        password = generate_password(32, use_uppercase=True, use_digits=True, use_symbols=True)
        assert any(ch in LOWERCASE_SHIRE for ch in password)
        assert any(ch in UPPERCASE_ASGARD for ch in password)
        assert any(ch in DIGIT_MATRIX for ch in password)
        assert any(ch in SYMBOL_BATCAVE for ch in password)

    def test_uniqueness(self) -> None:
        """Two consecutive calls should not produce the same password. Ever."""
        passwords = {generate_password() for _ in range(10)}
        assert len(passwords) == 10

    def test_only_valid_characters(self) -> None:
        full_pool = set(string.ascii_letters + string.digits + string.punctuation)
        password = generate_password(64)
        assert all(ch in full_pool for ch in password)


# ── _password_strength ────────────────────────────────────────────────


class TestPasswordStrength:
    """Test the strength rater — our very own Jarvis diagnostics."""

    def test_weak_password(self) -> None:
        result = _password_strength("abcdefgh")
        assert "Weak" in result

    def test_fair_password(self) -> None:
        result = _password_strength("Abcdefgh1")
        assert "Fair" in result

    def test_strong_password(self) -> None:
        result = _password_strength("Abcdefghijklmno1")
        assert "Strong" in result

    def test_unbreakable_password(self) -> None:
        result = _password_strength("Abcdefghijklmno1!")
        assert "Unbreakable" in result

    def test_empty_password(self) -> None:
        result = _password_strength("")
        assert "Weak" in result
