
from helpers import *
from brandnew_structure import *

from shapely_fonts import _font

from numpy import arange, linspace, cos, sin, array, hstack, degrees

from descartes import *
#from gdsCAD import *
from shapely.geometry import *
from shapely.geometry import Polygon
from shapely.affinity import *
from shapely.ops import unary_union, cascaded_union

import math

def v_dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def v_length(v):
    return math.sqrt(v_dotproduct(v, v))

def v_angle(v1, v2):
    return math.acos(v_dotproduct(v1, v2) / (v_length(v1) * v_length(v2)))

def get_airbridge_polys(x,y, A10, A20, NA=10, res=1000.):
    """
    x,y: coordinates along which to distribute the airbridges
    NA:  number of airbridges
    A10, A20: Airbridge Polygons (A20 is the larger one), use 
        "get_airbridge_poly" to get the boxes
    returns S1, S2 airbridge layers. 
    """

    L = LineString(zip(x,y))

    NA = NA
    dl = L.length/res

    v0 = array([0,1])

    S1 = []
    S2 = []

    for i in arange(NA):
        
        x0, y0     = L.interpolate((1+i)*L.length/(NA+1)).xy
        x0, y0     = x0[0], y0[0]
        dmx, dmy   = L.interpolate((1+i)*L.length/(NA+1)+dl).xy
        dpx, dpy   = L.interpolate((1+i)*L.length/(NA+1)-dl).xy
        vL = array([dmx[0]-dpx[0],
                    dmy[0]-dpy[0]])
        
        A1 = translate(A10, x0, y0)
        A2 = translate(A20, x0, y0)
        
        angle = degrees(v_angle(v0,vL))
        
        if dmx[0]>dpx[0]:
            angle = -angle
        
        A1 = rotate(A1, angle, (x0,y0))
        A2 = rotate(A2, angle, (x0,y0))
        
        S1 += [A1]
        S2 += [A2]
    return S1, S2

def get_airbridge_poly1(width=36,length=16,spacing=34):
    ''' returns a Polylist 
    Usage: 
    RES.add_STRUC1(S1a+S1b)
    '''
    b  = mybox((0,0), width, length)
    b1 = translate(b, xoff=spacing/2. , yoff=-length/2.)
    b2 = translate(b, xoff=-spacing/2-width , yoff=-length/2.)
    A10 = unary_union([b1,b2])
    return A10

def get_airbridge_poly2(length_out=180,width_out=90,length_in=100,width_in=10):
    '''
    RES.add_STRUC2(S2)
    '''
    b1 = mybox((0,0),length_out,width_out)
    b1 = translate(b1, xoff=-length_out/2., yoff=-width_out/2.)

    b2 = mybox((0,0),length_in,width_in)
    b2 = translate(b2, xoff=-length_in/2., yoff=-width_in/2.)

    A20 = b1.difference(b2)
    return A20

from shapely.geometry import Polygon
def mybox((x00, y00), width, height):
    """ Returns a rectangular polygon with the lower left edge at
        'x00, y00' of width 'width' and height 'height'.
    """
    polygon = Polygon([(x00, y00), (x00, y00+height), 
                     (x00+width, y00+height),(x00+width, y00)])
    return polygon

def MakeTransmissionLine(xvals,yvals, width, gap):
    xys = array(zip(xvals,yvals))
    line = LineString(zip(xvals,yvals))
    BOUNDARY = line.buffer(width/2.+gap,cap_style=2)
    STRUCTURE = line.buffer(width/2.,cap_style=2)
    RES = BRAND_NEW_STRUCTURE(BOUNDARY, STRUCTURE)
    RES.add_anker([xvals[0],yvals[0]])
    RES.add_anker([xvals[-1],yvals[-1]])
    return RES

def text2poly(text, size, position=(0, 0), horizontal=True, angle=0, layer=None, datatype=None) :

    polygons = []
    posX = 0
    posY = 0
    text_multiplier = size / 9.0

    for jj in range(len(text)):
        if text[jj] == '\n':
            if horizontal:
                posY -= 11
                posX = 0
            else:
                posX += 8
                posY = 0
        elif text[jj] == '\t':
            if horizontal:
                posX = posX + 32 - (posX + 8) % 32
            else:
                posY = posY - 11 - (posY - 22) % 44
        else:
            if _font.has_key(text[jj]):
                for p in _font[text[jj]]:
                    polygon = p[:]
                    for ii in range(len(polygon)):
                        xp = text_multiplier * (posX + polygon[ii][0])
                        yp = text_multiplier * (posY + polygon[ii][1])
                        polygon[ii] = (xp, yp)
                    #print polygon
                    polygons.append(Polygon(polygon))
            if horizontal:
                posX += 8
            else:
                posY -= 11
    #rotate(angle)
    #translate(position)
    return polygons