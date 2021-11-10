import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class Player:
    def __init__(self, hp, mp, wp, pt, arm=None):
        global hero
        global enemy_list
        global ex
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
        ex.label_arm.setText('Оружие: ' + self.weapon_in_hands.name)

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
        ex.log.append('ИГРА ОКОНЧЕНА!')
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
                ex.log.append('Вы нанесли урон врагу ' + target.name + ' в размере: '
                              + str(self.weapon_in_hands.damage + block) + '\nУ врага осталось '
                              + str(target.hit_points) + ' здоровья')
                return True
            else:
                raise ValueError('Мало маны')
        else:
            raise ValueError('Враг ' + target.name + ' умер')

    def defence(self):
        self.in_defence = True
        ex.log.append('Вы встали в защитную стойку')
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
            ex.log.append('Вы выпили зелье теперь у вас ' + str(self.hit_point)
                          + ' здоровья и ' + str(self.mana_point) + ' маны')
        else:
            raise ValueError('У вас не зелья')

    def change_weapon(self, new_wp):
        self.weapon_in_hands = new_wp
        ex.log.append('Вы подобрали новое оружие')
        ex.log.append(self.weapon_in_hands)
        ex.label_arm.setText('Оружие: ' + self.weapon_in_hands.name)

    def change_artefact(self, new_art):
        ex.log.append('Вы сменили артефакт ' + self.artefact.name + ' на ' + new_art.name)
        self.artefact = new_art
        self.artefact_plus_stats()
        ex.label_arm.setText('Артефакт: ' + self.artefact.name)

    def get_drink(self, pt):
        self.potion = pt
        ex.log.append('Вы получили новое зелье ' + self.potion.name)
        ex.log.append(self.potion)

    def put_armor(self, new_armor):
        ex.log.append('Теперь на вас надета ' + new_armor.name)
        if self.armor is not None:
            self.hit_point_max -= self.armor.plus_hit_point
            self.mana_point_max -= self.armor.plus_mana_point
        self.armor = new_armor
        self.armor_plus_stats()
        ex.log.append(self.armor)
        ex.label_arm.setText('Броня: ' + self.armor.name)


class Enemy:
    def __init__(self, nm, hp, pt, dm, img):
        global hero
        global enemy_list
        global ex
        self.name = nm
        self.hit_points = hp
        self.damage = dm
        self.pattern = pt  # attack, defense, heal
        self.next_move = 0
        self.in_defence = False
        self.image = img

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
            ex.log.append('Враг ' + self.name + ' нанёс урон в размере ' + str(self.damage - block) + ' вам')
        else:
            ex.log.append('Игра окончена')

    def heal(self):
        self.in_defence = False
        min_hp = 99999
        heal_him = ''
        for i in enemy_list.enemys:
            if i.hit_points < min_hp:
                min_hp = i.hit_points
                heal_him = enemy_list.enemys.index(i)
        enemy_list[heal_him].hit_points += self.damage
        ex.log.append('Враг ' + self.name + ' выличил ' + enemy_list[heal_him].name)

    def defence(self):
        self.in_defence = True
        ex.log.append('Враг ' + self.name + ' встал в защитную стойку')

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
        return 'Зелье ' + self.name + ' васстонавливает ' + str(self.hit_point_heal)\
               + ' здоровья ' + str(self.mana_point_heal) + ' маны'


class EnemyList:
    def __init__(self, enemys):
        global hero
        self.enemys = enemys
        # имя и патерны противника
        self.names = {'Большая крыса': [['attack', 'defence', 'attack'], ['defence', 'attack', 'defence']],
                      'Гоблин-воин': [['attack', 'attack', 'attack'], ['defence', 'attack', 'defence']],
                      'Гоблин-знахарь': [['defence', 'heal', 'heal']],
                      'Муравьиная королева': [['attack', 'defence', 'heal']],
                      'Муравей-рабочий': [['attack', 'attack', 'defence'], ['defence', 'defence', 'attack']],
                      'Муравей-трутень': [['attack', 'attack', 'defence'], ['defence', 'defence', 'attack']]}

    def __getitem__(self, key):
        return self.enemys[key]

    def generation_new_enemys(self):
        if random.choice(self.names) == 'Большая крыса':
            self.enemys = [Enemy('Большая крыса', hero.weapon_in_hands.damage * 3 + random.randint(-10, 10),
                                 self.names['Большая крыса'][0], hero.hit_point_max // 20, 'big_rat.png'),
                           Enemy('Большая крыса', hero.weapon_in_hands.damage * 3 + random.randint(-10, 10),
                                 self.names['Большая крыса'][1], hero.hit_point_max // 20, 'big_rat.png'),
                           Enemy('Большая крыса', hero.weapon_in_hands.damage * 3 + random.randint(-10, 10),
                                 self.names['Большая крыса'][1], hero.hit_point_max // 20, 'big_rat.png')]
        if random.choice(self.names) == 'Гоблин-воин' or random.choice(self.names) == 'Гоблин-знахарь':
            self.enemys = [Enemy('Гоблин-воин', hero.weapon_in_hands.damage * 5 + random.randint(-10, 10),
                                 self.names['Гоблин-воин'][0], hero.hit_point_max // 15, 'goblin_warrior.png'),
                           Enemy('Гоблин-знахарь', hero.weapon_in_hands.damage * 2 + random.randint(-10, 10),
                                 self.names['Гоблин-знахарь'][0], 0, 'goblin_healer.png'),
                           Enemy('Гоблин-воин', hero.weapon_in_hands.damage * 5 + random.randint(-10, 10),
                                 self.names['Гоблин-воин'][1], hero.hit_point_max // 15, 'goblin_warrior.png')]
        if random.choice(self.names) == 'Муравьиная-матка' or random.choice(self.names) == 'Муравей-рабочий'\
                or random.choice(self.names) == 'Муравей-трутень':
            self.enemys = [Enemy('Муравьиная королева', hero.weapon_in_hands.damage * 7 + random.randint(-10, 10),
                                 self.names['Муравьиная королева'][0], hero.hit_point_max // 7, 'ant_mother.png'),
                           Enemy('Муравей-рабочий', hero.weapon_in_hands.damage * 4 + random.randint(-10, 10),
                                 self.names['Муравей-рабочий'][0], hero.hit_point_max // 15, 'ant_worker.png'),
                           Enemy('Муравей-трутень', hero.weapon_in_hands.damage * 2 + random.randint(-10, 10),
                                 self.names['Муравей-трутень'][1], hero.hit_point_max // 10, 'ant_tryten.png')]


class MyWidget(QMainWindow):
    def __init__(self):
        self.art_names = ['Странная брошка', 'Счасливая монетка', 'Фигурка солдатика', 'Кольцо от любимого']
        self.wp_names = ['Большой меч', 'Клык дракона', 'Нож', 'Булава', 'Посох огня', 'Посох молнии']
        self.arm_names = ['Кольчуга', 'Кожанная куртка', 'Кирасса']
        self.pt_names = ['здоровья', 'маны', 'востановления сил']
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
        self.label_en1_im.setPixmap(QPixmap(enemy_list[0].image))
        self.label_en2_im.setPixmap(QPixmap(enemy_list[1].image))
        self.label_en3_im.setPixmap(QPixmap(enemy_list[2].image))

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

    def enemy_moves_and_end_room_check(self):
        check_alive = False
        for i in enemy_list.enemys:
            if i.alive():
                check_alive = True
                i.move()
        if check_alive is False:
            self.log.append('Комната зачищена пора двигаться дальше')
            hero.put_armor(Armor(random.choice(self.arm_names), hero.hit_point_max // 5 + random.randint(0, 20),
                                 hero.mana_point_max // 5 + random.randint(0, 20)))

            wp_name = random.choice(self.wp_names)
            if wp_name == 'Посох огня' or wp_name == 'Посох молнии' or wp_name == 'Клык дракона':
                hero.change_weapon(Weapon(wp_name, hero.hit_point_max // 5 + random.randint(5, 20),
                                          hero.mana_point_max // 10))
            else:
                hero.change_weapon(Weapon(wp_name, hero.hit_point_max // 7 + random.randint(5, 30), 0))

            pt_name = random.choice(self.pt_names)
            if pt_name == 'здоровья':
                hero.get_drink(Potion(pt_name, hero.hit_point_max // 2, hero.mana_point_max // 4))
            elif pt_name == 'маны':
                hero.get_drink(Potion(pt_name, hero.hit_point_max // 4, hero.mana_point_max // 2))
            else:
                hero.get_drink(Potion(pt_name, hero.hit_point_max, hero.mana_point_max))

            hero.change_artefact(Artefact(random.choice(self.art_names),
                                          random.randint(2, 20) + hero.artefact.plus_damage))

            enemy_list.generation_new_enemys()
            self.label_en1_im.setPixmap(QPixmap('big_rat.jpg'))
            self.label_en2_im.setPixmap(QPixmap('big_rat.jpg'))
            self.label_en3_im.setPixmap(QPixmap('big_rat.jpg'))


    def hero_defence(self):
        hero.defence()
        try:
            self.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def hero_drink_potion(self):
        hero.drink_potion()
        try:
            self.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def btn_attack_1(self):
        hero.attack(enemy_list[0])
        try:
            self.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def btn_attack_2(self):
        hero.attack(enemy_list[1])
        try:
            self.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def btn_attack_3(self):
        hero.attack(enemy_list[2])
        try:
            self.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    hero = Player()
    potion = Potion()
    enemy_1 = Enemy()
    enemy_2 = Enemy()
    enemy_3 = Enemy()
    enemy_list = EnemyList(enemy_1, enemy_2, enemy_3)
    sys.exit(app.exec())
