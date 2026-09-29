"""ASCII art banners, logos, and icons for Textcraft."""

import sys

# Platform detection for icon fallbacks on Windows
IS_WINDOWS = sys.platform == "win32"

TEXTCRAFT_BANNER = r"""[bold green]
  _______ ______ __   __ _______ _____ _____            ______ _______
 |__   __|  ____|\ \ / /|__   __/ ____|  __ \     /\   |  ____|__   __|
    | |  | |__    \ V /    | | | |    | |__) |   /  \  | |__     | |
    | |  |  __|    > <     | | | |    |  _  /   / /\ \ |  __|    | |
    | |  | |____  / . \    | | | |____| | \ \  / ____ \| |       | |
    |_|  |______|/_/ \_\   |_|  \_____|_|  \_\/_/    \_\_|       |_|
[/bold green][bold yellow]              A Rich Minecraft Text Adventure[/bold yellow]
"""

VICTORY_BANNER = r"""[bold magenta]
 __      _______ _____ _______ ____  _______     __ _ 
 \ \    / /_   _/ ____|__   __/ __ \|  __ \ \   / /| |
  \ \  / /  | || |       | | | |  | | |__) \ \_/ / | |
   \ \/ /   | || |       | | | |  | |  _  / \   /  | |
    \  /   _| || |____   | | | |__| | | \ \  | |   |_|
     \/   |_____\_____|  |_|  \____/|_|  \_\ |_|   (_)
[/bold magenta][bold gold1]
           You have defeated the Ender Dragon!
       The cosmos whispers your name across all realms.
[/bold gold1]"""

GAME_OVER_BANNER = r"""[bold red]
   _____          __  __ ______    ______      ________ _____  
  / ____|   /\   |  \/  |  ____|  / __ \ \    / /  ____|  __ \ 
 | |  __   /  \  | \  / | |__    | |  | \ \  / /| |__  | |__) |
 | | |_ | / /\ \ | |\/| |  __|   | |  | |\ \/ / |  __| |  _  / 
 | |__| |/ ____ \| |  | | |____  | |__| | \  /  | |____| | \ \ 
  \_____/_/    \_\_|  |_|______|  \____/   \/   |______|_|  \_\
[/bold red][dim red]
                  Score: {score}  |  Days Survived: {days}
[/dim red]"""

if IS_WINDOWS:
    BIOME_ICONS = {
        "plains": "*",
        "forest": "T",
        "desert": "~",
        "mountains": "^",
        "swamp": "=",
        "jungle": "J",
        "snowy_tundra": "#",
        "shallow_cave": "[C]",
        "deep_cave": "[D]",
        "deepslate_cavern": "[*]",
        "nether_wastes": "!",
        "nether_fortress": "[F]",
        "the_end_island": "[E]",
    }

    MOB_ICONS = {
        "cow": "C",
        "sheep": "S",
        "pig": "P",
        "chicken": "B",
        "zombie": "Z",
        "skeleton": "K",
        "creeper": "!",
        "spider": "8",
        "enderman": "?",
        "blaze": "@",
        "ghast": "G",
        "ender_dragon": "D",
    }
else:
    BIOME_ICONS = {
        "plains": "🌾",
        "forest": "🌲",
        "desert": "🏜️",
        "mountains": "⛰️",
        "swamp": "🌿",
        "jungle": "🌴",
        "snowy_tundra": "❄️",
        "shallow_cave": "⛏️",
        "deep_cave": "🪨",
        "deepslate_cavern": "💎",
        "nether_wastes": "🔥",
        "nether_fortress": "🏰",
        "the_end_island": "🌌",
    }

    MOB_ICONS = {
        "cow": "🐮",
        "sheep": "🐑",
        "pig": "🐷",
        "chicken": "🐔",
        "zombie": "🧟",
        "skeleton": "💀",
        "creeper": "💥",
        "spider": "🕷️",
        "enderman": "👁️",
        "blaze": "🔥",
        "ghast": "👻",
        "ender_dragon": "🐉",
    }
