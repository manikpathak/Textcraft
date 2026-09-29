"""Rich terminal display rendering for HUD, location panels, inventory, crafting, and map."""

from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.progress_bar import ProgressBar

from textcraft.config import (
    ICON_HEART, ICON_HUNGER, ICON_ARMOR, ICON_XP, ICON_CLOCK,
    ICON_FIRE, ICON_GRASS, ICON_CREATURES,
    COLOR_HEALTH, COLOR_HUNGER, COLOR_ARMOR, COLOR_XP,
    DIMENSION_OVERWORLD, DIMENSION_NETHER, DIMENSION_END
)
from textcraft.models.item import ITEM_REGISTRY, Item
from textcraft.models.recipe import RECIPES, find_recipes_for
from textcraft.ui.art import TEXTCRAFT_BANNER, BIOME_ICONS, MOB_ICONS

def render_hearts(health: int, max_health: int = 20) -> str:
    """Renders 10 hearts representing 20 HP."""
    full_hearts = health // 2
    half_heart = 1 if (health % 2 == 1) else 0
    empty_hearts = (max_health // 2) - full_hearts - half_heart
    return (
        f"[bold {COLOR_HEALTH}]" + (ICON_HEART * full_hearts) +
        ("½" if half_heart else "") +
        f"[/bold {COLOR_HEALTH}][dim white]" +
        ("♡" * max_hearts_empty(empty_hearts)) +
        "[/dim white]"
    )

def max_hearts_empty(count: int) -> int:
    return max(0, count)

def render_hunger(hunger: float, max_hunger: int = 20) -> str:
    """Renders drumsticks for hunger."""
    h_int = int(round(hunger))
    full = h_int // 2
    empty = max(0, (max_hunger // 2) - full)
    return (
        f"[bold {COLOR_HUNGER}]" + (ICON_HUNGER * full) +
        f"[/bold {COLOR_HUNGER}][dim white]" +
        ("○" * empty) +
        "[/dim white]"
    )

class Display:
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def welcome(self):
        self.console.print(TEXTCRAFT_BANNER)
        intro = (
            "[bold white]You awaken on a tranquil expanse under an endless sky.[/bold white]\n"
            "With bare hands, you must gather wood, fashion tools, build shelters, mine deep for diamonds,\n"
            "brave the fiery Nether, and conquer the Ender Dragon!\n\n"
            "[dim cyan]Type [bold white]help[/bold white] for command guide, [bold white]look[/bold white] to inspect surroundings, or [bold white]recipes[/bold white] to see crafting.[/dim cyan]"
        )
        self.console.print(Panel(intro, title="[bold gold1]✦ Welcome to Textcraft ✦[/bold gold1]", border_style="gold1"))
        self.console.print()

    def hud(self, game):
        player = game.player
        # Health & Hunger bars
        hearts_str = render_hearts(player.health, player.max_health)
        hunger_str = render_hunger(player.hunger, player.max_hunger)

        # Held item
        mainhand = player.equipment.get("mainhand")
        if mainhand:
            dur_str = f" ({mainhand.current_durability}/{mainhand.max_durability})" if mainhand.max_durability else ""
            tool_str = f"[bold cyan]Held:[/bold cyan] {mainhand.name}{dur_str}"
        else:
            tool_str = "[dim cyan]Held:[/dim cyan] Bare Hands"

        # Offhand / Shield
        offhand = player.equipment.get("offhand")
        off_str = f" | [bold cyan]Offhand:[/bold cyan] {offhand.name}" if offhand else ""

        # Coordinates & Time
        x, y, z = game.current_coords
        dim_name = game.current_dimension.replace("_", " ").title()
        time_icon = "☀️" if not game.is_night else "🌙"

        status_line_1 = f" [bold cyan]{player.name}[/bold cyan]  {hearts_str} [bold red]{player.health}/{player.max_health}[/bold red]   {hunger_str} [bold yellow]{int(player.hunger)}/20[/bold yellow]   [bold bright_cyan]{ICON_ARMOR} {player.total_armor}/20[/bold bright_cyan]   [bold green]{ICON_XP} Lvl {player.level}[/bold green]"
        status_line_2 = f" {time_icon} [bold bright_yellow]{game.time_formatted}[/bold bright_yellow]  |  [bold bright_cyan]{dim_name}[/bold bright_cyan] (X: {x}, Y: {y}, Z: {z})  |  {tool_str}{off_str}"

        self.console.print(Panel(
            f"{status_line_1}\n{status_line_2}",
            border_style="bright_blue",
            padding=(0, 1)
        ))

    def location(self, game):
        loc = game.get_current_location()
        icon = BIOME_ICONS.get(loc.biome, "🌍")

        content_parts = []
        content_parts.append(f"[italic white]{loc.description}[/italic white]\n")

        # Natural Resources
        if loc.resources:
            res_items = []
            for res_id, count in loc.resources.items():
                name = res_id.replace("_", " ").title()
                res_items.append(f"[bold dark_orange]{name}[/bold dark_orange] [dim]x{count}[/dim]")
            content_parts.append(f"[bold yellow]{ICON_GRASS} Natural Resources:[/bold yellow] {', '.join(res_items)}")
        else:
            content_parts.append(f"[dim yellow]{ICON_GRASS} Natural Resources:[/dim yellow] [dim]None remaining here.[/dim]")

        # Placed Structures
        structures = []
        if loc.has_shelter:
            structures.append("[bold green]🏡 Protective Shelter[/bold green]")
        if loc.has_crafting_table:
            structures.append("[bold dark_goldenrod]🔨 Crafting Table[/bold dark_goldenrod]")
        if loc.has_furnace:
            structures.append(f"[bold dark_orange3]{ICON_FIRE} Furnace[/bold dark_orange3]")
        if loc.has_chest:
            count = sum(loc.chest_inventory.values())
            structures.append(f"[bold gold1]📦 Storage Chest ({count} items)[/bold gold1]")
        if loc.has_bed:
            structures.append("[bold magenta]🛏️ Bed[/bold magenta]")
        if loc.is_lit:
            structures.append("[bold yellow]🕯️ Illuminated by Torches[/bold yellow]")
        if loc.has_portal:
            structures.append("[bold bright_magenta]🌀 Swirling Nether Portal[/bold bright_magenta]")

        if structures:
            content_parts.append(f"[bold cyan]🏛️ Structures Here:[/bold cyan] {' • '.join(structures)}")

        # Creatures / Mobs
        if loc.mobs:
            mob_parts = []
            for mob in loc.mobs:
                m_icon = MOB_ICONS.get(mob.id, "👾")
                color = "bold red" if mob.is_hostile else "bold green"
                if mob.is_boss:
                    color = "bold magenta"
                mob_parts.append(f"[{color}]{m_icon} {mob.name}[/{color}] [dim](HP: {mob.current_health}/{mob.max_health})[/dim]")
            content_parts.append(f"[bold red3]{ICON_CREATURES} Creatures Present:[/bold red3] {', '.join(mob_parts)}")

        # Available Exits
        exits = ["[bold cyan][N]orth[/bold cyan]", "[bold cyan][S]outh[/bold cyan]", "[bold cyan][E]ast[/bold cyan]", "[bold cyan][W]est[/bold cyan]"]
        if loc.y > -32:
            exits.append("[bold bright_blue][D]own / Dig Deep[/bold bright_blue]")
        if loc.y < 64:
            exits.append("[bold bright_blue][U]p / Climb Surface[/bold bright_blue]")
        if loc.has_portal:
            exits.append("[bold bright_magenta][P]ortal[/bold bright_magenta]")

        content_parts.append(f"[bold dim white]🚪 Exits:[/bold dim white] {' • '.join(exits)}")

        panel_title = f"{icon} [bold bright_green]{loc.title}[/bold bright_green] [dim]({loc.dimension}:{loc.x}, {loc.y}, {loc.z})[/dim]"
        self.console.print(Panel("\n".join(content_parts), title=panel_title, border_style="spring_green2"))

    def inventory(self, player):
        self.console.print(Panel("[bold cyan]🎒 PLAYER INVENTORY & EQUIPMENT[/bold cyan]", border_style="cyan"))

        # Equipment Table
        eq_table = Table(title="[bold yellow]Equipped Gear[/bold yellow]", border_style="dim cyan")
        eq_table.add_column("Slot", style="bold white", width=12)
        eq_table.add_column("Item", style="bold green", width=22)
        eq_table.add_column("Stats", style="bright_cyan", width=20)
        eq_table.add_column("Durability", style="yellow", width=16)

        slot_names = [
            ("Mainhand", "mainhand"),
            ("Offhand", "offhand"),
            ("Helmet", "helmet"),
            ("Chestplate", "chestplate"),
            ("Leggings", "leggings"),
            ("Boots", "boots")
        ]

        for display_slot, key in slot_names:
            gear = player.equipment.get(key)
            if gear:
                stats = []
                if gear.attack_damage > 1:
                    stats.append(f"+{gear.attack_damage} Atk")
                if gear.armor_points > 0:
                    stats.append(f"+{gear.armor_points} Armor")
                stats_str = ", ".join(stats) if stats else "Utility"
                dur_str = f"{gear.current_durability}/{gear.max_durability}" if gear.max_durability else "Infinite"
                eq_table.add_row(display_slot, gear.name, stats_str, dur_str)
            else:
                eq_table.add_row(display_slot, "[dim]Empty[/dim]", "-", "-")

        self.console.print(eq_table)

        # Inventory Items Table
        if not player.inventory:
            self.console.print("[dim italic]Your inventory is completely empty.[/dim italic]")
            return

        inv_table = Table(title=f"[bold yellow]Carried Items ({len(player.inventory)} item types)[/bold yellow]", border_style="dim green")
        inv_table.add_column("Item Name", style="bold green", width=24)
        inv_table.add_column("Count", style="bold gold1", justify="right", width=8)
        inv_table.add_column("Category", style="cyan", width=14)
        inv_table.add_column("Description", style="white", width=42)

        for item_id, count in sorted(player.inventory.items()):
            item_def = ITEM_REGISTRY.get(item_id, Item(item_id, item_id.replace("_", " ").title(), "material"))
            inv_table.add_row(item_def.name, str(count), item_def.category.capitalize(), item_def.description)

        self.console.print(inv_table)

    def recipes(self, player, has_table: bool, filter_query: str = ""):
        self.console.print(Panel(
            f"[bold gold1]🔨 CRAFTING RECIPE BOOK[/bold gold1] [dim](Crafting Table Active: {'[bold green]YES[/bold green]' if has_table else '[dim red]NO (2x2 only)[/dim red]'}[/dim])",
            border_style="gold1"
        ))

        table = Table(border_style="dim gold1")
        table.add_column("Result", style="bold green", width=20)
        table.add_column("Workstation", style="cyan", width=12)
        table.add_column("Ingredients Required", style="white", width=34)
        table.add_column("Craftable?", style="bold", width=12)

        filter_clean = filter_query.lower().strip()
        matched = 0

        for rec in RECIPES:
            res_def = ITEM_REGISTRY.get(rec.result_id, Item(rec.result_id, rec.result_id.replace("_", " ").title(), "material"))
            if filter_clean and (filter_clean not in rec.result_id and filter_clean not in res_def.name.lower()):
                continue

            matched += 1
            station = "3x3 Table" if rec.requires_crafting_table else "2x2 Hand"

            # Check materials
            ing_strs = []
            can_craft = True
            possible_crafts = []
            for ing_id, req_qty in rec.ingredients.items():
                have = player.inventory.get(ing_id, 0)
                ing_name = ITEM_REGISTRY.get(ing_id, Item(ing_id, ing_id.replace("_", " "), "material")).name
                color = "green" if have >= req_qty else "red"
                ing_strs.append(f"[{color}]{have}/{req_qty} {ing_name}[/{color}]")
                if have < req_qty:
                    can_craft = False
                else:
                    possible_crafts.append(have // req_qty)

            if rec.requires_crafting_table and not has_table:
                can_craft = False

            if can_craft:
                max_c = min(possible_crafts) if possible_crafts else 1
                craft_status = f"[bold green]YES ({max_c})[/bold green]"
            else:
                craft_status = "[dim red]NO[/dim red]"

            result_display = f"{rec.result_count}x {res_def.name}"
            table.add_row(result_display, station, ", ".join(ing_strs), craft_status)

        if matched == 0:
            self.console.print(f"[dim]No recipes matching '{filter_query}' found.[/dim]")
        else:
            self.console.print(table)
            self.console.print("[dim cyan]Usage: [bold white]craft <item_name> [amount][/bold white]  (e.g., [italic]craft wooden_pickaxe[/italic] or [italic]craft 4 torch[/italic])[/dim cyan]")

    def map(self, game):
        cur_x, cur_y, cur_z = game.current_coords
        dim = game.current_dimension

        map_table = Table(title=f"[bold bright_cyan]World Map ({dim.title()} - Level Y={cur_y})[/bold bright_cyan]", border_style="cyan")
        # 7 columns
        for _ in range(7):
            map_table.add_column(justify="center", width=5)

        # Render 7x7 grid centered at player (radius = 3)
        for dz in range(-3, 4):
            row = []
            for dx in range(-3, 4):
                tx = cur_x + dx
                tz = cur_z + dz
                if dx == 0 and dz == 0:
                    row.append("[bold bright_white on dark_green] @ [/bold bright_white on dark_green]")
                else:
                    key = f"{dim}:{tx},{cur_y},{tz}"
                    if key in game.world_cache and game.world_cache[key].visited:
                        loc = game.world_cache[key]
                        if loc.has_portal:
                            row.append("[bold magenta]🌀[/bold magenta]")
                        elif loc.has_shelter:
                            row.append("[bold green]🏡[/bold green]")
                        else:
                            icon = BIOME_ICONS.get(loc.biome, "·")
                            row.append(f"[bold]{icon}[/bold]")
                    else:
                        row.append("[dim] · [/dim]")
            map_table.add_row(*row)

        self.console.print(map_table)
        self.console.print("[dim]Legend: [bold white]@[/bold white] You  |  [bold green]🏡[/bold green] Shelter  |  [bold magenta]🌀[/bold magenta] Portal  |  [dim]·[/dim] Unexplored[/dim]")

    def help(self, topic: str = ""):
        help_table = Table(title="[bold gold1]Textcraft Command Manual[/bold gold1]", border_style="gold1")
        help_table.add_column("Category", style="bold cyan", width=15)
        help_table.add_column("Command Syntax", style="bold white", width=28)
        help_table.add_column("Description", style="white", width=38)

        commands = [
            ("Movement", "north / south / east / west (n, s, e, w)", "Move between adjacent world nodes"),
            ("Movement", "down / dig down (d)", "Descend deeper into caves and deepslate"),
            ("Movement", "up / climb up (u)", "Ascend toward the surface"),
            ("Exploration", "look / l", "Inspect surroundings, resources, and mobs"),
            ("Exploration", "inventory / i", "Inspect carried items and equipped gear"),
            ("Exploration", "map / m", "Display explored local mini-map"),
            ("Exploration", "status / time", "Check clock, survival stats, and level"),
            ("Gathering", "mine <target> / chop <wood>", "Harvest logs, stone, ores, dirt, or sand"),
            ("Crafting", "recipes [filter]", "Browse recipe book & material status"),
            ("Crafting", "craft <item> [count]", "Craft tools, weapons, armor, or items"),
            ("Smelting", "smelt <ore/food> [with <fuel>]", "Use furnace to smelt ingots or cook meat"),
            ("Placement", "place <block/station>", "Place crafting table, furnace, chest, bed"),
            ("Placement", "build shelter", "Construct shelter to prevent night monster spawns"),
            ("Sleep", "sleep", "Rest in bed to skip night and reset monsters"),
            ("Storage", "store <qty> <item>", "Deposit items into placed chest"),
            ("Storage", "take <qty> <item>", "Retrieve items from placed chest"),
            ("Equipment", "equip <item> / unequip <slot>", "Wield weapons/tools or wear armor pieces"),
            ("Survival", "eat <food> [count]", "Consume food portions to restore hunger & heal"),
            ("Combat", "attack <mob> / hit <mob>", "Melee attack with held weapon or fists"),
            ("Combat", "shoot <mob>", "Fire bow & arrow from a safe distance"),
            ("Combat", "block", "Raise shield in offhand to absorb attacks"),
            ("Dimensions", "enter portal", "Travel between Overworld and Nether/End"),
            ("System", "save [name] / load [name]", "Save or load your world state"),
            ("System", "quit / exit", "Exit the game")
        ]

        for cat, cmd, desc in commands:
            if not topic or topic.lower() in cat.lower() or topic.lower() in cmd.lower() or topic.lower() in desc.lower():
                help_table.add_row(cat, cmd, desc)

        self.console.print(help_table)

    def start_screen(self, saves: List[str]) -> tuple:
        """Display world selection screen and return (choice_type, save_name).

        choice_type is either "new" or "load".
        save_name is empty for "new", or the save name for "load".
        """
        while True:
            # Build the menu content
            lines = [" [bold]Choose Your Adventure[/bold]"]
            lines.append("")
            lines.append(" [bold green][N][/bold green] New Game")

            for i, save_name in enumerate(saves, 1):
                lines.append(f" [bold green][{i}][/bold green] {save_name}")

            menu_text = "\n".join(lines)
            self.console.print(Panel(menu_text, border_style="gold1", padding=(1, 2)))

            # Get user choice
            choice = self.console.input("[bold cyan]Enter choice (N or 1–{0}): [/bold cyan]".format(len(saves))).strip().upper()

            if choice == "N":
                return ("new", "")

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(saves):
                    return ("load", saves[idx])

            self.console.print("[yellow]Invalid choice. Try again.[/yellow]")

    def prompt_player_name(self) -> str:
        """Prompt for player name, return input or default to 'Steve'."""
        name = self.console.input("Enter your name [[bold]Steve[/bold]]: ").strip()
        return name if name else "Steve"
