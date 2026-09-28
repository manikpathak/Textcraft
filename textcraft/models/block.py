"""Block definitions, harvest requirements, drops, and functional block types."""

from dataclasses import dataclass
from typing import Optional, Dict
from textcraft.config import (
    TIER_HAND, TIER_WOOD, TIER_STONE, TIER_IRON, TIER_DIAMOND
)

@dataclass
class Block:
    id: str
    name: str
    harvest_tool: Optional[str] = None      # "pickaxe", "axe", "shovel"
    tool_required: bool = False             # If True, proper tool is strictly required to get drops
    min_tool_tier: int = TIER_HAND          # minimum tier needed to get drop
    drop_item_id: str = ""
    drop_count: int = 1
    xp_reward: int = 0
    is_solid: bool = True
    is_interactive: bool = False            # True for chests, furnaces, crafting tables, beds
    description: str = ""
    hardness: float = 1.0                   # Mining time multiplier; ticks = max(200, hardness * 1000 / effective_speed)

    def can_harvest_with(self, tool_type: Optional[str], tool_tier: int) -> bool:
        if not self.tool_required:
            return True
        if self.harvest_tool is not None and tool_type != self.harvest_tool:
            return False
        return tool_tier >= self.min_tool_tier

BLOCK_REGISTRY: Dict[str, Block] = {
    "oak_log": Block("oak_log", "Oak Log", harvest_tool="axe", tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="oak_log", hardness=2.0, description="Sturdy oak tree trunk."),
    "leaves": Block("leaves", "Leaves", harvest_tool=None, tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="apple", drop_count=1, hardness=0.2, description="Lush foliage with occasional hanging apples."),
    "dirt": Block("dirt", "Dirt", harvest_tool="shovel", tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="dirt", hardness=0.5, description="Soft brown earth."),
    "sand": Block("sand", "Sand", harvest_tool="shovel", tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="sand", hardness=0.5, description="Golden grains of sand."),
    "gravel": Block("gravel", "Gravel", harvest_tool="shovel", tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="gravel", hardness=0.6, description="Coarse pebbles that might contain flint."),
    "stone": Block("stone", "Stone", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_WOOD, drop_item_id="cobblestone", hardness=1.5, description="Solid natural bedrock."),
    "cobblestone": Block("cobblestone", "Cobblestone", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_WOOD, drop_item_id="cobblestone", hardness=1.5, description="Rough cobblestone."),
    "coal_ore": Block("coal_ore", "Coal Ore", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_WOOD, drop_item_id="coal", xp_reward=2, hardness=3.0, description="Stone veined with combustible black coal."),
    "iron_ore": Block("iron_ore", "Iron Ore", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_STONE, drop_item_id="raw_iron", xp_reward=1, hardness=3.0, description="Rock streaked with valuable raw iron seams."),
    "gold_ore": Block("gold_ore", "Gold Ore", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_IRON, drop_item_id="raw_gold", xp_reward=3, hardness=3.0, description="Glittering veins of raw gold embedded in stone."),
    "diamond_ore": Block("diamond_ore", "Diamond Ore", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_IRON, drop_item_id="diamond", xp_reward=7, hardness=3.0, description="Precious deep ore shimmering with azure diamonds!"),
    "deepslate": Block("deepslate", "Deepslate", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_WOOD, drop_item_id="deepslate", hardness=3.5, description="Dense, dark slate from profound depths."),
    "obsidian": Block("obsidian", "Obsidian", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_DIAMOND, drop_item_id="obsidian", hardness=50.0, description="Purple-black volcanic glass with immense hardness."),
    "netherrack": Block("netherrack", "Netherrack", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_WOOD, drop_item_id="netherrack", hardness=0.4, description="Flammable red stone of the Underworld."),
    "crafting_table": Block("crafting_table", "Crafting Table", harvest_tool="axe", tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="crafting_table", hardness=2.5, is_interactive=True, description="Workbench with a 3x3 crafting grid."),
    "furnace": Block("furnace", "Furnace", harvest_tool="pickaxe", tool_required=True, min_tool_tier=TIER_WOOD, drop_item_id="furnace", hardness=3.5, is_interactive=True, description="Cobblestone kiln for smelting ores and cooking meals."),
    "chest": Block("chest", "Chest", harvest_tool="axe", tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="chest", hardness=2.5, is_interactive=True, description="Secure container for stashing items."),
    "bed": Block("bed", "Bed", harvest_tool=None, tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="bed", hardness=0.2, is_interactive=True, description="Cozy bed for sleeping through the perilous night."),
    "torch": Block("torch", "Torch", harvest_tool=None, tool_required=False, min_tool_tier=TIER_HAND, drop_item_id="torch", hardness=0.0, is_interactive=False, description="Flickering torch illuminating the area and deterring monsters."),
}

