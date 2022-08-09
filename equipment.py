from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


WeaponSchema = marshmallow_dataclass.class_schema(Weapon)
ArmorSchema = marshmallow_dataclass.class_schema(Armor)


@dataclass
class EquipmentData:
    weapons: List
    armors: List


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        return [weapon for weapon in self.equipment.weapons if weapon_name == weapon.name][0]

    def get_armor(self, armor_name: str) -> Armor:
        return [armor for armor in self.equipment.armors if armor_name == armor.name][0]

    def get_weapons_names(self) -> list:
        return [weapons.name for weapons in self.equipment.weapons]

    def get_armors_names(self) -> list:
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """метод загружает json в переменную EquipmentData"""
        with open("./data/equipment.json", 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return EquipmentData(weapons=WeaponSchema(many=True).load(data['weapons']),
                             armors=ArmorSchema(many=True).load(data['armors']))
