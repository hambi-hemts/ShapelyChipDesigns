
from helpers import *

import mpld3 # version 0.2
from mpld3 import plugins
from pylab import gcf, gca
from matplotlib import pylab, mlab, pyplot
from matplotlib.pyplot import axis
import numpy as np
plt = pyplot

from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs

from shapely.geometry import Polygon
from shapely.ops import unary_union

from descartes import PolygonPatch
from shapely.geometry import mapping, MultiPolygon
import json
import os
import pkg_resources

import urllib2
import IPython
from IPython.lib import kernel
#connection_file_path = kernel.get_connection_file()
#connection_file = os.path.basename(connection_file_path)
#kernel_id = connection_file.split('-', 1)[1].split('.')[0]

def loaddxf_todict(filename):
    """  """
    try:
        os.remove('buffer.geojson')
    except:
        pass
        
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'

    os.system('ogr2ogr -f GEOJSON buffer.geojson '+filename)

    s =  open("buffer.geojson", "r").read()

    L = json.loads(s)

    return L

def loaddxf_polylist3(filename):
    """ (3 versions!)  """
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'
        
    Dict = loaddxf_todict(filename)

    PS = []

    for f in Dict['features']:
        #print f['geometry']
        c = f['geometry']['coordinates']
        #print len(c)
        """
        p = Polygon(c)
        PS += [p]
        """
        if len(c)>1:
            p = Polygon(c[0], c[1:])
        elif not len(c):
            p = empty()
        else: p = Polygon(c[0])
        
        PS += [p]
    return PS

def loaddxf_polylist4(filename):
    """ (4 versions!)  """
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'
        
    Dict = loaddxf_todict(filename)

    PS = []

    if Dict.has_key('features'):
        for f in Dict['features']:
            c = f['geometry']['coordinates']

            p = Polygon(c)

            PS += [p]

    else:
        if Dict.has_key('coordinates'):
            for d in Dict['coordinates']:
                if len(d)== 1:
                    p = Polygon(d[0])
                if len(d)>1:
                    p = Polygon(d[0],d[1:])
                PS += [p]

    return PS

def loaddxf_polylist2(filename):
    """ (3 versions!) """
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'

    try:
        os.remove('buffer.geojson')
    except:
        pass   

    os.system('ogr2ogr -f GEOJSON buffer.geojson '+filename+'.dxf')

    s =  open("buffer.geojson", "r").read()

    L = json.loads(s)

    CO = []
    PS = []

    for l in L['features']:
        c = l['geometry']['coordinates']

        if len(c)>1:
            p = Polygon(c[0], c[1:-1])
        else: p = Polygon(c[0])
        
        PS += [p]

    return PS


def load_dxf(filename,debug=False):
    f=filename
    G = []

    try:
        G = loaddxf_polylist3(f)
    except: 
        if debug: print 'no load with ver3'

    try:
        G = loaddxf_polylist2(f)
    except: 
        if debug: print 'no load with ver2'

    try:
        G = loaddxf_polylist4(f)
    except:
        if debug: print 'no load with ver4'

    return G

def NotebookName():
    """
    .. doctest::
    
        >>> import _ShapelyChipDesigns as SD
        >>> print SD.NotebookName()
    
    """
    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    # Updated answer with semi-solutions for both IPython 2.x and IPython < 2.x
    if IPython.version_info[0] < 2:
        ## Not sure if it's even possible to get the port for the
        ## notebook app; so just using the default...
        notebooks = json.load(urllib2.urlopen('http://127.0.0.1:8888/notebooks'))
        for nb in notebooks:
            if nb['kernel_id'] == kernel_id:
                return str(nb['name'])
                break
    else:
        sessions = json.load(urllib2.urlopen('http://127.0.0.1:8888/api/sessions'))
        for sess in sessions:
            if sess['kernel']['id'] == kernel_id:
                return str(sess['notebook']['name'])
                break

def savedxf_polylist(list_of_polygons, filename=None, 
    debug=False, save_as='POLYGON', union = False):
    """Saves a list_of_polygons to a dxf file. 
    The polygons have a HATCH-property, which is not supported by AutoCAD and LinkCAD. 
    It can be viewed in e.g. Klayout. 
    To convert the polygons into one which do not have the HATCH property, use the built-in convert function from ShapelyChipDesigns.
    
    .. plot::
    
        import ShapelyChipDesigns as SD
        C = SD.Point(0,0).buffer(5)
        SD.savedxf_polylist([C], 'acircle')
        C
    """
    try:
        os.remove('buffer.geojson')
    except:
        pass

    GNEW = []

    for p in list_of_polygons:
        
        if p.is_valid:
            GNEW += [p]
        if not p.is_valid:
            pnew = p.buffer(0)
            if pnew.is_valid:
                GNEW += [pnew]
                if debug: print 'new polygon made from self intersecting polygon, is valid: ',pnew.is_valid
            else:
                if debug: print 'self intersecting polygon thrown out.'
                else: pass

    if not GNEW:
        GNEW = [empty()]
            
    if union:
        buffer_obj = unary_union(GNEW)
    else:
        buffer_obj = MultiPolygon(GNEW)

    if debug: print 'started writing file ...'
    f = open("buffer.geojson", "wb")
    f.write(json.dumps(mapping(buffer_obj)))
    f.close()
    if debug: print 'finished.'

    if debug: print 'started conversion of geojson to dxf ...'
    if filename == None:
        filename = 'buffer'
    if debug: print 'save as MULTILINESTRING or POLYGON...'
    # --config("DXF_WRITE_HATCH", "NO")
    os.system('ogr2ogr -f DXF '+filename+'.dxf buffer.geojson')
    if debug: 
		print 'finished.'
		print 'saved '+filename+'.dxf'
    
def convert(input_filename, output_filename):
    """This function can also be used to repair the savedxf_polylist-output, by choosing
    the unrepaired file as input and another ``*.dxf`` file as output. The output will no longer have the hatch property.
    Relies on the command line access to klayout.
    (test by typing klayout into the command line, 
    if the command is not found, klayout needs to be added to the PATH variable.)"""
    c_file = pkg_resources.resource_filename('ShapelyChipDesigns', 'convert.rb')
    os.system('klayout -z -rd input='+input_filename+' -rd output='+output_filename+' -r '+c_file) 

def mouseshow():
    fig = gcf()
    plugins.connect(fig, plugins.MousePosition(fontsize=14))
    return mpld3.display(fig)
    
def showPolygons(list_of_polygons, list_of_colors = False, alpha=0.85, hatch='', fill = True):
    """ 
    Adds patches for a list of shapely polygons. A Multipolygon is a list of Polygons.
    """
    if list_of_colors:
        colors = list_of_colors
    else: 
        colormap = plt.cm.summer
        colors = [colormap(i) for i in np.linspace(0.35, 1.0, len(list_of_polygons))]

    fig = gcf()
    ax  = gca()
    
    
    
    # changed 141019
    if not isinstance(list_of_polygons, list):
        list_of_polygons = [list_of_polygons]

    for i,s in enumerate(list_of_polygons):
        ax.add_patch(PolygonPatch(s,fc=colors[i], ec = 'grey', color=colors[i], fill=fill, alpha=alpha, hatch=hatch))
            
    axis('equal')
	
###### SAVE A MULTILAYER BNS TO A DXF FILE ########

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
    
def remove_duplicates(seq): 
   # order preserving
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

def get_POLYLINE_entries(dxffile):
    """ Returns: str(polyline-entry). 
    The textsequence between : : and :ENDSEC: is the sequence
    of polyline entries. """
    
    with open (dxffile, "r") as myfile:
        data=myfile.read()
        
    poly_str = find_between_r(data, 'ENTITIES\n0\n' , 'ENDSEC')
    
    return poly_str

def get_layer_names(dxffile):
    """ Returns: array([str-layername1, str-layername2, ...])
    Input: poly-str from "get_POLYLINE_entries(dxffile)"
    Every second element after POLYLINE contains a layername. 
    """
    
    poly_str = get_POLYLINE_entries(dxffile)
    strarr = array(poly_str.split('\n'))
    
    inds = np.argwhere(strarr == 'POLYLINE')
    inds += 2
    layers =  strarr[inds].flatten()
    
    return remove_duplicates(layers)

def dxf_make_header(list_of_layernames):
    
    H1 = """0
SECTION
2
HEADER
9
$ACADVER
1
AC1006
0
ENDSEC
0
SECTION
2
TABLES
0
TABLE
2
LAYER
70
"""
    header = H1 + str(len(list_of_layernames)) 
    header += '\n0'
    
    for i, L in enumerate(list_of_layernames):
        LAYERSTR = """
LAYER
70
0
62 
""" + str(i+1)+ """
6
CONTINUOUS
2
""" + L + """
0"""
        
        header += LAYERSTR
        
    H2 = """
ENDTAB
0
ENDSEC
0
SECTION
2
BLOCKS
0
ENDSEC
0
SECTION
2
ENTITIES
0
"""
    
    header += H2
        
    return header

def combine_dxf_files(dxf_list_given, dxf_outname):
    
    all_layernames = []
    all_polylist_entries = []
    
    # get all layernames and polylist entries 
    
    ENTRIES = ''
    
    dxf_list = np.array(dxf_list_given)
    dxf_list = np.insert(dxf_list, 0, './dxf/temp/dummy.dxf')
    #dxf_list.insert(0, './dxf/temp/dummy.dxf')
    
    for D in dxf_list:
        all_polylist_entries += get_POLYLINE_entries(D)
        ENTRIES += get_POLYLINE_entries(D)
        all_layernames += get_layer_names(D)
        
    all_layernames = array(all_layernames)
    
    # check if layernames are duplicated - give warning
    
    # make header for layernames
    
    all_layernames = all_layernames.flatten()
    HEADER = dxf_make_header(all_layernames)
    
    # put polylist entries
    
    #for E in all_polylist_entries:
    #    ENTRIES += E
    
    # end of the dxf 
    
    EOF = """ENDSEC
0
EOF"""
    
    # output of the dxf file
    
    text_file = open(dxf_outname, "w")
    text_file.write(HEADER + ENTRIES + EOF)
    text_file.close()
	
import fileinput

def replace_L0D0_0_with_layername(dxffile, new_name):
    
    fileToSearch = dxffile
    fileOut = dxffile[:-4] + '_' + new_name +'.dxf'
    
    textToSearch = 'L0D0_0' 
    textToReplace = new_name
    
    with open(fileOut, "wt") as fout:
        with open(fileToSearch, "rt") as fin:
            for line in fin:
                fout.write(line.replace(textToSearch, textToReplace))
				
def save_BNS_to_DXF(BNS, DXFName, cleanup=True):
    
    if DXFName[-4:] == '.dxf':
        DXFName = DXFName[:-4]
    
    # get all layer names
    Layernames = BNS.layers.keys()
    UNI = []
    # save each layer to a dxf file
    for L in Layernames:
        polis = BNS.get_polygons(layername=L)
        if len(polis):
            filename = DXFName+'_'+L
            savedxf_polylist(polis, 
                                filename)
            convert(filename+'.dxf', 
                       filename+'.dxf')
            # substitute in each dxf file 
            # the 'L0D0_0' with the layername
            replace_L0D0_0_with_layername(filename+'.dxf',
                                          L)
            os.remove(filename+'.dxf')
            os.rename(filename+'_'+L+'.dxf', 
                      filename+'.dxf')
            
            UNI += [filename+'.dxf']
        
    # combine all dxf files to one
    combine_dxf_files(UNI,
                      DXFName + '.dxf')
    
    convert(DXFName + '.dxf', 
            DXFName + '.dxf')
    
    if cleanup:
        for f in UNI:
            os.remove(f)
            
############################## VER 2 ################################
def combine_dxf_files2(dxf_list_given, dxf_outname):
    
    all_layernames = []
    all_polylist_entries = []
    
    # get all layernames and polylist entries 
    
    ENTRIES = ''
    
    dxf_list = np.array(dxf_list_given)
    #dxf_list = np.insert(dxf_list, 0, './dxf/temp/dummy.dxf')
    #dxf_list.insert(0, './dxf/temp/dummy.dxf')
    
    for D in dxf_list:
        all_polylist_entries += get_POLYLINE_entries(D)
        ENTRIES += get_POLYLINE_entries(D)
        all_layernames += get_layer_names(D)
        
    all_layernames = array(all_layernames)
    
    # check if layernames are duplicated - give warning
    
    # make header for layernames
    
    all_layernames = all_layernames.flatten()
    HEADER = dxf_make_header(all_layernames)
    
    # put polylist entries
    
    #for E in all_polylist_entries:
    #    ENTRIES += E
    
    # end of the dxf 
    
    EOF = """ENDSEC
0
EOF"""
    
    # output of the dxf file
    
    text_file = open(dxf_outname, "w")
    text_file.write(HEADER + ENTRIES + EOF)
    text_file.close()
    
def polygon2dxf_str(polygon, layername):
    
    S = ''
    
    str1 = """POLYLINE
8
"""+layername+"""
70
1
40
0
41
0
66
1
0"""
    
    S += str1
    
    x, y = polygon.exterior.xy
    
    for i in np.arange(len(x)):
        
        str2 = """
VERTEX
8
"""+layername+"""
10
"""+str(x[i])+"""
20
"""+str(y[i])+"""
0"""
        
        S += str2
        
    ####################################################
    if len(polygon.interiors):
        for cs in polygon.interiors:
            x, y = cs.xy
            
            for i in np.arange(len(x)):
            
                str2 = """
VERTEX
8
"""+layername+"""
10
"""+str(x[i])+"""
20
"""+str(y[i])+"""
0"""

        ###

                S += str2
    
    str3 = """
SEQEND
0
""" 
    
    S += str3
    
    return S
    
import os


def save_BNS2DXF_direct_write(BNS, DXFName):
    
    if DXFName[-4:] != '.dxf':
        DXFName = DXFName + '.dxf'
    dxfname = DXFName.replace('.dxf', '')
        
    # get all layer names
    Layernames = BNS.layers.keys()
    UNI = []

        
    FINAL  = ''

    H = dxf_make_header(Layernames)
    FINAL += H
    
    UNI = []

    # save each layer to a dxf file
    for L in Layernames:
        polis = BNS.get_polygons(layername=L)
        
        if len(polis):
            P_INT = []
            
            for p in polis:
                ### if interior polygons >> save to dxf, combine in the end
                if len(p.interiors):
                    P_INT += [p]
                else: 
                    C = polygon2dxf_str(p, L)
                    FINAL += C
                    
            if len(P_INT):        
                filename = dxfname+'_'+L
                savedxf_polylist(P_INT, 
                                    filename)
                convert(filename+'.dxf', 
                           filename+'.dxf')
                # substitute in each dxf file 
                # the 'L0D0_0' with the layername
                replace_L0D0_0_with_layername(filename+'.dxf',
                                              L)
                os.remove(filename+'.dxf')
                os.rename(filename+'_'+L+'.dxf', 
                          filename+'.dxf')

                UNI += [filename+'.dxf']
        
    ENDSEC = """ENDSEC
0
"""
    FINAL += ENDSEC

    EOF = """EOF"""

    FINAL += EOF
    
    with open(DXFName, 'wt') as fout:
        for line in FINAL: 
            fout.write(line)
            
    if len(UNI):
        combine_dxf_files2(UNI+[DXFName],
                             DXFName)
        
        for f in UNI:
            os.remove(f)
    
    convert(DXFName, 
               DXFName)