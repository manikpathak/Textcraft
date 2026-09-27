"""Tests for Player state, inventory, equipment, armor, and survival metabolism."""

import pytest
from textcraft.models.player import Player
from textcraft.models.item import Item

def test_player_initial_state():
    p = Player()
    assert p.health == 20
    assert p.max_health == 20
    assert p.hunger == 20.0
    assert p.is_alive
    assert p.total_armor == 0
    assert p.attack_damage == 1

def test_player_inventory_operations():
    p = Player()
    p.add_item("oak_log", 4)
    assert p.has_item("oak_log", 4)
    assert p.has_item("oak_log", 3)
    assert not p.has_item("oak_log", 5)

    assert p.remove_item("oak_log", 2)
    assert p.inventory["oak_log"] == 2

    assert not p.remove_item("oak_log", 5)
    assert p.inventory["oak_log"] == 2

    assert p.remove_item("oak_log", 2)
    assert "oak_log" not in p.inventory

def test_player_equipment_and_armor():
    p = Player()
    p.add_item("diamond_chestplate", 1)
    p.add_item("diamond_sword", 1)

    ok, msg = p.equip("diamond_chestplate")
    assert ok
    assert p.equipment["chestplate"] is not None
    assert p.equipment["chestplate"].id == "diamond_chestplate"
    assert p.total_armor == 8
    assert not p.has_item("diamond_chestplate", 1)

    ok, msg = p.equip("diamond_sword")
    assert ok
    assert p.equipment["mainhand"] is not None
    assert p.attack_damage == 7

    # Unequip
    ok, msg = p.unequip("chestplate")
    assert ok
    assert p.equipment["chestplate"] is None
    assert p.total_armor == 0
    assert p.has_item("diamond_chestplate", 1)

def test_player_eating_and_hunger():
    p = Player()
    p.hunger = 10.0
    p.add_item("steak", 1)

    ok, msg = p.eat("steak")
    assert ok
    assert p.hunger == 18.0
    assert not p.has_item("steak", 1)

def test_player_eating_multiple_portions():
    p = Player()
    p.hunger = 8.0
    # Add 5 apples (apple restores 4 hunger)
    p.add_item("apple", 5)

    # Eat 2 apples: restores 8 hunger -> hunger = 16.0
    ok, msg = p.eat("apple", count=2)
    assert ok
    assert "2x Apple" in msg
    assert p.hunger == 16.0
    assert p.inventory["apple"] == 3

    # Eat 3 apples: 1 apple brings hunger to 20.0 (full), so stops early eating only 1 apple!
    ok, msg = p.eat("apple", count=3)
    assert ok
    assert "1x Apple" in msg
    assert "hunger reached maximum" in msg
    assert p.hunger == 20.0
    assert p.inventory["apple"] == 2

    # Attempt to eat while full
    ok, msg = p.eat("apple", count=1)
    assert not ok
    assert "completely full" in msg


def test_player_damage_and_armor_absorption():
    p = Player()
    p.add_item("diamond_chestplate", 1)
    p.equip("diamond_chestplate")

    # With diamond chestplate (8 armor points = 32% damage reduction)
    dealt = p.take_damage(10)
    assert dealt < 10
    assert p.health == 20 - dealt

def test_player_xp_and_level_up():
    p = Player()
    assert p.level == 0
    # Level 1 requires 10 XP
    leveled = p.add_xp(15)
    assert leveled
    assert p.level == 1
    assert p.xp == 5
