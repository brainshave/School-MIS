from visual import *
from math import sqrt, copysign

scene.range = 5
arm =  cylinder (pos = (-1,2,0), color = color.white, radius = 0.01, axis = (0,-2,0))
ball = sphere   (pos = (-1,0,0), color = color.white, radius = 0.1)

greyarm = cylinder (pos = arm.pos, color = (0.5,0.5,0.5), radius = arm.radius, axis = arm.axis)
redball = sphere (pos = ball.pos, color = color.red, radius = 0.15)
redarm =  cylinder (pos = arm.pos, color = color.red, radius = arm.radius, axis = arm.axis)

deltat = 0.01
t = 0.0

a = 0
w = 0
term = 0


def recalc ():
    global a, w, term, t
    w = 1.0 / sqrt(redarm.axis.mag / 9.81)
    term = 2.0 * pi / w
    a = diff_angle(redarm.axis, (0,-1,0))
    ball.pos = redball.pos
    arm.axis = redarm.axis
    t = copysign(0.5 * pi / w, redarm.axis.x)

recalc()

pick = None
while True:
    rate(100)

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
    arm.axis = rotate(vector(0,-1,0) * arm.axis.mag, a*sin(t*w), (0,0,1))
    ball.pos = arm.pos + arm.axis

    t += deltat

