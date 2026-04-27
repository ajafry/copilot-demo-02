"""Tests for the calculator module."""

from unittest.mock import MagicMock, patch

import pytest

from views.calculator import (
    ALLOWED_CHARS,
    BUTTON_ROWS,
    COLUMNS_PER_ROW,
    OPERATOR_MAP,
    _append,
    _backspace,
    _clear,
    _evaluate,
)


@pytest.fixture(autouse=True)
def _mock_session_state():
    """Provide a fresh mock session_state for every test."""
    mock_state = MagicMock()
    mock_state.calc_expr = ""
    mock_state.calc_result = ""
    with patch("views.calculator.st") as mock_st:
        mock_st.session_state = mock_state
        yield mock_state


# ── Constants ──────────────────────────────────────────────────────────


class TestConstants:
    """Verify module-level constants are well-formed."""

    def test_allowed_chars_contains_digits(self) -> None:
        for digit in "0123456789":
            assert digit in ALLOWED_CHARS

    def test_allowed_chars_contains_operators(self) -> None:
        for op in "+-*/":
            assert op in ALLOWED_CHARS

    def test_allowed_chars_contains_parens_and_dot(self) -> None:
        for ch in ".() ":
            assert ch in ALLOWED_CHARS

    def test_operator_map_entries(self) -> None:
        assert OPERATOR_MAP == {"÷": "/", "×": "*", "−": "-"}

    def test_button_rows_structure(self) -> None:
        assert len(BUTTON_ROWS) == 5
        for row in BUTTON_ROWS:
            assert len(row) == COLUMNS_PER_ROW

    def test_columns_per_row_value(self) -> None:
        assert COLUMNS_PER_ROW == 4


# ── _append ────────────────────────────────────────────────────────────


class TestAppend:
    """Test the _append helper."""

    def test_append_digit(self, _mock_session_state: MagicMock) -> None:
        _append("5")
        assert _mock_session_state.calc_expr == "5"
        assert _mock_session_state.calc_result == ""

    def test_append_multiple(self, _mock_session_state: MagicMock) -> None:
        _append("1")
        _append("+")
        _append("2")
        assert _mock_session_state.calc_expr == "1+2"

    def test_append_clears_result(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_result = "42"
        _append("7")
        assert _mock_session_state.calc_result == ""

    def test_append_operator(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "3"
        _append("*")
        assert _mock_session_state.calc_expr == "3*"


# ── _clear ─────────────────────────────────────────────────────────────


class TestClear:
    """Test the _clear helper."""

    def test_clear_resets_expression(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "123+456"
        _mock_session_state.calc_result = "579"
        _clear()
        assert _mock_session_state.calc_expr == ""
        assert _mock_session_state.calc_result == ""

    def test_clear_on_empty(self, _mock_session_state: MagicMock) -> None:
        _clear()
        assert _mock_session_state.calc_expr == ""
        assert _mock_session_state.calc_result == ""


# ── _backspace ─────────────────────────────────────────────────────────


class TestBackspace:
    """Test the _backspace helper."""

    def test_backspace_removes_last_char(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "123"
        _backspace()
        assert _mock_session_state.calc_expr == "12"

    def test_backspace_clears_result(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "9"
        _mock_session_state.calc_result = "9"
        _backspace()
        assert _mock_session_state.calc_result == ""

    def test_backspace_on_empty(self, _mock_session_state: MagicMock) -> None:
        _backspace()
        assert _mock_session_state.calc_expr == ""

    def test_backspace_single_char(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "7"
        _backspace()
        assert _mock_session_state.calc_expr == ""


# ── _evaluate ──────────────────────────────────────────────────────────


class TestEvaluate:
    """Test the _evaluate helper."""

    def test_evaluate_simple_addition(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "2+3"
        _evaluate()
        assert _mock_session_state.calc_result == "5"

    def test_evaluate_subtraction(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "10-4"
        _evaluate()
        assert _mock_session_state.calc_result == "6"

    def test_evaluate_multiplication(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "6*7"
        _evaluate()
        assert _mock_session_state.calc_result == "42"

    def test_evaluate_division(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "10/2"
        _evaluate()
        assert _mock_session_state.calc_result == "5.0"

    def test_evaluate_float_result(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "7/3"
        _evaluate()
        result = float(_mock_session_state.calc_result)
        assert pytest.approx(result, rel=1e-9) == 7 / 3

    def test_evaluate_parentheses(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "(2+3)*4"
        _evaluate()
        assert _mock_session_state.calc_result == "20"

    def test_evaluate_empty_expression(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = ""
        _evaluate()
        assert _mock_session_state.calc_result == "Error"

    def test_evaluate_invalid_chars(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "abc"
        _evaluate()
        assert _mock_session_state.calc_result == "Error"

    def test_evaluate_division_by_zero(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "1/0"
        _evaluate()
        assert _mock_session_state.calc_result == "Error"

    def test_evaluate_malformed_expression(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "2+*3"
        _evaluate()
        assert _mock_session_state.calc_result == "Error"

    def test_evaluate_complex_expression(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "(10+5)*2/3"
        _evaluate()
        assert _mock_session_state.calc_result == "10.0"

    def test_evaluate_single_number(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "42"
        _evaluate()
        assert _mock_session_state.calc_result == "42"

    def test_evaluate_decimal_input(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "3.14+1.86"
        _evaluate()
        assert _mock_session_state.calc_result == "5.0"

    def test_evaluate_negative_result(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "3-10"
        _evaluate()
        assert _mock_session_state.calc_result == "-7"

    def test_evaluate_spaces_in_expression(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "2 + 3"
        _evaluate()
        assert _mock_session_state.calc_result == "5"

    def test_evaluate_chained_addition(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "1+2+3"
        _evaluate()
        assert _mock_session_state.calc_result == "6"

    def test_evaluate_mixed_multiply_add(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "3*2+1"
        _evaluate()
        assert _mock_session_state.calc_result == "7"

    def test_evaluate_chained_subtraction(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "10-3-2"
        _evaluate()
        assert _mock_session_state.calc_result == "5"

    def test_evaluate_mixed_add_multiply(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "1+2*3"
        _evaluate()
        assert _mock_session_state.calc_result == "7"

    def test_evaluate_mixed_divide_add(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "10/2+3"
        _evaluate()
        assert _mock_session_state.calc_result == "8.0"

    def test_evaluate_chained_multiply(self, _mock_session_state: MagicMock) -> None:
        _mock_session_state.calc_expr = "2*3*4"
        _evaluate()
        assert _mock_session_state.calc_result == "24"
