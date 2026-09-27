"""Procedural world generator creating deterministic biomes, resources, and mobs."""

import hashlib
import random
from typing import Dict, Tuple
from textcraft.config import (
    DIMENSION_OVERWORLD, DIMENSION_NETHER, DIMENSION_END
)
from textcraft.models.location import Location
from textcraft.models.mob import MOB_TEMPLATES
from textcraft.world.biomes import BIOMES

class WorldGenerator:
    def __init__(self, seed: int = 1337):
        self.seed = seed

    def _coord_hash(self, x: int, y: int, z: int, dimension: str, extra: str = "") -> int:
        """Produces a deterministic 32-bit integer for a given coordinate."""
        raw = f"{self.seed}:{dimension}:{x}:{y}:{z}:{extra}"
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return int(digest[:8], 16)

    def determine_biome_id(self, x: int, y: int, z: int, dimension: str) -> str:
        if dimension == DIMENSION_NETHER:
            h = self._coord_hash(x, y, z, dimension, "biome")
            return "nether_fortress" if (h % 5 == 0) else "nether_wastes"

        if dimension == DIMENSION_END:
            return "the_end_island"

        # Overworld
        if y <= -1:
            return "deepslate_cavern"
        elif y <= 32:
            return "deep_cave"
        elif y < 64:
            return "shallow_cave"

        # Surface (y >= 64)
        if x == 0 and z == 0:
            return "plains"  # Always start at friendly plains

        # Surface biome selector based on pseudo-noise
        h = self._coord_hash(x, 64, z, dimension, "biome")
        surface_biomes = ["plains", "forest", "desert", "mountains", "swamp", "jungle", "snowy_tundra"]
        # Weight towards plains & forest
        weights = [25, 25, 12, 12, 10, 8, 8]
        idx = h % sum(weights)
        accum = 0
        for b_name, w in zip(surface_biomes, weights):
            accum += w
            if idx < accum:
                return b_name
        return "plains"

    def generate_location(self, x: int, y: int, z: int, dimension: str, is_night: bool = False) -> Location:
        biome_id = self.determine_biome_id(x, y, z, dimension)
        biome_def = BIOMES.get(biome_id, BIOMES["plains"])

        loc = Location(
            x=x,
            y=y,
            z=z,
            dimension=dimension,
            biome=biome_id,
            title=biome_def.name,
            description=biome_def.description,
        )

        # Roll resources deterministically
        rng = random.Random(self._coord_hash(x, y, z, dimension, "resources"))
        for res_id, (min_c, max_c) in biome_def.resource_weights.items():
            count = rng.randint(min_c, max_c)
            if count > 0:
                loc.resources[res_id] = count

        # Boss at (0, 0) in The End
        if dimension == DIMENSION_END and x == 0 and z == 0:
            loc.title = "The Dragon's Nest"
            loc.description = (
                "A colossal central pillar of obsidian rises into the twilight. "
                "The Ender Dragon circles above, its wings whipping vortexes of void dust!"
            )
            loc.mobs.append(MOB_TEMPLATES["ender_dragon"].clone())
            return loc

        # Nether Portal at spawn if visited
        # Roll initial mobs
        mob_rng = random.Random(self._coord_hash(x, y, z, dimension, "mobs"))
        if dimension == DIMENSION_OVERWORLD and y >= 64:
            if not is_night and biome_def.passive_mobs:
                # Daytime: spawn 1-2 passive animals
                mob_type = mob_rng.choice(biome_def.passive_mobs)
                mob_count = mob_rng.randint(1, 2)
                for _ in range(mob_count):
                    loc.mobs.append(MOB_TEMPLATES[mob_type].clone())
            elif is_night and biome_def.hostile_mobs:
                # Nighttime: spawn 1 hostile mob
                mob_type = mob_rng.choice(biome_def.hostile_mobs)
                loc.mobs.append(MOB_TEMPLATES[mob_type].clone())
        elif y < 64 or dimension != DIMENSION_OVERWORLD:
            # Underground or other dimensions: hostile mobs
            if biome_def.hostile_mobs and mob_rng.random() < 0.65:
                mob_type = mob_rng.choice(biome_def.hostile_mobs)
                loc.mobs.append(MOB_TEMPLATES[mob_type].clone())

        return loc
