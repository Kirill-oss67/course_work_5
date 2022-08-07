from flask import Flask, render_template, request, redirect, url_for

from classes import unit_classes
from equipment import Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit
from base import Arena

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes, result="Бой начался!")


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)
    return render_template("fight.html", heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == "GET":
        header = "Выберите героя"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template(
            "hero_choosing.html",
            result={
                "header": header,
                "classes": classes,
                "weapons": weapons,
                "armors": armors
            }
        )
    if request.method == "POST":
        name = request.form.get("name")
        armor_name = request.form.get("armor")
        weapon_name = request.form.get("weapon")
        unit_class = request.form.get("unit_class")
        player = PlayerUnit(name=name,
                            weapon=Equipment().get_weapon(weapon_name),
                            armor=Equipment().get_armor(armor_name),
                            unit_class=unit_classes.get(unit_class))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        player.equip_armor(Equipment().get_armor(armor_name))
        heroes["player"] = player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        header = "Выберите врага"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template(
            "hero_choosing.html",
            result={
                "header": header,
                "classes": classes,
                "weapons": weapons,
                "armors": armors
            }
        )
    if request.method == "POST":
        name = request.form.get("name")
        armor_name = request.form.get("armor")
        weapon_name = request.form.get("weapon")
        unit_class = request.form.get("unit_class")
        enemy = EnemyUnit(name=name,
                          weapon=Equipment().get_weapon(weapon_name),
                          armor=Equipment().get_armor(armor_name),
                          unit_class=unit_classes.get(unit_class))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        enemy.equip_armor(Equipment().get_armor(armor_name))
        heroes["enemy"] = enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run(debug=True,port=9999)
