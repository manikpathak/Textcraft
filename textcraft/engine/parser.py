"""Natural language command parser mapping user input to game actions."""

import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class ParsedCommand:
    verb: str
    target: str = ""
    extra: str = ""
    count: int = 1
    raw: str = ""

class CommandParser:
    @staticmethod
    def parse(user_input: str) -> ParsedCommand:
        raw = user_input.strip()
        if not raw:
            return ParsedCommand(verb="look", raw="")

        words = raw.split()
        first = words[0].lower()

        # Direct directional abbreviations
        if first in ("n", "north"):
            return ParsedCommand(verb="move", target="north", raw=raw)
        if first in ("s", "south"):
            return ParsedCommand(verb="move", target="south", raw=raw)
        if first in ("e", "east"):
            return ParsedCommand(verb="move", target="east", raw=raw)
        if first in ("w", "west"):
            return ParsedCommand(verb="move", target="west", raw=raw)
        if first in ("u", "up", "ascend", "surface"):
            return ParsedCommand(verb="move", target="up", raw=raw)
        if first in ("d", "down", "descend"):
            return ParsedCommand(verb="move", target="down", raw=raw)

        # Inventory / Map / Stats abbreviations
        if first in ("i", "inv", "inventory", "bag"):
            return ParsedCommand(verb="inventory", raw=raw)
        if first in ("m", "map"):
            return ParsedCommand(verb="map", raw=raw)
        if first in ("l", "look", "survey", "examine", "glance"):
            return ParsedCommand(verb="look", raw=raw)
        if first in ("stats", "status", "health"):
            return ParsedCommand(verb="status", raw=raw)
        if first in ("time", "clock", "date"):
            return ParsedCommand(verb="time", raw=raw)
        if first in ("recipes", "recipe"):
            target = " ".join(words[1:]) if len(words) > 1 else ""
            return ParsedCommand(verb="recipes", target=target, raw=raw)
        if first in ("sleep", "rest"):
            return ParsedCommand(verb="sleep", raw=raw)
        if first in ("block", "defend"):
            return ParsedCommand(verb="block", raw=raw)
        if first in ("help", "?", "commands"):
            topic = " ".join(words[1:]) if len(words) > 1 else ""
            return ParsedCommand(verb="help", target=topic, raw=raw)
        if first in ("quit", "exit", "q"):
            return ParsedCommand(verb="quit", raw=raw)

        # Movement with 'go' or 'walk'
        if first in ("go", "walk", "travel", "head"):
            dir_str = " ".join(words[1:]).lower()
            return ParsedCommand(verb="move", target=dir_str, raw=raw)

        # Dig down or mine down
        if raw.lower() in ("dig down", "mine down", "enter cave"):
            return ParsedCommand(verb="move", target="down", raw=raw)
        if raw.lower() in ("climb up", "head up"):
            return ParsedCommand(verb="move", target="up", raw=raw)

        # Portal travel
        if raw.lower() in ("enter portal", "portal", "enter nether", "go to nether", "enter end"):
            return ParsedCommand(verb="portal", raw=raw)

        # Build shelter
        if raw.lower() in ("build shelter", "build house", "make shelter", "shelter"):
            return ParsedCommand(verb="shelter", raw=raw)

        # Mining / Chopping / Gathering: 'mine oak log', 'chop wood', 'dig dirt'
        if first in ("mine", "chop", "dig", "harvest", "gather", "cut"):
            target = " ".join(words[1:])
            # Normalize target aliases (e.g., 'tree' -> 'oak_log', 'wood' -> 'oak_log')
            if target.lower() in ("tree", "wood", "logs", "log"):
                target = "oak_log"
            return ParsedCommand(verb="mine", target=target, raw=raw)

        # Crafting: 'craft wooden_pickaxe [count]' or 'craft 4 torch'
        if first in ("craft", "make", "create"):
            rest = words[1:]
            count = 1
            if rest and rest[0].isdigit():
                count = int(rest[0])
                target = " ".join(rest[1:])
            elif rest and rest[-1].isdigit():
                count = int(rest[-1])
                target = " ".join(rest[:-1])
            else:
                target = " ".join(rest)
            return ParsedCommand(verb="craft", target=target, count=max(1, count), raw=raw)

        # Smelting: 'smelt iron_ore with coal', 'cook beef', 'smelt 4 iron_ore'
        if first in ("smelt", "cook", "bake", "burn"):
            rest = " ".join(words[1:])
            # Check for 'with' fuel
            fuel = ""
            count = 1
            if " with " in rest:
                item_part, fuel_part = rest.split(" with ", 1)
                fuel = fuel_part.strip()
                item_part_words = item_part.strip().split()
                if item_part_words and item_part_words[0].isdigit():
                    count = int(item_part_words[0])
                    target = " ".join(item_part_words[1:])
                else:
                    target = item_part
            else:
                rest_words = words[1:]
                if rest_words and rest_words[0].isdigit():
                    count = int(rest_words[0])
                    target = " ".join(rest_words[1:])
                else:
                    target = rest
            return ParsedCommand(verb="smelt", target=target, extra=fuel, count=max(1, count), raw=raw)

        # Placing: 'place crafting table', 'put down bed'
        if first in ("place", "put", "build", "set"):
            target = " ".join(words[1:])
            if target.startswith("down "):
                target = target[5:]
            return ParsedCommand(verb="place", target=target, raw=raw)

        # Equipping: 'equip iron sword', 'wear helmet', 'hold pickaxe'
        if first in ("equip", "wear", "wield", "hold"):
            target = " ".join(words[1:])
            return ParsedCommand(verb="equip", target=target, raw=raw)

        # Unequipping: 'unequip mainhand', 'take off helmet'
        if first in ("unequip", "remove"):
            target = " ".join(words[1:])
            return ParsedCommand(verb="unequip", target=target, raw=raw)
        if raw.lower().startswith("take off "):
            target = raw[9:].strip()
            return ParsedCommand(verb="unequip", target=target, raw=raw)

        # Eating: 'eat apple', 'eat steak', 'eat 3 steak', 'eat steak 2', 'eat all bread'
        if first in ("eat", "consume", "drink"):
            rest = words[1:]
            count = 1
            if not rest:
                return ParsedCommand(verb="eat", target="", count=1, raw=raw)
            if rest[0].isdigit():
                count = int(rest[0])
                target = " ".join(rest[1:])
            elif rest[-1].isdigit():
                count = int(rest[-1])
                target = " ".join(rest[:-1])
            elif rest[0].lower() in ("all", "max"):
                count = 999
                target = " ".join(rest[1:])
            elif rest[-1].lower() in ("all", "max"):
                count = 999
                target = " ".join(rest[:-1])
            else:
                target = " ".join(rest)
            return ParsedCommand(verb="eat", target=target, count=max(1, count), raw=raw)

        # Chest storage: 'store 5 coal', 'put 5 iron in chest'
        if first in ("store", "deposit"):
            rest = words[1:]
            count = 1
            if rest and rest[0].isdigit():
                count = int(rest[0])
                target = " ".join(rest[1:])
            else:
                target = " ".join(rest)
            return ParsedCommand(verb="chest_store", target=target, count=max(1, count), raw=raw)
        if raw.lower().startswith("put ") and " in chest" in raw.lower():
            mid = raw[4:raw.lower().index(" in chest")].strip().split()
            count = 1
            if mid and mid[0].isdigit():
                count = int(mid[0])
                target = " ".join(mid[1:])
            else:
                target = " ".join(mid)
            return ParsedCommand(verb="chest_store", target=target, count=max(1, count), raw=raw)

        # Chest take: 'take 5 coal from chest', 'withdraw 2 iron'
        if first in ("withdraw", "retrieve"):
            rest = words[1:]
            count = 1
            if rest and rest[0].isdigit():
                count = int(rest[0])
                target = " ".join(rest[1:])
            else:
                target = " ".join(rest)
            return ParsedCommand(verb="chest_take", target=target, count=max(1, count), raw=raw)
        if raw.lower().startswith("take ") and " from chest" in raw.lower():
            mid = raw[5:raw.lower().index(" from chest")].strip().split()
            count = 1
            if mid and mid[0].isdigit():
                count = int(mid[0])
                target = " ".join(mid[1:])
            else:
                target = " ".join(mid)
            return ParsedCommand(verb="chest_take", target=target, count=max(1, count), raw=raw)

        # Combat: 'attack zombie', 'hit creeper', 'kill spider', 'strike skeleton'
        if first in ("attack", "hit", "strike", "kill", "fight", "slay"):
            target = " ".join(words[1:])
            return ParsedCommand(verb="attack", target=target, raw=raw)

        # Shooting: 'shoot skeleton', 'shoot at creeper', 'fire bow'
        if first in ("shoot", "fire"):
            target = " ".join(words[1:])
            if target.startswith("at "):
                target = target[3:]
            return ParsedCommand(verb="shoot", target=target, raw=raw)

        # Save & Load
        if first in ("save", "quicksave"):
            name = words[1] if len(words) > 1 else "world"
            return ParsedCommand(verb="save", target=name, raw=raw)
        if first in ("load", "quickload"):
            name = words[1] if len(words) > 1 else "world"
            return ParsedCommand(verb="load", target=name, raw=raw)
        if first == "saves":
            return ParsedCommand(verb="saves", raw=raw)

        # Unrecognized fallback
        return ParsedCommand(verb="unknown", target=raw, raw=raw)
