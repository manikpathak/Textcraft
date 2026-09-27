"""Configuration constants, game balance, and visual tokens for Textcraft."""

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

# Symbols & Icons
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
