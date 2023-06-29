import csv
import gamelib
from random import randint
from clases import Equipo
from clases import Pokemon
from clases import Movimiento

POKE_WIDTH = 200
BG = randint(0, 8)

def crear_diccionario_pokemon():

    with open("pokemons.csv") as pok:
        resultado = {}
        lector = csv.DictReader(pok, delimiter = ";")

        for fila in lector:
            resultado[fila["nombre"]] = fila
            fila.pop("nombre")
         
    return resultado

def crear_diccionario_de_movimientos():
    
    with open("detalle_movimientos.csv") as mov:
        resultado = {}
        lector = csv.DictReader(mov)

        for fila in lector:
            resultado[fila["nombre"]] = fila
            fila.pop("nombre")
    
    return resultado

def crear_diccionario_de_tipos():

    with open("tabla_tipos.csv") as archivo:
        resultado = {}
        defensores = archivo.readline()
        defensores = defensores.rstrip("\n").split(";")

        for linea in archivo:
            linea = linea.rstrip("\n").split(";")
            atacante = linea[0]
            for i in range(1, len(defensores)):
                resultado[(atacante,defensores[i])] = float(linea[i])
        
        return resultado


def cargar_equipos(diccionario_pokemon, diccionario_de_movimientos):

    resultado = {}
    pokemons = {}
    dict_de_movs = {}
    index = 0

    try:
        with open("equipos.csv") as entrada:
            entrada.readline()
            
            for linea in entrada:
                equipo, pokemones, movimientos = linea.rstrip().split(";")
                lista_de_movimientos = movimientos.split(",")
                lista_de_pokemones = pokemones.split(",")

                for movs in lista_de_movimientos:

                    if lista_de_pokemones[index] == "":
                        resultado[equipo] = {}
                        continue

                    for mov in movs.split("-"):
                        dict_de_movs[mov] = Movimiento(mov, diccionario_de_movimientos)

                    pokemons[lista_de_pokemones[index]] = Pokemon(diccionario_pokemon, lista_de_pokemones[index], dict_de_movs)
                    resultado[equipo] = pokemons
                    index += 1
                    if index == len(lista_de_movimientos):
                        index = 0
                    
                    dict_de_movs = {}
                
                pokemons = {}

        return resultado
    
    except FileNotFoundError:
        with open("equipos.csv", "w") as f:
            return {}

def mostrar_campo_batalla(equipo1, equipo2):
    gamelib.draw_image(f"bgs/bg{BG}.gif", 50, 30)

    gamelib.draw_text(equipo1.jugador, 120, 480, size=18, bold=True, fill='black')
    gamelib.draw_image("imgs/trainer1.gif", 70, 530)

    gamelib.draw_text(equipo2.jugador, 820, 200, size=18, bold=True, fill='black')
    gamelib.draw_image("imgs/trainer2.gif", 770, 250)

    mostrar_pokeballs(equipo1, 90, 505)
    mostrar_pokeballs(equipo2, 790, 225)

    mostrar_hp(equipo1.poke_activo, 250, 460, POKE_WIDTH)
    if not equipo1.poke_activo.vivo() and equipo1.poke_activo.numero < 26:
        gamelib.draw_image(equipo1.poke_activo.imagen_muerto, 250, 480)
    else:
        gamelib.draw_image(equipo1.poke_activo.imagen, 250, 480)
    mostrar_hp(equipo2.poke_activo, 550, 210, POKE_WIDTH)
    if not equipo2.poke_activo.vivo() and equipo2.poke_activo.numero < 26:
        gamelib.draw_image(equipo2.poke_activo.imagen_muerto, 550, 230)
    else:
        gamelib.draw_image(equipo2.poke_activo.imagen, 550, 230)


def mostrar_hp(poke, x, y, width):
    porcentaje_restante = poke.hp / poke.hp_total
    if porcentaje_restante > 0.7:
        color = "green"
    elif 0.2 < porcentaje_restante <= 0.7:
        color = "yellow"
    else:
        color = "red"
    gamelib.draw_text(f"Hp: {poke.hp}", x, y-15, size=15, bold=True, fill='black')
    gamelib.draw_rectangle(x, y, x + width, y + 10, fill='gray')
    gamelib.draw_rectangle(x, y, x + (width * porcentaje_restante), y + 10, fill=color)

def mostrar_pokeballs(equipo, x_inicial, y):
    for i, poke in enumerate(list(equipo.pokemons.values())):
        if poke.vivo():
            gamelib.draw_image("imgs/pokeball.gif", x_inicial + i * 20, y)

def ejecutar_movimientos(equipo1, equipo2, jugador1, jugador2, movimiento1, movimiento2, diccionario_de_tipos):

    turno = 0

    if equipo1.poke_activo.spe == equipo2.poke_activo.spe:

        turno = randint(1,2)

    if equipo1.poke_activo.spe > equipo2.poke_activo.spe or turno == 1:

        atacante = equipo1
        usuario_atacante = jugador1
        defensor = equipo2
        usuario_defensor = jugador2
        mov_atacante = movimiento1
        mov_defensor = movimiento2

    elif equipo1.poke_activo.spe < equipo2.poke_activo.spe or turno == 2:

        atacante = equipo2
        usuario_atacante = jugador2
        defensor = equipo1
        usuario_defensor = jugador1
        mov_atacante = movimiento2
        mov_defensor = movimiento1

    if not mov_atacante == "cambiar":


        atacante.poke_activo.usar_movimiento(atacante.poke_activo.movimientos[mov_atacante], defensor.poke_activo, diccionario_de_tipos)


        if not defensor.poke_activo.vivo():

            gamelib.draw_begin()
            mostrar_campo_batalla(equipo1, equipo2)
            gamelib.draw_end()

            nuevo_pokemon = None
            gamelib.say(f"{usuario_defensor}\nsu Pokemon murió")
            defensor.restar_vivos()
            if defensor.vivos == 0:
                sentinela = 2
                return sentinela

            while not (nuevo_pokemon in defensor.pokemons):
                pokes = defensor.pokemons
                nombres_pokes = " - ".join(list(pokes.keys()))
                nuevo_pokemon = gamelib.input(f"{usuario_atacante}\nIngrese el nombre del pokémon con el que desea continuar\nPokemones disponibles: {nombres_pokes}")
            
            defensor.cambiar_pokemon_activo(nuevo_pokemon)
        
        else:
            
            if not mov_defensor == "cambiar":

                defensor.poke_activo.usar_movimiento(defensor.poke_activo.movimientos[mov_defensor], atacante.poke_activo, diccionario_de_tipos)

                if not atacante.poke_activo.vivo():

                    gamelib.draw_begin()
                    mostrar_campo_batalla(equipo1, equipo2)
                    gamelib.draw_end()

                    nuevo_pokemon = None
                    gamelib.say(f"{usuario_atacante}\nSu Pokemon murió")
                    atacante.restar_vivos()
                    if atacante.vivos == 0:
                        sentinela = 1
                        return sentinela
                    
                    while not (nuevo_pokemon in atacante.pokemons):
                        pokes = atacante.pokemons
                        nombres_pokes = " - ".join(list(pokes.keys()))
                        nuevo_pokemon = gamelib.input(f"{usuario_atacante}\nIngrese el nombre del pokémon con el que desea continuar\nPokemones disponibles: {nombres_pokes}")

                    atacante.cambiar_pokemon_activo(nuevo_pokemon)
            
            gamelib.draw_begin()
            mostrar_campo_batalla(atacante, defensor)
            gamelib.draw_end()

    else:

        if not mov_defensor == "cambiar":

            defensor.poke_activo.usar_movimiento(defensor.poke_activo.movimientos[mov_defensor], atacante.poke_activo, diccionario_de_tipos)

            if not atacante.poke_activo.vivo():

                gamelib.draw_begin()
                mostrar_campo_batalla(equipo1, equipo2)
                gamelib.draw_end()

                nuevo_pokemon = None
                gamelib.say(f"{usuario_atacante}\nSu Pokemon murió")
                atacante.restar_vivos()
                if atacante.vivos == 0:
                    sentinela = 1
                    return sentinela
                
                while not (nuevo_pokemon in atacante.pokemons):
                    pokes = atacante.pokemons
                    nombres_pokes = " - ".join(list(pokes.keys()))
                    nuevo_pokemon = gamelib.input(f"{usuario_atacante}\nIngrese el nombre del pokémon con el que desea continuar\nPokemones disponibles: {nombres_pokes}")

                atacante.cambiar_pokemon_activo(nuevo_pokemon)
        
        gamelib.draw_begin()
        mostrar_campo_batalla(atacante, defensor)
        gamelib.draw_end()

def main():

    gamelib.title("POKEMON SHOWDOWN")
    gamelib.resize(1000, 700)

    diccionario_pokemon = crear_diccionario_pokemon()
    diccionario_de_movimientos = crear_diccionario_de_movimientos()
    diccionario_de_equipos = cargar_equipos(diccionario_pokemon, diccionario_de_movimientos)
    diccionario_de_tipos = crear_diccionario_de_tipos()

    jugador1 = None
    jugador2 = None
    poke1 = None
    poke2 = None
    equipo1 = None
    equipo2 = None
    sentinela = None
   
    while gamelib.is_alive():

        if not jugador1 and not jugador2:
            gamelib.draw_begin()
            gamelib.draw_image("screen2.gif", 50, 50)
            gamelib.draw_end()
        
        elif sentinela != None:

            if sentinela == 1:
                gamelib.draw_begin()
                gamelib.draw_image("screen3.gif", 50, 50)
                gamelib.draw_text(f"{jugador2} GANÓ", 460, 450, size=25, bold=True, fill='black')
                gamelib.draw_end()

                ev = gamelib.wait()
                ev = gamelib.wait()
                ev = gamelib.wait()
                break
            
            else:
                gamelib.draw_begin()
                gamelib.draw_image("screen3.gif", 50, 50)
                gamelib.draw_text(f"{jugador1} GANÓ", 460, 450, size=25, bold=True, fill='black')
                gamelib.draw_end()

                ev = gamelib.wait()
                ev = gamelib.wait()
                ev = gamelib.wait()
                break

        else:
            gamelib.draw_begin()
            mostrar_campo_batalla(equipo1, equipo2)
            gamelib.draw_end()

        ev = gamelib.wait()

        if not jugador1 and not jugador2:

            jugador1 = gamelib.input("Ingrese el nombre del Jugador 1.")
            jugador2 = gamelib.input("Ingrese el nombre del Jugador 2.")

            while not (equipo1 in diccionario_de_equipos and equipo2 in diccionario_de_equipos):
                equipo1 = gamelib.input(f"{jugador1}\nIngrese el número del Equipo con el que desea jugar\nPuede elegir entre el 1 y el {int(max(diccionario_de_equipos.keys())) + 1}.")
                equipo2 = gamelib.input(f"{jugador2}\nIngrese el número del Equipo con el que desea jugar\nPuede elegir entre el 1 y el {int(max(diccionario_de_equipos.keys())) + 1}.")

                equipo1 = str(int(equipo1) - 1)
                equipo2 = str(int(equipo2) - 1)

                if equipo1 == equipo2:
                    gamelib.say("No pueden elegir el mismo equipo ambos jugadores")
                    equipo1 = None
                    equipo2 = None
                    continue

            equipo1 = diccionario_de_equipos[equipo1]
            equipo2 = diccionario_de_equipos[equipo2]
            while not (poke1 in equipo1 and poke2 in equipo2):
                poks1 = equipo1
                nombres_poks1 = " - ".join(list(poks1.keys()))
                poke1 = gamelib.input(f"{jugador1}\nIngrese el nombre del pokémon con el que desea comenzar.\nPokemones disponibles: {nombres_poks1}")

                poks2 = equipo2
                nombres_poks2 = " - ".join(list(poks2.keys()))
                poke2 = gamelib.input(f"{jugador2}\nIngrese el nombre del pokémon con el que desea comenzar.\nPokemones disponibles: {nombres_poks2}")

            poke1 = equipo1[poke1]
            poke2 = equipo2[poke2]

            equipo1 = Equipo(jugador1, equipo1, poke1)
            equipo2 = Equipo(jugador2, equipo2, poke2)

            gamelib.draw_begin()
            mostrar_campo_batalla(equipo1, equipo2)
            gamelib.draw_end()

        if equipo1.vivos != 0 and equipo2.vivos != 0:

            movimiento1 = None
            contador1 = 0

            while not (movimiento1 in equipo1.poke_activo.movimientos) and contador1 != 1:
                movis = equipo1.poke_activo.movimientos
                nombres_movis = " - ".join(list(movis.keys()))
                movimiento1 = gamelib.input(f"{jugador1}\nIngrese el movimiento\nmovimientos disponibles: {nombres_movis}\nCambiar Pokemon = cambiar\nRendirse = exit")

                if movimiento1 == "cambiar":
                    contador1 += 1
                    nuevo_pokemon = None
                    while not (nuevo_pokemon in equipo1.pokemons):
                        pokes = equipo1.pokemons
                        nombres_pokes = list(pokes.keys())
                        nombres_pokes.remove(equipo1.poke_activo.nombre)
                        nombres_pokes = " - ".join(nombres_pokes)
                        nuevo_pokemon = gamelib.input(f"{jugador1}\nIngrese el nombre del pokémon con el que desea continuar\nPokemones disponibles: {nombres_pokes}")
                        if nuevo_pokemon == equipo1.poke_activo.nombre:
                            nuevo_pokemon = None

                    equipo1.cambiar_pokemon_activo(nuevo_pokemon)

                    gamelib.draw_begin()
                    mostrar_campo_batalla(equipo1, equipo2)
                    gamelib.draw_end()
                
                elif movimiento1 == "exit":
                    sentinela = 1
                    break
            
            if movimiento1 == "exit":
                continue
            
            movimiento2 = None
            contador2 = 0
            
            while not (movimiento2 in equipo2.poke_activo.movimientos) and contador2 != 1:
                movis = equipo2.poke_activo.movimientos
                nombres_movis = " - ".join(list(movis.keys()))
                movimiento2 = gamelib.input(f"{jugador2}\nIngrese el movimiento\nmovimientos disponibles: {nombres_movis}\nCambiar Pokemon = cambiar\nRendirse = exit")

                if movimiento2 == "cambiar":
                    contador2 += 1 
                    nuevo_pokemon = None
                    while not (nuevo_pokemon in equipo2.pokemons):
                        pokes = equipo2.pokemons
                        nombres_pokes = list(pokes.keys())
                        nombres_pokes.remove(equipo2.poke_activo.nombre)
                        nombres_pokes = " - ".join(nombres_pokes)
                        nuevo_pokemon = gamelib.input(f"{jugador2}\nIngrese el nombre del pokémon con el que desea continuar\nPokemones disponibles: {nombres_pokes}")
                        if nuevo_pokemon == equipo2.poke_activo.nombre:
                            nuevo_pokemon = None

                    equipo2.cambiar_pokemon_activo(nuevo_pokemon)

                    gamelib.draw_begin()
                    mostrar_campo_batalla(equipo1, equipo2)
                    gamelib.draw_end()
                
                elif movimiento2 == "exit":
                    sentinela = 2
                    break

            if movimiento2 == "exit":
                continue

            sentinela = ejecutar_movimientos(equipo1, equipo2, jugador1, jugador2, movimiento1, movimiento2, diccionario_de_tipos)

gamelib.init(main)