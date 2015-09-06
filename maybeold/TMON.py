
########### Make the Transmon qubit ########

TBOUNDS = T#.get_polygons('BOUNDARY')
ISLAND,RESERVOIR= B.difference(TBOUNDS[0])

TMON = SD.BRAND_NEW_STRUCTURE(BB,[])
TMON.EBL.add_polis([RESERVOIR,ISLAND])

########### Ankers ############
P = TMON.BOUNDARY.POLIS
x,y = P[0].boundary.xy
inds = SD.find_vertex('top', x,y)
ytop = [y[i] for i in inds[0]]
ytop = mean(ytop)
xtop = [x[i] for i in inds[0]]
xtop = mean(xtop)

TMON.add_anker([xtop, ytop], 
               'Flux Line')

P = TMON.BOUNDARY.POLIS
x, y = P[0].centroid.xy
TMON.add_anker([x[0],y[0]], 
               'EBL markers')

xl, yl = SD.anker(TMON.BOUNDARY.POLIS[0],'lower_left')
TMON.add_anker([xl,yl], 
               'Resonator LL')

xl, yl = SD.anker(TMON.BOUNDARY.POLIS[0],'lower_right')
TMON.add_anker([xl,yl],
               'Resonator LR')

########## Plot ##############

SD.showPolygons(TMON.get_polygons()+TMON.get_polygons('EBL'))

for k in TMON.ANKERS.keys():
    x,y = TMON.ANKERS[k]
    plot(x,y,'o', markersize=5, label=str(k))

legend()
tight_layout()
grid()
#SD.mouseshow()