import random

class Equipo:

    def __init__(self, jugador, lista_de_pokemones, pokemon):
        self.jugador = jugador
        self.pokemons = lista_de_pokemones
        self.poke_activo = pokemon
        self.vivos = len(lista_de_pokemones)

    def restar_vivos(self):
        self.vivos -= 1
        del self.pokemons[self.poke_activo.nombre]

    def cambiar_pokemon_activo(self, pokemon):
        self.poke_activo = self.pokemons[pokemon]


class Movimiento:

    def __init__(self, nombre, diccionario_de_movimientos):
        self.nombre = nombre
        self.categoria = diccionario_de_movimientos[nombre]["categoria"]
        self.objetivo = diccionario_de_movimientos[nombre]["objetivo"]
        self.pp = int(diccionario_de_movimientos[nombre]["pp"])
        self.poder = int(diccionario_de_movimientos[nombre]["poder"])
        self.tipo = diccionario_de_movimientos[nombre]["tipo"]
        self.stats = diccionario_de_movimientos[nombre]["stats"]

class Pokemon:

    def __init__(self, dic_pokemones, nombre_pokemon, movimientos):
        self.nombre = nombre_pokemon
        self.numero = int(dic_pokemones[nombre_pokemon]["numero"])
        self.imagen_muerto = "imgs/Inked" + dic_pokemones[nombre_pokemon]["numero"] + ".gif"
        self.imagen = dic_pokemones[nombre_pokemon]["imagen"]
        self.tipo = dic_pokemones[nombre_pokemon]["tipos"]
        self.hp = int(dic_pokemones[nombre_pokemon]["hp"]) + 110
        self.hp_total = int(dic_pokemones[nombre_pokemon]["hp"]) + 110
        self.atk = int(dic_pokemones[nombre_pokemon]["atk"])
        self.defense = int(dic_pokemones[nombre_pokemon]["def"])
        self.spa = int(dic_pokemones[nombre_pokemon]["spa"])
        self.spd = int(dic_pokemones[nombre_pokemon]["spd"])
        self.spe = int(dic_pokemones[nombre_pokemon]["spe"])
        self.movimientos = movimientos

    def usar_movimiento(self, movimiento, otro, dic_tipos):
        movimiento.pp -= 1

        if movimiento.categoria == "Status":

            modificaciones = movimiento.stats.split(";")

            if movimiento.objetivo == "self":
                for mod in modificaciones:
                    if mod == "spe":
                        self.spe *= 2

                    if mod == "atk":
                        self.atk *= 2
                    
                    if mod == "def":
                        self.defense *= 2

                    if mod == "":
                        self.hp += (self.hp_total / 2)

                        if self.hp > self.hp_total:
                            self.hp = self.hp_total
            else:
                for mod in modificaciones:
                    if mod == "spe":
                        otro.spe /= 2

                    if mod == "atk":
                        otro.atk /= 2
                    
                    if mod == "def":
                        otro.defense /= 2

        if movimiento.categoria == "Physical":
            damage = 15 * movimiento.poder * (self.atk / otro.defense) / 50

        if movimiento.categoria == "Special":
            damage = 15 * movimiento.poder * (self.spa / otro.spd) / 50

        if movimiento.categoria == "Status":
            damage = 0

        if self.tipo == movimiento.tipo:
            damage *= 1.5
        
        tipo = otro.tipo.split(",")

        damage *= dic_tipos[(tipo[0], movimiento.tipo)]
        if len(tipo) == 2:
            damage *= dic_tipos[(tipo[1], movimiento.tipo)]

        efectividad = random.randint(80, 100)

        damage = (damage * efectividad) / 100

        otro.hp -= int(damage)
        if otro.hp < 0:
            otro.hp = 0

        if movimiento.pp == 0:
            del self.movimientos[movimiento.nombre]

    def vivo(self):
        if self.hp <= 0:
            return False
        else:
            return True