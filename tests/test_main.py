import unittest

from game.main import TURN_LIMIT, run_game


class GameLoopTests(unittest.TestCase):
    def play(self, commands: list[str]) -> tuple[list[str], object]:
        command_iter = iter(commands)
        output: list[str] = []
        player = run_game(
            input_fn=lambda _prompt: next(command_iter),
            output_fn=output.append,
        )
        return output, player

    def test_look_and_failed_move_do_not_consume_turns(self) -> None:
        output, _ = self.play(["look", "go west", "quit"])

        self.assertFalse(any(line.startswith("Turns remaining:") for line in output))
        self.assertIn("You can't go that way.", output)

    def test_go_changes_room_and_take_updates_inventory(self) -> None:
        output, player = self.play(["take keycard", "look", "go north", "look", "quit"])

        self.assertEqual(player.current_room, "Hallway")
        self.assertEqual(player.inventory, ["keycard"])
        self.assertIn("You take the keycard.", output)
        self.assertIn("Items: none", output)
        self.assertIn("Hallway: A narrow hallway leads deeper into the facility.", output)
        self.assertEqual(
            [line for line in output if line.startswith("Turns remaining:")],
            ["Turns remaining: 9", "Turns remaining: 8"],
        )

    def test_missing_item_and_unknown_command_do_not_consume_turns(self) -> None:
        output, _ = self.play(["take screwdriver", "dance", "quit"])

        self.assertIn("That item isn't here.", output)
        self.assertIn("Unknown or incomplete command. Use go, look, take, or quit.", output)
        self.assertFalse(any(line.startswith("Turns remaining:") for line in output))

    def test_quit_does_not_consume_turn(self) -> None:
        output, _ = self.play(["quit"])

        self.assertFalse(any(line.startswith("Turns remaining:") for line in output))

    def test_overheating_after_tenth_successful_action(self) -> None:
        output, _ = self.play(["go north", "go south"] * (TURN_LIMIT // 2))

        self.assertIn("Turns remaining: 0", output)
        self.assertIn("The servers overheat. Game over.", output)
        self.assertEqual(sum(line.startswith("Turns remaining:") for line in output), TURN_LIMIT)


if __name__ == "__main__":
    unittest.main()