

from pylab import *
from numpy import *

import numpy
import matplotlib
from matplotlib import pylab, mlab, pyplot
np = numpy
plt = pyplot

from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs

from shapely.geometry import Point, LineString, Polygon
from shapely.affinity import translate, rotate

from math import pi
from numpy import linspace

colors = lambda NPlots: [plt.cm.rainbow(i) for i in np.linspace(0.35, 1.0, NPlots)]

#############
def circle_step(l0, da):
    cx, cy = l0.xy
    l1 = rotate(l0, da, origin=[cx[0], cy[0]])
    return translate(l1, cx[-1]-cx[0], cy[-1]-cy[0])

def split_up(l0,dl):
    """split up the LineString l0 into parts of length dl. 
    Return a list of LineStrings."""
    
    np  = int(l0.length/dl)
    cx, cy = l0.xy
    dx, dy = cx[-1]-cx[0], cy[-1]-cy[0]
    
    xco = [cx[0]+i*dx/np for i in arange(np+1)]
    yco = [cy[0]+i*dy/np for i in arange(np+1)]
    
    L = []
    for i, x in enumerate(xco[0:-1]):
        lnew = LineString([[xco[i],yco[i]],
                           [xco[i+1],yco[i+1]]])
        L += [lnew]
        
    return L

def roll_along(Llist, n, Lother, show=False):

    L = Llist

    #smoothy = [[L[0].xy[0][0],
    #            L[0].xy[1][0]]]
    smoothy = []
    
    da = 360./n
    cs = colors(len(Llist))
    lbuffer = []
    
    ok = True

    for j, l in enumerate(L):

        # circle up
        lbuffer = []
        l0 = l

        for i in arange(n):
            l1 = circle_step(l0,da)
            if show: plot(l1.xy[0], l1.xy[1], lw=2, c=cs[int(j%n)])
            lbuffer += [l1]
            if l1.intersects(Lother): 
                ok = False
                break
            l0 = l1

        if ok:
            # circle down
            lbuffer = []
            l0 = l

            for i in arange(n):
                l1 = circle_step(l0,-da)
                if show: plot(l1.xy[0], l1.xy[1], lw=2, c=cs[int(j%n)])
                lbuffer += [l1]
                if l1.intersects(Lother): 
                    ok = False
                    break
                l0 = l1

        if show: plot(l.xy[0],l.xy[1], lw=3)
           
        if not ok:
            smoothy += [array([b.xy[0][0], b.xy[1][0]]) for b in lbuffer]
            IP = lbuffer[-1].intersection(Lother).xy
            break
               
    return array(smoothy)

def smoothen(geom, r, n, show=False):
    """ returns a smoothened version of the geometry.
    geom: polygon or linestring
    r:    radius of curvature for the smoothing
    n:    resolution of the smoothing (=number of points on the smoothing-circle)
    """
    res = []
    
    if isinstance(geom, Polygon):
        CX, CY = geom.boundary.xy
        d = 1
        d2 = 1
    elif isinstance(geom, LineString):
        CX, CY = geom.xy
        d = 2
        d2 = 0
        res += [[CX[0], CY[0]]]
    else: 
        raise exception("unsupported geometry type. geom must be LineString or Polygon.")
    
    da = 360./n
    ds = 2*pi*r/n
    
    #for i, cx in enumerate(CX):
    for i in arange(len(CX)-d):
    
        i0, i1, i2 = array(arange(i,i+3))%(len(CX)-d2)
        
        L0 = LineString([[CX[i0], CY[i0]],
                         [CX[i1], CY[i1]]])
        L1 = LineString([[CX[i1], CY[i1]],
                         [CX[i2], CY[i2]]])   
        
        L = split_up(L0,ds)
        
        s = roll_along(L,n,L1,show=show)
        res += list(s)
        
    if isinstance(geom, LineString):
        res += [[CX[-1], CY[-1]]]
    return array(res)