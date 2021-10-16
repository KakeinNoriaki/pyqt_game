class Player:
    def __init__(self, hp, mp, wp, ar=None, arteff=None):
        self.hit_point_max = 100
        self.hit_poin = hp
        self.mana_point_max = 100
        self.mana_point = mp
        self.weapon_in_hands = wp
        self.weapon_inventory = []
        self.armor = ar
        self.artefact_effect = arteff
        self.potion_effect = None


class Enemy:
    def __init__(self, nm, hp, dm):
        self.name = nm
        self.hit_points = hp
        self.damage = dm
        self.pattern = []
        self.next_move = None


class Weapon:
    def __init__(self, nm, dm):
        self.name = nm
        self.damage = dm


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

