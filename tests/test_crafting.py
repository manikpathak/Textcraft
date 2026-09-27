"""Tests for crafting and smelting recipe verification."""

import pytest
from textcraft.engine.game import Game
from textcraft.models.recipe import RECIPES, SMELTING_RECIPES, find_recipes_for

def test_recipes_registry_validity():
    assert len(RECIPES) > 20
    assert len(SMELTING_RECIPES) >= 10

    # Ensure wood to planks exists
    plank_rec = find_recipes_for("oak_planks")
    assert len(plank_rec) >= 1
    assert plank_rec[0].result_count == 4
    assert plank_rec[0].ingredients == {"oak_log": 1}

def test_game_crafting_workflow():
    g = Game(seed=42)
    # Give player 1 log
    g.player.add_item("oak_log", 1)

    # Craft 4 planks
    logs = g.craft("oak_planks", count=1)
    assert g.player.inventory.get("oak_planks") == 4
    assert not g.player.has_item("oak_log", 1)

    # Craft crafting table (needs 4 planks)
    logs = g.craft("crafting_table", count=1)
    assert g.player.inventory.get("crafting_table") == 1
    assert not g.player.has_item("oak_planks", 1)

    # Try to craft wooden pickaxe without placing table or having planks
    logs = g.craft("wooden_pickaxe")
    assert "Not enough materials" in logs[0] or "requires a Crafting Table" in logs[0]

def test_smelting_workflow():
    g = Game(seed=42)
    loc = g.get_current_location()

    # Attempt to smelt without furnace placed
    g.player.add_item("raw_iron", 2)
    g.player.add_item("coal", 1)
    logs = g.smelt("raw_iron", count=2)
    assert "There is no Furnace here" in logs[0]

    # Place furnace
    loc.place_block("furnace", 1)
    logs = g.smelt("raw_iron", fuel_query="coal", count=2)
    assert g.player.inventory.get("iron_ingot") == 2
    assert not g.player.has_item("raw_iron", 1)
    assert not g.player.has_item("coal", 1)

def test_hoe_crafting_and_equipping():
    g = Game(seed=42)
    loc = g.get_current_location()
    loc.place_block("crafting_table", 1)

    # Give resources for wooden hoe: 2 planks, 2 sticks
    g.player.add_item("oak_planks", 2)
    g.player.add_item("stick", 2)

    logs = g.craft("wooden_hoe", count=1)
    assert any("crafted" in log.lower() for log in logs)
    assert g.player.has_item("wooden_hoe", 1)

    # Equip the hoe
    ok, msg = g.player.equip("wooden_hoe")
    assert ok
    assert g.player.equipment["mainhand"] is not None
    assert g.player.equipment["mainhand"].id == "wooden_hoe"
    assert g.player.tool_type == "hoe"

