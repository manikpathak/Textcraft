# Textcraft 🌲⛏️

A rich, atmospheric text adventure that recreates the full survival progression of **Minecraft** right inside your terminal, powered by Python, [Rich](https://github.com/Textualize/rich), and [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).

```
  _______ ______ _  _______ _____ _____            ______ _______ 
 |__   __|  ____| |/ /__   __/ ____|  __ \     /\   |  ____|__   __|
    | |  | |__  | ' /   | | | |    | |__) |   /  \  | |__     | |   
    | |  |  __| |  <    | | | |    |  _  /   / /\ \ |  __|    | |   
    | |  | |____| . \   | | | |____| | \ \  / ____ \| |       | |   
    |_|  |______|_|\_\  |_|  \_____|_|  \_\/_/    \_\_|       |_|   
              A Rich Minecraft Text Adventure
```

> **⚠️  Windows Support Notice**: The Windows version is still in **(WIP)** - Windows compatibility features are being developed. Full Windows support coming soon! Mac/Linux versions fully supported.

---

## ✨ Features

- **Classic Text Adventure & MUD Gameplay**: Natural language command parser (`mine oak log`, `craft wooden_pickaxe`, `smelt raw_iron with coal`, `attack zombie`, `build shelter`, `sleep`, `go north`, `dig down`).
- **Rich Terminal UI**:
  - **Live Survival HUD**: Health hearts (`♥♥♥♥♥♥♥♥♥♥`), Hunger drumsticks (`🍗🍗🍗🍗🍗🍗🍗🍗🍗🍗`), Armor rating (`🛡️`), Experience levels (`✦`), In-game clock (`☀️ / 🌙`), and active equipment.
  - **Atmospheric Biome Panels**: Detailed narratives for Plains, Oak Forests, Deserts, Craggy Mountains, Swamps, Jungles, Snowy Tundras, Underground Caves, Deepslate Caverns, Nether Wastes, and The End.
  - **ASCII Local Mini-Map**: Dynamic 7x7 grid rendering player coordinates, explored biomes, shelters, and portals.
  - **Autocomplete & History**: Smooth tab-completion for commands, items, blocks, and mobs via `prompt_toolkit`.
- **Procedural Infinite World & Dimensions**:
  - **Surface Elevation (Y=64)**: Diverse biomes with passive animals and trees.
  - **Subterranean Depths**: Dig down into Shallow Caves (Y=48), Deep Ravines (Y=16), and pitch-black Deepslate (Y=-32).
  - **The Nether**: Build an Obsidian portal frame (10 obsidian), enter the Underworld, fight Blazes and Ghasts, and harvest ancient debris for Netherite.
  - **The End**: Craft Eyes of Ender, enter The End, and face the mighty **Ender Dragon**!
- **Complete Minecraft Survival Mechanics**:
  - **Mining & Tool Tiers**: Fists → Wood → Stone → Iron → Diamond → Netherite with durability tracking. Stone and ores require proper pickaxe tiers to drop.
  - **Advanced Mining System**: 
    - **Block Hardness & Mining Timers**: Each block has realistic hardness values (dirt is fast, obsidian takes time). Mining time scales with tool speed and block hardness.
    - **Tool Efficiency**: Correct tool types (pickaxe for stone, axe for logs, shovel for dirt) mine significantly faster. Wrong tools are slow but still work.
    - **Batch Mining**: Mine multiple blocks at once (`mine dirt 5` or `mine all stone`) for efficient resource gathering.
  - **Crafting Engine**: 2x2 basic crafting anywhere; place a Crafting Table to unlock full 3x3 weapons, armor, tools, and utilities.
  - **Smelting & Cooking**: Place a Furnace to smelt ores (`raw_iron` → `iron_ingot`) or cook meats (`raw_beef` → `steak`) using fuels like Coal, Charcoal, or Wood.
  - **Building & Shelter**: Construct shelters (`build shelter`) using logs, planks, or cobblestone to create monster-free safe havens. Place beds to sleep through the night and set your respawn point.
  - **Combat & Mobs**:
    - **Passive Mobs**: Cows, Sheep, Pigs, Chickens.
    - **Hostile Mobs**: Zombies and Skeletons (burn in daylight!), Spiders, Endermen, and Creepers (with fuse hissing countdowns!).
    - **Combat Tactics**: Melee weapon swings, critical strikes, bow & arrows at range, and shields to deflect physical strikes and explosions.
- **Player Customization**:
  - **Custom Player Names**: Name your character at game start (defaults to "Steve").
  - **World Selection Screen**: Start a new game or load from multiple saved worlds with an intuitive menu.
  - **Persistent Identity**: Player names are saved and restored with your world.
- **Cross-Platform Support**:
  - **Mac/Linux**: Full support with rich emoji icons for immersive experience.
  - **Windows**: ASCII-friendly icon fallbacks for PowerShell compatibility (emojis replaced with readable symbols).
  - **Auto-Detection**: Platform automatically detected; no configuration needed.
- **Save & Load System**: JSON-based quicksaving and multi-slot saves preserving inventory, world changes, player stats, and names.

---

## 🚀 Quickstart & Installation

### Requirements
- Python 3.9+
- macOS, Linux, or Windows

### Setup
```bash
# Clone or navigate to the repository
cd Textcraft

# Activate virtual environment
source .venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run Textcraft!
python3 run.py
```

---

## 🕹️ Command Reference

| Category | Command | Aliases / Examples | Description |
|---|---|---|---|
| **Movement** | `north`, `south`, `east`, `west` | `n`, `s`, `e`, `w`, `go north` | Travel between connected world tiles |
| **Depth** | `down`, `dig down` | `d`, `descend`, `enter cave` | Dig deeper into caves and deepslate |
| **Ascent** | `up`, `climb up` | `u`, `ascend`, `surface` | Climb back up toward the surface |
| **Exploration** | `look` | `l`, `survey`, `examine` | Inspect current location, resources, and mobs |
| **Inventory** | `inventory` | `i`, `inv`, `bag` | View carried items and equipped gear |
| **Map** | `map` | `m` | Display the 7x7 local mini-map |
| **Status** | `status`, `time` | `clock` | Display survival stats and in-game time |
| **Gathering** | `mine <block> [count]` | `mine dirt`, `mine ore 5`, `mine all stone`, `chop tree`, `dig dirt` | Harvest wood, stone, ores, or soil. Supports batch mining with count or "all" keyword |
| **Recipes** | `recipes [filter]` | `recipe pickaxe`, `recipes` | View recipe book and material requirements |
| **Crafting** | `craft <item> [count]` | `craft wooden_pickaxe`, `craft 4 torch` | Craft tools, armor, or items |
| **Smelting** | `smelt <item> [with <fuel>]` | `smelt raw_iron with coal`, `cook raw_beef` | Smelt ingots or cook food in a furnace |
| **Placement** | `place <block>` | `place crafting_table`, `place bed` | Place workstations, storage, or blocks |
| **Shelter** | `build shelter` | `shelter` | Build safe haven to prevent night monsters |
| **Sleep** | `sleep` | `rest` | Sleep in a bed to skip night and set spawn |
| **Storage** | `store <qty> <item>` | `store 5 coal`, `put 10 iron in chest` | Deposit items into a placed chest |
| **Storage** | `take <qty> <item>` | `take 5 coal from chest` | Withdraw items from a placed chest |
| **Equipment** | `equip <item>` | `wear iron_chestplate`, `hold diamond_sword` | Equip armor, weapons, tools, or shields |
| **Equipment** | `unequip <slot>` | `unequip helmet`, `take off chestplate` | Return equipped gear to inventory |
| **Survival** | `eat <food> [count]` | `eat 3 steak`, `eat apple 2`, `eat all bread` | Consume food portions to replenish hunger and heal |
| **Combat** | `attack <mob>` | `hit zombie`, `kill creeper` | Attack creature with weapon or fists |
| **Combat** | `shoot <mob>` | `shoot at skeleton` | Fire bow & arrow from a safe distance |
| **Defense** | `block` | `defend` | Raise shield to block incoming damage |
| **Portals** | `enter portal` | `portal`, `enter nether` | Step through an active dimensional portal |
| **Saves** | `save [name]` / `load [name]` | `save world1`, `load world1`, `saves` | Save or load world progress |
| **System** | `help [topic]` | `?`, `commands` | Show help manual |
| **System** | `quit` | `exit`, `q` | Quicksave and quit to terminal |

---

## 🗺️ Progression Guide

1. **Survive Day 1**:
   - `mine oak_log` to gather raw logs.
   - `craft oak_planks 2` then `craft crafting_table 1`.
   - `place crafting_table` at your location.
   - `craft stick 2` and `craft wooden_pickaxe 1`.
   - `equip wooden_pickaxe`.
2. **Stone Age & Shelter**:
   - `mine stone` to gather cobblestone.
   - `craft stone_pickaxe 1` and `craft stone_sword 1`.
   - `mine coal_ore` and `craft 4 torch`.
   - `build shelter` with extra planks or cobblestone to stay safe through the night.
3. **Iron Age**:
   - `craft furnace 1` and `place furnace`.
   - `dig down` into the underground caves.
   - `mine iron_ore` and `smelt raw_iron with coal`.
   - `craft iron_pickaxe 1`, `craft iron_sword 1`, and `craft shield 1`.
   - `equip shield`.
4. **Diamonds & The Nether**:
   - Dig deeper into Deepslate (Y=-32) and `mine diamond_ore`.
   - `craft diamond_pickaxe 1`.
   - `mine obsidian` (10 blocks).
   - `place obsidian` (10 times) to construct and ignite a **Nether Portal**!
   - `enter portal` to explore the Nether, harvest Blaze Rods, and forge Netherite gear.
5. **The End & The Dragon**:
   - Combine Ender Pearls and Blaze Powder into Eyes of Ender (`craft eye_of_ender`).
   - Discover or travel to The End and face the legendary **Ender Dragon**!

---

## 🧪 Testing

Textcraft includes an extensive test suite verifying game logic, combat formulas, procedural biomes, crafting registries, and save/load serialization:

```bash
.venv/bin/pytest tests/ -v
```

All 23 tests pass in under a second!

---

## 📜 License
MIT License. Created with passion for the Minecraft and text adventure communities.
