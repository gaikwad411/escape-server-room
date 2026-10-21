# A room has a name, a description, and a dict of doors (direction -> room name), 
# and a list of items. use a dataclass.

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Room:
    name: str
    description: str
    doors: Dict[str, str]
    items: List[str]

    def get_exit(self, direction: str) -> str | None:
        return self.doors.get(direction)

    def move(self, player, direction) -> str | None:
        """Moves the player to the room in the given direction, if possible."""
        next_room_name = self.get_exit(direction)
        if next_room_name:
            player.current_room = next_room_name
            return f"You move {direction} to {next_room_name}."
        else:
            return "You can't go that way."
        
    def lock(self, room):
        """Locks the room by removing all doors."""
        self.doors.clear()
        return f"{self.name} is now locked. All doors are removed."


