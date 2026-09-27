"""Tests for procedural world generation, biomes, depth layers, and dimension logic."""

import pytest
from textcraft.world.generator import WorldGenerator
from textcraft.world.dimensions import get_portal_destination
from textcraft.config import DIMENSION_OVERWORLD, DIMENSION_NETHER, DIMENSION_END

def test_spawn_location():
    gen = WorldGenerator(seed=12345)
    loc = gen.generate_location(0, 64, 0, DIMENSION_OVERWORLD)
    assert loc.biome == "plains"
    assert loc.x == 0 and loc.y == 64 and loc.z == 0
    assert "dirt" in loc.resources or "oak_log" in loc.resources

def test_underground_layers():
    gen = WorldGenerator(seed=12345)
    loc_shallow = gen.generate_location(5, 48, 5, DIMENSION_OVERWORLD)
    assert loc_shallow.biome == "shallow_cave"

    loc_deep = gen.generate_location(5, 16, 5, DIMENSION_OVERWORLD)
    assert loc_deep.biome == "deep_cave"

    loc_deepslate = gen.generate_location(5, -32, 5, DIMENSION_OVERWORLD)
    assert loc_deepslate.biome == "deepslate_cavern"

def test_nether_generation():
    gen = WorldGenerator(seed=12345)
    loc_nether = gen.generate_location(10, 64, 10, DIMENSION_NETHER)
    assert loc_nether.biome in ("nether_wastes", "nether_fortress")
    assert "netherrack" in loc_nether.resources

def test_portal_coordinate_scaling():
    dest_dim, coords = get_portal_destination(DIMENSION_OVERWORLD, (80, 64, -160))
    assert dest_dim == DIMENSION_NETHER
    assert coords == (10, 64, -20)

    dest_dim_2, coords_2 = get_portal_destination(DIMENSION_NETHER, (10, 64, -20))
    assert dest_dim_2 == DIMENSION_OVERWORLD
    assert coords_2 == (80, 64, -160)
