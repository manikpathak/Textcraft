"""Combat system handling attacks, weapons, shields, critical strikes, and mob retaliation."""

import random
from typing import List, Tuple, Optional
from textcraft.models.player import Player
from textcraft.models.mob import Mob
from textcraft.models.location import Location

class CombatEngine:
    @staticmethod
    def attack_mob(player: Player, mob: Mob, location: Location, is_ranged: bool = False) -> List[str]:
        """Executes a player attack turn against a mob. Returns log messages of events."""
        logs = []

        if not mob.is_alive():
            logs.append(f"{mob.name} is already defeated.")
            return logs

        # Calculate base damage
        if is_ranged:
            base_damage = 7
        else:
            base_damage = player.attack_damage

        # Critical strike chance (20% for melee, 25% for bow)
        is_crit = random.random() < (0.25 if is_ranged else 0.20)
        final_damage = int(round(base_damage * 1.5)) if is_crit else base_damage

        # Damage the mob
        dealt = mob.take_damage(final_damage)
        crit_text = " [bold yellow]★ CRITICAL HIT! ★[/bold yellow]" if is_crit else ""
        weapon_name = "bow" if is_ranged else (player.equipment.get("mainhand").name if player.equipment.get("mainhand") else "bare fists")
        logs.append(f"You struck {mob.name} with your {weapon_name} for [bold red]{dealt}[/bold red] damage!{crit_text}")

        # Damage player weapon durability
        if not is_ranged:
            broken = player.damage_mainhand(1)
            if broken:
                logs.append(f"[bold red]Your {broken} shattered from the blow![/bold red]")

        # Check if mob died
        if not mob.is_alive():
            logs.append(f"[bold green]{mob.name} collapsed and dissolved into dust![/bold green]")
            location.remove_mob(mob)

            # Award XP
            leveled = player.add_xp(mob.xp_reward)
            logs.append(f"You gained [bold green]+{mob.xp_reward} XP[/bold green]!")
            if leveled:
                logs.append(f"[bold gold1]✦ LEVEL UP! You reached Level {player.level}! ✦[/bold gold1]")

            # Loot drops
            loot = mob.roll_loot()
            if loot:
                loot_strs = []
                for item_id, count in loot:
                    player.add_item(item_id, count)
                    loot_strs.append(f"{count}x {item_id.replace('_', ' ')}")
                logs.append(f"Collected spoils: [bold gold1]{', '.join(loot_strs)}[/bold gold1]")

            # Check boss victory
            if mob.is_boss:
                logs.append("[bold magenta]★★★★★ THE ENDER DRAGON HAS BEEN SLAIN! VICTORY! ★★★★★[/bold magenta]")
                logs.append("A luminous exit portal of bedrock and stars opens before you!")
                location.has_portal = True

            return logs

        # Mob is still alive - Mob action / Retaliation
        if mob.fuse is not None:
            # Creeper fuse
            mob.fuse -= 1
            if mob.fuse <= 0:
                # Detonate!
                logs.append("[bold red]💥 The Creeper DETONATES with an ear-splitting BOOM! 💥[/bold red]")
                boom_dmg = player.take_damage(16)
                logs.append(f"The explosive blast dealt [bold red]{boom_dmg}[/bold red] damage to you!")
                location.remove_mob(mob)
                return logs
            else:
                logs.append(f"[bold red]⚠️ The Creeper swells and HISSES violently! (Fuse: {mob.fuse} ticks left!)[/bold red]")
        elif mob.attack_damage > 0:
            # Standard mob attack
            raw_dmg = mob.attack_damage
            dmg_taken = player.take_damage(raw_dmg)
            logs.append(f"{mob.name} {mob.attack_verb} you, dealing [bold red]{dmg_taken}[/bold red] damage! (Armor absorbed the rest)")

        return logs

    @staticmethod
    def block_with_shield(player: Player, location: Location) -> List[str]:
        """Raises shield for the turn, completely nullifying standard damage."""
        logs = []
        offhand = player.equipment.get("offhand")
        if not offhand or offhand.id != "shield":
            logs.append("You don't have a shield equipped in your offhand slot!")
            return logs

        logs.append("[bold cyan]🛡️ You raise your shield into a defensive stance![/bold cyan]")
        # Mobs attack the shield
        for mob in list(location.mobs):
            if not mob.is_hostile or not mob.is_alive():
                continue
            if mob.fuse is not None:
                mob.fuse -= 1
                if mob.fuse <= 0:
                    logs.append("[bold blue]💥 The Creeper explodes against your raised shield! The blast is completely blocked![/bold blue]")
                    location.remove_mob(mob)
                    offhand.damage(15)
                else:
                    logs.append(f"The Creeper hisses right in front of your shield! (Fuse: {mob.fuse})")
            else:
                logs.append(f"{mob.name} {mob.attack_verb} you, but your shield [bold cyan]DEFLECTS[/bold cyan] the entire impact!")
                offhand.damage(1)

        if offhand.current_durability is not None and offhand.current_durability <= 0:
            player.equipment["offhand"] = None
            logs.append("[bold red]Your shield broke from absorbing the heavy impacts![/bold red]")

        return logs
