"""Tests for CommandParser natural language parsing and argument extraction."""

import pytest
from textcraft.engine.parser import CommandParser

def test_direction_shortcuts():
    assert CommandParser.parse("n").verb == "move"
    assert CommandParser.parse("n").target == "north"

    assert CommandParser.parse("south").verb == "move"
    assert CommandParser.parse("south").target == "south"

    assert CommandParser.parse("go east").verb == "move"
    assert CommandParser.parse("go east").target == "east"

    assert CommandParser.parse("d").verb == "move"
    assert CommandParser.parse("d").target == "down"

    assert CommandParser.parse("dig down").verb == "move"
    assert CommandParser.parse("dig down").target == "down"

    assert CommandParser.parse("u").verb == "move"
    assert CommandParser.parse("u").target == "up"

def test_mining_commands():
    cmd = CommandParser.parse("mine oak log")
    assert cmd.verb == "mine"
    assert cmd.target == "oak log"

    cmd2 = CommandParser.parse("chop tree")
    assert cmd2.verb == "mine"
    assert cmd2.target == "oak_log"

def test_crafting_commands():
    cmd = CommandParser.parse("craft 4 torch")
    assert cmd.verb == "craft"
    assert cmd.target == "torch"
    assert cmd.count == 4

    cmd2 = CommandParser.parse("craft wooden_pickaxe")
    assert cmd2.verb == "craft"
    assert cmd2.target == "wooden_pickaxe"
    assert cmd2.count == 1

def test_smelting_commands():
    cmd = CommandParser.parse("smelt 3 raw_iron with coal")
    assert cmd.verb == "smelt"
    assert cmd.target == "raw_iron"
    assert cmd.extra == "coal"
    assert cmd.count == 3

def test_combat_commands():
    cmd = CommandParser.parse("attack zombie")
    assert cmd.verb == "attack"
    assert cmd.target == "zombie"

    cmd2 = CommandParser.parse("shoot at skeleton")
    assert cmd2.verb == "shoot"
    assert cmd2.target == "skeleton"

    cmd3 = CommandParser.parse("block")
    assert cmd3.verb == "block"
