#!/usr/bin/python
# -*- coding: utf-8 -*-
from visual import *
from visual.graph import *
from math import sqrt

scene.range = 5
scene.height = 700

# głóne wahadło
arm =  cylinder (pos = (0,4,0), color = color.white, radius = 0.01, axis = (0,-4,0))
ball = sphere   (pos = (0,0,0), color = color.white, radius = 0.1)

# wielkości fizyczne
t = 0.0 # aktualny czas
tdelta = 0 # aktualne zboczenie czasu (dostosowywanie, by ruch zaczynał się w od czasu t na wykresie)
g = 9.81 # przyspieszenie ziemskie
m = 1.0 # masa [kg]
mfac = 0.1 # przelicznik siły na długość wektora na ekranie
v = 0 # prędkość chwilowa
a = 0 # amplituda
w = 0 # prędkość kątowa
x = 0 # aktualna pozycja
term = 0 # okres
ep = 0
ek = 0

# wektory reprezentujące wielkości fizyczne
f =  arrow (pos = ball.pos, color = (0, 1, 0), radius = 0.01, axis = (0, 0, 0))
s =  arrow (pos = ball.pos, color = (0, 0, 1), radius = 0.01, axis = (0, 0, 0))
mg = arrow (pos = ball.pos, color = (0.5, 0, 0), radius = 0.005, axis = (0, -m*g*mfac, 0))

# wahadło nastawne
greyarm = cylinder (pos = arm.pos, color = (0.5,0,0), radius = arm.radius, axis = arm.axis)
redball = sphere (pos = ball.pos, color = color.red, radius = 0.15)
redarm =  cylinder (pos = arm.pos, color = color.red, radius = arm.radius, axis = arm.axis)

# etykiety prezentujące wielkości fizyczne
forces = None
label_pos = (3,3,0)
fcurve = None
scurve = None

xvgraph = None
xcurve = None
vcurve = None

ekcurve = None
epcurve = None

# slabel # siła przeciwna sile sprzężystośći nitki
# mglabel


def recalc ():
    global a, w, term, t, tdelta, fcurve, scurve, forces, xvgraph, xcurve, vcurve, ekcurve, epcurve
    w = 1.0 / sqrt(redarm.axis.mag / g)
    term = 2.0 * pi / w
    a = diff_angle(redarm.axis, (0,-1,0))
    ball.pos = redball.pos
    arm.axis = redarm.axis
    tdelta = 0.5 * pi / w
    t = 0
    if redarm.axis.x > 0:
    	tdelta = -tdelta
    mg.pos = ball.pos
    mg.axis = vector(0,-m*g*mfac,0)
    #fcurve.color = (0, 0.3, 0)
    height = 256
    if forces:
        forces.display.visible = False
    forces = gdisplay(title="Wykres", xtitle = "t[s]", ytitle = "x[m] (cyan), v[m/s] (zolty), Ep (magenta), Ek (czerwony) [J]",
                      x = scene.x + scene.width, y = scene.y, height=height, xmax = 11.0)
    fcurve = gcurve (display = forces, color = (0, 1, 0), dot=True)
    scurve = gcurve (display = forces, color = (0, 0, 1), dot=True)

    #if xvgraph:
    #    xvgraph.display.visible = False
    #xvgraph = gdisplay(title="Prędkość i wychylenie w czasie", xtitle = "t[s]", ytitle = "x[m], v[m/s]", x = forces.display.x, y = forces.display.y + height, height = height)
    vcurve = gcurve (display = forces, color = (1,1,0), dot = True) # żółty
    xcurve = gcurve (display = forces, color = (0,1,1), dot = True) # cyan
    ekcurve = gcurve (display = forces, color = (1,0,0), dot = True) # czerwony
    epcurve = gcurve (display = forces, color = (1,0,1), dot = True) # magenta
    
recalc()

pick = None
deltat = 0.02
while True:
    rate(50)

    # Ustawienie myszką:
    if scene.mouse.events: 
        m1 = scene.mouse.getevent() 
        if m1.drag and m1.pick == redball:
            drag_pos = m1.pickpos
            pick = m1.pick 
        elif m1.drop:
            pick = None
            recalc()
    if pick:
        new_pos = scene.mouse.project(normal=(0,0,1)) 
        if new_pos != drag_pos: 
            pick.pos += new_pos - drag_pos
            drag_pos = new_pos
            redarm.axis = redball.pos - redarm.pos
            greyarm.axis = redarm.axis
            greyarm.axis.x = - redarm.axis.x
            
    # Ruch samodzielny:
    x = a*sin((t - tdelta)*w)
    #v = a * w * cos(2*w*(t-tdelta) + diff_angle((0,-1,0), redarm.axis))
    v = a * w * cos(w * (t - tdelta))
    
    arm.axis = rotate(vector(0,-1,0) * arm.axis.mag, x, (0,0,1))
    ball.pos = arm.pos + arm.axis
    mg.pos = s.pos = f.pos = ball.pos
    s.axis = arm.axis.norm() * (mg.axis.mag * cos(diff_angle((0,-1,0), arm.axis)))
    if arm.axis.x > 0:
    	turn = -1
    else:
    	turn = 1
    f.axis = rotate(arm.axis.norm(), pi/2, (0,0,1)) * (mg.axis.mag * sin(diff_angle((0,-1,0), arm.axis)) * turn)
    
    if a != 0 and t < 11:
        ek = 0.5 * m * v * v
        ep = 0.5 * x * x * (f.axis.mag2 / (a * mfac))
        #fcurve.plot(pos = (t, (f.axis.mag / mfac)))
        #scurve.plot(pos = (t, (s.axis.mag / mfac)))
        xcurve.plot(pos = (t, x))
        vcurve.plot(pos = (t, v))
        ekcurve.plot(pos = (t, ek))
        epcurve.plot(pos = (t, ep))
        
    t += deltat
    

