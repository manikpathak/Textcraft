"""Location (World Tile) model tracking biomes, resources, placed blocks, chests, and mobs."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from textcraft.models.mob import Mob
from textcraft.config import DIMENSION_OVERWORLD

@dataclass
class Location:
    x: int
    y: int
    z: int
    dimension: str = DIMENSION_OVERWORLD
    biome: str = "plains"
    title: str = "Grassy Plains"
    description: str = ""
    resources: Dict[str, int] = field(default_factory=dict)
    placed_blocks: Dict[str, int] = field(default_factory=dict)
    chest_inventory: Dict[str, int] = field(default_factory=dict)
    mobs: List[Mob] = field(default_factory=list)
    has_shelter: bool = False
    has_portal: bool = False
    visited: bool = False

    @property
    def key(self) -> str:
        return f"{self.dimension}:{self.x},{self.y},{self.z}"

    @property
    def has_crafting_table(self) -> bool:
        return self.placed_blocks.get("crafting_table", 0) > 0

    @property
    def has_furnace(self) -> bool:
        return self.placed_blocks.get("furnace", 0) > 0

    @property
    def has_chest(self) -> bool:
        return self.placed_blocks.get("chest", 0) > 0

    @property
    def has_bed(self) -> bool:
        return self.placed_blocks.get("bed", 0) > 0

    @property
    def is_lit(self) -> bool:
        return self.placed_blocks.get("torch", 0) > 0

    def harvest_resource(self, block_id: str, count: int = 1) -> bool:
        current = self.resources.get(block_id, 0)
        if current < count:
            return False
        if current == count:
            del self.resources[block_id]
        else:
            self.resources[block_id] = current - count
        return True

    def place_block(self, block_id: str, count: int = 1) -> None:
        self.placed_blocks[block_id] = self.placed_blocks.get(block_id, 0) + count

    def remove_placed_block(self, block_id: str, count: int = 1) -> bool:
        current = self.placed_blocks.get(block_id, 0)
        if current < count:
            return False
        if current == count:
            del self.placed_blocks[block_id]
        else:
            self.placed_blocks[block_id] = current - count
        return True

    def find_mob(self, mob_query: str) -> Optional[Mob]:
        query = mob_query.lower().strip()
        for mob in self.mobs:
            if query in mob.id.lower() or query in mob.name.lower():
                return mob
        return None

    def remove_mob(self, mob: Mob) -> None:
        if mob in self.mobs:
            self.mobs.remove(mob)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "dimension": self.dimension,
            "biome": self.biome,
            "title": self.title,
            "description": self.description,
            "resources": dict(self.resources),
            "placed_blocks": dict(self.placed_blocks),
            "chest_inventory": dict(self.chest_inventory),
            "mobs": [m.to_dict() for m in self.mobs],
            "has_shelter": self.has_shelter,
            "has_portal": self.has_portal,
            "visited": self.visited,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Location":
        loc = cls(
            x=data["x"],
            y=data["y"],
            z=data["z"],
            dimension=data.get("dimension", DIMENSION_OVERWORLD),
            biome=data.get("biome", "plains"),
            title=data.get("title", "Plains"),
            description=data.get("description", ""),
            resources=data.get("resources", {}),
            placed_blocks=data.get("placed_blocks", {}),
            chest_inventory=data.get("chest_inventory", {}),
            has_shelter=data.get("has_shelter", False),
            has_portal=data.get("has_portal", False),
            visited=data.get("visited", False),
        )
        for mob_data in data.get("mobs", []):
            loc.mobs.append(Mob.from_dict(mob_data))
        return loc
