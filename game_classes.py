import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import Qt


class Player:  # класс игрока
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
        ex.label_wp.setText('Оружие: ' + self.weapon_in_hands.name)
        self.print_stats()
        self.ester_egg = 0  # не большой секрет

    def armor_plus_stats(self):  # прибавляем статы от брони
        if self.armor is not None:
            self.hit_point_max += self.armor.plus_hit_point
            self.hit_point += self.armor.plus_hit_point
            self.mana_point_max += self.armor.plus_mana_point
            self.mana_point += self.armor.plus_mana_point
        self.print_stats()

    def print_stats(self):  # выводим статы игрока
        ex.label_hp.setText('Здоровье: ' + str(self.hit_point))
        ex.label_mp.setText('Мана: ' + str(self.mana_point))
        ex.label_lvl.setText('Урон: ' + str(self.damage))

    def artefact_plus_stats(self):   # Прибавляем статы от артефакта
        if self.artefact is not None:
            self.damage += self.artefact.plus_damage
            self.print_stats()

    def alive(self):  # проверям что игрок жив
        if self.hit_point > 0:
            return True
        #  если игрок мёртв блокируем все кнопки
        ex.pushButton_attack_1.setEnabled(False)
        ex.pushButton_attack_2.setEnabled(False)
        ex.pushButton_attack_3.setEnabled(False)
        ex.pushButton_back.setEnabled(False)
        ex.pushButton_attack.setEnabled(False)
        ex.pushButton_block.setEnabled(False)
        ex.pushButton_heal.setEnabled(False)
        ex.log.append('ИГРА ОКОНЧЕНА!')
        return False

    def check_attack(self, target):    # проверям можно ли атаковать противника
        if not target.alive():
            ex.log.append('Враг погиб')
            self.ester_egg += 1  # если будет 100 то будет выведен небольшой секрет
            if self.ester_egg > 100:
                ex.log.append('Ты оживить его предлагаешь?')
            return False

        else:
            if self.mana_point - self.weapon_in_hands.mana_points_use >= 0:
                return True
            else:
                ex.log.append('Мало маны')
                return False

    def art_plus_damage(self):   # это функция что бы считать урон для нового артефакта
        if self.artefact is not None:
            return self.artefact.plus_damage
        return 0

    def attack(self, target):  # атакуем врага
        block = 0  # срезает урон если враг в защитной стойке НА 70%
        if target.in_defence is True:
            block = (self.weapon_in_hands.damage // 100) * 70
        self.in_defence = False
        target.hit_points -= self.weapon_in_hands.damage - block
        self.mana_point -= self.weapon_in_hands.mana_points_use
        ex.log.append('Вы нанесли урон врагу ' + target.name + ' в размере: '
                      + str(self.weapon_in_hands.damage + block) + '\nУ врага осталось '
                      + str(target.hit_points) + ' здоровья')
        self.print_stats()

    def defence(self):  # игрок принимает защитную стойку и получает меньше дамага и четь лечится и востанавливает ману
        ex.log.append('Вы встали в защитную стойку')
        self.in_defence = True
        self.mana_point += 20
        self.hit_point += 20
        self.print_stats()

    def drink_potion(self):  # при выпивании зелья игрок встаёт в защитную стойку но без прибавке к мане и здоровью
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
            self.print_stats()
        else:
            raise ValueError('У вас не зелья')

    def change_weapon(self, new_wp):  # функция для выдачи нового оружия когда комната будет зачищена
        self.weapon_in_hands = new_wp
        ex.log.append('Вы подобрали новое оружие')
        ex.log.append(str(self.weapon_in_hands))
        ex.label_wp.setText('Оружие: ' + self.weapon_in_hands.name)
        self.damage = self.weapon_in_hands.damage
        self.print_stats()

    def change_artefact(self, new_art):  # функция для выдачи нового оружия когда комната будет зачищена
        self.artefact = new_art
        self.artefact_plus_stats()
        ex.label_art.setText('Артефакт: ' + self.artefact.name)
        self.print_stats()

    def get_drink(self, pt):  # функция для выдачи нового зелья когда комната будет зачищена
        self.potion = pt
        ex.log.append('Вы получили новое зелье ' + self.potion.name)
        ex.log.append(str(self.potion))

    def put_armor(self, new_armor):  # функция для выдачи новой брони когда комната будет зачищена
        ex.log.append('Теперь на вас надета ' + new_armor.name)
        if self.armor is not None:
            self.hit_point_max -= self.armor.plus_hit_point
            self.mana_point_max -= self.armor.plus_mana_point
        self.armor = new_armor
        self.armor_plus_stats()
        ex.log.append(str(self.armor))
        ex.label_arm.setText('Броня: ' + self.armor.name)
        self.print_stats()


class Enemy:   # класс врагов
    def __init__(self, nm, hp, pt, dm, img):
        global hero
        global enemy_list
        global ex
        self.name = nm
        self.hit_points = hp
        self.damage = dm
        self.pattern = pt  # attack, defense, heal
        self.next_move = 0  # курсор для self.pattern
        self.in_defence = False  # срезает урон на 70% по себе
        self.image = img

    def alive(self):  # проверям что враг жив и его можно атаковать
        if self.hit_points > 0 and self.hit_points != 0:
            return True
        return False

    def attack(self, target):   # атакуем игрока
        self.in_defence = False
        block = 0  # срезает урон если игрок в защитной стойке НА 90%
        if target.in_defence:
            block = (self.damage // 100) * 90
        if target.alive():   # проверям что игрок жив
            target.hit_point = target.hit_point - self.damage - block
            ex.log.append('Враг ' + self.name + ' нанёс урон в размере ' +
                          str(self.damage - block) + ' вам')
        else:
            ex.log.append('Игра окончена')

    def heal(self):   # лечит другого врага, у которого меньше всего здороья(может оживить труп)
        self.in_defence = False
        min_hp = 99999
        heal_him = ''
        for i in enemy_list.enemys:
            if i.hit_points < min_hp:
                min_hp = i.hit_points
                heal_him = enemy_list.enemys.index(i)
        enemy_list[heal_him].hit_points += self.damage
        ex.log.append('Враг ' + self.name + ' выличил ' + enemy_list[heal_him].name)

    def defence(self):  # враг встаёт в защитную стойку
        self.in_defence = True
        ex.log.append('Враг ' + self.name + ' встал в защитную стойку')

    def move(self):   # из спика pattern выбираем действия и передвигаем next_move на один зод вперёд или начало
        if self.pattern[self.next_move] == 'attack':
            self.attack(hero)
        elif self.pattern[self.next_move] == 'heal':
            self.heal()
        elif self.pattern[self.next_move] == 'defence':
            self.defence()
        if self.next_move == len(self.pattern) - 1:  # если курсор дашёл до конца списка возвращаем в конец
            self.next_move = 0
        else:
            self.next_move += 1


class Weapon:  # класс оружия
    def __init__(self, nm, dm, mpu=0):
        self.name = nm
        self.damage = dm
        self.mana_points_use = mpu

    def __str__(self):
        return 'Оружие ' + self.name + ' наносит ' + str(self.damage) +\
               ' урона используя ' + str(self.mana_points_use) + ' маны'


class Armor:  # класс брони
    def __init__(self, nm, php, pmp):
        self.name = nm
        self.plus_hit_point = php
        self.plus_mana_point = pmp

    def __str__(self):
        return self.name + ' прибавляет ' + str(self.plus_hit_point) +\
               ' здоровья и ' + str(self.plus_mana_point) + ' маны'


class Artefact:   # класс артефактов
    def __init__(self, nm, pd):
        self.name = nm
        self.plus_damage = pd

    def __str__(self):
        return 'Артефакт ' + self.name + ' прибавляет ' + str(self.plus_damage)


class Potion:   # класс зелий
    def __init__(self, nm, hph, mph):
        self.name = nm
        self.hit_point_heal = hph
        self.mana_point_heal = mph

    def __str__(self):
        return 'Зелье ' + self.name + ' васстонавливает ' + str(self.hit_point_heal)\
               + ' здоровья ' + str(self.mana_point_heal) + ' маны'


class EnemyList:   # класс списка противеиков и комнат(каждый раз когда убиваем 3 противников мы создаём трёх новых)
    def __init__(self, enemys):
        global hero
        global ex

        self.lvl = 0    # это уровни, усли проити 10 то это конец игры
        self.start = True    # проверяем что только начали игру
        self.enemys = enemys   # тут храним список противников
        # имя и патерны противников
        self.names_and_paterns = {'Большая крыса': [['attack', 'defence', 'attack'],
                                                    ['defence', 'attack', 'defence']],
                                  'Гоблин-воин': [['attack', 'attack', 'attack'], ['defence', 'attack', 'defence']],
                                  'Гоблин-знахарь': [['defence', 'heal', 'heal']],
                                  'Муравьиная королева': [['attack', 'defence', 'heal']],
                                  'Муравей-рабочий': [['attack', 'attack', 'defence'],
                                                      ['defence', 'defence', 'attack']],
                                  'Муравей-трутень': [['attack', 'attack', 'defence'],
                                                      ['defence', 'defence', 'attack']]}
        # вспомогательные списки для генерации предметов
        self.names = ['Большая крыса', 'Гоблин-воин', 'Муравей-рабочий']
        self.art_names = ['Странная брошка', 'Счасливая монетка', 'Фигурка солдатика', 'Кольцо от любимого']
        self.wp_names = ['Большой меч', 'Клык дракона', 'Нож', 'Булава', 'Посох огня', 'Посох молнии']
        self.arm_names = ['Кольчуга', 'Кожанная куртка', 'Кирасса']
        self.pt_names = ['здоровья', 'маны', 'востановления сил']

    # выбираем нужного противника
    def __getitem__(self, key):
        return self.enemys[key]

    def generation_new_enemys(self):  # создаём новых противников
        enemy_choice = random.choice(self.names)
        if enemy_choice == 'Большая крыса':
            self.enemys = [Enemy('Большая крыса', hero.weapon_in_hands.damage * 3 +
                                 random.randint(-10, 10), self.names_and_paterns['Большая крыса'][0],
                                 hero.hit_point_max // 20, 'big_rat.png'),
                           Enemy('Большая крыса', hero.weapon_in_hands.damage * 3 +
                                 random.randint(-10, 10), self.names_and_paterns['Большая крыса'][1],
                                 hero.hit_point_max // 20, 'big_rat.png'),
                           Enemy('Большая крыса', hero.weapon_in_hands.damage * 3 +
                                 random.randint(-10, 10),
                                 self.names_and_paterns['Большая крыса'][1],
                                 hero.hit_point_max // 20, 'big_rat.png')]
        if enemy_choice == 'Гоблин-воин' or enemy_choice == 'Гоблин-знахарь':
            self.enemys = [Enemy('Гоблин-воин', hero.weapon_in_hands.damage * 5 +
                                 random.randint(-10, 10), self.names_and_paterns['Гоблин-воин'][0],
                                 hero.hit_point_max // 15, 'goblin_warrior.png'),
                           Enemy('Гоблин-знахарь', hero.weapon_in_hands.damage * 2 +
                                 random.randint(-10, 10),
                                 self.names_and_paterns['Гоблин-знахарь'][0], 0,
                                 'goblin_healer.png'),
                           Enemy('Гоблин-воин', hero.weapon_in_hands.damage * 5 +
                                 random.randint(-10, 10),
                                 self.names_and_paterns['Гоблин-воин'][1],
                                 hero.hit_point_max // 15, 'goblin_warrior.png')]
        if enemy_choice == 'Муравьиная-матка' or enemy_choice == 'Муравей-рабочий' \
                or enemy_choice == 'Муравей-трутень':
            self.enemys = [Enemy('Муравьиная королева', hero.weapon_in_hands.damage * 7 +
                                 random.randint(-10, 10),
                                 self.names_and_paterns['Муравьиная королева'][0],
                                 hero.hit_point_max // 7, 'ant_mother.png'),
                           Enemy('Муравей-рабочий', hero.weapon_in_hands.damage * 4
                                 + random.randint(-10, 10),
                                 self.names_and_paterns['Муравей-рабочий'][0],
                                 hero.hit_point_max // 15, 'ant_worker.png'),
                           Enemy('Муравей-трутень', hero.weapon_in_hands.damage * 2
                                 + random.randint(-10, 10),
                                 self.names_and_paterns['Муравей-трутень'][1],
                                 hero.hit_point_max // 10, 'ant_worker.png')]

    def enemy_moves_and_end_room_check(self):  # враги делают свои ходы
        check_alive = False  # будет True если в комнате есть живые враги
        for i in [0, 1, 2]:
            if self.enemys[i].alive():
                check_alive = True
                self.enemys[i].move()
        if check_alive is False:  # если нет живых врагов создаём новых и выдаём новые предметы
            ex.log.append('Комната зачищена пора двигаться дальше')
            ex.log.append('________________________________________')
            if self.start:  # если только начало игры то выводим немного истории
                ex.log.append('Духи растворились в комнате, после активного '
                              'размахивания руками, в ходе которого вы неоднакратно '
                              'ударялись о стены')
                ex.log.append('Чуть отышавшись вы осмотрелись')
                ex.log.append('Стены хоть и походят на стены пещевы, выглядят аккуратными и'
                              ' рукотворными и геометрия окружаещего пространства'
                              ' представляла собой паралелипипед')
                ex.log.append('После нескольких секунд упорных раздумий вы не знаете '
                              'кто вы и как сюда попали')
                ex.log.append('Вы увидели проход в другую часть пещеры и '
                              'поняв что другой дороги здесь нет вы направились в прямо туда')
                ex.log.append('Вы вошли в комнату и увидели несколько недружелюбных фигур')
                ex.log.append('Проход прямо за вами расстворился')
                ex.log.append('Анализируя ситуацию вы поняли что у вас из неоткуда появилось'
                              ' оружие, броня и странный артефакт')
                ex.log.append('Видимо так вы будет путешевствовать пока не выберетесь от сюда')
                ex.log.append('________________________________________')
            elif self.lvl != 10:   # cообщаем о переходе в новую комнату
                ex.log.append('Перейдя в новую комнату вы почувтвывали странные покалывания')
                ex.log.append('Осмотрев себя вы поняли что у вас другое оружие и броня')
                ex.log.append('Странный флакон поменял содержание')
                ex.log.append('У вас появился новый талисманчик')
            else:  # если прошли  10 уровней игра окончена
                ex.log.append('________________________________________')
                ex.log.append('Победив очередную группу противников вы отрехнулись и '
                              'собрались идти дальше')
                ex.log.append('Вы увидили яркий солнечный свет в следующем проходе')
                ex.log.append('Вы тут же рванули к нему')
                ex.log.append('Только подойдя вы были ослеплены, чуть пощурившись вы пошли дальше')
                ex.log.append('Выйдя наружу перед вами предстал дележанс в свете яркого солнца')
                ex.log.append('Дверь дележанса открылась')
                ex.log.append('Немного постояв вы поняли, что от туда ни кто не собирается выходить')
                ex.log.append('Подойдя поближе вы увидили надпись что вам следует здесь сесть')
                ex.log.append('Вы почувствовали что вас кто то заталкнул в дележанс и тут же оказались в нём')
                ex.log.append('Дверь захлопнулась, а дележанс помчался в вперёд, но не известно куда')
                ex.log.append('________________________________________')
                ex.pushButton_attack_1.setEnabled(False)
                ex.pushButton_attack_2.setEnabled(False)
                ex.pushButton_attack_3.setEnabled(False)
                ex.pushButton_back.setEnabled(False)
                ex.pushButton_attack.setEnabled(False)
                ex.pushButton_block.setEnabled(False)
                ex.pushButton_heal.setEnabled(False)
                ex.log.append('ИГРА ОКОНЧЕНА!')
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
            art_name = random.choice(self.art_names)
            plus_dm = hero.art_plus_damage() + random.randint(2, 20)
            hero.change_artefact(Artefact(art_name, plus_dm))
            ex.log.append('Вы сменили артефакт')
            self.generation_new_enemys()
            ex.label_en1_im.setPixmap(QPixmap(enemy_list[0].image))
            ex.label_en2_im.setPixmap(QPixmap(enemy_list[1].image))
            ex.label_en3_im.setPixmap(QPixmap(enemy_list[2].image))
            self.start = False
            self.lvl += 1


class MyWidget(QMainWindow):  # окно приложения
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
        self.label_en1_im.setPixmap(QPixmap(enemy_list[0].image))
        self.label_en2_im.setPixmap(QPixmap(enemy_list[1].image))
        self.label_en3_im.setPixmap(QPixmap(enemy_list[2].image))
        #  рассказываем немного истории
        self.log.append('Вы очутились в странной пещере, вокруго и сыро')
        self.log.append('Ощупав корманы вы нащупали странный флакон')
        self.log.append('Откупарив бутылёк вы почувствывали странный запах')
        self.log.append('Вы не вспонили что это за запах, но вспомнили'
                        ' что оно явно очень бодрит и залечивает раны')
        self.log.append('В комнате возникли странные фигуры')
        self.log.append('ЭТО ПРИЗРАКИ')
        self.log.append('________________________________________')

    def hero_attack(self):  # показываем кнопки для атаки
        self.show_attack_buttons()

    def attack_cancel(self):  # прячем кнопки для атаки
        self.pushButton_attack_1.hide()
        self.pushButton_attack_2.hide()
        self.pushButton_attack_3.hide()
        self.pushButton_back.hide()

    def show_attack_buttons(self):  # показываем кнопки для атаки
        self.pushButton_attack_1.show()
        self.pushButton_attack_2.show()
        self.pushButton_attack_3.show()
        self.pushButton_back.show()

    def hero_defence(self):  # игрок делает ход встать в защитную стойку
        hero.defence()
        enemy_list.enemy_moves_and_end_room_check()

    def hero_drink_potion(self):  # игрок делает ход выпить зелье
        hero.drink_potion()
        try:
            enemy_list.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def btn_attack_1(self):  # игрок делает и бьёт первого врага
        try:
            if hero.check_attack(enemy_list[0]):
                hero.attack(enemy_list[0])
                enemy_list.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def btn_attack_2(self):  # игрок делает и бьёт второго врага
        try:
            if hero.check_attack(enemy_list[1]):
                hero.attack(enemy_list[1])
                enemy_list.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def btn_attack_3(self):   # игрок делает и бьёт третьего врага
        try:
            if hero.check_attack(enemy_list[2]):
                hero.attack(enemy_list[2])
                enemy_list.enemy_moves_and_end_room_check()
        except ValueError as error:
            self.log.append(error)

    def keyPressEvent(self, event):    # конопочками уравлять удобнее
        if event.key() == Qt.Key_A:
            self.hero_attack()
        if event.key() == Qt.Key_S:
            self.hero_drink_potion()
        if event.key() == Qt.Key_D:
            self.hero_defence()
        if event.key() == Qt.Key_1:
            self.btn_attack_1()
        if event.key() == Qt.Key_2:
            self.btn_attack_2()
        if event.key() == Qt.Key_3:
            self.btn_attack_3()
        if event.key() == Qt.Key_4:
            self.attack_cancel()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # создаём стартовое зелье
    potion = Potion('подземелья', 50, 20)
    # создаём стартовых врагов
    enemy_1 = Enemy('Дух', 5, ['attack', 'defence'], 5, 'duh.png')
    enemy_2 = Enemy('Дух', 5, ['attack', 'defence'], 5, 'duh.png')
    enemy_3 = Enemy('Дух', 5, ['attack', 'defence'], 5, 'duh.png')
    # создаём список врагов
    enemy_list = EnemyList([enemy_1, enemy_2, enemy_3])
    ex = MyWidget()
    ex.show()
    # создаём игрока
    hero = Player(100, 50, Weapon('Кулаки', 3), potion)
    sys.exit(app.exec())
