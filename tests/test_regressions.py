"""Regression tests for Dark Castle gameplay bugs."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from game.engine import GameEngine  # noqa: E402


class DarkCastleRegressionTests(unittest.TestCase):
    def test_combine_requires_all_three_key_fragments(self) -> None:
        engine = GameEngine()
        engine.new_game()
        self.assertIsNotNone(engine.world)

        engine.world.inventory = ["key_fragment_a", "key_fragment_b"]
        result = engine.process_command("combine")

        self.assertFalse(result["success"])
        self.assertNotIn("complete_key", engine.world.inventory)

    def test_bedroom_does_not_reveal_drawer_key_before_opening(self) -> None:
        engine = GameEngine()
        engine.new_game()

        engine.process_command("go north")
        engine.process_command("go west")
        result = engine.process_command("look")

        self.assertNotIn("small key", result["message"].lower())

    def test_dropped_hidden_item_appears_in_room_description(self) -> None:
        engine = GameEngine()
        engine.new_game()
        self.assertIsNotNone(engine.world)

        engine.process_command("go north")
        engine.process_command("go west")
        engine.process_command("open nightstand")
        engine.process_command("take small key")
        small_key = engine.world.get_item("small_key")
        self.assertIsNotNone(small_key)
        small_key.hidden = True
        engine.process_command("drop small key")
        result = engine.process_command("look")

        self.assertIn("small key", result["message"].lower())


if __name__ == "__main__":
    unittest.main()
