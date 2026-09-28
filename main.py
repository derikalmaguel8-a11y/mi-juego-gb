#!/usr/bin/env python3
"""
🎮 JUEGO GB — Motor estilo Game Boy con controles táctiles
Adaptado para compilar como APK de Android con Buildozer.

Controles:
  Táctil: D-Pad + A/B
  Teclado: Flechas/WASD, Z, X, E, Esc
"""

import pygame
import sys
import os
import json

# ============================================================
# DETECCIÓN DE PLATAFORMA
# ============================================================
ES_ANDROID = "ANDROID_ROOT" in os.environ or "ANDROID_ARGUMENT" in os.environ
ES_TERMUX = "TERMUX_VERSION" in os.environ
ES_MOVIL = ES_ANDROID or ES_TERMUX

# ============================================================
# CONFIGURACIÓN
# ============================================================
GB_W = 160
GB_H = 144
TILE = 8
FPS = 60

# Paleta Game Boy
PALETA = [
    (15, 56, 15),
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15),
]
NEGRO = PALETA[0]
OSCURO = PALETA[1]
CLARO = PALETA[2]
FONDO = PALETA[3]

# Tipos de tile
T_VACIO = 0
T_PARED = 1
T_AGUA = 2
T_ARBOL = 3
T_CAMINO = 4
T_CASA = 5
T_PUERTA = 6

# ============================================================
# JUEGO DE EJEMPLO (formato .jgb)
# ============================================================
JUEGO_EJEMPLO = {
    "nombre": "Mi Aventura",
    "version": "1.0",
    "inicio": {"mapa": "pueblo", "x": 10, "y": 12},
    "mapas": {
        "pueblo": {
            "ancho": 25,
            "alto": 18,
            "tiles": [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,3,3,0,0,5,5,0,0,0,0,0,0,5,5,5,0,0,0,3,3,3,0,1],
                [1,0,3,3,0,0,5,5,0,0,0,0,0,0,5,5,5,0,0,0,3,3,3,0,1],
                [1,0,0,0,0,0,5,5,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,5,5,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,1],
                [1,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ],
            "conexiones": {
                "norte": {"mapa": "bosque", "x": 12, "y": 16}
            }
        },
        "bosque": {
            "ancho": 25,
            "alto": 18,
            "tiles": [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,3,3,3,0,0,3,3,3,0,0,3,3,3,0,0,3,3,3,0,0,3,3,1],
                [1,0,3,0,3,0,0,3,0,3,0,0,3,0,3,0,0,3,0,3,0,0,3,3,1],
                [1,0,3,0,3,0,0,3,0,3,0,0,3,0,3,0,0,3,0,3,0,0,0,0,1],
                [1,0,3,0,3,0,0,3,0,3,0,0,3,0,3,0,0,3,0,3,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,3,3,3,0,0,0,3,3,3,3,3,0,0,0,3,3,3,0,0,0,0,1],
                [1,0,0,3,0,3,0,0,0,3,0,0,0,3,0,0,0,3,0,3,0,0,0,0,1],
                [1,0,0,3,0,3,0,0,0,3,0,0,0,3,0,0,0,3,0,3,0,0,0,0,1],
                [1,0,0,3,0,3,0,0,0,3,0,0,0,3,0,0,0,3,0,3,0,0,0,0,1],
                [1,0,0,3,3,3,0,0,0,3,3,3,3,3,0,0,0,3,3,3,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ],
            "conexiones": {
                "sur": {"mapa": "pueblo", "x": 10, "y": 2}
            }
        }
    },
    "npcs": [
        {"mapa": "pueblo", "x": 10, "y": 5, "nombre": "Anciano",
         "dialogo": "Bienvenido, aventurero. El bosque al norte es peligroso."},
        {"mapa": "pueblo", "x": 15, "y": 5, "nombre": "Niña",
         "dialogo": "¡Hola! ¿Vas a explorar? Ten cuidado con los slimes."},
    ],
    "enemigos": [
        {"mapa": "bosque", "x": 10, "y": 8, "tipo": "slime", "hp": 10},
        {"mapa": "bosque", "x": 15, "y": 10, "tipo": "slime", "hp": 10},
    ]
}


# ============================================================
# MAPA
# ============================================================
class Mapa:
    def __init__(self, nombre, datos):
        self.nombre = nombre
        self.ancho = datos["ancho"]
        self.alto = datos["alto"]
        self.tiles = datos["tiles"]
        self.conexiones = datos.get("conexiones", {})

    def tile_en(self, x, y):
        if x < 0 or x >= self.ancho or y < 0 or y >= self.alto:
            return T_PARED
        return self.tiles[y][x]

    def es_transitable(self, x, y):
        t = self.tile_en(x, y)
        return t not in (T_PARED, T_AGUA, T_ARBOL, T_CASA)


# ============================================================
# ENTIDADES
# ============================================================
class Jugador:
    def __init__(self, x, y):
        self.x = x * TILE
        self.y = y * TILE
        self.velocidad = 1.5
        self.direccion = "abajo"
        self.anim_timer = 0

    def mover(self, dx, dy, mapa):
        if dx != 0:
            nx = self.x + dx
            if dx > 0:
                self.direccion = "derecha"
            else:
                self.direccion = "izquierda"
            if self._puede(nx, self.y, mapa):
                self.x = nx

        if dy != 0:
            ny = self.y + dy
            if dy > 0:
                self.direccion = "abajo"
            else:
                self.direccion = "arriba"
            if self._puede(self.x, ny, mapa):
                self.y = ny

        if dx != 0 or dy != 0:
            self.anim_timer += 1
            if self.anim_timer > 8:
                self.anim_timer = 0

    def _puede(self, x, y, mapa):
        for px, py in [(x, y), (x + TILE - 1, y),
                       (x, y + TILE - 1), (x + TILE - 1, y + TILE - 1)]:
            tx = int(px // TILE)
            ty = int(py // TILE)
            if not mapa.es_transitable(tx, ty):
                return False
        return True


class NPC:
    def __init__(self, datos):
        self.x = datos["x"] * TILE
        self.y = datos["y"] * TILE
        self.nombre = datos["nombre"]
        self.dialogo = datos["dialogo"]


class Enemigo:
    def __init__(self, datos):
        self.x = datos["x"] * TILE
        self.y = datos["y"] * TILE
        self.tipo = datos["tipo"]
        self.hp = datos["hp"]
        self.hp_max = datos["hp"]
        self.vivo = True
        self.anim_timer = 0


# ============================================================
# CONTROLES TÁCTILES
# ============================================================
class ControlTactil:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.zona_juego_h = int(h * 0.65)
        self.control_y = self.zona_juego_h
        self.btn_size = int(min(w, h) * 0.13)
        self.margen = int(self.btn_size * 0.5)

        cx = self.margen + self.btn_size + self.margen // 2
        cy = self.control_y + (h - self.control_y) // 2
        self.dpad_centro = (cx, cy)

        s = self.btn_size
        self.rect_arriba = pygame.Rect(cx - s // 2, cy - s - s // 2, s, s)
        self.rect_abajo = pygame.Rect(cx - s // 2, cy + s // 2, s, s)
        self.rect_izq = pygame.Rect(cx - s - s // 2, cy - s // 2, s, s)
        self.rect_der = pygame.Rect(cx + s // 2, cy - s // 2, s, s)

        btn_a_x = w - self.margen - self.btn_size
        btn_a_y = cy - self.btn_size // 2
        self.rect_a = pygame.Rect(btn_a_x, btn_a_y, self.btn_size, self.btn_size)

        btn_b_x = btn_a_x - self.btn_size - self.margen
        btn_b_y = btn_a_y + self.btn_size // 2
        self.rect_b = pygame.Rect(btn_b_x, btn_b_y, self.btn_size, self.btn_size)

        self.activos = {"arriba": False, "abajo": False, "izq": False,
                        "der": False, "a": False, "b": False}

    def toque(self, pos, tipo):
        x, y = pos
        if y < self.control_y:
            return
        if tipo == "down":
            self.activos = {k: False for k in self.activos}
        if self.rect_arriba.collidepoint(x, y):
            self.activos["arriba"] = True
        if self.rect_abajo.collidepoint(x, y):
            self.activos["abajo"] = True
        if self.rect_izq.collidepoint(x, y):
            self.activos["izq"] = True
        if self.rect_der.collidepoint(x, y):
            self.activos["der"] = True
        if self.rect_a.collidepoint(x, y):
            self.activos["a"] = True
        if self.rect_b.collidepoint(x, y):
            self.activos["b"] = True

    def reset(self):
        self.activos = {k: False for k in self.activos}

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, NEGRO,
                         (0, self.control_y, self.w, self.h - self.control_y))

        for rect, key in [(self.rect_arriba, "arriba"), (self.rect_abajo, "abajo"),
                          (self.rect_izq, "izq"), (self.rect_der, "der")]:
            color = CLARO if self.activos[key] else OSCURO
            pygame.draw.rect(pantalla, color, rect, border_radius=4)
            pygame.draw.rect(pantalla, FONDO, rect, width=2, border_radius=4)

        cx, cy = self.dpad_centro
        s = self.btn_size
        pygame.draw.rect(pantalla, OSCURO,
                         (cx - s // 4, cy - s // 4, s // 2, s // 2),
                         border_radius=2)

        color_a = CLARO if self.activos["a"] else OSCURO
        color_b = CLARO if self.activos["b"] else OSCURO
        pygame.draw.rect(pantalla, color_a, self.rect_a,
                         border_radius=self.btn_size // 2)
        pygame.draw.rect(pantalla, FONDO, self.rect_a, width=2,
                         border_radius=self.btn_size // 2)
        pygame.draw.rect(pantalla, color_b, self.rect_b,
                         border_radius=self.btn_size // 2)
        pygame.draw.rect(pantalla, FONDO, self.rect_b, width=2,
                         border_radius=self.btn_size // 2)

        try:
            fuente = pygame.font.SysFont("monospace", self.btn_size // 2, bold=True)
            txt_a = fuente.render("A", True, FONDO)
            txt_b = fuente.render("B", True, FONDO)
            pantalla.blit(txt_a, txt_a.get_rect(center=self.rect_a.center))
            pantalla.blit(txt_b, txt_b.get_rect(center=self.rect_b.center))
        except Exception:
            pass


# ============================================================
# JUEGO
# ============================================================
class Juego:
    def __init__(self, datos_juego):
        pygame.init()

        try:
            pygame.mixer.init()
        except Exception:
            pass

        pygame.display.set_caption(datos_juego.get("nombre", "JGB"))

        if ES_MOVIL:
            try:
                info = pygame.display.Info()
                self.w = info.current_w
                self.h = info.current_h
                self.pantalla = pygame.display.set_mode((self.w, self.h),
                                                        pygame.FULLSCREEN)
            except Exception:
                self.w = GB_W * 4
                self.h = GB_H * 4
                self.pantalla = pygame.display.set_mode((self.w, self.h))
        else:
            self.w = GB_W * 4
            self.h = GB_H * 4
            self.pantalla = pygame.display.set_mode((self.w, self.h))

        self.reloj = pygame.time.Clock()
        self.corriendo = True

        self.juego_h = int(self.h * 0.65)
        self.pantalla_gb = pygame.Surface((GB_W, GB_H))

        self.datos = datos_juego
        self.mapas = {n: Mapa(n, d) for n, d in self.datos["mapas"].items()}
        self.mapa_actual = self.datos["inicio"]["mapa"]
        self.mapa = self.mapas[self.mapa_actual]

        self.jugador = Jugador(self.datos["inicio"]["x"], self.datos["inicio"]["y"])

        self.npcs = [NPC(n) for n in self.datos.get("npcs", [])
                     if n["mapa"] == self.mapa_actual]
        self.enemigos = [Enemigo(e) for e in self.datos.get("enemigos", [])
                         if e["mapa"] == self.mapa_actual]

        self.camara_x = 0
        self.camara_y = 0

        self.control = ControlTactil(self.w, self.h)
        self.teclas = {}

        self.dialogo_activo = None
        self.dialogo_texto = ""

        try:
            self.fuente = pygame.font.SysFont("monospace", 10, bold=True)
        except Exception:
            self.fuente = pygame.font.Font(None, 10)

    def actualizar_camara(self):
        self.camara_x = self.jugador.x - (GB_W // 2) + TILE // 2
        self.camara_y = self.jugador.y - (GB_H // 2) + TILE // 2
        max_x = self.mapa.ancho * TILE - GB_W
        max_y = self.mapa.alto * TILE - GB_H
        self.camara_x = max(0, min(self.camara_x, max_x))
        self.camara_y = max(0, min(self.camara_y, max_y))

    def manejar_eventos(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.corriendo = False
            elif ev.type == pygame.KEYDOWN:
                self.teclas[ev.key] = True
                if ev.key == pygame.K_ESCAPE:
                    self.corriendo = False
                elif ev.key == pygame.K_z:
                    self.accion_a()
                elif ev.key == pygame.K_x:
                    self.accion_b()
                elif ev.key == pygame.K_e:
                    self.interactuar()
            elif ev.type == pygame.KEYUP:
                self.teclas[ev.key] = False
            elif ev.type == pygame.FINGERDOWN:
                x = int(ev.x * self.w)
                y = int(ev.y * self.h)
                self.control.toque((x, y), "down")
            elif ev.type == pygame.FINGERMOTION:
                x = int(ev.x * self.w)
                y = int(ev.y * self.h)
                self.control.toque((x, y), "motion")
            elif ev.type == pygame.FINGERUP:
                self.control.reset()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                self.control.toque(ev.pos, "down")
            elif ev.type == pygame.MOUSEMOTION and ev.buttons[0]:
                self.control.toque(ev.pos, "motion")
            elif ev.type == pygame.MOUSEBUTTONUP:
                self.control.reset()

    def accion_a(self):
        if self.dialogo_activo:
            self.cerrar_dialogo()
            return
        self.interactuar()

    def accion_b(self):
        if self.dialogo_activo:
            self.cerrar_dialogo()

    def interactuar(self):
        if self.dialogo_activo:
            self.cerrar_dialogo()
            return
        for npc in self.npcs:
            if abs(npc.x - self.jugador.x) <= TILE and abs(npc.y - self.jugador.y) <= TILE:
                self.dialogo_activo = npc.nombre
                self.dialogo_texto = npc.dialogo
                return

    def cerrar_dialogo(self):
        self.dialogo_activo = None
        self.dialogo_texto = ""

    def actualizar(self):
        if self.dialogo_activo:
            return

        dx, dy = 0, 0
        if self.teclas.get(pygame.K_LEFT) or self.teclas.get(pygame.K_a):
            dx = -1
        if self.teclas.get(pygame.K_RIGHT) or self.teclas.get(pygame.K_d):
            dx = 1
        if self.teclas.get(pygame.K_UP) or self.teclas.get(pygame.K_w):
            dy = -1
        if self.teclas.get(pygame.K_DOWN) or self.teclas.get(pygame.K_s):
            dy = 1

        if self.control.activos["izq"]:
            dx = -1
        if self.control.activos["der"]:
            dx = 1
        if self.control.activos["arriba"]:
            dy = -1
        if self.control.activos["abajo"]:
            dy = 1

        if dx != 0 or dy != 0:
            self.jugador.mover(dx * self.jugador.velocidad,
                               dy * self.jugador.velocidad, self.mapa)

        self.comprobar_conexiones()

        for e in self.enemigos:
            e.anim_timer = (e.anim_timer + 1) % 60

        self.actualizar_camara()

    def comprobar_conexiones(self):
        jx = int(self.jugador.x // TILE)
        jy = int(self.jugador.y // TILE)

        if jy <= 0 and "norte" in self.mapa.conexiones:
            self.cambiar_mapa("norte")
        elif jy >= self.mapa.alto - 1 and "sur" in self.mapa.conexiones:
            self.cambiar_mapa("sur")
        elif jx <= 0 and "oeste" in self.mapa.conexiones:
            self.cambiar_mapa("oeste")
        elif jx >= self.mapa.ancho - 1 and "este" in self.mapa.conexiones:
            self.cambiar_mapa("este")

    def cambiar_mapa(self, direccion):
        conexion = self.mapa.conexiones[direccion]
        self.mapa_actual = conexion["mapa"]
        self.mapa = self.mapas[self.mapa_actual]
        self.jugador.x = conexion["x"] * TILE
        self.jugador.y = conexion["y"] * TILE

        self.npcs = [NPC(n) for n in self.datos.get("npcs", [])
                     if n["mapa"] == self.mapa_actual]
        self.enemigos = [Enemigo(e) for e in self.datos.get("enemigos", [])
                         if e["mapa"] == self.mapa_actual]
        self.actualizar_camara()

    def dibujar_tile(self, tile, x, y):
        px = x - self.camara_x
        py = y - self.camara_y
        if px < -TILE or px > GB_W or py < -TILE or py > GB_H:
            return

        if tile == T_VACIO:
            pygame.draw.rect(self.pantalla_gb, FONDO, (px, py, TILE, TILE))
            pygame.draw.rect(self.pantalla_gb, CLARO, (px + 2, py + 3, 1, 1))
            pygame.draw.rect(self.pantalla_gb, CLARO, (px + 5, py + 6, 1, 1))
        elif tile == T_CAMINO:
            pygame.draw.rect(self.pantalla_gb, CLARO, (px, py, TILE, TILE))
            pygame.draw.rect(self.pantalla_gb, FONDO, (px + 1, py + 1, 1, 1))
            pygame.draw.rect(self.pantalla_gb, FONDO, (px + 5, py + 4, 1, 1))
        elif tile == T_PARED:
            pygame.draw.rect(self.pantalla_gb, OSCURO, (px, py, TILE, TILE))
            pygame.draw.rect(self.pantalla_gb, NEGRO, (px, py, TILE, 1))
            pygame.draw.rect(self.pantalla_gb, NEGRO, (px, py, 1, TILE))
            pygame.draw.rect(self.pantalla_gb, NEGRO, (px + 4, py + 4, 3, 3))
        elif tile == T_AGUA:
            pygame.draw.rect(self.pantalla_gb, NEGRO, (px, py, TILE, TILE))
            pygame.draw.rect(self.pantalla_gb, OSCURO, (px + 1, py + 2, 3, 1))
            pygame.draw.rect(self.pantalla_gb, OSCURO, (px + 4, py + 5, 3, 1))
        elif tile == T_ARBOL:
            pygame.draw.rect(self.pantalla_gb, FONDO, (px, py, TILE, TILE))
            pygame.draw.rect(self.pantalla_gb, OSCURO, (px + 2, py + 2, 4, 4))
            pygame.draw.rect(self.pantalla_gb, NEGRO, (px + 3, py + 3, 2, 2))
        elif tile == T_CASA:
            pygame.draw.rect(self.pantalla_gb, OSCURO, (px, py, TILE, TILE))
            pygame.draw.rect(self.pantalla_gb, NEGRO, (px, py, TILE, 2))
            pygame.draw.rect(self.pantalla_gb, CLARO, (px + 2, py + 4, 4, 4))
        elif tile == T_PUERTA:
            pygame.draw.rect(self.pantalla_gb, FONDO, (px, py, TILE, TILE))
            pygame.draw.rect(self.pantalla_gb, NEGRO, (px + 2, py + 1, 4, 7))

    def dibujar_jugador(self):
        sx = int(self.jugador.x - self.camara_x)
        sy = int(self.jugador.y - self.camara_y)
        pygame.draw.rect(self.pantalla_gb, OSCURO, (sx + 1, sy + 1, 6, 6))
        if self.jugador.direccion == "abajo":
            pygame.draw.rect(self.pantalla_gb, FONDO, (sx + 2, sy + 2, 1, 1))
            pygame.draw.rect(self.pantalla_gb, FONDO, (sx + 5, sy + 2, 1, 1))
        elif self.jugador.direccion == "arriba":
            pygame.draw.rect(self.pantalla_gb, NEGRO, (sx + 1, sy + 1, 6, 2))
        elif self.jugador.direccion == "izquierda":
            pygame.draw.rect(self.pantalla_gb, FONDO, (sx + 1, sy + 2, 1, 1))
        elif self.jugador.direccion == "derecha":
            pygame.draw.rect(self.pantalla_gb, FONDO, (sx + 6, sy + 2, 1, 1))

    def dibujar_npcs(self):
        for npc in self.npcs:
            sx = int(npc.x - self.camara_x)
            sy = int(npc.y - self.camara_y)
            pygame.draw.rect(self.pantalla_gb, NEGRO, (sx + 1, sy + 1, 6, 6))
            pygame.draw.rect(self.pantalla_gb, FONDO, (sx + 2, sy + 2, 1, 1))
            pygame.draw.rect(self.pantalla_gb, FONDO, (sx + 5, sy + 2, 1, 1))

    def dibujar_enemigos(self):
        for e in self.enemigos:
            if not e.vivo:
                continue
            sx = int(e.x - self.camara_x)
            sy = int(e.y - self.camara_y)
            offset = 0 if e.anim_timer < 30 else 1
            pygame.draw.rect(self.pantalla_gb, OSCURO,
                             (sx + 1, sy + 1 + offset, 6, 6 - offset))
            pygame.draw.rect(self.pantalla_gb, FONDO,
                             (sx + 2, sy + 2 + offset, 1, 1))
            pygame.draw.rect(self.pantalla_gb, FONDO,
                             (sx + 5, sy + 2 + offset, 1, 1))

    def dibujar_dialogo(self):
        if not self.dialogo_activo:
            return
        pygame.draw.rect(self.pantalla_gb, FONDO, (2, GB_H - 40, GB_W - 4, 38))
        pygame.draw.rect(self.pantalla_gb, NEGRO, (2, GB_H - 40, GB_W - 4, 38), 2)

        try:
            nombre_txt = self.fuente.render(self.dialogo_activo, True, NEGRO)
            self.pantalla_gb.blit(nombre_txt, (6, GB_H - 36))
        except Exception:
            pass

        palabras = self.dialogo_texto.split()
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            prueba = (linea_actual + " " + palabra).strip()
            try:
                ancho = self.fuente.size(prueba)[0]
            except Exception:
                ancho = len(prueba) * 6
            if ancho < GB_W - 16:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        if linea_actual:
            lineas.append(linea_actual)

        for i, linea in enumerate(lineas[:3]):
            try:
                txt = self.fuente.render(linea, True, NEGRO)
                self.pantalla_gb.blit(txt, (6, GB_H - 28 + i * 9))
            except Exception:
                pass

    def dibujar(self):
        self.pantalla.fill(NEGRO)
        self.pantalla_gb.fill(FONDO)

        tx_ini = int(self.camara_x // TILE)
        ty_ini = int(self.camara_y // TILE)
        tx_fin = tx_ini + (GB_W // TILE) + 2
        ty_fin = ty_ini + (GB_H // TILE) + 2

        for ty in range(ty_ini, ty_fin):
            for tx in range(tx_ini, tx_fin):
                if 0 <= tx < self.mapa.ancho and 0 <= ty < self.mapa.alto:
                    self.dibujar_tile(self.mapa.tiles[ty][tx],
                                      tx * TILE, ty * TILE)

        self.dibujar_npcs()
        self.dibujar_enemigos()
        self.dibujar_jugador()
        self.dibujar_dialogo()

        escala = min(self.w / GB_W, self.juego_h / GB_H)
        rw = int(GB_W * escala)
        rh = int(GB_H * escala)
        rx = (self.w - rw) // 2
        ry = (self.juego_h - rh) // 2
        escalada = pygame.transform.scale(self.pantalla_gb, (rw, rh))
        self.pantalla.blit(escalada, (rx, ry))

        self.control.dibujar(self.pantalla)
        pygame.display.flip()

    def ejecutar(self):
        try:
            while self.corriendo:
                self.manejar_eventos()
                self.actualizar()
                self.dibujar()
                self.reloj.tick(FPS)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            pygame.quit()


# ============================================================
# MAIN
# ============================================================
def main():
    if len(sys.argv) > 1 and sys.argv[1].endswith(".jgb"):
        with open(sys.argv[1], "r") as f:
            datos = json.load(f)
        juego = Juego(datos)
        juego.ejecutar()
    else:
        juego = Juego(JUEGO_EJEMPLO)
        juego.ejecutar()


if __name__ == "__main__":
    main()
