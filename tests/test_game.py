"""End-to-end integration tests for Game mechanics, saving, loading, shelter, and combat."""

import os
import pytest
from textcraft.engine.game import Game
from textcraft.engine.save_system import SaveSystem
from textcraft.models.mob import MOB_TEMPLATES

def test_full_progression_workflow():
    game = Game(seed=999)
    loc = game.get_current_location()

    # Ensure some oak logs exist
    loc.resources["oak_log"] = 10

    # Mine oak log
    logs = game.mine("oak_log")
    assert any("You mined Oak Log" in line for line in logs)
    assert game.player.has_item("oak_log", 1)

    # Craft 4 planks
    game.craft("oak_planks", 1)
    assert game.player.has_item("oak_planks", 4)

    # Craft Crafting Table
    game.craft("crafting_table", 1)
    assert game.player.has_item("crafting_table", 1)

    # Place Crafting Table
    game.place("crafting_table")
    assert loc.has_crafting_table
    assert not game.player.has_item("crafting_table", 1)

def test_build_shelter_and_sleep():
    game = Game(seed=999)
    loc = game.get_current_location()

    # Give materials for shelter
    game.player.add_item("oak_planks", 12)
    logs = game.build_shelter()
    assert loc.has_shelter
    assert any("constructed a sturdy shelter" in line for line in logs)

    # Place bed
    loc.place_block("bed", 1)

    # Can't sleep during day
    logs = game.sleep()
    assert any("only sleep at night" in line for line in logs)

    # Set night time
    game.ticks = 14000  # night
    assert game.is_night
    logs = game.sleep()
    assert any("wake up refreshed" in line for line in logs)
    assert not game.is_night

def test_combat_interaction():
    game = Game(seed=999)
    loc = game.get_current_location()

    zombie = MOB_TEMPLATES["zombie"].clone()
    loc.mobs.append(zombie)

    # Equip sword
    game.player.add_item("diamond_sword", 1)
    game.player.equip("diamond_sword")

    # Attack zombie
    initial_hp = zombie.current_health
    logs = game.attack("zombie")
    assert any("You struck Zombie" in line for line in logs)
    assert zombie.current_health < initial_hp or not zombie.is_alive()

def test_nether_portal_creation_and_travel():
    game = Game(seed=999)
    loc = game.get_current_location()

    # Place 10 obsidian
    game.player.add_item("obsidian", 10)
    for _ in range(10):
        game.place("obsidian")

    assert loc.has_portal

    # Enter portal
    logs = game.enter_portal()
    assert game.current_dimension == "nether"
    assert any("Entering Nether" in line for line in logs)

def test_save_and_load():
    game = Game(seed=777)
    game.player.add_item("diamond", 5)
    game.player.health = 18
    game.move("north")

    save_path = SaveSystem.save_game(game, "test_save")
    assert os.path.exists(save_path)

    loaded_game = SaveSystem.load_game("test_save")
    assert loaded_game is not None
    assert loaded_game.seed == 777
    assert loaded_game.player.has_item("diamond", 5)
    assert loaded_game.player.health == game.player.health
    assert loaded_game.current_coords == game.current_coords

    # Clean up test save
    if os.path.exists(save_path):
        os.remove(save_path)
