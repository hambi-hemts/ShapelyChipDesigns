
Introduction
============

.. raw:: html

   <ol>

.. raw:: html

   <li>

Make one or more BRANDNEWSTRUCTUREs

.. raw:: html

   </li>

.. raw:: html

   <li>

Give them ANKER-points

.. raw:: html

   </li>

.. raw:: html

   <li>

Use all\_parts to attach them to each other and generate a documentation

.. raw:: html

   </li>

.. raw:: html

   <li>

Add everything to a GROUNDPLANE

.. raw:: html

   </li>

.. raw:: html

   <li>

Export to dxf

.. raw:: html

   </li>

.. raw:: html

   </ol>

.. code:: python

    import imp, os.path, sys
    
    sys.path.insert(0, "E:\\IPython2\\141007 Sphinx and ShapelyChipDesigns\\try4\\src")
    
    def import_(filename):
        path, name = os.path.split(filename)
        name, ext = os.path.splitext(name)
    
        print 'Before: %s in sys.modules ==' % name, name in sys.modules
        file, filename, data = imp.find_module(name, [path])
        print path
        mod = imp.load_module(name, file, filename, data)
        print 'After: %s in sys.modules ==' % name, name in sys.modules
        return mod
    
    rePath = imp.find_module('ShapelyChipDesigns')[1]
    SD = import_(rePath)
    SD.__file__

.. parsed-literal::

    Before: ShapelyChipDesigns in sys.modules == False
    E:\IPython2\141007 Sphinx and ShapelyChipDesigns\try4\src
    After: ShapelyChipDesigns in sys.modules == True
    

.. parsed-literal::

    C:\Python27\lib\site-packages\IPython\lib\kernel.py:8: DeprecationWarning: IPython.lib.kernel moved to IPython.kernel.connect in IPython 1.0
      DeprecationWarning
    



.. parsed-literal::

    'E:\\IPython2\\141007 Sphinx and ShapelyChipDesigns\\try4\\src\\ShapelyChipDesigns\\__init__.pyc'



.. code:: python

    # import the ShapelyChipDesigns package: 
    #import ShapelyChipDesigns as SD
    
    # import packages for plotting:
    from matplotlib import pyplot as plt
    %pylab inline

.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib
    

.. code:: python

    name = 'Introduction'#SD.NotebookName()
    #name = name.replace('.ipynb', '')
    print name

.. parsed-literal::

    Introduction
    

Make one or more BRANDNEWSTRUCTUREs
-----------------------------------

.. code:: python

    # make two circles: 
    
    radius1 = 2
    radius2 = 1.5
    radius3 = 0.5
    radius4 = radius3
    
        # they are centered at [0,0]:
    point  = SD.Point([0,0])
    circle1 = point.buffer(radius1)
    circle2 = point.buffer(radius2)
    
    circle3 = point.buffer(radius3)
    circle4 = point.buffer(radius4)
    circle3 = SD.translate(circle3, 2, 2)
    circle4 = SD.translate(circle4, -2, 2)
    
    # and an important point:
    
    a_dot = [0, radius2]
.. code:: python

    title('parts for a BRAND_NEW_STRUCTURE')
    
    bx = -1
    annotate(
        'BOUNDARY',
        xy=(2, 2), arrowprops=dict(arrowstyle='->'), xytext=(bx, 3))
    
    annotate(
        '',
        xy=(0, radius1-0.05*radius1), arrowprops=dict(arrowstyle='->'), xytext=(bx, 3))
    
    annotate(
        '',
        xy=(-2, 2), arrowprops=dict(arrowstyle='->'), xytext=(bx, 3))
    
    annotate(
        'STRUCTURE',
        xy=(0, radius2-0.9*radius2), arrowprops=dict(arrowstyle='->'), xytext=(-4, -2))
    
    SD.showPolygons([circle1, circle3, circle4, circle2])
    
    plot(a_dot[0], a_dot[1], 'o', label='some anker point')
    
    legend(loc=3)
    gca().set_ylim(-2*radius1, 2*radius1)
    savefig('images/'+name+'_fig00.png')


.. image:: Introduction_files/Introduction_7_0.png


.. code:: python

    C = SD.BRAND_NEW_STRUCTURE([circle1, circle3, circle4], circle2)
    C.add_anker(a_dot, 'some anker point')
    C.add_anker([0, 0], 'a center')
    C.show_info()

.. parsed-literal::

    {'a center': [0, 0], 'some anker point': [0, 1.5]}
    


.. image:: Introduction_files/Introduction_8_1.png


.. code:: python

    title('scale, rotate and translate')
    
    myCs = []
    
    for i in arange(10):
        
        Ccopy = C.make_copy()
        Ccopy.rotate(i*20, [0, 0])
        Ccopy.scale(1-i*0.05, 1-i*0.05, [0, 0])
        Ccopy.translate([(10-i*0.5)*cos(i*2*pi/10.), (10-i*0.5)*sin(i*2*pi/10.)], [0, 0])
        
        myCs += [Ccopy]
        
        SD.showPolygons(Ccopy.get_polygons())
        
        the_dot = Ccopy.get_ankers()['some anker point']
        plot(the_dot[0], the_dot[1], 'o', color='blue')
        
        if i == 5:
            C4 = Ccopy.make_copy()
            
    savefig('images/'+name+'_fig01.png')


.. image:: Introduction_files/Introduction_9_0.png


.. code:: python

    G = SD.GROUNDPLANE(40, 25, -15, -10)
    
    G.add_shapes(myCs)
    G.show_info()


.. image:: Introduction_files/Introduction_10_0.png


.. code:: python

    SD.savedxf_polylist(G.get_polygons(), 'dxf/Introduction_00')

.. parsed-literal::

    saved dxf/Introduction_00.dxf
    

.. code:: python

    SD.convert('dxf/Introduction_00.dxf', 'dxf/Introduction_00.dxf')
.. code:: python

    R = 3
    w1, w2 = 0.75, 0.5
    phis = linspace(1.5*pi, 2*pi)
    
    x, y = R*cos(phis), R*sin(phis)
.. code:: python

    ls = SD.LineString(zip(x, y))
    
    L = SD.BRAND_NEW_STRUCTURE(ls.buffer(w1, cap_style = 2), 
                               ls.buffer(w2, cap_style = 2))
    
    L.add_anker([0, -R], 'attach me')
    
    L.show_info()

.. parsed-literal::

    {'attach me': [0, -3]}
    


.. image:: Introduction_files/Introduction_14_1.png


.. code:: python

    import os
    def reload_rm(module_name):
        os.system('rm ' + str(module_name) + '.pyc')
        reload(module_name)
.. code:: python

    reload_rm(SD)
.. code:: python

    parts = SD.all_parts(globals())
.. code:: python

    parts.join_parts('C4', 'L', ['a center', 'attach me'])

.. parsed-literal::

    I am so new!
    

.. code:: python

    parts.update_joined_parts()
    for S in parts.D.values():
        SD.showPolygons(S.get_polygons())

::


    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)

    <ipython-input-18-bca82154b0cc> in <module>()
    ----> 1 parts.update_joined_parts()
          2 for S in parts.D.values():
          3     SD.showPolygons(S.get_polygons())
    

    E:\IPython2\141007 Sphinx and ShapelyChipDesigns\try4\src\ShapelyChipDesigns\allparts.py in update_joined_parts(self)
        124             V = self.joined[self.joined.keys()[i]]
        125             #print k1, k2, V
    --> 126             self.join_parts(k1, k2, V, self.g)
        127 
        128     def update_glob(self, new_glob):
    

    TypeError: join_parts() takes exactly 4 arguments (5 given)



.. code:: python

    BOUNDARY =list(flatten([C4.get_polygons('BOUNDARY'), 
                               L.get_polygons('BOUNDARY')[0]])) #SD.unary_union(list(flatten([C4.get_polygons('BOUNDARY'), L.get_polygons('BOUNDARY')[0]])))
    
    STRUCTURE = SD.unary_union([C4.get_polygons('STRUCTURE')[0], 
                               L.get_polygons('STRUCTURE')[0]])
    
    SD.showPolygons(BOUNDARY+[STRUCTURE])
.. code:: python

    title('new structure and added layers')
    NEWER = SD.BRAND_NEW_STRUCTURE(BOUNDARY, STRUCTURE)
    Cadd = SD.Point(-1, 3).buffer(1)
    NEWER.add_layer([Cadd], 'added layer')
    NEWER.show_info()
.. code:: python

    G = SD.GROUNDPLANE(15, 15, -12, -4)
    G.add_shapes([NEWER])
    G.show_info()
.. code:: python

    SD.showPolygons(G.get_groundpolys())
.. code:: python

    SD.NotebookName()
.. code:: python

    !ipython nbconvert Introduction.ipynb --to rst
.. code:: python

    f = open('Introduction.rst', 'r')
    content = f.read()
    f.close()
    content = content.replace('/','/')
    
    f = open('Introduction.rst', 'w')
    f.write(content)
    f.close()
