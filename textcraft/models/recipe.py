"""Crafting and smelting recipe definitions and helper lookups."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class Recipe:
    result_id: str
    result_count: int
    ingredients: Dict[str, int]
    requires_crafting_table: bool = False
    category: str = "general"
    description: str = ""

@dataclass
class SmeltRecipe:
    input_id: str
    output_id: str
    xp: float = 0.7

RECIPES: List[Recipe] = [
    # Basic 2x2 Crafting
    Recipe("oak_planks", 4, {"oak_log": 1}, requires_crafting_table=False, category="materials", description="Craft 4 wooden planks from 1 log."),
    Recipe("stick", 4, {"oak_planks": 2}, requires_crafting_table=False, category="materials", description="Craft 4 sticks from 2 planks."),
    Recipe("crafting_table", 1, {"oak_planks": 4}, requires_crafting_table=False, category="utilities", description="Craft a 3x3 workbench."),
    Recipe("torch", 4, {"coal": 1, "stick": 1}, requires_crafting_table=False, category="utilities", description="Craft 4 illumination torches."),
    Recipe("torch", 4, {"charcoal": 1, "stick": 1}, requires_crafting_table=False, category="utilities", description="Craft 4 illumination torches from charcoal."),
    Recipe("flint_and_steel", 1, {"flint": 1, "iron_ingot": 1}, requires_crafting_table=False, category="utilities", description="Fire starter and portal igniter."),
    Recipe("blaze_powder", 2, {"blaze_rod": 1}, requires_crafting_table=False, category="materials", description="Grind blaze rod into powder."),
    Recipe("eye_of_ender", 1, {"ender_pearl": 1, "blaze_powder": 1}, requires_crafting_table=False, category="utilities", description="Craft an eye of ender."),

    # 3x3 Workstation / Storage
    Recipe("furnace", 1, {"cobblestone": 8}, requires_crafting_table=True, category="utilities", description="Smelting furnace."),
    Recipe("chest", 1, {"oak_planks": 8}, requires_crafting_table=True, category="utilities", description="Storage chest."),
    Recipe("bed", 1, {"wool": 3, "oak_planks": 3}, requires_crafting_table=True, category="utilities", description="Bed to sleep through the night."),
    Recipe("bucket", 1, {"iron_ingot": 3}, requires_crafting_table=True, category="utilities", description="Iron bucket for water or lava."),
    Recipe("shield", 1, {"iron_ingot": 1, "oak_planks": 6}, requires_crafting_table=True, category="armor", description="Defensive shield."),

    # Wooden Tools & Weapons
    Recipe("wooden_pickaxe", 1, {"oak_planks": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Basic wooden pickaxe."),
    Recipe("wooden_axe", 1, {"oak_planks": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Basic wooden axe."),
    Recipe("wooden_sword", 1, {"oak_planks": 2, "stick": 1}, requires_crafting_table=False, category="weapons", description="Basic wooden sword."),
    Recipe("wooden_shovel", 1, {"oak_planks": 1, "stick": 2}, requires_crafting_table=True, category="tools", description="Wooden shovel."),

    # Stone Tools & Weapons
    Recipe("stone_pickaxe", 1, {"cobblestone": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Stone pickaxe for iron/coal."),
    Recipe("stone_axe", 1, {"cobblestone": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Durable stone axe."),
    Recipe("stone_sword", 1, {"cobblestone": 2, "stick": 1}, requires_crafting_table=False, category="weapons", description="Stone sword."),
    Recipe("stone_shovel", 1, {"cobblestone": 1, "stick": 2}, requires_crafting_table=True, category="tools", description="Stone shovel."),

    # Iron Tools & Weapons
    Recipe("iron_pickaxe", 1, {"iron_ingot": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Iron pickaxe for gold/diamond."),
    Recipe("iron_axe", 1, {"iron_ingot": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Sharp iron axe."),
    Recipe("iron_sword", 1, {"iron_ingot": 2, "stick": 1}, requires_crafting_table=True, category="weapons", description="Iron sword."),
    Recipe("iron_shovel", 1, {"iron_ingot": 1, "stick": 2}, requires_crafting_table=True, category="tools", description="Iron shovel."),

    # Diamond Tools & Weapons
    Recipe("diamond_pickaxe", 1, {"diamond": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Diamond pickaxe for obsidian."),
    Recipe("diamond_axe", 1, {"diamond": 3, "stick": 2}, requires_crafting_table=True, category="tools", description="Superior diamond axe."),
    Recipe("diamond_sword", 1, {"diamond": 2, "stick": 1}, requires_crafting_table=True, category="weapons", description="Lethal diamond blade."),
    Recipe("diamond_shovel", 1, {"diamond": 1, "stick": 2}, requires_crafting_table=True, category="tools", description="Diamond shovel."),

    # Netherite Tools
    Recipe("netherite_ingot", 1, {"netherite_scrap": 4, "gold_ingot": 4}, requires_crafting_table=True, category="materials", description="Combine scrap and gold into netherite ingot."),
    Recipe("netherite_pickaxe", 1, {"diamond_pickaxe": 1, "netherite_ingot": 1}, requires_crafting_table=True, category="tools", description="Upgrade diamond pickaxe to netherite."),
    Recipe("netherite_axe", 1, {"diamond_axe": 1, "netherite_ingot": 1}, requires_crafting_table=True, category="tools", description="Upgrade diamond axe to netherite."),
    Recipe("netherite_sword", 1, {"diamond_sword": 1, "netherite_ingot": 1}, requires_crafting_table=True, category="weapons", description="Upgrade diamond sword to netherite."),

    # Bow & Arrows
    Recipe("bow", 1, {"stick": 3, "string": 3}, requires_crafting_table=True, category="weapons", description="Ranged bow."),
    Recipe("arrow", 4, {"flint": 1, "stick": 1, "feather": 1}, requires_crafting_table=True, category="weapons", description="Craft 4 arrows."),

    # Iron Armor
    Recipe("iron_helmet", 1, {"iron_ingot": 5}, requires_crafting_table=True, category="armor", description="Iron helmet."),
    Recipe("iron_chestplate", 1, {"iron_ingot": 8}, requires_crafting_table=True, category="armor", description="Iron chestplate."),
    Recipe("iron_leggings", 1, {"iron_ingot": 7}, requires_crafting_table=True, category="armor", description="Iron leggings."),
    Recipe("iron_boots", 1, {"iron_ingot": 4}, requires_crafting_table=True, category="armor", description="Iron boots."),

    # Diamond Armor
    Recipe("diamond_helmet", 1, {"diamond": 5}, requires_crafting_table=True, category="armor", description="Diamond helmet."),
    Recipe("diamond_chestplate", 1, {"diamond": 8}, requires_crafting_table=True, category="armor", description="Diamond chestplate."),
    Recipe("diamond_leggings", 1, {"diamond": 7}, requires_crafting_table=True, category="armor", description="Diamond leggings."),
    Recipe("diamond_boots", 1, {"diamond": 4}, requires_crafting_table=True, category="armor", description="Diamond boots."),

    # Food Recipes
    Recipe("golden_apple", 1, {"apple": 1, "gold_ingot": 8}, requires_crafting_table=True, category="food", description="Golden apple granting vitality."),
]

SMELTING_RECIPES: Dict[str, SmeltRecipe] = {
    "raw_iron": SmeltRecipe("raw_iron", "iron_ingot", xp=0.7),
    "iron_ore": SmeltRecipe("iron_ore", "iron_ingot", xp=0.7),
    "raw_gold": SmeltRecipe("raw_gold", "gold_ingot", xp=1.0),
    "gold_ore": SmeltRecipe("gold_ore", "gold_ingot", xp=1.0),
    "raw_beef": SmeltRecipe("raw_beef", "steak", xp=0.35),
    "raw_porkchop": SmeltRecipe("raw_porkchop", "cooked_porkchop", xp=0.35),
    "raw_chicken": SmeltRecipe("raw_chicken", "cooked_chicken", xp=0.35),
    "raw_mutton": SmeltRecipe("raw_mutton", "cooked_mutton", xp=0.35),
    "cobblestone": SmeltRecipe("cobblestone", "stone", xp=0.1),
    "sand": SmeltRecipe("sand", "glass", xp=0.1),
    "oak_log": SmeltRecipe("oak_log", "charcoal", xp=0.15),
}

# Fuel values (how many items 1 unit of this fuel can smelt)
FURNACE_FUELS: Dict[str, float] = {
    "coal": 8.0,
    "charcoal": 8.0,
    "lava_bucket": 100.0,
    "blaze_rod": 12.0,
    "oak_log": 1.5,
    "oak_planks": 1.5,
    "stick": 0.5,
}

def find_recipes_for(item_id: str) -> List[Recipe]:
    """Finds all recipes producing the given item."""
    return [r for r in RECIPES if r.result_id == item_id]

def get_all_craftable_recipes(inventory: Dict[str, int], has_table: bool) -> List[Tuple[Recipe, int]]:
    """Returns list of (recipe, max_possible_crafts) for recipes the player can currently craft."""
    craftable = []
    for recipe in RECIPES:
        if recipe.requires_crafting_table and not has_table:
            continue
        possible_crafts = []
        for ing, count in recipe.ingredients.items():
            have = inventory.get(ing, 0)
            if have < count:
                possible_crafts.append(0)
                break
            possible_crafts.append(have // count)
        if possible_crafts and min(possible_crafts) > 0:
            craftable.append((recipe, min(possible_crafts)))
    return craftable
