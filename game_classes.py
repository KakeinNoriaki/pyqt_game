import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class Player:
    def __init__(self, hp, mp, wp, pt, arm=None):
        global hero
        global enemy_list
        self.hit_point_max = 100
        self.hit_point = hp
        self.mana_point_max = 100
        self.mana_point = mp
        self.weapon_in_hands = wp
        self.armor = arm
        self.in_defence = False  # если True то срезает урон по герою на 90%
        self.potion = None
        self.artefact = None
        self.damage = self.weapon_in_hands.damage
        self.armor_plus_stats()
        self.get_drink(pt)
        self.artefact_plus_stats()

    def armor_plus_stats(self):
        if self.armor is not None:
            self.hit_point_max += self.armor.plus_hit_point
            self.hit_point += self.armor.plus_hit_point
            self.mana_point_max += self.armor.plus_mana_point
            self.mana_point += self.armor.plus_mana_point

    def artefact_plus_stats(self):
        self.damage += self.artefact.plus_damage

    def alive(self):
        if self.hit_point > 0:
            return True
        print('ИГРА ОКОНЧЕНА!')
        return False

    def attack(self, target):
        block = 0  # срезает урон если враг в защитной стойке НА 70%
        if target.in_defence:
            block = (self.weapon_in_hands.damage / 100) * 70
        self.in_defence = False
        if target.alive is True:
            if self.mana_point - self.weapon_in_hands.mana_points_use >= 0:
                target.hit_points -= self.weapon_in_hands.damage - block
                self.mana_point -= self.weapon_in_hands.mana_points_use
                print('Вы нанесли урон врагу ' + target.name + ' в размере: '
                      + str(self.weapon_in_hands.damage + block) + '\nУ врага осталось '
                      + str(target.hit_points) + ' здоровья')
            else:
                print('мало маны')
        else:
            print('Враг ' + target.name + ' умер')

    def defence(self):
        self.in_defence = True
        print('Вы встали в защитную стойку')
        self.mana_point += 10
        if self.mana_point > self.mana_point_max:
            self.mana_point = self.mana_point_max

    def drink_potion(self):  # при выпивании зелья игрок встаёт в защитную стойку но без прибавке к мане
        if self.potion is not None:
            self.hit_point += self.potion.hit_point_heal
            if self.hit_point > self.hit_point_max:
                self.hit_point = self.hit_point_max
            self.mana_point += self.potion.mana_point_heal
            if self.mana_point > self.hit_point_max:
                self.mana_point = self.mana_point_max
            self.potion = None
            self.in_defence = True
            print('Вы выпили зелье теперь у вас ' + str(self.hit_point)
                  + ' здоровья и ' + str(self.mana_point) + ' маны')
        else:
            print('У вас не зелья')

    def change_weapon(self, new_wp):
        self.weapon_in_hands = new_wp

    def change_artefact(self, new_art):
        print('Вы сменили артефакт ' + self.artefact.name + ' на ' + new_art.name)
        self.artefact = new_art
        self.artefact_plus_stats()

    def get_drink(self, pt):
        self.potion = pt
        print('Вы получили новое зелье ' + self.potion.name)
        print(self.potion)

    def put_armor(self, new_armor):
        print('Теперь на вас надета ' + new_armor.name)
        self.hit_point_max -= self.armor.plus_hit_point
        self.mana_point_max -= self.armor.plus_mana_point
        self.armor = new_armor
        self.armor_plus_stats()


class Enemy:
    def __init__(self, nm, hp, pt, dm, btn):
        global hero
        global enemy_list
        self.name = nm
        self.hit_points = hp
        self.damage = dm
        self.pattern = pt  # attack, defense, heal
        self.next_move = 0
        self.button = btn
        self.in_defence = False

    def alive(self):
        if self.hit_points > 0:
            return True
        return False

    def attack(self, target):
        self.in_defence = False
        block = 0  # срезает урон если враг в защитной стойке НА 90%
        if target.in_defence:
            block = (self.damage / 100) * 90
        if target.alive:
            target.hit_points -= self.damage - block
            print('Враг ' + self.name + ' нанёс урон в размере ' + str(self.damage - block) + ' вам')
        else:
            print('Игра окончена')

    def heal(self):
        self.in_defence = False
        min_hp = 99999
        heal_him = ''
        for i in enemy_list:
            if i.hit_points < min_hp:
                min_hp = i.hit_points
                heal_him = enemy_list.index(i)
        enemy_list[heal_him].hit_points += self.damage
        print('Враг ' + self.name + ' выличил ' + enemy_list[heal_him].name)

    def defence(self):
        self.in_defence = True
        print('Враг ' + self.name + ' встал в защитную стойку')

    def move(self):
        if self.pattern[self.next_move] == 'attack':
            self.attack(hero)
        if self.pattern[self.next_move] == 'heal':
            self.heal()
        if self.pattern[self.next_move] == 'defence':
            self.defence()
        if self.next_move == len(self.pattern) - 1:
            self.next_move = 0
        else:
            self.next_move += 1


class Weapon:
    def __init__(self, nm, dm, mpu=0):
        self.name = nm
        self.damage = dm
        self.mana_points_use = mpu

    def __str__(self):
        return 'Оружие ' + self.name + ' наносит ' + str(self.damage) +\
               ' урона используя ' + str(self.mana_points_use) + ' маны'


class Armor:
    def __init__(self, nm, php, pmp):
        self.name = nm
        self.plus_hit_point = php
        self.plus_mana_point = pmp

    def __str__(self):
        return self.name + ' прибавляет ' + str(self.plus_hit_point) + ' и ' + str(self.plus_mana_point)


class Artefact:
    def __init__(self, nm, pd):
        self.name = nm
        self.plus_damage = pd

    def __str__(self):
        return 'Артефакт ' + self.name + ' прибавляет ' + str(self.plus_damage)


class Potion:
    def __init__(self, nm, hph, mph):
        self.name = nm
        self.hit_point_heal = hph
        self.mana_point_heal = mph

    def __str__(self):
        return 'Зелье ' + self.name + ' востонавливает ' + str(self.hit_point_heal)\
               + ' здоровья ' + str(self.mana_point_heal) + ' мана'


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('game_ui_disign.ui', self)
        self.initUI()
        global hero
        global enemy_list

    def initUI(self):
        pixmap_hero = QPixmap("ёлка.png")
        self.label_im_pl.setPixmap(pixmap_hero)
        pixmap_fon = QPixmap('фон.jpg')
        self.label_fon.setPixmap(pixmap_fon)
        self.attack_cancel()
        self.pushButton_attack_1.clicked.connect(self.btn_attack_1)
        self.pushButton_attack_2.clicked.connect(self.btn_attack_2)
        self.pushButton_attack_3.clicked.connect(self.btn_attack_3)
        self.pushButton_back.clicked.connect(self.attack_cancel)
        self.pushButton_attack.clicked.connect(self.hero_attack)
        self.pushButton_block.clicked.connect(self.hero_defence)
        self.pushButton_heal.clicked.connect(self.hero_drink_potion)

    def hero_attack(self):
        self.show_attack_buttons()

    def attack_cancel(self):
        self.pushButton_attack_1.hide()
        self.pushButton_attack_2.hide()
        self.pushButton_attack_3.hide()
        self.pushButton_back.hide()

    def show_attack_buttons(self):
        self.pushButton_attack_1.show()
        self.pushButton_attack_2.show()
        self.pushButton_attack_3.show()
        self.pushButton_back.show()

    def hero_defence(self):
        hero.defence()

    def hero_drink_potion(self):
        hero.drink_potion()

    def btn_attack_1(self):
        hero.attack(enemy_list[0])

    def btn_attack_2(self):
        hero.attack(enemy_list[1])

    def btn_attack_3(self):
        hero.attack(enemy_list[2])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
    hero = Player()
    potion = Potion()
    enemy_1 = Enemy()
    enemy_2 = Enemy()
    enemy_3 = Enemy()
    enemy_list = [enemy_1, enemy_2, enemy_3]
