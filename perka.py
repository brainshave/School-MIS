#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
from visual import *
from math import sqrt, cos, floor
from random import shuffle, randint

xsize = 5
ysize = 5
zsize = 3

size = xsize * ysize * zsize

sys.setrecursionlimit(size * 80)

scene.range = max([xsize,ysize,zsize]) + 1
xstart = xsize / 2.0 - 0.5
ystart = ysize / 2.0 - 0.5
zstart = zsize / 2.0 - 0.5
scene.center = (xstart, ystart, zstart)
grey = (0.25, 0.25, 0.25)
balls = [[[box (pos = (x, y, z),
                opacity = 1,
                width=0.5, height = 0.5, length=0.5,
                color = grey)
           for z in range (zsize)]
          for y in range (ysize)]
         for x in range (xsize)]

def flat (balls):
    return [ball for wall in balls for row in wall for ball in row]

balls_flat = flat(balls)

def conductors () : return filter (lambda x: x.color != grey, balls_flat)
def resistors () : return filter (lambda x: x.color == grey, balls_flat)

# oznacz jako przewodzace z pewnym prawdopodobienstwem      
def colorize (p):
    ball_count = xsize * ysize * zsize
    target = int(ball_count * p)
    uncolorized = resistors()
    colorized = conductors()
    to_colorize = target - len(colorized)
    if to_colorize > 0:
        random.shuffle(uncolorized)
        for ball in uncolorized[:to_colorize]:
            ball.color = color.white
    elif to_colorize < 0:
        random.shuffle(colorized)
        for ball in colorized[:-to_colorize]:
            ball.color = grey

pipes = []

#pipe(balls_flat[0], balls_flat[1])

colors = [(r / 256.0 ,g / 256.0, b / 256.0)
          for r in range(94, 256, 12)
          for g in range(95, 256, 12)
          for b in range(96, 256, 12)]
shuffle(colors)


def pipe (one, two):
    #pipes.append(box (color = one.color, pos = (one.pos + two.pos)/2,
    #                  axis = (two.pos - one.pos)/2, width=0.05, height=0.05))
    return two

def color_neighbors (ball, c):
    #if ball.color == color.white:
    ball.color = c
    map(lambda b: color_neighbors(b,c),
        map(lambda b: pipe(ball,b),
            filter(lambda b: b.color != grey and b.color != c,
                   map(lambda (x,y,z): balls[x][y][z],
                       filter(lambda (x,y,z): x >= 0 and y >= 0 and z >=0
                              and x < xsize and y < ysize and z < zsize,
                              map(lambda (x,y,z): (int(x), int(y), int(z)),
                                  [ball.pos - v
                                   for v in [(1,0,0), (0,1,0), (0,0,1),
                                             (-1,0,0), (0,-1,0), (0,0,-1)]]))))))

def color_random_one():
    r = resistors()
    a = r[randint(0,len(r)-1)]
    c = colors.pop()
    a.color = c
    for v in [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]:
        x, y, z = a.pos - v
        if (x >= 0 and y >= 0 and z >=0 and x < xsize
            and y < ysize and z < zsize):
            other = balls[int(x)][int(y)][int(z)]
            if other.color != grey:
                a.color = other.color
                c = other.color
                color_neighbors(a, c)
                break
    colors.insert(0,c)

def clusters ():
    for p in pipes: p.visible = False
    del pipes[:]
    for ball in conductors():
        c = colors.pop()
        color_neighbors(ball, c)
        colors.insert(0,c)

def percolation ():
    for x1 in range(xsize):
        for z1 in range(zsize):
            b1 = balls[x1][0][z1]
            for x2 in range(xsize):
                for z2 in range(zsize):
                    b2 = balls[x2][ysize-1][z2]
                    if (b1.color != grey and b2.color != grey
                        and b1.color == b2.color):
                        return True
    return False

while True:
    for a in range(int(size)):
        color_random_one()
        if percolation():
            rate(0.75)
            break
        else:
            rate(20)
    for ball in balls_flat:
        ball.color = grey

