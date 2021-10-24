class Player:
    def __init__(self, hp, mp, wp, pt, ar=None, art_ef=None):
        self.hit_point_max = 100
        self.hit_point = hp
        self.mana_point_max = 100
        self.mana_point = mp
        self.weapon_in_hands = wp
        self.armor = ar
        self.artefact_effect = art_ef
        self.in_defence = False  # если True то срезает урон по герою на 90%
        self.potion = None
        self.potion_effect = None
        self.armor_plus_stats()
        self.get_drink(pt)

    def armor_plus_stats(self):
        if self.armor is not None:
            self.hit_point_max += self.armor.plus_hit_point
            self.hit_point += self.armor.plus_hit_point
            self.mana_point_max += self.armor.plus_mana_point
            self.mana_point += self.armor.plus_mana_point

    def alive(self):
        if self.hit_point > 0:
            return True
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
                if self.weapon_in_hands.effect is not None:
                    target.effect = self.weapon_in_hands.effect

    def deffence(self):
        self.in_defence = True
        self.mana_point += 10
        if self.mana_point > self.mana_point_max:
            self.mana_point = self.mana_point_max

    def drink_potion(self):  # при выпивании зелья игрок встаёт в защитную стойку
        if self.potion is not None:
            self.hit_point += self.potion.hit_point_heal
            if self.hit_point > self.hit_point_max:
                self.hit_point = self.hit_point_max
            self.mana_point += self.potion.mana_point_heal
            if self.mana_point > self.hit_point_max:
                self.mana_point = self.mana_point_max
            if self.potion.effect is not None:
                self.potion_effect = self.potion.effect
            self.potion = None
            self.in_defence = True
            if self.potion.effect is not None:
                self.potion_effect = self.potion.effect

    def change_weapon(self, new_wp):
        self.weapon_in_hands = new_wp

    def get_drink(self, pt):
        self.potion = pt
        self.potion_effect = None

    def put_armour(self, new_armor):
        self.hit_point_max -= self.armor.plus_hit_point
        self.mana_point_max -= self.armor.plus_mana_point
        self.armor = new_armor
        self.armor_plus_stats()


class Enemy:
    def __init__(self, nm, hp, pt, dm, btn):
        self.name = nm
        self.hit_points = hp
        self.damage = dm
        self.pattern = pt  # attack, defense, heal
        self.next_move = 0
        self.button = btn
        self.effect = None
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
        self.in_defence = False
        if target.alive:
            target.hit_points -= self.damage - block
        else:
            print('чё за фигня?')

    def heal(self):
        self.in_defence = False
        min_hp = 99999
        heal_him = ''
        for i in enemy_list:
            if i.hit_points < min_hp:
                min_hp = i.hit_points
                heal_him = enemy_list.index(i)
        enemy_list[heal_him].hit_points += self.damage

    def defence(self):
        self.in_defence = True

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
    def __init__(self, nm, dm, eff, mpu=0):
        self.name = nm
        self.damage = dm
        self.mana_points_use = mpu
        self.effect = eff


class Armor:
    def __init__(self, nm, php, pmp):
        self.name = nm
        self.plus_hit_point = php
        self.plus_mana_point = pmp


class Artefact:
    def __init__(self, nm, pd, ef):
        self.name = nm
        self.plus_damage = pd
        self.effect = ef


class Potion:
    def __init__(self, nm, hph, mph, ef):
        self.name = nm
        self.hit_point_heal = hph
        self.mana_point_heal = mph
        self.effect = ef


hero = Player()
potion = Potion()
enemy_1 = Enemy()
enemy_2 = Enemy()
enemy_3 = Enemy()
enemy_list = [enemy_1, enemy_2, enemy_3]
