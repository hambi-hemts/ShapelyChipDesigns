
from .helpers import *
from .designs_poly import *
from .brandnew_structure import *
from descartes import *
#from gdsCAD import *
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import unary_union, cascaded_union
from shapely.ops import unary_union, cascaded_union

class GROUNDPLANE:

    def __init__(self, width, height,x0=0, y0=0):
        self.DX = width
        self.DY = height 
        self.GROUND = [mybox((x0,y0), self.DX, self.DY)]
        
        E = EMPTY()
        self.G0     = self.GROUND
        
        self.SHAPES = [E]
        self.BOUNDARY  = LAYER([],'BOUNDARY')
        self.STRUCTURE = LAYER([],'STRUCTURE')
        
        self.ANKERS = {0: [x0,y0]}
        
        self.STRUC1 = LAYER([],'STRUC1')
        self.STRUC2 = LAYER([],'STRUC2')
        self.EBL = LAYER([],'EBL')
        
        self.layers = {'BOUNDARY':self.BOUNDARY,
                        'STRUCTURE':self.STRUCTURE,
                        'STRUC1':self.STRUC1,
                        'STRUC2':self.STRUC2,
                        'EBL':self.EBL
                        }

    def add_anker(self, ankerpoint, name=None):
        if name:
            self.ANKERS[name] = ankerpoint
        else: 
            name = len(self.ANKERS)
            self.ANKERS[name] = ankerpoint
            
    def add_diff_groundplane(self, polygon):
        GROUNDPLANES = array(self.GROUND)
        res = array([G.difference(polygon) for G in GROUNDPLANES])
        GROUNDPLANES = res.flatten()
        GROUNDPLANES = flattenMultipolyG(GROUNDPLANES)
        self.GROUND = GROUNDPLANES  

    def get_intersections_groundplane(self, polygon):
        '''added 140918 '''
        GROUNDPLANES = array(self.GROUND)
        print('pt',type(polygon))
        res = array([polygon.intersection(G) for G in GROUNDPLANES])
        print('res',res)
        inters = res.flatten()
        print('inters',inters)
        inters = flattenMultipolyG(inters)
        return inters

    '''        
        def add_structure(self, polygon):
            self.STRUCTURES += [polygon.intersection(g) for g in self.GROUND]
        
        def add_STRUC1(self, STRUC1):
            print 'Deprecated: Use G.STRUC1.add_polis()'
            if isinstance(STRUC1,list):
                for el in STRUC1:
                    self.STRUC1 += [el]
            else:    
                self.STRUC1 += [STRUC1]
                
        def add_STRUC2(self, STRUC2):
            print 'Deprecated: Use G.STRUC1.add_polis()'
            if isinstance(STRUC2,list):
                for el in STRUC2:
                    self.STRUC2 += [el]
            else:    
                self.STRUC2 += [STRUC2]
                
        def add_EBL(self, EBL):
            print 'Deprecated: Use G.STRUC1.add_polis()'
            if isinstance(EBL,list):
                for el in EBL:
                    self.EBL += [el.intersection(g) for g in self.G0]
                    #self.EBL += [el.union(g) for g in self.GROUND]
            else:    
                el = EBL
                self.EBL += [el.intersection(g) for g in self.G0]
                
        def add_EBL_list(self, EBLlist):
            self.EBL = EBLlist
            
        def add_GROUND_list(self, GROUNDlist):
            self.GROUND = GROUNDlist
            
        def add_STRUC_list(self, STRUClist):
            self.STRUCTURES = STRUClist
            
    '''
    
    def add_GROUND_list(self, GROUNDlist):
        self.GROUND = GROUNDlist
            
    def add_layer(self,polylist,name):
        setattr(self, name, LAYER(polylist,name))
        self.layers[name]=LAYER(polylist,name)
        
    def add_shapes(self,LIST_OF_BRANDNEWSTRUCTURES):
    
        LIST = LIST_OF_BRANDNEWSTRUCTURES
        
        for BNS in LIST: 
            # check out the layers contained in the BNS, add them to the groundplane
            """
            if 'BOUNDARY' in BNS.layers.keys():
                layername = 'BOUNDARY'
                LL = getattr(BNS,layername)
                polys = LL.POLIS
                
                boundarypolys = polys#BNS.get_polis_from_layer('BOUNDARY')
                for el in boundarypolys:
                    self.add_diff_groundplane(el)"""
            
            for layername in list(BNS.layers.keys()):
                LL = getattr(BNS,layername)
                polys = LL.POLIS#get_polis_from_layer(layername)
                
                if layername != 'BOUNDARY':
                
                    #if overlap_only: polys = array([self.get_intersections_groundplane(poly) for poly in polys]).flatten()
                    
                    if layername in list(self.layers.keys()):
                        L = getattr(self,layername)
                        L.add_polis(polys)
                    else:
                        self.add_layer(polys,layername)
                        
                elif layername == 'BOUNDARY':
                    boundarypolys = polys#BNS.get_polis_from_layer('BOUNDARY')
                    for el in boundarypolys:
                        self.add_diff_groundplane(el)
                    
                """         
                else:

                    boundarypolys = polys#BNS.get_polis_from_layer('BOUNDARY')
                    for el in boundarypolys:
                        self.add_diff_groundplane(el)
                """
                        
    def get_polis_from_layer(self,layername):
        """ Do not use, use instead get_polygons()"""
        return self.layers[layername].get_polis()
             
    def get_polygons(self,layername=None):
        if layername:
            L = getattr(self,layername)
            polys = L.get_polis()
        else: 
            GR = list(self.GROUND)
            L = getattr(self, 'STRUCTURE')
            SR = L.get_polis() #self.get_polis_from_layer('STRUCTURE')
            polys = GR + SR
        return polys
        
    def get_ankers(self):
        for name in list(self.layers.keys()):
            L = getattr(self,name)
            ankers = L.ANKERS
            for a in list(ankers.keys()):
                self.ANKERS[a] = L.ANKERS[a]
        return self.ANKERS
        
    def show_info(self):
        print('so new')
        showPolygons(list(self.GROUND),['blue']*len(self.GROUND))
        colormap = plt.cm.rainbow
        colors = [colormap(i) for i in np.linspace(0.0, 1.0, 1+len(list(self.layers.keys())))]
        for j,k in enumerate(self.layers.keys()):
            polys = self.get_polygons(k)#self.layers[k].get_polis()
            if len(polys):
                gca().add_patch(PolygonPatch(empty(),fc=colors[j],alpha=0.85,label=k))
            showPolygons(polys,[colors[j]]*len(polys))
        ankers = self.get_ankers()
        for a in list(ankers.keys()):
            plot(ankers[a][0],ankers[a][1],'o',label=a)
        #legend()

    def get_groundpolys(self):
        GR = [GS for GS in self.GROUND]
        return GR
        
    def get_strucpolys(self):
        SR = [S for S in hstack([cascaded_union(self.STRUCTURES)])]
        return SR

    def get_struc1(self):
        SR = [S for S in hstack([cascaded_union(self.STRUC1)])]
        return SR

    def get_struc2(self):
        SR = [S for S in hstack([cascaded_union(self.STRUC2)])]
        return SR

    def get_ebl(self):
        SR = [S for S in hstack([cascaded_union(self.EBL)])]
        return SR

    def make_copy(self):
        G = GROUNDPLANE(self.DX, self.DY)
        for k in list(self.ANKERS.keys()):
            G.add_anker(self.ANKERS[k], k)
        G.add_GROUND_list(self.get_groundpolys())
        for k in list(self.layers.keys()):
            L = getattr(self,k)
            G.add_layer(L.get_polis(),k)
            Slayer = getattr(G,k)
            ankers = L.ANKERS
            for a in list(ankers.keys()):
                Slayer.add_anker(ankers[a],a)
        return G