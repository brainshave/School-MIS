#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from visual.graph import *
from math import sqrt, cos, floor
from pprint import pprint

graph = gdisplay (xmin = -2, xmax = 4, ymin = -0.5, ymax = 1.5,
            title = "Iteracja logistyczna / Szymon Witamborski")
plot = gdots (display = graph.display, shape = "round", size = 1, color=(1,1,1))

def logist (k, x):
    return k * x * (1.0 - x)

def logist_list (k, elems):
    return reduce(lambda li, _: li + [logist(k, li[-1])], range(elems), [0.0001])

resx = 200
resy = 100
ommit = 200

[plot.plot(pos=(k,v))
 for k in map (lambda x: float(x) / resx, range(-2 * resx, 4 * resx + 1))
 for v in logist_list(k, resy + ommit)[ommit:]]
