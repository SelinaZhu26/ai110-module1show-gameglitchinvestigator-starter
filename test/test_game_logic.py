import sys
import types
import unittest.mock as mock

# Stub out streamlit before importing app so module-level st calls don't fail
st_stub = types.ModuleType("streamlit")
for _attr in [
    "set_page_config", "title", "caption", "sidebar", "subheader",
    "info", "expander", "text_input", "columns", "button", "checkbox",
    "success", "error", "warning", "balloons", "divider", "stop", "rerun",
    "write", "selectbox", "header",
]:
    setattr(st_stub, _attr, mock.MagicMock())
st_stub.session_state = mock.MagicMock()
st_stub.session_state.__contains__ = mock.MagicMock(return_value=True)
st_stub.sidebar.selectbox = mock.MagicMock(return_value="Normal")
sys.modules["streamlit"] = st_stub

from app import get_range_for_difficulty, parse_guess, check_guess, update_score  # noqa: E402


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy_returns_1_to_20(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal_returns_1_to_50(self):
        assert get_range_for_difficulty("Normal") == (1, 50)

    def test_hard_returns_1_to_100(self):
        assert get_range_for_difficulty("Hard") == (1, 100)

    def test_unknown_difficulty_falls_back_to_1_100(self):
        assert get_range_for_difficulty("Impossible") == (1, 100)


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

class TestParseGuess:
    def test_none_input_is_invalid(self):
        ok, val, err = parse_guess(None)
        assert ok is False
        assert val is None
        assert err is not None

    def test_empty_string_is_invalid(self):
        ok, val, err = parse_guess("")
        assert ok is False
        assert val is None

    def test_valid_integer_string(self):
        ok, val, err = parse_guess("42")
        assert ok is True
        assert val == 42
        assert err is None

    def test_float_string_is_truncated_to_int(self):
        ok, val, err = parse_guess("7.9")
        assert ok is True
        assert val == 7

    def test_non_numeric_string_is_invalid(self):
        ok, val, err = parse_guess("abc")
        assert ok is False
        assert val is None
        assert err is not None

    def test_negative_number_is_parsed(self):
        ok, val, err = parse_guess("-5")
        assert ok is True
        assert val == -5


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

class TestCheckGuess:
    def test_correct_guess_returns_win(self):
        outcome, _ = check_guess(42, 42)
        assert outcome == "Win"

    def test_guess_too_high(self):
        outcome, _ = check_guess(80, 50)
        assert outcome == "Too High"

    def test_guess_too_low(self):
        outcome, _ = check_guess(10, 50)
        assert outcome == "Too Low"

    def test_string_secret_correct_guess(self):
        # On even attempts the secret is cast to str; check_guess must handle it
        outcome, _ = check_guess(7, "7")
        assert outcome == "Win"

    def test_string_secret_too_high(self):
        outcome, _ = check_guess(9, "5")
        assert outcome == "Too High"

    def test_string_secret_too_low(self):
        outcome, _ = check_guess(3, "5")
        assert outcome == "Too Low"

    # Bug 1 fix: hint messages were swapped (too high said "Go HIGHER", too low said "Go LOWER")
    def test_too_high_message_says_go_lower(self):
        _, message = check_guess(60, 50)
        assert "LOWER" in message

    def test_too_low_message_says_go_higher(self):
        _, message = check_guess(30, 50)
        assert "HIGHER" in message


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

class TestUpdateScore:
    def test_win_on_first_attempt_gives_max_points(self):
        # attempt_number=1 → points = 100 - 10*(1+1) = 80
        new_score = update_score(0, "Win", 1)
        assert new_score == 80

    def test_win_points_floor_at_10(self):
        # attempt_number=10 → raw points = 100 - 110 = -10 → clamped to 10
        new_score = update_score(0, "Win", 10)
        assert new_score == 10

    def test_too_high_on_even_attempt_adds_5(self):
        new_score = update_score(50, "Too High", 2)
        assert new_score == 55

    def test_too_high_on_odd_attempt_subtracts_5(self):
        new_score = update_score(50, "Too High", 3)
        assert new_score == 45

    def test_too_low_always_subtracts_5(self):
        new_score = update_score(50, "Too Low", 2)
        assert new_score == 45

    def test_unknown_outcome_leaves_score_unchanged(self):
        new_score = update_score(100, "Draw", 1)
        assert new_score == 100
