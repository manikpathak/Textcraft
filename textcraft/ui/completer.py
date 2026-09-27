"""Prompt-toolkit autocomplete completer for smooth in-game typing."""

from typing import Iterable
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

from textcraft.models.item import ITEM_REGISTRY
from textcraft.models.recipe import RECIPES

COMMAND_VERBS = [
    "north", "south", "east", "west", "up", "down",
    "look", "inventory", "map", "status", "time", "recipes",
    "mine", "chop", "dig", "craft", "smelt", "place", "build shelter",
    "equip", "unequip", "eat", "attack", "shoot", "block", "sleep",
    "enter portal", "store", "take", "save", "load", "help", "quit"
]

class TextcraftCompleter(Completer):
    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        words = text.split()

        if len(words) == 0:
            for cmd in COMMAND_VERBS:
                yield Completion(cmd, start_position=0)
            return

        first_word = words[0].lower()
        word_before_cursor = document.get_word_before_cursor()

        # Completing the first word
        if len(words) == 1 and not text.endswith(" "):
            for cmd in COMMAND_VERBS:
                if cmd.lower().startswith(first_word):
                    yield Completion(cmd, start_position=-len(first_word))
            return

        # Completing arguments based on verb
        if first_word in ("craft", "recipe"):
            for rec in RECIPES:
                if rec.result_id.startswith(word_before_cursor.lower()):
                    yield Completion(rec.result_id, start_position=-len(word_before_cursor))
        elif first_word in ("mine", "chop", "dig", "harvest"):
            common_blocks = ["oak_log", "dirt", "stone", "coal_ore", "iron_ore", "gold_ore", "diamond_ore", "sand", "gravel", "deepslate", "obsidian"]
            for block in common_blocks:
                if block.startswith(word_before_cursor.lower()):
                    yield Completion(block, start_position=-len(word_before_cursor))
        elif first_word in ("equip", "place", "store", "take"):
            for item_id in ITEM_REGISTRY.keys():
                if item_id.startswith(word_before_cursor.lower()):
                    yield Completion(item_id, start_position=-len(word_before_cursor))
        elif first_word == "unequip":
            for slot in ["mainhand", "offhand", "helmet", "chestplate", "leggings", "boots"]:
                if slot.startswith(word_before_cursor.lower()):
                    yield Completion(slot, start_position=-len(word_before_cursor))
        elif first_word in ("attack", "shoot"):
            for mob_name in ["zombie", "skeleton", "creeper", "spider", "enderman", "cow", "sheep", "pig", "chicken", "blaze", "ghast", "ender_dragon"]:
                if mob_name.startswith(word_before_cursor.lower()):
                    yield Completion(mob_name, start_position=-len(word_before_cursor))
        elif first_word == "eat":
            for item_id, item_def in ITEM_REGISTRY.items():
                if item_def.is_food and item_id.startswith(word_before_cursor.lower()):
                    yield Completion(item_id, start_position=-len(word_before_cursor))
