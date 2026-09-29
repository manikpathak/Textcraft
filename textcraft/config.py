"""Configuration constants, game balance, and visual tokens for Textcraft."""

import sys

# Detect if running on Windows (use ASCII icons as fallback)
IS_WINDOWS = sys.platform == "win32"

# Survival Constants
MAX_HEALTH = 20
MAX_HUNGER = 20
DEFAULT_STARTING_HEALTH = 20
DEFAULT_STARTING_HUNGER = 20
HUNGER_DEPLETION_PER_ACTION = 0.4
HEAL_HUNGER_THRESHOLD = 18
STARVATION_HUNGER_THRESHOLD = 0
HEAL_AMOUNT = 1
STARVATION_DAMAGE = 1

# Time & Cycle Constants
# Minecraft day is 24000 ticks.
# We set 1 action/command = 1000 ticks (24 actions per 24h day/night cycle)
TICKS_PER_DAY = 24000
TICKS_PER_ACTION = 1000

# Dimensions
DIMENSION_OVERWORLD = "overworld"
DIMENSION_NETHER = "nether"
DIMENSION_END = "the_end"

# Tool Tiers
TIER_HAND = 0
TIER_WOOD = 1
TIER_STONE = 2
TIER_IRON = 3
TIER_DIAMOND = 4
TIER_NETHERITE = 5

# Mining Speed (multiplier for block hardness)
MINING_SPEED = {
    TIER_HAND:       1.0,
    TIER_WOOD:       2.0,
    TIER_STONE:      4.0,
    TIER_IRON:       6.0,
    TIER_DIAMOND:    8.0,
    TIER_NETHERITE:  9.0,
}

# Mining speed with wrong tool type
MINING_SPEED_WRONG_TOOL = {
    TIER_HAND:       1.0,
    TIER_WOOD:       0.5,
    TIER_STONE:      0.75,
    TIER_IRON:       1.0,
    TIER_DIAMOND:    1.5,
    TIER_NETHERITE:  2.0,
}

TIER_NAMES = {
    TIER_HAND: "Bare Hands",
    TIER_WOOD: "Wood",
    TIER_STONE: "Stone",
    TIER_IRON: "Iron",
    TIER_DIAMOND: "Diamond",
    TIER_NETHERITE: "Netherite",
}

# Rich Palette & Theme Colors
COLOR_HEALTH = "bright_red"
COLOR_HUNGER = "bright_yellow"
COLOR_ARMOR = "bright_cyan"
COLOR_XP = "bright_green"
COLOR_BIOME = "spring_green2"
COLOR_TIME = "bright_yellow"
COLOR_ITEM = "bold green"
COLOR_BLOCK = "bold dark_orange"
COLOR_TOOL = "bold steel_blue1"
COLOR_MOB_PASSIVE = "bold chartreuse2"
COLOR_MOB_HOSTILE = "bold red3"
COLOR_LOOT = "bold gold1"
COLOR_DAMAGE = "bold red"
COLOR_INFO = "bright_blue"
COLOR_HINT = "dim cyan"

# Symbols & Icons (with Windows ASCII fallbacks)
if IS_WINDOWS:
    ICON_HEART = "♥"        # Works on Windows
    ICON_HUNGER = "[F]"     # Food
    ICON_ARMOR = "[A]"      # Armor
    ICON_XP = "*"           # XP star
    ICON_SUN = "[D]"        # Day
    ICON_MOON = "[N]"       # Night
    ICON_COMPASS = "[C]"    # Compass
    ICON_CLOCK = "[T]"      # Time
    ICON_SWORD = "[W]"      # Weapon
    ICON_PICKAXE = "[P]"    # Pickaxe
    ICON_CHEST = "[B]"      # Box/storage
    ICON_PORTAL = "[*]"     # Portal
    ICON_FIRE = "[!]"       # Fire
    ICON_DEATH = "[X]"      # Death
    ICON_GRASS = "[*]"      # Grass/resources
    ICON_CREATURES = "[+]"  # Creatures
else:
    # Full emoji icons on non-Windows platforms
    ICON_HEART = "♥"
    ICON_HUNGER = "🍗"
    ICON_ARMOR = "🛡️"
    ICON_XP = "✦"
    ICON_SUN = "☀️"
    ICON_MOON = "🌙"
    ICON_COMPASS = "🧭"
    ICON_CLOCK = "⏱️"
    ICON_SWORD = "⚔️"
    ICON_PICKAXE = "⛏️"
    ICON_CHEST = "📦"
    ICON_PORTAL = "🌀"
    ICON_FIRE = "🔥"
    ICON_DEATH = "☠️"
    ICON_GRASS = "🌾"
    ICON_CREATURES = "🐾"
