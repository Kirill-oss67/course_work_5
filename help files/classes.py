from dataclasses import dataclass
from typing import Optional
from skills import FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Optional[FuryPunch, HardShot]


WarriorClass = UnitClass("Warrior", 60.0, 30.0, 0.8, 0.9, 1.2,
                         FuryPunch)  # TODO Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов

ThiefClass = UnitClass("Trief", 50.0, 25.0, 1.5, 1.2, 1.0, HardShot)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
