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
farrow = arrow (pos = ball.pos, color = (0, 1, 0), radius = 0.01, axis = (0, 0, 0))
sarrow =  arrow (pos = ball.pos, color = (0, 0, 1), radius = 0.01, axis = (0, 0, 0))
mgarrow = arrow (pos = ball.pos, color = (0.5, 0, 0), radius = 0.005, 
                 axis = (0, -m*g*mfac, 0))

def restart():
    global A, w, k, T, t, Angle
    global m, L, g
    L = redarm.axis.mag
    Angle = diff_angle ( (0,-1,0), redarm.axis )
    w = sqrt ( g / L )
    A = sin ( angle ) * L
    k = ( m * g ) / L
    T = 2 * pi * sqrt ( L / g)

def actual():
    #global m, L, mfac, g
    #global A, w, k, T
    global t, angle, x, v, ep, ek, f, s
    global arm, ball
    ## obliczanie wielkości fizycznych
    x = A * sin (t * w)
    angle = Angle * sin (t * w)
    f = m * g * sin (angle)
    s = m * g * cos (angle)

    ## wizualizacje
    # ramię
    arm.axis = rotate((0,-L,0), angle, (0,0,1))
    ball.pos = arm.pos + arm.axis
    # siły
    for arr in [farrow, sarrow, mgarrow]: arr.pos = ball.pos
    mgarrow.axis = (0, - m * g * mfac, 0)
    sarrow.axis = arm.axis.norm() * s * mfac
    farrow.axis = rotate(arm.axis.norm(), -pi/2, (0,0,1)) * f * mfac
    

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
        if m1.drag and m1.pick == redball:
            drag_pos = m1.pickpos
            pick = m1.pick 
        elif m1.drop:
            pick = None
            restart()
    if pick:
        new_pos = scene.mouse.project(normal=(0,0,1)) 
        if new_pos != drag_pos: 
            pick.pos += new_pos - drag_pos
            drag_pos = new_pos
            redarm.axis = redball.pos - redarm.pos
            greyarm.axis = redarm.axis
            greyarm.axis.x = - redarm.axis.x
