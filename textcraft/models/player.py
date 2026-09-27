"""Player model representing health, hunger, inventory, equipment, armor, and stats."""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, Any
from textcraft.config import (
    MAX_HEALTH, MAX_HUNGER, DEFAULT_STARTING_HEALTH, DEFAULT_STARTING_HUNGER,
    TIER_HAND, HEAL_HUNGER_THRESHOLD, STARVATION_HUNGER_THRESHOLD,
    HEAL_AMOUNT, STARVATION_DAMAGE
)
from textcraft.models.item import (
    Item, ITEM_REGISTRY, ITEM_CATEGORY_ARMOR, ITEM_CATEGORY_FOOD,
    ARMOR_SLOT_HELMET, ARMOR_SLOT_CHESTPLATE, ARMOR_SLOT_LEGGINGS,
    ARMOR_SLOT_BOOTS, ARMOR_SLOT_OFFHAND
)

@dataclass
class Player:
    health: int = DEFAULT_STARTING_HEALTH
    max_health: int = MAX_HEALTH
    hunger: float = float(DEFAULT_STARTING_HUNGER)
    max_hunger: int = MAX_HUNGER
    saturation: float = 5.0
    xp: int = 0
    level: int = 0
    inventory: Dict[str, int] = field(default_factory=dict)
    # Equipment slots: mainhand, offhand, helmet, chestplate, leggings, boots
    equipment: Dict[str, Optional[Item]] = field(default_factory=lambda: {
        "mainhand": None,
        "offhand": None,
        "helmet": None,
        "chestplate": None,
        "leggings": None,
        "boots": None,
    })
    spawn_point: Tuple[int, int, int, str] = (0, 64, 0, "overworld")

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def total_armor(self) -> int:
        points = 0
        for slot in ["helmet", "chestplate", "leggings", "boots", "offhand"]:
            item = self.equipment.get(slot)
            if item and item.armor_points:
                points += item.armor_points
        return min(20, points)

    @property
    def attack_damage(self) -> int:
        mainhand = self.equipment.get("mainhand")
        if mainhand:
            return mainhand.attack_damage
        return 1  # Bare fists

    @property
    def tool_type(self) -> Optional[str]:
        mainhand = self.equipment.get("mainhand")
        if mainhand and mainhand.tool_type:
            return mainhand.tool_type
        return None

    @property
    def tool_tier(self) -> int:
        mainhand = self.equipment.get("mainhand")
        if mainhand:
            return mainhand.tool_tier
        return TIER_HAND

    def add_item(self, item_id: str, count: int = 1) -> int:
        """Adds count items to inventory. Returns new count."""
        if count <= 0:
            return self.inventory.get(item_id, 0)
        self.inventory[item_id] = self.inventory.get(item_id, 0) + count
        return self.inventory[item_id]

    def remove_item(self, item_id: str, count: int = 1) -> bool:
        """Removes count items from inventory. Returns True if successful, False if insufficient."""
        if count <= 0:
            return True
        current = self.inventory.get(item_id, 0)
        if current < count:
            return False
        if current == count:
            del self.inventory[item_id]
        else:
            self.inventory[item_id] = current - count
        return True

    def has_item(self, item_id: str, count: int = 1) -> bool:
        return self.inventory.get(item_id, 0) >= count

    def equip(self, item_id: str, target_slot: Optional[str] = None) -> Tuple[bool, str]:
        """Equips an item from inventory to its designated or specified slot."""
        if not self.has_item(item_id, 1):
            return False, f"You don't have any {item_id.replace('_', ' ')} in your inventory."

        item_def = ITEM_REGISTRY.get(item_id)
        if not item_def:
            return False, f"Unknown item: {item_id}"

        # Determine target slot
        if not target_slot:
            if item_def.category == ITEM_CATEGORY_ARMOR:
                target_slot = item_def.armor_slot
            elif item_def.is_tool_or_weapon:
                target_slot = "mainhand"
            elif item_id == "shield":
                target_slot = "offhand"
            else:
                target_slot = "mainhand"

        if target_slot not in self.equipment:
            return False, f"Invalid equipment slot: {target_slot}"

        # Unequip existing item in that slot back into inventory if present
        current = self.equipment[target_slot]
        if current:
            self.add_item(current.id, 1)

        # Remove from inventory and set equipment
        self.remove_item(item_id, 1)
        self.equipment[target_slot] = Item.from_id(item_id)
        return True, f"Equipped {item_def.name} in {target_slot} slot."

    def unequip(self, slot: str) -> Tuple[bool, str]:
        """Unequips item from slot back into inventory."""
        if slot not in self.equipment:
            return False, f"Invalid slot: {slot}"
        item = self.equipment[slot]
        if not item:
            return False, f"Nothing is equipped in {slot}."
        self.add_item(item.id, 1)
        self.equipment[slot] = None
        return True, f"Unequipped {item.name} from {slot}."

    def eat(self, item_id: str, count: int = 1) -> Tuple[bool, str]:
        """Eats one or more food items from inventory, restoring hunger and saturation."""
        target = item_id.lower().strip().replace(" ", "_")
        if not self.has_item(target, 1):
            # Check if there is an item in inventory matching partial query
            matched = None
            for inv_id in self.inventory.keys():
                if target in inv_id or inv_id in target:
                    matched = inv_id
                    break
            if matched:
                target = matched
            else:
                return False, f"You don't have {item_id.replace('_', ' ')} to eat."

        item_def = ITEM_REGISTRY.get(target)
        if not item_def or not item_def.is_food:
            return False, f"{target.replace('_', ' ').title()} is not edible!"

        if self.hunger >= self.max_hunger and target != "golden_apple":
            return False, "Your hunger bar is already completely full (20/20)!"

        available = self.inventory.get(target, 0)
        to_eat = min(count, available)

        eaten = 0
        old_hunger = self.hunger

        while eaten < to_eat:
            if self.hunger >= self.max_hunger and target != "golden_apple":
                break
            self.remove_item(target, 1)
            self.hunger = min(float(self.max_hunger), self.hunger + item_def.food_points)
            self.saturation = min(float(self.hunger), self.saturation + item_def.saturation)
            if target == "golden_apple":
                self.heal(4)
            eaten += 1

        restored = int(round(self.hunger - old_hunger))
        stopped_early = (eaten < count and self.hunger >= self.max_hunger and target != "golden_apple")

        portion_text = f"{eaten}x {item_def.name}"
        if stopped_early:
            return True, f"You ate {portion_text} (hunger reached maximum 20/20). Restored {restored} hunger points!"
        else:
            return True, f"You ate {portion_text}. Restored {restored} hunger points!"

    def take_damage(self, amount: int, ignore_armor: bool = False) -> int:
        """Applies damage considering armor reduction (Minecraft damage formula)."""
        if amount <= 0:
            return 0
        if ignore_armor:
            final_damage = amount
        else:
            # Minecraft formula: damage * (1 - min(20, max(armor / 5, armor - damage / (2 + toughness / 4))) / 25)
            # Simplified text adventure formula:
            reduction = min(0.80, (self.total_armor * 0.04))
            final_damage = max(1, int(round(amount * (1.0 - reduction))))

        # Damage armor durability
        if not ignore_armor and self.total_armor > 0:
            for slot in ["helmet", "chestplate", "leggings", "boots", "offhand"]:
                gear = self.equipment.get(slot)
                if gear and gear.max_durability:
                    if gear.damage(1):
                        self.equipment[slot] = None

        self.health = max(0, self.health - final_damage)
        return final_damage

    def heal(self, amount: int) -> int:
        if amount <= 0:
            return 0
        actual = min(self.max_health - self.health, amount)
        self.health += actual
        return actual

    def burn_hunger(self, amount: float):
        """Burns saturation first, then hunger."""
        if self.saturation > 0:
            sat_loss = min(self.saturation, amount)
            self.saturation -= sat_loss
            amount -= sat_loss
        if amount > 0:
            self.hunger = max(0.0, self.hunger - amount)

    def tick_metabolism(self) -> Optional[str]:
        """Handles natural regeneration and starvation damage."""
        if self.hunger >= HEAL_HUNGER_THRESHOLD and self.health < self.max_health:
            self.heal(HEAL_AMOUNT)
            self.burn_hunger(1.0)
            return "You feel a surge of stamina and regenerate health."
        elif self.hunger <= STARVATION_HUNGER_THRESHOLD:
            self.take_damage(STARVATION_DAMAGE, ignore_armor=True)
            return "You are starving! You took starvation damage!"
        return None

    def add_xp(self, amount: int) -> bool:
        """Adds experience points, calculates level ups. Returns True if leveled up."""
        if amount <= 0:
            return False
        self.xp += amount
        needed_for_next = (self.level + 1) * 10
        leveled_up = False
        while self.xp >= needed_for_next:
            self.xp -= needed_for_next
            self.level += 1
            leveled_up = True
            needed_for_next = (self.level + 1) * 10
        return leveled_up

    def damage_mainhand(self, amount: int = 1) -> Optional[str]:
        """Damages current held tool or weapon. Returns item name if it breaks."""
        mainhand = self.equipment.get("mainhand")
        if mainhand and mainhand.max_durability:
            if mainhand.damage(amount):
                broken_name = mainhand.name
                self.equipment["mainhand"] = None
                return broken_name
        return None

    def to_dict(self) -> Dict[str, Any]:
        eq_dict = {}
        for slot, item in self.equipment.items():
            eq_dict[slot] = item.to_dict() if item else None
        return {
            "health": self.health,
            "max_health": self.max_health,
            "hunger": self.hunger,
            "max_hunger": self.max_hunger,
            "saturation": self.saturation,
            "xp": self.xp,
            "level": self.level,
            "inventory": dict(self.inventory),
            "equipment": eq_dict,
            "spawn_point": list(self.spawn_point),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        player = cls(
            health=data.get("health", DEFAULT_STARTING_HEALTH),
            max_health=data.get("max_health", MAX_HEALTH),
            hunger=float(data.get("hunger", DEFAULT_STARTING_HUNGER)),
            max_hunger=data.get("max_hunger", MAX_HUNGER),
            saturation=float(data.get("saturation", 5.0)),
            xp=data.get("xp", 0),
            level=data.get("level", 0),
            inventory=data.get("inventory", {}),
            spawn_point=tuple(data.get("spawn_point", (0, 64, 0, "overworld"))),
        )
        eq_data = data.get("equipment", {})
        for slot, item_data in eq_data.items():
            if item_data:
                player.equipment[slot] = Item.from_id(item_data["id"], item_data.get("current_durability"))
        return player
