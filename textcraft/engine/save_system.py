"""Save and load game state system using JSON serialization."""

import os
import json
from typing import Dict, Any, List, Optional
from textcraft.engine.game import Game
from textcraft.models.player import Player
from textcraft.models.location import Location

SAVES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "saves")

class SaveSystem:
    @staticmethod
    def ensure_saves_dir() -> str:
        if not os.path.exists(SAVES_DIR):
            os.makedirs(SAVES_DIR, exist_ok=True)
        return SAVES_DIR

    @staticmethod
    def list_saves() -> List[str]:
        SaveSystem.ensure_saves_dir()
        saves = []
        for f in os.listdir(SAVES_DIR):
            if f.endswith(".json"):
                saves.append(f[:-5])
        return sorted(saves)

    @staticmethod
    def save_game(game: Game, save_name: str = "world") -> str:
        SaveSystem.ensure_saves_dir()
        filepath = os.path.join(SAVES_DIR, f"{save_name}.json")

        save_data: Dict[str, Any] = {
            "version": "1.0",
            "seed": game.seed,
            "player": game.player.to_dict(),
            "current_coords": list(game.current_coords),
            "current_dimension": game.current_dimension,
            "ticks": game.ticks,
            "weather": game.weather,
            "world_cache": {
                key: loc.to_dict() for key, loc in game.world_cache.items()
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2)

        return filepath

    @staticmethod
    def load_game(save_name: str = "world") -> Optional[Game]:
        SaveSystem.ensure_saves_dir()
        filepath = os.path.join(SAVES_DIR, f"{save_name}.json")
        if not os.path.exists(filepath):
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            save_data = json.load(f)

        seed = save_data.get("seed", 1337)
        game = Game(seed=seed)
        game.player = Player.from_dict(save_data["player"])
        game.current_coords = tuple(save_data["current_coords"])
        game.current_dimension = save_data.get("current_dimension", "overworld")
        game.ticks = save_data.get("ticks", 6000)
        game.weather = save_data.get("weather", "clear")

        game.world_cache = {}
        for key, loc_data in save_data.get("world_cache", {}).items():
            game.world_cache[key] = Location.from_dict(loc_data)

        return game
