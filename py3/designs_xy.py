
from .helpers import *
from .brandnew_structure import *

from numpy import arange, linspace, cos, sin, array, hstack, sqrt
from math import pi

from descartes import *
#from gdsCAD import *
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import unary_union, cascaded_union
from numpy import insert, append, degrees, arctan2


def wiggled(r,res=50):
    phi = linspace(pi,0,res)
    w = [r*cos(phi),r*sin(phi)]
    return w

def show_LS(linestring):
    x,y = linestring.xy
    plot(x,y)

def angle_between_points(P1,P2):
    a = degrees(arctan2((P2.y-P1.y),(P2.x-P1.x)))
    return a

def make_wiggle_xy(P1,P2,up=True):
    r = (P1.distance(P2))/2.
    a = degrees(arctan2((P2.y-P1.y),(P2.x-P1.x)))
    
    x,y = wiggled(r)
    wiggle = LineString(zip(x,y))
    wiggle = translate(wiggle,r)
    if not up:
        wiggle = scale(wiggle,yfact=-1,origin=[0,0,0])
    wiggle = rotate(wiggle,a,[0,0])
    wiggle = translate(wiggle,P1.x,P1.y)
    
    x,y = wiggle.xy
    return x,y
	
def find_intersection(line1, line2, showlines=False):
    ''' line1 will be translated until it intersects with line2 '''
    if showlines:
        show_LS(line1)
        show_LS(line2)
    if line1.intersects(line2):
        Pi = line1.intersection(line2)
        return Pi
    else: 
        P0 = line1.interpolate(0)
        P1 = line1.interpolate(line1.length)
        line1 = translate(line1, xoff=P1.x-P0.x, yoff=P1.y-P0.y)
        return find_intersection(line1, line2,showlines)
		
		
def wiggled_function(line_c, line_1, line_2, r1, r2, upfirst=True, showtries=False, no_wiggle=False):
    ''' line_1: upper line, radius of curvature r1 
    no_wiggle: True will result in no wiggle but a straight line segment instead'''
    
    l0 = 0.0
    
    ll = [line_1, line_2]
    rr = [r1, r2]
    ss = [+1, -1]
    up = [True, False]
    
    if upfirst == False:
        up = [False, True]
    
    i = 0
    
    rx, ry = [], []
    
    # special treatment for the first point:
    P0 = line_c.interpolate(l0)
    x0, y0 = P0.xy
    rx += [x0[0]]
    ry += [y0[0]]
    
    r = rr[i]
    
    while l0 < line_c.length-2*r:
        
        r = rr[i]
        l = ll[i]
        
        Pl0 = line_c.interpolate(l0)
        P2r = line_c.interpolate(l0+2*r)
        
        ld = LineString(zip([Pl0.x, P2r.x],
                               [Pl0.y, P2r.y]))
        
        ld = rotate(ld, ss[i]*90, origin=[Pl0.x,Pl0.y])
        
        Pi1 = find_intersection(ld, l, showtries)
        
        ld = translate(ld, 
                       xoff=P2r.x-Pl0.x, 
                       yoff=P2r.y-Pl0.y)
        
        Pi2 = find_intersection(ld, l, showtries)
        
        if no_wiggle:
            wx = [Pi1.x, Pi2.x]
            wy = [Pi1.y, Pi2.y]
        else:
            wx, wy = make_wiggle_xy(Pi1, Pi2, up[i])
        
        rx += wx
        ry += wy
        
        l0 += 2*r
        
        i += 1
        i = i%2
        r = rr[i]
        
    x0, y0 = P2r.xy
    rx += [x0[0]]
    ry += [y0[0]]
    
    return rx, ry

def connect_h(VA, VB, D=0.5):
    """ 
    VA, VB = [pointx, pointy] of the first, second port
    D: distance from port A where a horizontal line should be drawn (in percent) 
    """
    C = []
    C += [VA] 
    if VA[0] == VB[0]:
        C += [VA[0]+(VB[0]-VA[0])/4., VA[1]+(VB[1]-VA[1])/4.]
        C += [VA[0]+2*(VB[0]-VA[0])/4., VA[1]+2*(VB[1]-VA[1])/4.]
        C += [VB]
        return array(C)
    else:
        distance_y = VB[1] - VA[1]
        C += [VA + array([0, distance_y*D])]
        C += [VB + array([0, -distance_y*(1-D)])]
        C += [VB]
        return array(C)

def connect_v(VA, VB, D=0.5):
    """ 
    vertical connection
    VA, VB = [pointx, pointy] of the first, second port
    D: distance from port A where a vertical line should be drawn (in percent) 
    """
    C = []
    C += [VA] 
    if VA[1] == VB[1]:
        #C += [VA[0]+(VB[0]-VA[0])/4., VA[1]+(VB[1]-VA[1])/4.]
        #C += [VA[0]+2*(VB[0]-VA[0])/4., VA[1]+2*(VB[1]-VA[1])/4.]
        C += [VB]
        return array(C)
    else:
        distance_x = VB[0] - VA[0]
        C += [VA + array([distance_x*D, 0])]
        C += [VB + array([-distance_x*(1-D),0])]
        C += [VB]
        return array(C)


def get_launcher_xy(wc1, wg1, wc2, wg2, l):
    """ Get a LAUNCHER's xy coordinates.
        wc1: conductor width(narrow side)
        wc2: conductor width (wider side) 
        wg1 and wg2: gap width 
        l: length/extension 
    Returns: STRUCTURE, BOUNDARY arrays of the xy coordinates
    """
    STRUCTURE = array([[l,wc1/2], [l, -wc1/2], [0, -wc2/2], [0, wc2/2]])
    BOUNDARY  = array([[l,wc1/2+wg1], [l, -wc1/2-wg1], [0, -wc2/2-wg2], [0, wc2/2+wg2]])
    return STRUCTURE, BOUNDARY

def make_resonator(length, width, wiggle_radius, wiggle_number, height=None, points_in_arc=10): 
    """Make a resonator of physical length _length_ and a horizontal physical extension _width_. 
    The wiggle radius _wiggle_radius_ and number of wiggles _wiggle_number_ must be given. 
    OPTIONAL: 
    * The height instead of the width can be specified
    * The resolution of the wiggles can be given by _points_in_arc_
    """
    # ----- ws 
    # |
    # |
    # | hs (short) and hw (long)
    l, w, r, N, h, p = length, width, wiggle_radius, wiggle_number, height, points_in_arc
    if height!=None:
        ws = 0.5*(l-(N+1)*pi*r-N*h+2*r*(N+1))
    else: 
        ws = 0.5*(w-(N+1)*2*r) 
        h  = N**(-1)*(l-2*ws-(N+1)*pi*r+2*r*(N+1))
    CX, CY = wiggled_line(h,r,N)
    # straight piece in front:
    CX = insert(CX, 0, CX[0]-ws)
    CY = insert(CY, 0, CY[0])
    # straight piece in the end:
    CX = append(CX, CX[-1]+ws)
    CY = append(CY, CY[-1])
    return CX, CY


########### REGULAR POLYGON #########################
##############################################
##############################################
def get_RegPoly_xy(center_xy, edgelength, edges):
    """ Get a REGULAR POLYGON's xy coordinates.
    Returns: X, Y arrays of the coordinates. 
    """
    x,y,l,e = center_xy[0], center_xy[1], edgelength, edges
    thetas   = linspace(0,2*pi,e+1)
    CX, CY , V = [], [], []
    for t in thetas:
        CX.append(cos(t))
        CY.append(sin(t))
        V.append([cos(t),sin(t)])
    cucu   = array(V[1])-array(V[0])
    length = sqrt(array(cucu[1])**2+array(cucu[0])**2)
    return l/length*array(CX)+x, l/length*array(CY)+y

#### A WIGGLED LINE ###
def wiggled_line(Height, Radius, Number_of_Wiggles, Resolution_of_Arc=10):
    
    #################################################################

    R, L = Radius, Height - 2*Radius
    N_WIGGLES = Number_of_Wiggles
    P = Resolution_of_Arc
    
    CX, CY = [], []
    
    ##### FIRST RADIUS #####
    
    t = linspace(3*pi/2,2*pi,P)
    cx, cy = R*(cos(t)), R*(sin(t)) 
    CAPHALF = LineString(zip(cx,cy))
    DUMMY = translate(CAPHALF, xoff=-R, yoff=Height/2+R)
    CX = CX + list(DUMMY.xy[0][:])
    CY = CY + list(DUMMY.xy[1][:])

    ##### WIGGLES ####
    
    t = linspace(pi,0,P)
    cx, cy = R*(cos(t)), R*(1+sin(t)) 
    CAP = LineString(zip(cx,cy))
    for i in arange(N_WIGGLES):
        if i%2==0:
            DUMMY = translate(CAP, xoff = 2*R*i+R, yoff=L)
        else:
            CAPM = scale(CAP, yfact=-1)
            DUMMY = translate(CAPM, xoff = 2*R*i+R, yoff=-R)
        CX = CX + list(DUMMY.xy[0][:])
        CY = CY + list(DUMMY.xy[1][:])
        
    ##### LAST RADIUS #####
    
    if N_WIGGLES%2!=0:
        DUMMY = scale(CAPHALF,xfact=-1)
        DUMMY = translate(DUMMY, xoff = 2*R*i+2*R, yoff=Height/2+R)
    else: 
        DUMMY = scale(CAPHALF,xfact=-1, yfact=-1)
        DUMMY = translate(DUMMY, xoff = 2*R*i+2*R, yoff=Height/2+R)

    CX = CX + list(DUMMY.xy[0][::-1])
    CY = CY + list(DUMMY.xy[1][::-1])
    
    CX = array(hstack(CX))    
    CY = array(hstack(CY))
    return CX, CY