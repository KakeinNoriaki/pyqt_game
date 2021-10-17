class Player:
    def __init__(self, hp, mp, wp, ar=None, arteff=None, pt):
        self.hit_point_max = 100
        self.hit_point = hp
        self.mana_point_max = 100
        self.mana_point = mp
        self.weapon_in_hands = wp
        self.weapon_inventory = [wp]
        self.armor = ar
        self.artefact_effect = arteff
        self.in_defence = False # если True то срезает урон по герою на 90%
        self.potion = pt
        self.potion_effect = None

    def attack(self, target):
        self.in_defence = False
        if target.alive is True:
            if self.mana_point - self.weapon_in_hands.mana_points_use >= 0:
                target.hit_points -= self.weapon_in_hands.damage
                self.mana_point -= self.weapon_in_hands.mana_points_use
                if self.weapon_in_hands.effect is not None:
                    target.effect = self.weapon_in_hands.effect


    def deffence(self):
        self.in_defence = True
        self.mana_point += 10
        if self.mana_point > self.mana_point_max:
            self.mana_point = self.mana_point_max

    def drink_potion(self): # при выпивании зелья игрок встаёт в защитную стойку
        if self.potion is not None:
            self.hit_point += self.potion.hit_point_heall
            if self.hit_point > self.hit_point_max:
                self.hit_point = self.hit_point_max
            if self.potion.effect is not None:
                self.potion_effect = self.potion.effect
            self.potion = None
            self.in_defence = True

    def change_weapon(self):
        if len(self.weapon_inventory) > 1:
            if self.weapon_inventory.index(self.weapon_in_hands) == 3:
                self.weapon_in_hands = self.weapon_inventory[self.weapon_inventory.
                                                                 index(self.weapon_in_hands) - 1]
            else:
                self.weapon_in_hands = self.weapon_inventory[self.weapon_inventory.
                                                                 index(self.weapon_in_hands) + 1]

    def get_drink(self, pt):
        self.potion = pt
        self.potion_effect = None

class Enemy:
    def __init__(self, nm, hp, dm, btn):
        self.name = nm
        self.hit_points = hp
        self.damage = dm
        self.pattern = []
        self.next_move = 0
        self.alive = True
        self.button = btn
        self.effect = None


class Weapon:
    def __init__(self, nm, dm, mpu=0, eff):
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
    def __init__(self, nm, hph, ef):
        self.name = nm
        self.hit_point_heall = hph
        self.effect = ef

