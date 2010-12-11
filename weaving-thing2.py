#!/usr/bin/python
# -*- coding: utf-8 -*-
from visual import *
from visual.graph import *
from math import sqrt, cos, sin, asin

scene.range = 5
scene.height = 700


#### WIELKOŚCI FIZYCZNE
# stałe
g = 9.81
mfac = 0.1 # przelicznik siły na długość wektora na ekranie

# cechy fizyczne
m = 1.0 # masa [kg]
L = 0 # długość linki

# paramtetry wyliczane raz dla ruchu
A = 0 # amplituda liniowa
Angle = 0 # początkowe wychylenie
w = 0 # prędkość kątowa
k = 0 # współczynnik
T = 0 # okres

# parametry zmieniające się w czasie
t = 0 # aktualny czas
angle = 0 # aktualne wychylenie
x = 0 # pozycja liniowa
v = 0 # prędkość liniowa
ep = 0 # energia potencjalna
ek = 0 # energia kinetyczna
f = 0 # siła wypadkowa
s = 0 # siła równoważąca sprężystość nitki

#### OBIEKTY GRAFICZNE
# główne wahadło
arm =  cylinder (pos = (0,4,0), color = color.white, radius = 0.01, axis = (0,-4,0))
ball = sphere   (pos = (0,0,0), color = color.white, radius = 0.1)

# wahadło sterujące
greyarm = cylinder (pos = arm.pos, color = (0.5,0,0), radius = arm.radius, axis = arm.axis)
redball = sphere (pos = ball.pos, color = color.red, radius = 0.15)
redarm =  cylinder (pos = arm.pos, color = color.red, radius = arm.radius, axis = arm.axis)

# wektory reprezentujące siły
farrow = arrow (pos = ball.pos, color = (0, 1, 0), radius = 0.001, axis = (0, 0, 0))
sarrow =  arrow (pos = ball.pos, color = (0, 0, 1), radius = 0.001, axis = (0, 0, 0))
mgarrow = arrow (pos = ball.pos, color = (0.5, 0, 0), radius = 0.001, 
                 axis = (0, -m*g*mfac, 0))

# suwak od masy:
mass_scale = cylinder (pos = (-1.3, -4.7, 0), axis = (4, 0, 0), color = (0.5, 0.5, 0.5), radius = 0.02)
mass_ball = sphere (pos = mass_scale.pos + (0.1 * mass_scale.axis), radius = 0.1, color = (0.5, 0.5, 0.6))
mass_label = label (pos = (-2.35, -4.7, 0), text = "masa: 1.0kg")

#### WYKRES
graph_display = None
vgraph = None
xgraph = None
epgraph = None
ekgraph = None

def restart_graphs():
    global graph_display, vgraph, epgraph, ekgraph, xgraph
    if graph_display:
        graph_display.display.visible = False
        graph_display = None
    graph_display = gdisplay(title="Wykres", xtitle = "t[s]",
                             ytitle = "x[m] (cyan), v[m/s] (zolty), Ep (magenta), Ek (czerwony) [J]",
                             x = scene.x + scene.width, y = scene.y, height = 300, xmax = 11.0)
    vgraph = gcurve (display = graph_display, color = (1,1,0), dot = True) # żółty
    xgraph = gcurve (display = graph_display, color = (0,1,1), dot = True) # cyan
    ekgraph = gcurve (display = graph_display, color = (1,0,0), dot = True) # czerwony
    epgraph = gcurve (display = graph_display, color = (1,0,1), dot = True) # magenta

def restart():
    global A, w, k, T, t, Angle
    global m, L, g
    L = redarm.axis.mag
    Angle = diff_angle ( (0,-1,0), redarm.axis )
    w = sqrt (g / L)
    A = sin (angle) * L
    T = 2 * pi * sqrt (L / g)
    t = 0
    #t = 0.25 * T
    #if redarm.axis.x < 0 : t = -t
    restart_graphs()

def actual():
    global m, L, mfac, g
    global A, w, k, T
    global t, angle, x, v, ep, ek, f, s
    global arm, ball
    global vgraph, xgraph, ekgraph, epgraph
    ## obliczanie wielkości fizycznych
    x = A * sin (t * w)
    angle = Angle * sin (t * w)
    f = m * g * sin (angle)
    s = m * g * cos (angle)
    v = A * w * cos (w * t)
    k = (m * g) / L
    ek = 0.5 * k * ((A * cos (w * t)) ** 2)
    ep = 0.5 * k * ((A * sin (w * t)) ** 2)

    ## wizualizacje
    # ramię
    arm.axis = rotate((0,-L,0), angle, (0,0,1))
    ball.pos = arm.pos + arm.axis
    # wykresy
    if t < 11:
        for graph, value in [(vgraph, v), (xgraph, x), (ekgraph, ek), (epgraph, ep)]:
            if graph: graph.plot(pos = (t, value))
    # siły
    for arr in [farrow, sarrow, mgarrow]: arr.pos = ball.pos
    mgarrow.axis = (0, - m * g * mfac, 0)
    sarrow.axis = arm.axis.norm() * s * mfac
    farrow.axis = rotate(arm.axis.norm(), -pi/2, (0,0,1)) * f * mfac
    
    
restart()

pick = None
deltat = 0.02
while True:
    rate(50)
    # Ruch:
    actual()
    t += deltat
    # Ustawienie myszką:
    if scene.mouse.events: 
        m1 = scene.mouse.getevent() 
        if m1.drag and (m1.pick == redball or m1.pick == mass_ball):
            drag_pos = m1.pickpos
            pick = m1.pick
            pick.radius *= 1.5
        elif m1.drop:
            if pick == redball: restart()
            if pick: pick.radius /= 1.5
            pick = None
    if pick == redball:
        new_pos = scene.mouse.project(normal=(0,0,1)) 
        if new_pos != drag_pos: 
            pick.pos += new_pos - drag_pos
            drag_pos = new_pos
            redarm.axis = redball.pos - redarm.pos
            greyarm.axis = redarm.axis
            greyarm.axis.x = - redarm.axis.x
    elif pick == mass_ball:
        new_pos = scene.mouse.pos #scene.mouse.project(normal=(0,0,1))
        if new_pos != drag_pos:
            pick.pos += (new_pos.x - drag_pos.x, 0, 0)
            if pick.pos.x < mass_scale.pos.x: pick.pos.x = mass_scale.pos.x
            if pick.pos.x > (mass_scale.pos + mass_scale.axis).x :
                pick.pos = mass_scale.pos + mass_scale.axis
            drag_pos = new_pos
            m = ((pick.pos.x - mass_scale.pos.x) / mass_scale.axis.x) * 10
            mass_label.text = "masa: %.1fkg" % m
            ball.radius = m * 0.1
