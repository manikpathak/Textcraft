"""Biome definitions, natural resource distributions, and mob spawn tables."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class BiomeDef:
    id: str
    name: str
    description: str
    resource_weights: Dict[str, Tuple[int, int]]  # item_id -> (min_count, max_count)
    passive_mobs: List[str] = field(default_factory=list)
    hostile_mobs: List[str] = field(default_factory=list)
    temperature: float = 0.5                      # 0.0 cold to 1.0 hot
    rainfall: float = 0.5                         # 0.0 dry to 1.0 wet

BIOMES: Dict[str, BiomeDef] = {
    # Surface Biomes
    "plains": BiomeDef(
        id="plains",
        name="Sunlit Plains",
        description="Vast undulating grasslands dotted with wildflowers, tall grass, and occasional solitary oak trees.",
        resource_weights={
            "dirt": (10, 20),
            "oak_log": (4, 8),
            "leaves": (6, 12),
            "stone": (4, 10),
        },
        passive_mobs=["cow", "sheep", "pig", "chicken"],
        hostile_mobs=["zombie", "skeleton", "creeper", "spider"],
        temperature=0.8,
        rainfall=0.4,
    ),
    "forest": BiomeDef(
        id="forest",
        name="Oak Forest",
        description="A dense canopy of mature oak and birch trees. Sunbeams filter through the leaves onto mossy soil.",
        resource_weights={
            "oak_log": (12, 24),
            "leaves": (14, 28),
            "dirt": (8, 16),
            "stone": (4, 8),
        },
        passive_mobs=["cow", "pig", "chicken", "sheep"],
        hostile_mobs=["zombie", "skeleton", "creeper", "spider"],
        temperature=0.7,
        rainfall=0.8,
    ),
    "desert": BiomeDef(
        id="desert",
        name="Arid Desert",
        description="Rolling golden dunes of dry sand baking under an unrelenting sun. Occasional dead shrubs crackle in the breeze.",
        resource_weights={
            "sand": (20, 40),
            "sandstone": (6, 12),
            "stone": (2, 6),
        },
        passive_mobs=[],
        hostile_mobs=["zombie", "skeleton", "spider"],
        temperature=1.0,
        rainfall=0.0,
    ),
    "mountains": BiomeDef(
        id="mountains",
        name="Craggy Mountains",
        description="Towering peaks of exposed rock and gravel reaching high into the crisp mountain air. Exposed coal veins pierce the cliffs.",
        resource_weights={
            "stone": (20, 40),
            "gravel": (10, 20),
            "coal_ore": (4, 10),
            "iron_ore": (2, 6),
        },
        passive_mobs=["sheep"],
        hostile_mobs=["skeleton", "creeper", "spider"],
        temperature=0.2,
        rainfall=0.3,
    ),
    "swamp": BiomeDef(
        id="swamp",
        name="Murky Swamp",
        description="Still, brackish waters covered in lily pads, surrounded by weeping willow oaks draped with Spanish moss.",
        resource_weights={
            "dirt": (10, 20),
            "oak_log": (6, 14),
            "leaves": (8, 16),
            "stone": (2, 6),
        },
        passive_mobs=["pig", "chicken"],
        hostile_mobs=["zombie", "skeleton", "spider", "creeper"],
        temperature=0.6,
        rainfall=0.9,
    ),
    "jungle": BiomeDef(
        id="jungle",
        name="Dense Jungle",
        description="Towering tropical trees wrapped in twisting vines, bursting with dense foliage and vibrant exotic life.",
        resource_weights={
            "oak_log": (16, 32),
            "leaves": (18, 36),
            "dirt": (10, 20),
        },
        passive_mobs=["chicken", "pig"],
        hostile_mobs=["spider", "creeper", "skeleton"],
        temperature=0.9,
        rainfall=0.9,
    ),
    "snowy_tundra": BiomeDef(
        id="snowy_tundra",
        name="Snowy Tundra",
        description="A frigid expanse of powdered snow and icy winds under pale skies.",
        resource_weights={
            "dirt": (6, 12),
            "stone": (4, 8),
            "gravel": (4, 8),
        },
        passive_mobs=["sheep"],
        hostile_mobs=["skeleton", "zombie", "spider"],
        temperature=0.0,
        rainfall=0.5,
    ),

    # Underground / Cave Biomes
    "shallow_cave": BiomeDef(
        id="shallow_cave",
        name="Shallow Cavern",
        description="Echoing subterranean chamber where moisture drips from the stone ceiling. Veins of coal and iron glint in the dark.",
        resource_weights={
            "stone": (25, 45),
            "cobblestone": (10, 20),
            "gravel": (6, 12),
            "coal_ore": (4, 10),
            "iron_ore": (2, 6),
        },
        passive_mobs=[],
        hostile_mobs=["zombie", "skeleton", "spider", "creeper"],
        temperature=0.5,
        rainfall=0.5,
    ),
    "deep_cave": BiomeDef(
        id="deep_cave",
        name="Deep Cave Network",
        description="A vast, forbidding subterranean ravine. Distant magma glows beneath jagged crags where precious minerals rest.",
        resource_weights={
            "stone": (20, 40),
            "deepslate": (10, 25),
            "iron_ore": (4, 10),
            "gold_ore": (2, 6),
            "diamond_ore": (1, 3),
            "coal_ore": (3, 8),
        },
        passive_mobs=[],
        hostile_mobs=["zombie", "skeleton", "creeper", "spider", "enderman"],
        temperature=0.7,
        rainfall=0.2,
    ),
    "deepslate_cavern": BiomeDef(
        id="deepslate_cavern",
        name="Deepslate Cavern",
        description="The deepest hollows of the world, composed of pitch-black slate compressed by immense pressure. Diamonds twinkle in the abyss.",
        resource_weights={
            "deepslate": (30, 60),
            "diamond_ore": (2, 5),
            "gold_ore": (2, 6),
            "iron_ore": (3, 8),
            "obsidian": (1, 4),
        },
        passive_mobs=[],
        hostile_mobs=["creeper", "skeleton", "enderman", "zombie"],
        temperature=0.8,
        rainfall=0.1,
    ),

    # Nether Biomes
    "nether_wastes": BiomeDef(
        id="nether_wastes",
        name="Nether Wastes",
        description="An infernal cavern beneath a vaulted roof of netherrack, over vast seas of boiling incandescent lava.",
        resource_weights={
            "netherrack": (30, 60),
            "soul_sand": (10, 20),
        },
        passive_mobs=[],
        hostile_mobs=["blaze", "ghast"],
        temperature=1.0,
        rainfall=0.0,
    ),
    "nether_fortress": BiomeDef(
        id="nether_fortress",
        name="Nether Fortress",
        description="Monolithic corridors of dark nether brick bridging burning chasms. The smell of brimstone and blaze rods is suffocating.",
        resource_weights={
            "netherrack": (20, 40),
            "netherite_scrap": (1, 2),
        },
        passive_mobs=[],
        hostile_mobs=["blaze"],
        temperature=1.0,
        rainfall=0.0,
    ),

    # The End Biome
    "the_end_island": BiomeDef(
        id="the_end_island",
        name="The End Island",
        description="A desolate pale island floating in a starry cosmic void, ringed with towering obsidian pillars. Shadows whisper all around.",
        resource_weights={
            "obsidian": (10, 20),
        },
        passive_mobs=[],
        hostile_mobs=["enderman"],
        temperature=0.5,
        rainfall=0.0,
    ),
}
