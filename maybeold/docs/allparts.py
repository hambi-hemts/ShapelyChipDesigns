
#from brandnew_structure import *
from ShapelyChipDesigns.brandnew_structure import *
from collections import OrderedDict
from collections import Counter
import os

class ListTable(list):
    """ Overridden list class which takes a 2-dimensional list of 
        the form [[1,2,3],[4,5,6]], and renders an HTML Table in 
        IPython Notebook. """
    
    def _repr_html_(self):
        html = ["<table>"]
        for row in self:
            html.append("<tr>")
            
            for col in row:
                html.append("<td>{0}</td>".format(col))
            
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)
    
def make_table(column1,*kwargs):
    table = ListTable()
    f0 = column1
    for i,f in enumerate(f0):
        tba = [x[i] for x in kwargs]
        table.append([f0[i]]+tba)
    return table

# To join all parts together, pass the list of parts. 
# If an anker name is the same the two parts will be joined.
# Copies will be made if needed.
# For debug the list of passed parts together with their anker points
# is shown.

class all_parts:
    """ no doc:"""
    def __init__(self, glob):
        self.D = OrderedDict({})
        self.I = OrderedDict({})
        self.joined = OrderedDict({})
        self.g = glob
        
    def get_part_from_list(self, name, list):
        g = list
        name1 = name
        if g ==None:
            part1 = eval(name1)
        if name1[-1] == ']':
            NAME = name1.replace(']','')
            nameP0, nameP1  = NAME.split('[')
            part1 = g[nameP0][int(nameP1)]
        else: 
            part1 = g[name1]
            
        return part1 
        
    def add_part(self, name):
        P = self.get_part_from_list(name, self.g)
        self.D[name] = P
        
    def get_part_table(self):
        
        parts = self.D.keys()
        
        ankers = [getattr(part, 'ANKERS').keys() 
                  for part in self.D.values()]
        
        t = make_table(parts, 
                       ankers)
        return t
    
    def join_parts(self, name1, name2, anker12):
        ''' the name2 part will be translated to the position of the
        name1 part. 
        anker12 = [name of anker1, name of anker2]'''
        
        part1 = self.get_part_from_list(name1, self.g)
        part2 = self.get_part_from_list(name2, self.g)
        
        # check if parts are in part-list
        for name in [name1, name2]:
            if name in self.D.keys():
                pass
            else: 
                self.add_part(name, self.g)

        if anker12[0] in getattr(part1, 'ANKERS').keys():
            AP1 = getattr(part1, 'ANKERS')[anker12[0]]
        else:
            AP1 = [0,0]
            print "anker12[0] not in getattr(part1, 'ANKERS').keys()"
            print "partname = ", name1
            print "ankername = ", anker12[0]
            
        if anker12[1] in getattr(part2, 'ANKERS').keys():
            AP2 = getattr(part2, 'ANKERS')[anker12[1]]
        else:
            AP2 = [0,0]
            print "anker12[1] not in getattr(part2, 'ANKERS').keys()"
            print "partname = ", name2
            print "ankername = ", anker12[1]
            
        self.joined[name1+', '+name2] = anker12
        
        part2.translate(AP1, AP2)
        
        # check if translated: 
        AP1 = getattr(part1, 'ANKERS')[anker12[0]] 
        AP2 = getattr(part2, 'ANKERS')[anker12[1]]
        
        if AP1 != AP2:
            self.join_parts(name1, name2, anker12, self.g)
        
    def update_joined_parts(self):
        ''' update all joined parts to new locations '''
        for i, k in enumerate(self.joined.keys()):
            k1, k2 = self.joined.keys()[i].split(', ')
            V = self.joined[self.joined.keys()[i]]
            #print k1, k2, V
            self.join_parts(k1, k2, V, self.g)
        
    def update_glob(self, new_glob):
        self.g = new_glob
        
    def get_joined_table(self):
        t = make_table(self.joined.keys(), 
               self.joined.values())
        return t
    
    def add_info(self, partname, info):
        if partname in self.I.keys():
            self.I[partname] += '<br>'+info
        else: 
            self.I[partname] = info
    
    def get_info_table(self):
        t = make_table(self.I.keys(), 
                       self.I.values())
        return t