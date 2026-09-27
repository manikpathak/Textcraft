"""Core Game Engine managing world state, time cycle, player actions, and mechanics."""

import random
from typing import Dict, List, Optional, Tuple, Any
from textcraft.config import (
    TICKS_PER_DAY, TICKS_PER_ACTION, DIMENSION_OVERWORLD, DIMENSION_NETHER,
    DIMENSION_END, HUNGER_DEPLETION_PER_ACTION, TIER_HAND
)
from textcraft.models.player import Player
from textcraft.models.location import Location
from textcraft.models.item import ITEM_REGISTRY, Item
from textcraft.models.block import BLOCK_REGISTRY
from textcraft.models.recipe import (
    RECIPES, SMELTING_RECIPES, FURNACE_FUELS, find_recipes_for
)
from textcraft.world.generator import WorldGenerator
from textcraft.world.dimensions import get_portal_destination
from textcraft.engine.combat import CombatEngine

class Game:
    def __init__(self, seed: int = 1337):
        self.seed = seed
        self.world_gen = WorldGenerator(seed)
        self.player = Player()
        self.world_cache: Dict[str, Location] = {}
        self.current_coords: Tuple[int, int, int] = (0, 64, 0)
        self.current_dimension: str = DIMENSION_OVERWORLD
        self.ticks: int = 6000  # Start at Noon (12:00) on Day 1
        self.weather: str = "clear"
        self.is_game_over: bool = False
        self.action_logs: List[str] = []

        # Ensure starting location is loaded and visited
        start_loc = self.get_current_location()
        start_loc.visited = True

    @property
    def day_number(self) -> int:
        return (self.ticks // TICKS_PER_DAY) + 1

    @property
    def time_of_day_ticks(self) -> int:
        return self.ticks % TICKS_PER_DAY

    @property
    def is_night(self) -> bool:
        tod = self.time_of_day_ticks
        return 13000 <= tod <= 23000

    @property
    def time_formatted(self) -> str:
        # 0 = 06:00, 6000 = 12:00, 12000 = 18:00, 18000 = 00:00
        total_minutes = int((self.time_of_day_ticks / TICKS_PER_DAY) * 24 * 60)
        hours = (6 + (total_minutes // 60)) % 24
        minutes = total_minutes % 60
        phase = self.time_phase_name
        return f"Day {self.day_number}, {hours:02d}:{minutes:02d} ({phase})"

    @property
    def time_phase_name(self) -> str:
        tod = self.time_of_day_ticks
        if 0 <= tod < 2000:
            return "Dawn"
        elif 2000 <= tod < 10000:
            return "Day"
        elif 10000 <= tod < 13000:
            return "Sunset"
        elif 13000 <= tod < 17000:
            return "Dusk / Night"
        elif 17000 <= tod < 21000:
            return "Midnight"
        else:
            return "Deep Night"

    def get_location(self, x: int, y: int, z: int, dimension: str) -> Location:
        key = f"{dimension}:{x},{y},{z}"
        if key not in self.world_cache:
            loc = self.world_gen.generate_location(x, y, z, dimension, self.is_night)
            self.world_cache[key] = loc
        return self.world_cache[key]

    def get_current_location(self) -> Location:
        x, y, z = self.current_coords
        return self.get_location(x, y, z, self.current_dimension)

    def advance_time(self, ticks: int = TICKS_PER_ACTION) -> List[str]:
        logs = []
        old_is_night = self.is_night
        self.ticks += ticks

        # Burn player hunger
        self.player.burn_hunger(HUNGER_DEPLETION_PER_ACTION)
        metabolism_msg = self.player.tick_metabolism()
        if metabolism_msg:
            logs.append(metabolism_msg)

        # Check death from starvation or damage
        if not self.player.is_alive:
            self.is_game_over = True
            logs.append("[bold red]☠️ You died! Game over. ☠️[/bold red]")
            return logs

        # Check day/night transition
        new_is_night = self.is_night
        if not old_is_night and new_is_night:
            logs.append("[bold blue]🌙 The sun sinks below the horizon. Shadows stretch as darkness falls over the realm...[/bold blue]")
        elif old_is_night and not new_is_night:
            logs.append("[bold yellow]☀️ Dawn breaks! Warm sunlight illuminates the wilderness.[/bold yellow]")

        # Sunlight burn on undead mobs on surface
        loc = self.get_current_location()
        if loc.dimension == DIMENSION_OVERWORLD and loc.y >= 64 and not new_is_night:
            for mob in list(loc.mobs):
                if mob.burns_in_daylight and mob.is_alive():
                    mob.take_damage(8)
                    logs.append(f"[bold yellow]🔥 {mob.name} catches fire under the harsh daylight sun![/bold yellow]")
                    if not mob.is_alive():
                        logs.append(f"{mob.name} burned away to ash.")
                        loc.remove_mob(mob)
                        self.player.add_xp(mob.xp_reward)

        return logs

    # Movement Commands
    def move(self, direction: str) -> List[str]:
        dir_clean = direction.lower().strip()
        x, y, z = self.current_coords
        logs = []

        if dir_clean in ("north", "n"):
            z -= 1
        elif dir_clean in ("south", "s"):
            z += 1
        elif dir_clean in ("east", "e"):
            x += 1
        elif dir_clean in ("west", "w"):
            x -= 1
        elif dir_clean in ("down", "d", "dig down", "descend"):
            if y == 64:
                y = 48  # Shallow cave
            elif y == 48:
                y = 16  # Deep cave
            elif y == 16:
                y = -32 # Deepslate
            else:
                return ["You strike solid, impenetrable bedrock and cannot descend further."]
        elif dir_clean in ("up", "u", "climb up", "ascend", "surface"):
            if y == -32:
                y = 16
            elif y == 16:
                y = 48
            elif y == 48:
                y = 64
            else:
                return ["You are already on the surface and cannot ascend higher."]
        else:
            return [f"Unknown direction: {direction}. Use north, south, east, west, up, or down."]

        self.current_coords = (x, y, z)
        new_loc = self.get_current_location()
        new_loc.visited = True
        logs.append(f"You moved {dir_clean} to [bold cyan]{new_loc.title}[/bold cyan] ({x}, {y}, {z}).")
        logs.extend(self.advance_time())
        return logs

    # Mining & Gathering Commands
    def mine(self, target_query: str) -> List[str]:
        target = target_query.lower().strip().replace(" ", "_")
        loc = self.get_current_location()
        logs = []

        # Find matching resource
        matched_block_id = None
        for res_id in loc.resources.keys():
            if target == res_id or target in res_id or res_id in target:
                matched_block_id = res_id
                break

        if not matched_block_id:
            return [f"There is no '{target_query}' here to mine or harvest. Type 'look' to see available resources."]

        block_def = BLOCK_REGISTRY.get(matched_block_id)
        if not block_def:
            block_def = BLOCK_REGISTRY.get("stone")

        # Check tool requirements
        can_drop = block_def.can_harvest_with(self.player.tool_type, self.player.tool_tier)

        # Harvest 1 unit
        loc.harvest_resource(matched_block_id, 1)

        # Damage tool
        broken_tool = self.player.damage_mainhand(1)

        if can_drop:
            drop_id = block_def.drop_item_id or matched_block_id
            drop_count = block_def.drop_count
            self.player.add_item(drop_id, drop_count)
            item_name = ITEM_REGISTRY.get(drop_id, Item(drop_id, drop_id.replace("_", " "), "material")).name
            logs.append(f"⛏️ You mined {block_def.name} and collected [bold gold1]{drop_count}x {item_name}[/bold gold1]!")

            if block_def.xp_reward > 0:
                leveled = self.player.add_xp(block_def.xp_reward)
                logs.append(f"+{block_def.xp_reward} XP")
                if leveled:
                    logs.append(f"[bold gold1]✦ LEVEL UP! Reached Level {self.player.level}! ✦[/bold gold1]")
        else:
            logs.append(f"[yellow]⚠️ You broke the {block_def.name}, but without the proper tool ({block_def.harvest_tool} tier {block_def.min_tool_tier}+), it crumbled into nothingness![/yellow]")

        if broken_tool:
            logs.append(f"[bold red]Your {broken_tool} shattered while mining![/bold red]")

        logs.extend(self.advance_time())
        return logs

    # Crafting
    def craft(self, recipe_query: str, count: int = 1) -> List[str]:
        target = recipe_query.lower().strip().replace(" ", "_")
        loc = self.get_current_location()
        has_table = loc.has_crafting_table or self.player.has_item("crafting_table", 1)

        # Find matching recipe
        matching_recipes = find_recipes_for(target)
        if not matching_recipes:
            # Try fuzzy match
            for rec in RECIPES:
                if target in rec.result_id or rec.result_id in target:
                    matching_recipes.append(rec)
                    break

        if not matching_recipes:
            return [f"Unknown recipe: '{recipe_query}'. Type 'recipes' to see what you can craft!"]

        recipe = matching_recipes[0]

        if recipe.requires_crafting_table and not has_table:
            return [f"Crafting [bold]{recipe.result_id.replace('_', ' ')}[/bold] requires a Crafting Table! Place or carry one."]

        # Check required ingredients for count crafts
        for ing, req_qty in recipe.ingredients.items():
            total_req = req_qty * count
            if not self.player.has_item(ing, total_req):
                have = self.player.inventory.get(ing, 0)
                ing_name = ITEM_REGISTRY.get(ing, Item(ing, ing.replace("_", " "), "material")).name
                return [f"Not enough materials! Need {total_req}x {ing_name} (you have {have})."]

        # Deduct ingredients
        for ing, req_qty in recipe.ingredients.items():
            self.player.remove_item(ing, req_qty * count)

        # Add crafted result
        total_produced = recipe.result_count * count
        self.player.add_item(recipe.result_id, total_produced)
        result_name = ITEM_REGISTRY.get(recipe.result_id, Item(recipe.result_id, recipe.result_id.replace("_", " "), "material")).name

        logs = [f"🔨 Successfully crafted [bold green]{total_produced}x {result_name}[/bold green]!"]
        logs.extend(self.advance_time(500))
        return logs

    # Smelting in Furnace
    def smelt(self, item_query: str, fuel_query: Optional[str] = None, count: int = 1) -> List[str]:
        loc = self.get_current_location()
        if not loc.has_furnace:
            return ["There is no Furnace here! Place a furnace first to smelt ores or cook food."]

        target = item_query.lower().strip().replace(" ", "_")
        matched_input = None
        for inp in SMELTING_RECIPES.keys():
            if target == inp or target in inp or inp in target:
                matched_input = inp
                break

        if not matched_input:
            return [f"'{item_query}' cannot be smelted or cooked in a furnace."]

        if not self.player.has_item(matched_input, count):
            have = self.player.inventory.get(matched_input, 0)
            return [f"You do not have {count}x {matched_input.replace('_', ' ')} to smelt (you have {have})."]

        # Determine fuel
        selected_fuel = None
        if fuel_query:
            clean_fuel = fuel_query.lower().strip().replace(" ", "_")
            if clean_fuel in FURNACE_FUELS and self.player.has_item(clean_fuel, 1):
                selected_fuel = clean_fuel
        else:
            # Pick best available fuel automatically
            for f in ["coal", "charcoal", "lava_bucket", "oak_log", "oak_planks", "stick"]:
                if self.player.has_item(f, 1):
                    selected_fuel = f
                    break

        if not selected_fuel:
            return ["No furnace fuel available! You need coal, charcoal, wood, or sticks to fire the furnace."]

        # Calculate fuel needed
        fuel_power = FURNACE_FUELS[selected_fuel]
        fuel_units_needed = max(1, int(-(-count // fuel_power)))  # ceiling division
        if not self.player.has_item(selected_fuel, fuel_units_needed):
            return [f"You need {fuel_units_needed}x {selected_fuel} to smelt {count} items."]

        # Consume items and fuel
        self.player.remove_item(matched_input, count)
        self.player.remove_item(selected_fuel, fuel_units_needed)
        if selected_fuel == "lava_bucket":
            self.player.add_item("bucket", fuel_units_needed)

        recipe = SMELTING_RECIPES[matched_input]
        self.player.add_item(recipe.output_id, count)
        xp_gain = int(recipe.xp * count)
        if xp_gain > 0:
            self.player.add_xp(xp_gain)

        out_name = ITEM_REGISTRY.get(recipe.output_id, Item(recipe.output_id, recipe.output_id.replace("_", " "), "material")).name
        logs = [f"🔥 Smelted {count}x {matched_input.replace('_', ' ')} using {fuel_units_needed}x {selected_fuel}. Received [bold gold1]{count}x {out_name}[/bold gold1]!"]
        logs.extend(self.advance_time(1000 * count))
        return logs

    # Placing Blocks / Functional Objects
    def place(self, item_query: str) -> List[str]:
        target = item_query.lower().strip().replace(" ", "_")
        matched_id = None
        for inv_id in self.player.inventory.keys():
            if target == inv_id or target in inv_id or inv_id in target:
                matched_id = inv_id
                break

        if not matched_id:
            return [f"You do not have '{item_query}' in your inventory to place."]

        loc = self.get_current_location()

        # Handle specific blocks
        self.player.remove_item(matched_id, 1)
        loc.place_block(matched_id, 1)
        name = matched_id.replace("_", " ").title()

        logs = [f"Placed a [bold cyan]{name}[/bold cyan] at this location."]

        # Check if portal completed
        if matched_id == "obsidian" and loc.placed_blocks.get("obsidian", 0) >= 10:
            if not loc.has_portal:
                loc.has_portal = True
                logs.append("[bold magenta]✨ The obsidian frame pulses with otherworldly energy! A swirling purple Nether Portal has opened! ✨[/bold magenta]")

        logs.extend(self.advance_time(200))
        return logs

    # Build Shelter
    def build_shelter(self) -> List[str]:
        loc = self.get_current_location()
        if loc.has_shelter:
            return ["A protective shelter is already built here!"]

        # Check for 8 logs, 12 cobblestone, or 16 dirt
        materials = [
            ("oak_planks", 12),
            ("cobblestone", 12),
            ("oak_log", 6),
            ("dirt", 16)
        ]
        chosen_mat = None
        for mat, req in materials:
            if self.player.has_item(mat, req):
                chosen_mat = (mat, req)
                break

        if not chosen_mat:
            return ["You need at least 12 Planks, 12 Cobblestone, 6 Logs, or 16 Dirt to construct a shelter."]

        mat_id, count = chosen_mat
        self.player.remove_item(mat_id, count)
        loc.has_shelter = True
        logs = [f"🏡 You constructed a sturdy shelter using {count}x {mat_id.replace('_', ' ')}! This area is now protected from nighttime monster spawns."]
        logs.extend(self.advance_time(2000))
        return logs

    # Sleep
    def sleep(self) -> List[str]:
        loc = self.get_current_location()
        if not loc.has_bed and not self.player.has_item("bed", 1):
            return ["You need a bed to sleep! Craft and place one."]

        if not self.is_night:
            return ["You can only sleep at night or during a thunderstorm!"]

        # Check for monsters nearby
        for mob in loc.mobs:
            if mob.is_hostile and mob.is_alive():
                return [f"You may not rest now, there are monsters nearby: {mob.name}!"]

        # Sleep: advance ticks until next dawn (0 ticks)
        ticks_to_dawn = TICKS_PER_DAY - self.time_of_day_ticks
        self.ticks += ticks_to_dawn
        self.player.heal(10)
        self.player.spawn_point = (loc.x, loc.y, loc.z, loc.dimension)

        # Clear remaining hostile mobs from area
        loc.mobs = [m for m in loc.mobs if not m.is_hostile]

        logs = [
            "[bold cyan]💤 You lie down and drift off to sleep...[/bold cyan]",
            "[bold yellow]☀️ You wake up refreshed as the sun rises over the horizon. Spawn point set![/bold yellow]"
        ]
        return logs

    # Portal Travel
    def enter_portal(self) -> List[str]:
        loc = self.get_current_location()
        if not loc.has_portal:
            return ["There is no active portal here! Build an obsidian frame (10 obsidian) or find a stronghold."]

        dest_dim, dest_coords = get_portal_destination(self.current_dimension, self.current_coords)
        self.current_dimension = dest_dim
        self.current_coords = dest_coords

        new_loc = self.get_current_location()
        new_loc.has_portal = True
        new_loc.visited = True

        logs = [
            f"[bold magenta]🌀 The portal ripples and pulls you across dimensions! Entering {dest_dim.title()}...[/bold magenta]",
            f"You materialize at [bold cyan]{new_loc.title}[/bold cyan] ({dest_coords[0]}, {dest_coords[1]}, {dest_coords[2]})."
        ]
        logs.extend(self.advance_time(1000))
        return logs

    # Combat Commands
    def attack(self, target_query: str) -> List[str]:
        loc = self.get_current_location()
        mob = loc.find_mob(target_query)
        if not mob:
            mob_names = [m.name for m in loc.mobs]
            if mob_names:
                return [f"Could not find '{target_query}'. Visible creatures here: {', '.join(mob_names)}"]
            return ["There are no creatures here to attack."]

        logs = CombatEngine.attack_mob(self.player, mob, loc, is_ranged=False)
        logs.extend(self.advance_time(500))
        return logs

    def shoot(self, target_query: str) -> List[str]:
        if not self.player.has_item("bow", 1):
            return ["You don't have a Bow equipped or in your inventory!"]
        if not self.player.has_item("arrow", 1):
            return ["You don't have any arrows!"]

        loc = self.get_current_location()
        mob = loc.find_mob(target_query)
        if not mob:
            return [f"Could not find target '{target_query}'."]

        self.player.remove_item("arrow", 1)
        logs = CombatEngine.attack_mob(self.player, mob, loc, is_ranged=True)
        logs.extend(self.advance_time(500))
        return logs

    def block(self) -> List[str]:
        loc = self.get_current_location()
        logs = CombatEngine.block_with_shield(self.player, loc)
        logs.extend(self.advance_time(500))
        return logs

    # Chest interactions
    def chest_store(self, item_query: str, count: int = 1) -> List[str]:
        loc = self.get_current_location()
        if not loc.has_chest:
            return ["There is no chest here! Craft and place one first."]
        matched_id = None
        for inv_id in self.player.inventory.keys():
            if item_query in inv_id or inv_id in item_query:
                matched_id = inv_id
                break
        if not matched_id or not self.player.has_item(matched_id, count):
            return [f"You don't have {count}x {item_query} to store."]
        self.player.remove_item(matched_id, count)
        loc.chest_inventory[matched_id] = loc.chest_inventory.get(matched_id, 0) + count
        return [f"Stored {count}x {matched_id.replace('_', ' ')} in the chest."]

    def chest_take(self, item_query: str, count: int = 1) -> List[str]:
        loc = self.get_current_location()
        if not loc.has_chest:
            return ["There is no chest here!"]
        matched_id = None
        for c_id in loc.chest_inventory.keys():
            if item_query in c_id or c_id in item_query:
                matched_id = c_id
                break
        if not matched_id or loc.chest_inventory.get(matched_id, 0) < count:
            return [f"The chest does not have {count}x {item_query}."]
        current = loc.chest_inventory[matched_id]
        if current == count:
            del loc.chest_inventory[matched_id]
        else:
            loc.chest_inventory[matched_id] -= count
        self.player.add_item(matched_id, count)
        return [f"Retrieved {count}x {matched_id.replace('_', ' ')} from the chest."]
