"""Item models, categories, and item registry for Textcraft."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from textcraft.config import (
    TIER_HAND, TIER_WOOD, TIER_STONE, TIER_IRON, TIER_DIAMOND, TIER_NETHERITE
)

ITEM_CATEGORY_MATERIAL = "material"
ITEM_CATEGORY_TOOL = "tool"
ITEM_CATEGORY_WEAPON = "weapon"
ITEM_CATEGORY_ARMOR = "armor"
ITEM_CATEGORY_FOOD = "food"
ITEM_CATEGORY_UTILITY = "utility"
ITEM_CATEGORY_BLOCK = "block"

ARMOR_SLOT_HELMET = "helmet"
ARMOR_SLOT_CHESTPLATE = "chestplate"
ARMOR_SLOT_LEGGINGS = "leggings"
ARMOR_SLOT_BOOTS = "boots"
ARMOR_SLOT_OFFHAND = "offhand"  # e.g., shield

@dataclass
class Item:
    id: str
    name: str
    category: str
    description: str = ""
    stack_size: int = 64
    tool_type: Optional[str] = None       # "pickaxe", "axe", "shovel", "sword", "hoe"
    tool_tier: int = TIER_HAND
    max_durability: Optional[int] = None
    current_durability: Optional[int] = None
    attack_damage: int = 1
    armor_points: int = 0
    armor_slot: Optional[str] = None      # "helmet", "chestplate", "leggings", "boots", "offhand"
    food_points: int = 0
    saturation: float = 0.0
    placeable_block: Optional[str] = None # block id if this item can be placed in world

    def __post_init__(self):
        if self.max_durability is not None and self.current_durability is None:
            self.current_durability = self.max_durability

    @property
    def is_tool_or_weapon(self) -> bool:
        return self.category in (ITEM_CATEGORY_TOOL, ITEM_CATEGORY_WEAPON)

    @property
    def is_armor(self) -> bool:
        return self.category == ITEM_CATEGORY_ARMOR

    @property
    def is_food(self) -> bool:
        return self.category == ITEM_CATEGORY_FOOD

    def damage(self, amount: int = 1) -> bool:
        """Inflicts durability damage. Returns True if the item broke, False otherwise."""
        if self.current_durability is None:
            return False
        self.current_durability -= amount
        return self.current_durability <= 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "current_durability": self.current_durability,
        }

    @classmethod
    def from_id(cls, item_id: str, current_durability: Optional[int] = None) -> "Item":
        base = ITEM_REGISTRY.get(item_id)
        if not base:
            # Fallback placeholder item
            return cls(
                id=item_id,
                name=item_id.replace("_", " ").title(),
                category=ITEM_CATEGORY_MATERIAL,
                description=f"A mysterious object ({item_id})"
            )
        # Create a copy so durability is independent
        item = cls(
            id=base.id,
            name=base.name,
            category=base.category,
            description=base.description,
            stack_size=base.stack_size,
            tool_type=base.tool_type,
            tool_tier=base.tool_tier,
            max_durability=base.max_durability,
            current_durability=current_durability if current_durability is not None else base.max_durability,
            attack_damage=base.attack_damage,
            armor_points=base.armor_points,
            armor_slot=base.armor_slot,
            food_points=base.food_points,
            saturation=base.saturation,
            placeable_block=base.placeable_block,
        )
        return item


# Durability standard values:
DURABILITY_WOOD = 59
DURABILITY_STONE = 131
DURABILITY_IRON = 250
DURABILITY_DIAMOND = 1561
DURABILITY_NETHERITE = 2031

# Global items registry
ITEM_REGISTRY: Dict[str, Item] = {
    # Materials / Blocks
    "oak_log": Item("oak_log", "Oak Log", ITEM_CATEGORY_BLOCK, "A solid chunk of oak tree trunk.", placeable_block="oak_log"),
    "oak_planks": Item("oak_planks", "Oak Planks", ITEM_CATEGORY_BLOCK, "Versatile wooden boards for building and crafting.", placeable_block="oak_planks"),
    "stick": Item("stick", "Stick", ITEM_CATEGORY_MATERIAL, "A sturdy wooden stick used as handles for tools."),
    "cobblestone": Item("cobblestone", "Cobblestone", ITEM_CATEGORY_BLOCK, "Rugged blocks of mined stone.", placeable_block="cobblestone"),
    "stone": Item("stone", "Stone", ITEM_CATEGORY_BLOCK, "Smooth natural stone.", placeable_block="stone"),
    "deepslate": Item("deepslate", "Deepslate", ITEM_CATEGORY_BLOCK, "Tough, dark stone from deep beneath the earth.", placeable_block="deepslate"),
    "dirt": Item("dirt", "Dirt", ITEM_CATEGORY_BLOCK, "Rich fertile soil.", placeable_block="dirt"),
    "sand": Item("sand", "Sand", ITEM_CATEGORY_BLOCK, "Fine grains of desert or shoreline sand.", placeable_block="sand"),
    "gravel": Item("gravel", "Gravel", ITEM_CATEGORY_BLOCK, "Loose coarse stones.", placeable_block="gravel"),
    "flint": Item("flint", "Flint", ITEM_CATEGORY_MATERIAL, "A sharp flake of dark mineral from gravel."),
    "coal": Item("coal", "Coal", ITEM_CATEGORY_MATERIAL, "Combustible black rock, ideal for torches and smelting fuel."),
    "charcoal": Item("charcoal", "Charcoal", ITEM_CATEGORY_MATERIAL, "Burnt wood usable as an efficient fuel source."),
    "raw_iron": Item("raw_iron", "Raw Iron", ITEM_CATEGORY_MATERIAL, "Dense chunks of unrefined iron ore."),
    "iron_ingot": Item("iron_ingot", "Iron Ingot", ITEM_CATEGORY_MATERIAL, "A refined bar of durable iron."),
    "raw_gold": Item("raw_gold", "Raw Gold", ITEM_CATEGORY_MATERIAL, "Gleaming nuggets of unrefined gold ore."),
    "gold_ingot": Item("gold_ingot", "Gold Ingot", ITEM_CATEGORY_MATERIAL, "A shiny bar of pure gold."),
    "diamond": Item("diamond", "Diamond", ITEM_CATEGORY_MATERIAL, "A rare, brilliant gemstone with supreme hardness."),
    "netherite_scrap": Item("netherite_scrap", "Netherite Scrap", ITEM_CATEGORY_MATERIAL, "Ancient debris smelted into indestructible metal scrap."),
    "netherite_ingot": Item("netherite_ingot", "Netherite Ingot", ITEM_CATEGORY_MATERIAL, "An alloy of gold and netherite scrap."),
    "obsidian": Item("obsidian", "Obsidian", ITEM_CATEGORY_BLOCK, "Extremely hard volcanic glass formed by water and lava.", placeable_block="obsidian"),
    "glass": Item("glass", "Glass", ITEM_CATEGORY_BLOCK, "Clear transparent blocks smelted from sand.", placeable_block="glass"),
    "netherrack": Item("netherrack", "Netherrack", ITEM_CATEGORY_BLOCK, "Porous blood-red stone from the Nether that burns indefinitely.", placeable_block="netherrack"),
    "soul_sand": Item("soul_sand", "Soul Sand", ITEM_CATEGORY_BLOCK, "Eerie sand that slows down anything treading upon it.", placeable_block="soul_sand"),
    "glowstone_dust": Item("glowstone_dust", "Glowstone Dust", ITEM_CATEGORY_MATERIAL, "Luminous shimmering dust from the Nether."),
    "blaze_rod": Item("blaze_rod", "Blaze Rod", ITEM_CATEGORY_MATERIAL, "A smoldering rod harvested from a fiery Blaze."),
    "blaze_powder": Item("blaze_powder", "Blaze Powder", ITEM_CATEGORY_MATERIAL, "Intense incendiary powder ground from a blaze rod."),
    "ender_pearl": Item("ender_pearl", "Ender Pearl", ITEM_CATEGORY_MATERIAL, "An ominous, shimmering green sphere dropped by an Enderman.", stack_size=16),
    "eye_of_ender": Item("eye_of_ender", "Eye of Ender", ITEM_CATEGORY_UTILITY, "A glowing eye that seeks out Strongholds and activates End Portals.", stack_size=16),
    "string": Item("string", "String", ITEM_CATEGORY_MATERIAL, "Thin flexible silk dropped by spiders."),
    "bone": Item("bone", "Bone", ITEM_CATEGORY_MATERIAL, "A skeletal bone dropped by undead archers."),
    "feather": Item("feather", "Feather", ITEM_CATEGORY_MATERIAL, "A soft bird feather dropped by chickens."),
    "leather": Item("leather", "Leather", ITEM_CATEGORY_MATERIAL, "Tough animal hide dropped by cows."),
    "wool": Item("wool", "Wool", ITEM_CATEGORY_BLOCK, "Soft sheep fleece for making beds.", placeable_block="wool"),

    # Tools - Pickaxes
    "wooden_pickaxe": Item("wooden_pickaxe", "Wooden Pickaxe", ITEM_CATEGORY_TOOL, "Basic pickaxe for gathering stone.", stack_size=1, tool_type="pickaxe", tool_tier=TIER_WOOD, max_durability=DURABILITY_WOOD, attack_damage=2),
    "stone_pickaxe": Item("stone_pickaxe", "Stone Pickaxe", ITEM_CATEGORY_TOOL, "Sturdy pickaxe capable of mining iron and coal.", stack_size=1, tool_type="pickaxe", tool_tier=TIER_STONE, max_durability=DURABILITY_STONE, attack_damage=3),
    "iron_pickaxe": Item("iron_pickaxe", "Iron Pickaxe", ITEM_CATEGORY_TOOL, "Strong pickaxe capable of mining gold, redstone, and diamond.", stack_size=1, tool_type="pickaxe", tool_tier=TIER_IRON, max_durability=DURABILITY_IRON, attack_damage=4),
    "diamond_pickaxe": Item("diamond_pickaxe", "Diamond Pickaxe", ITEM_CATEGORY_TOOL, "Master-grade pickaxe capable of breaking obsidian.", stack_size=1, tool_type="pickaxe", tool_tier=TIER_DIAMOND, max_durability=DURABILITY_DIAMOND, attack_damage=5),
    "netherite_pickaxe": Item("netherite_pickaxe", "Netherite Pickaxe", ITEM_CATEGORY_TOOL, "Ultimate pickaxe, immune to fire and exceptionally fast.", stack_size=1, tool_type="pickaxe", tool_tier=TIER_NETHERITE, max_durability=DURABILITY_NETHERITE, attack_damage=6),

    # Tools - Axes
    "wooden_axe": Item("wooden_axe", "Wooden Axe", ITEM_CATEGORY_TOOL, "Crude axe for felling trees faster.", stack_size=1, tool_type="axe", tool_tier=TIER_WOOD, max_durability=DURABILITY_WOOD, attack_damage=3),
    "stone_axe": Item("stone_axe", "Stone Axe", ITEM_CATEGORY_TOOL, "Stone axe with heavy chopping power.", stack_size=1, tool_type="axe", tool_tier=TIER_STONE, max_durability=DURABILITY_STONE, attack_damage=4),
    "iron_axe": Item("iron_axe", "Iron Axe", ITEM_CATEGORY_TOOL, "Sharp iron axe for rapid woodchopping.", stack_size=1, tool_type="axe", tool_tier=TIER_IRON, max_durability=DURABILITY_IRON, attack_damage=5),
    "diamond_axe": Item("diamond_axe", "Diamond Axe", ITEM_CATEGORY_TOOL, "Razor-sharp diamond axe.", stack_size=1, tool_type="axe", tool_tier=TIER_DIAMOND, max_durability=DURABILITY_DIAMOND, attack_damage=6),
    "netherite_axe": Item("netherite_axe", "Netherite Axe", ITEM_CATEGORY_TOOL, "Heavy devastating netherite axe.", stack_size=1, tool_type="axe", tool_tier=TIER_NETHERITE, max_durability=DURABILITY_NETHERITE, attack_damage=7),

    # Tools - Swords
    "wooden_sword": Item("wooden_sword", "Wooden Sword", ITEM_CATEGORY_WEAPON, "A carved wooden blade for defense.", stack_size=1, tool_type="sword", tool_tier=TIER_WOOD, max_durability=DURABILITY_WOOD, attack_damage=4),
    "stone_sword": Item("stone_sword", "Stone Sword", ITEM_CATEGORY_WEAPON, "Chiseled stone blade with reliable punch.", stack_size=1, tool_type="sword", tool_tier=TIER_STONE, max_durability=DURABILITY_STONE, attack_damage=5),
    "iron_sword": Item("iron_sword", "Iron Sword", ITEM_CATEGORY_WEAPON, "Tempered iron longsword for monster slaying.", stack_size=1, tool_type="sword", tool_tier=TIER_IRON, max_durability=DURABILITY_IRON, attack_damage=6),
    "diamond_sword": Item("diamond_sword", "Diamond Sword", ITEM_CATEGORY_WEAPON, "Gleaming blue blade of lethal sharpness.", stack_size=1, tool_type="sword", tool_tier=TIER_DIAMOND, max_durability=DURABILITY_DIAMOND, attack_damage=7),
    "netherite_sword": Item("netherite_sword", "Netherite Sword", ITEM_CATEGORY_WEAPON, "Ancient dark blade forged in Nether heat.", stack_size=1, tool_type="sword", tool_tier=TIER_NETHERITE, max_durability=DURABILITY_NETHERITE, attack_damage=8),

    # Tools - Shovels
    "wooden_shovel": Item("wooden_shovel", "Wooden Shovel", ITEM_CATEGORY_TOOL, "Simple spade for digging dirt and sand.", stack_size=1, tool_type="shovel", tool_tier=TIER_WOOD, max_durability=DURABILITY_WOOD, attack_damage=1),
    "stone_shovel": Item("stone_shovel", "Stone Shovel", ITEM_CATEGORY_TOOL, "Stone spade for digging soil.", stack_size=1, tool_type="shovel", tool_tier=TIER_STONE, max_durability=DURABILITY_STONE, attack_damage=2),
    "iron_shovel": Item("iron_shovel", "Iron Shovel", ITEM_CATEGORY_TOOL, "Clean iron spade that tears through gravel and dirt.", stack_size=1, tool_type="shovel", tool_tier=TIER_IRON, max_durability=DURABILITY_IRON, attack_damage=3),
    "diamond_shovel": Item("diamond_shovel", "Diamond Shovel", ITEM_CATEGORY_TOOL, "Diamond shovel for effortless excavation.", stack_size=1, tool_type="shovel", tool_tier=TIER_DIAMOND, max_durability=DURABILITY_DIAMOND, attack_damage=4),
    "netherite_shovel": Item("netherite_shovel", "Netherite Shovel", ITEM_CATEGORY_TOOL, "Indestructible spade.", stack_size=1, tool_type="shovel", tool_tier=TIER_NETHERITE, max_durability=DURABILITY_NETHERITE, attack_damage=5),

    # Weapons & Combat Gear
    "bow": Item("bow", "Bow", ITEM_CATEGORY_WEAPON, "A ranged weapon strung with spider silk.", stack_size=1, max_durability=384, attack_damage=6),
    "arrow": Item("arrow", "Arrow", ITEM_CATEGORY_MATERIAL, "Fletched projectile with flint tip.", stack_size=64),
    "shield": Item("shield", "Shield", ITEM_CATEGORY_ARMOR, "Sturdy iron-reinforced wooden shield to block blows.", stack_size=1, armor_slot=ARMOR_SLOT_OFFHAND, max_durability=336, armor_points=2),

    # Armor - Iron
    "iron_helmet": Item("iron_helmet", "Iron Helmet", ITEM_CATEGORY_ARMOR, "Protects the head.", stack_size=1, armor_slot=ARMOR_SLOT_HELMET, max_durability=165, armor_points=2),
    "iron_chestplate": Item("iron_chestplate", "Iron Chestplate", ITEM_CATEGORY_ARMOR, "Heavy iron plate protecting the torso.", stack_size=1, armor_slot=ARMOR_SLOT_CHESTPLATE, max_durability=240, armor_points=6),
    "iron_leggings": Item("iron_leggings", "Iron Leggings", ITEM_CATEGORY_ARMOR, "Iron greaves protecting the legs.", stack_size=1, armor_slot=ARMOR_SLOT_LEGGINGS, max_durability=225, armor_points=5),
    "iron_boots": Item("iron_boots", "Iron Boots", ITEM_CATEGORY_ARMOR, "Iron sabatons protecting the feet.", stack_size=1, armor_slot=ARMOR_SLOT_BOOTS, max_durability=195, armor_points=2),

    # Armor - Diamond
    "diamond_helmet": Item("diamond_helmet", "Diamond Helmet", ITEM_CATEGORY_ARMOR, "Glistening diamond helmet.", stack_size=1, armor_slot=ARMOR_SLOT_HELMET, max_durability=363, armor_points=3),
    "diamond_chestplate": Item("diamond_chestplate", "Diamond Chestplate", ITEM_CATEGORY_ARMOR, "Impenetrable diamond chestplate.", stack_size=1, armor_slot=ARMOR_SLOT_CHESTPLATE, max_durability=528, armor_points=8),
    "diamond_leggings": Item("diamond_leggings", "Diamond Leggings", ITEM_CATEGORY_ARMOR, "Diamond leggings.", stack_size=1, armor_slot=ARMOR_SLOT_LEGGINGS, max_durability=495, armor_points=6),
    "diamond_boots": Item("diamond_boots", "Diamond Boots", ITEM_CATEGORY_ARMOR, "Diamond boots.", stack_size=1, armor_slot=ARMOR_SLOT_BOOTS, max_durability=429, armor_points=3),

    # Utilities & Functional Blocks
    "crafting_table": Item("crafting_table", "Crafting Table", ITEM_CATEGORY_UTILITY, "A 3x3 workbench enabling advanced crafting.", placeable_block="crafting_table"),
    "furnace": Item("furnace", "Furnace", ITEM_CATEGORY_UTILITY, "Cobblestone hearth for smelting ores and cooking food.", placeable_block="furnace"),
    "chest": Item("chest", "Chest", ITEM_CATEGORY_UTILITY, "Wooden container for storing your spoils.", placeable_block="chest"),
    "bed": Item("bed", "Bed", ITEM_CATEGORY_UTILITY, "Soft bed to rest and skip through dangerous nights.", placeable_block="bed"),
    "torch": Item("torch", "Torch", ITEM_CATEGORY_UTILITY, "Provides warmth and illumination, keeping monsters away.", placeable_block="torch"),
    "bucket": Item("bucket", "Bucket", ITEM_CATEGORY_UTILITY, "Iron pail capable of carrying liquids.", stack_size=16),
    "water_bucket": Item("water_bucket", "Water Bucket", ITEM_CATEGORY_UTILITY, "Bucket filled with fresh water.", stack_size=1),
    "lava_bucket": Item("lava_bucket", "Lava Bucket", ITEM_CATEGORY_UTILITY, "Bucket filled with scorching lava. Excellent furnace fuel.", stack_size=1),
    "flint_and_steel": Item("flint_and_steel", "Flint and Steel", ITEM_CATEGORY_UTILITY, "Ignites fires and activates obsidian Nether Portals.", stack_size=1, max_durability=64),

    # Foods
    "apple": Item("apple", "Apple", ITEM_CATEGORY_FOOD, "A crisp sweet red apple found among oak leaves.", food_points=4, saturation=2.4),
    "bread": Item("bread", "Bread", ITEM_CATEGORY_FOOD, "Warm baked loaf of wheat bread.", food_points=5, saturation=6.0),
    "raw_beef": Item("raw_beef", "Raw Beef", ITEM_CATEGORY_FOOD, "Uncooked steak taken from a cow.", food_points=3, saturation=1.8),
    "steak": Item("steak", "Steak", ITEM_CATEGORY_FOOD, "Juicy fire-cooked steak. Restores substantial hunger.", food_points=8, saturation=12.8),
    "raw_porkchop": Item("raw_porkchop", "Raw Porkchop", ITEM_CATEGORY_FOOD, "Uncooked slice of pork.", food_points=3, saturation=1.8),
    "cooked_porkchop": Item("cooked_porkchop", "Cooked Porkchop", ITEM_CATEGORY_FOOD, "Tender roasted porkchop.", food_points=8, saturation=12.8),
    "raw_chicken": Item("raw_chicken", "Raw Chicken", ITEM_CATEGORY_FOOD, "Uncooked chicken. Eating raw might make you feel sick.", food_points=2, saturation=1.2),
    "cooked_chicken": Item("cooked_chicken", "Cooked Chicken", ITEM_CATEGORY_FOOD, "Crispy roast chicken drumstick.", food_points=6, saturation=7.2),
    "raw_mutton": Item("raw_mutton", "Raw Mutton", ITEM_CATEGORY_FOOD, "Uncooked sheep meat.", food_points=2, saturation=1.2),
    "cooked_mutton": Item("cooked_mutton", "Cooked Mutton", ITEM_CATEGORY_FOOD, "Delicious seasoned roast mutton.", food_points=6, saturation=9.6),
    "golden_apple": Item("golden_apple", "Golden Apple", ITEM_CATEGORY_FOOD, "An apple encased in pure gold. Grants healing and invigoration.", food_points=4, saturation=9.6),
    "rotten_flesh": Item("rotten_flesh", "Rotten Flesh", ITEM_CATEGORY_FOOD, "Decaying flesh dropped by zombies. Edible in desperate hunger.", food_points=4, saturation=0.8),
}
