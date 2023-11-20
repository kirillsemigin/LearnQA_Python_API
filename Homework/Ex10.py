import pytest

class Test:
    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        phrase_lenghth = len(phrase)

        assert phrase_lenghth < 15, f"Phrase lenghth is more than 15 characters"