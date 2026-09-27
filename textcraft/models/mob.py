"""Mob models, passive/hostile behaviors, loot tables, and mob registry."""

import random
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional

@dataclass
class LootDrop:
    item_id: str
    min_count: int
    max_count: int
    chance: float = 1.0

@dataclass
class Mob:
    id: str
    name: str
    max_health: int
    attack_damage: int = 0
    is_hostile: bool = False
    is_boss: bool = False
    burns_in_daylight: bool = False
    attack_verb: str = "attacks"
    description: str = ""
    current_health: int = 0
    loot_drops: List[LootDrop] = field(default_factory=list)
    fuse: Optional[int] = None       # Creeper countdown
    xp_reward: int = 5

    def __post_init__(self):
        if self.current_health <= 0:
            self.current_health = self.max_health

    def is_alive(self) -> bool:
        return self.current_health > 0

    def take_damage(self, amount: int) -> int:
        actual = min(self.current_health, amount)
        self.current_health -= actual
        return actual

    def roll_loot(self) -> List[Tuple[str, int]]:
        drops = []
        for drop in self.loot_drops:
            if random.random() <= drop.chance:
                count = random.randint(drop.min_count, drop.max_count)
                if count > 0:
                    drops.append((drop.item_id, count))
        return drops

    def clone(self) -> "Mob":
        return Mob(
            id=self.id,
            name=self.name,
            max_health=self.max_health,
            current_health=self.max_health,
            attack_damage=self.attack_damage,
            is_hostile=self.is_hostile,
            is_boss=self.is_boss,
            burns_in_daylight=self.burns_in_daylight,
            attack_verb=self.attack_verb,
            description=self.description,
            loot_drops=list(self.loot_drops),
            fuse=self.fuse,
            xp_reward=self.xp_reward,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "current_health": self.current_health,
            "max_health": self.max_health,
            "fuse": self.fuse,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Mob":
        base = MOB_TEMPLATES.get(data["id"])
        if base:
            mob = base.clone()
            mob.current_health = data.get("current_health", mob.max_health)
            mob.fuse = data.get("fuse")
            return mob
        return Mob(id=data["id"], name=data.get("name", "Unknown Mob"), max_health=10, current_health=10)


MOB_TEMPLATES: Dict[str, Mob] = {
    # Passive Mobs
    "cow": Mob(
        id="cow",
        name="Cow",
        max_health=10,
        attack_damage=0,
        is_hostile=False,
        description="A peaceful spotted bovine grazing contentedly.",
        loot_drops=[
            LootDrop("raw_beef", 1, 3, 1.0),
            LootDrop("leather", 0, 2, 0.8),
        ],
        xp_reward=2
    ),
    "sheep": Mob(
        id="sheep",
        name="Sheep",
        max_health=8,
        attack_damage=0,
        is_hostile=False,
        description="A gentle sheep with fluffy white fleece.",
        loot_drops=[
            LootDrop("raw_mutton", 1, 2, 1.0),
            LootDrop("wool", 1, 1, 1.0),
        ],
        xp_reward=2
    ),
    "pig": Mob(
        id="pig",
        name="Pig",
        max_health=10,
        attack_damage=0,
        is_hostile=False,
        description="A pink pig trotting around and oinking softly.",
        loot_drops=[
            LootDrop("raw_porkchop", 1, 3, 1.0),
        ],
        xp_reward=2
    ),
    "chicken": Mob(
        id="chicken",
        name="Chicken",
        max_health=4,
        attack_damage=0,
        is_hostile=False,
        description="A small white chicken clucking and pecking at the grass.",
        loot_drops=[
            LootDrop("raw_chicken", 1, 1, 1.0),
            LootDrop("feather", 1, 2, 0.8),
        ],
        xp_reward=1
    ),

    # Hostile Overworld Mobs
    "zombie": Mob(
        id="zombie",
        name="Zombie",
        max_health=20,
        attack_damage=3,
        is_hostile=True,
        burns_in_daylight=True,
        attack_verb="groans and claws at",
        description="A rotting undead corpse with outstretched arms.",
        loot_drops=[
            LootDrop("rotten_flesh", 1, 2, 1.0),
            LootDrop("raw_iron", 1, 1, 0.1),
        ],
        xp_reward=5
    ),
    "skeleton": Mob(
        id="skeleton",
        name="Skeleton",
        max_health=20,
        attack_damage=4,
        is_hostile=True,
        burns_in_daylight=True,
        attack_verb="draws its bow and shoots an arrow at",
        description="An ominous clattering animated skeleton wielding a recurve bow.",
        loot_drops=[
            LootDrop("bone", 1, 2, 1.0),
            LootDrop("arrow", 1, 3, 0.8),
            LootDrop("bow", 1, 1, 0.1),
        ],
        xp_reward=5
    ),
    "creeper": Mob(
        id="creeper",
        name="Creeper",
        max_health=20,
        attack_damage=14,
        is_hostile=True,
        burns_in_daylight=False,
        attack_verb="hisses violently and prepares to detonate",
        description="A stealthy green creature that trembles with volatile explosive fury!",
        fuse=3,  # Counts down 3 -> 2 -> 1 -> BOOM!
        loot_drops=[],
        xp_reward=5
    ),
    "spider": Mob(
        id="spider",
        name="Spider",
        max_health=16,
        attack_damage=2,
        is_hostile=True,
        burns_in_daylight=False,
        attack_verb="pounces and bites",
        description="A giant eight-legged arachnid with piercing crimson eyes.",
        loot_drops=[
            LootDrop("string", 1, 2, 1.0),
        ],
        xp_reward=5
    ),
    "enderman": Mob(
        id="enderman",
        name="Enderman",
        max_health=40,
        attack_damage=7,
        is_hostile=True,
        burns_in_daylight=False,
        attack_verb="teleports and fiercely strikes",
        description="A tall, shadowy entity vibrating with purple void particles.",
        loot_drops=[
            LootDrop("ender_pearl", 1, 1, 0.8),
        ],
        xp_reward=10
    ),

    # Nether Mobs
    "blaze": Mob(
        id="blaze",
        name="Blaze",
        max_health=20,
        attack_damage=5,
        is_hostile=True,
        burns_in_daylight=False,
        attack_verb="hurls scorching fireballs at",
        description="A hovering infernal core surrounded by spinning flaming rods.",
        loot_drops=[
            LootDrop("blaze_rod", 1, 2, 0.9),
        ],
        xp_reward=10
    ),

    # Boss Mob - Ender Dragon
    "ender_dragon": Mob(
        id="ender_dragon",
        name="Ender Dragon",
        max_health=200,
        attack_damage=10,
        is_hostile=True,
        is_boss=True,
        burns_in_daylight=False,
        attack_verb="swoops down with terrifying fury and breathes dragon breath at",
        description="The colossal ruler of The End, an immense dragon of obsidian scales and purple glowing eyes!",
        loot_drops=[],
        xp_reward=100
    )
}
