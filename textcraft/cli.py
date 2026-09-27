"""Main CLI interface and interactive game loop for Textcraft."""

import sys
import random
from typing import Optional
from rich.console import Console

from textcraft.engine.game import Game
from textcraft.engine.parser import CommandParser, ParsedCommand
from textcraft.engine.save_system import SaveSystem
from textcraft.ui.display import Display
from textcraft.ui.completer import TextcraftCompleter
from textcraft.ui.art import GAME_OVER_BANNER, VICTORY_BANNER

def run_cli():
    console = Console()
    display = Display(console)

    display.welcome()

    # World setup
    game = Game(seed=random.randint(1000, 9999))

    # Try setting up prompt_toolkit session
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import InMemoryHistory
        session = PromptSession(completer=TextcraftCompleter(), history=InMemoryHistory())
        use_prompt_toolkit = sys.stdin.isatty()
    except Exception:
        session = None
        use_prompt_toolkit = False

    # Initial view
    display.hud(game)
    display.location(game)

    while not game.is_game_over:
        try:
            if use_prompt_toolkit and session:
                user_input = session.prompt("Textcraft ❯ ")
            else:
                user_input = input("Textcraft ❯ ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Saving game before exit...[/yellow]")
            SaveSystem.save_game(game, "quicksave")
            console.print("[green]Saved to quicksave.json. Farewell, adventurer![/green]")
            break

        cmd = CommandParser.parse(user_input)

        if cmd.verb == "quit":
            console.print("[yellow]Quicksaving world...[/yellow]")
            SaveSystem.save_game(game, "quicksave")
            console.print("[bold green]Thank you for playing Textcraft! Until next time.[/bold green]")
            break

        execute_command(game, cmd, display, console)

        if game.is_game_over:
            score = game.player.level * 100 + len(game.world_cache) * 20
            console.print(GAME_OVER_BANNER.format(score=score, days=game.day_number))
            break

def execute_command(game: Game, cmd: ParsedCommand, display: Display, console: Console):
    verb = cmd.verb

    if verb == "look":
        display.hud(game)
        display.location(game)
        return

    if verb == "inventory":
        display.inventory(game.player)
        return

    if verb == "map":
        display.map(game)
        return

    if verb == "status":
        display.hud(game)
        return

    if verb == "time":
        console.print(f"[bold bright_yellow]⏱️ Current Time: {game.time_formatted}[/bold bright_yellow]")
        return

    if verb == "help":
        display.help(cmd.target)
        return

    if verb == "recipes":
        loc = game.get_current_location()
        has_table = loc.has_crafting_table or game.player.has_item("crafting_table", 1)
        display.recipes(game.player, has_table, filter_query=cmd.target)
        return

    # Game state modifying commands
    logs = []
    if verb == "move":
        logs = game.move(cmd.target)
        display.hud(game)
        display.location(game)
    elif verb == "mine":
        logs = game.mine(cmd.target)
    elif verb == "craft":
        logs = game.craft(cmd.target, count=cmd.count)
    elif verb == "smelt":
        logs = game.smelt(cmd.target, fuel_query=cmd.extra, count=cmd.count)
    elif verb == "place":
        logs = game.place(cmd.target)
    elif verb == "shelter":
        logs = game.build_shelter()
    elif verb == "sleep":
        logs = game.sleep()
    elif verb == "portal":
        logs = game.enter_portal()
        display.hud(game)
        display.location(game)
    elif verb == "attack":
        logs = game.attack(cmd.target)
    elif verb == "shoot":
        logs = game.shoot(cmd.target)
    elif verb == "block":
        logs = game.block()
    elif verb == "eat":
        success, msg = game.player.eat(cmd.target)
        logs = [f"[bold green]{msg}[/bold green]" if success else f"[bold yellow]{msg}[/bold yellow]"]
    elif verb == "equip":
        success, msg = game.player.equip(cmd.target)
        logs = [f"[bold green]{msg}[/bold green]" if success else f"[bold yellow]{msg}[/bold yellow]"]
    elif verb == "unequip":
        success, msg = game.player.unequip(cmd.target)
        logs = [f"[bold green]{msg}[/bold green]" if success else f"[bold yellow]{msg}[/bold yellow]"]
    elif verb == "chest_store":
        logs = game.chest_store(cmd.target, count=cmd.count)
    elif verb == "chest_take":
        logs = game.chest_take(cmd.target, count=cmd.count)
    elif verb == "save":
        s_name = cmd.target or "world"
        path = SaveSystem.save_game(game, s_name)
        logs = [f"[bold green]World saved successfully to {path}[/bold green]"]
    elif verb == "load":
        s_name = cmd.target or "world"
        loaded = SaveSystem.load_game(s_name)
        if loaded:
            # Transfer state
            game.__dict__.update(loaded.__dict__)
            logs = [f"[bold green]World loaded successfully from '{s_name}'![/bold green]"]
            display.hud(game)
            display.location(game)
        else:
            logs = [f"[bold red]Could not find save file for '{s_name}'. Type 'saves' to view saves.[/bold red]"]
    elif verb == "saves":
        saves = SaveSystem.list_saves()
        if saves:
            logs = [f"Available saves: [bold cyan]{', '.join(saves)}[/bold cyan]"]
        else:
            logs = ["No save files found."]
    elif verb == "unknown":
        logs = [f"[dim red]I don't understand '{cmd.raw}'. Type [bold white]help[/bold white] for command manual.[/dim red]"]

    # Output logs
    for log in logs:
        console.print(log)

if __name__ == "__main__":
    run_cli()
