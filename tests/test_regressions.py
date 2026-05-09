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


if __name__ == "__main__":
    unittest.main()
