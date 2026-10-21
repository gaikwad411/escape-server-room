from dataclasses import dataclass, field
from typing import Callable

from game.rooms import Room


TURN_LIMIT = 10


@dataclass
class Player:
    current_room: str
    inventory: list[str] = field(default_factory=list)


def build_rooms() -> dict[str, Room]:
    return {
        "Server Room": Room(
            name="Server Room",
            description="Fans roar around a bank of hot servers.",
            doors={"north": "Hallway"},
            items=["keycard"],
        ),
        "Hallway": Room(
            name="Hallway",
            description="A narrow hallway leads deeper into the facility.",
            doors={"south": "Server Room", "east": "Control Room"},
            items=[],
        ),
        "Control Room": Room(
            name="Control Room",
            description="A control panel hums beside the exit door.",
            doors={"west": "Hallway"},
            items=[],
        ),
    }


def describe_room(room: Room, player: Player, output_fn: Callable[[str], None]) -> None:
    output_fn(f"{room.name}: {room.description}")
    exits = ", ".join(room.doors) or "none"
    items = ", ".join(room.items) or "none"
    inventory = ", ".join(player.inventory) or "empty"
    output_fn(f"Exits: {exits}")
    output_fn(f"Items: {items}")
    output_fn(f"Inventory: {inventory}")


def run_game(
    input_fn: Callable[[str], str] | None = None,
    output_fn: Callable[[str], None] | None = None,
) -> Player:
    if input_fn is None:
        input_fn = input
    if output_fn is None:
        output_fn = print

    rooms = build_rooms()
    player = Player(current_room="Server Room")
    turns_remaining = TURN_LIMIT

    output_fn("The server room is overheating. Find a way out before the systems fail.")

    while True:
        raw_command = input_fn("Command (go/look/take/quit): ").strip()
        command, _, argument = raw_command.partition(" ")
        command = command.casefold()
        argument = argument.strip()
        action_succeeded = False

        if command == "quit":
            output_fn("You quit the game.")
            break
        if command == "look" and not argument:
            describe_room(rooms[player.current_room], player, output_fn)
        elif command == "go" and argument:
            previous_room = player.current_room
            output_fn(rooms[player.current_room].move(player, argument.casefold()))
            action_succeeded = player.current_room != previous_room
        elif command == "take" and argument:
            room = rooms[player.current_room]
            matching_item = next(
                (item for item in room.items if item.casefold() == argument.casefold()),
                None,
            )
            if matching_item is None:
                output_fn("That item isn't here.")
            else:
                room.items.remove(matching_item)
                player.inventory.append(matching_item)
                output_fn(f"You take the {matching_item}.")
                action_succeeded = True
        else:
            output_fn("Unknown or incomplete command. Use go, look, take, or quit.")

        if action_succeeded:
            turns_remaining -= 1
            output_fn(f"Turns remaining: {turns_remaining}")
            if turns_remaining == 0:
                output_fn("The servers overheat. Game over.")
                break

    return player


if __name__ == "__main__":
    run_game()