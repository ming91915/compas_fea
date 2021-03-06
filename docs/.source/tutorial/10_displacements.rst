********************************************************************************
Displacements
********************************************************************************

This page shows how **Displacement** objects are added to the **Structure** object, here given as a **Structure** named ``mdl``. **Displacement** objects can be used to describe boundary conditions or imposed displacements.

====================
Adding displacements
====================

**Displacement** objects are used to apply boundary conditions as well as impose movements directly at selected nodes. Along with **Load** objects, they form the main actions acting on a structure during the analysis when combined with **Step** objects. It is necessary for the first step in the **Structure** to be associated with the boundary condition **Displacement** objects that do not change throughout the analysis. The following example shows how a **PinnedDisplacement** class is first imported, an object instantiated and then added to the dictionary ``.displacements`` of the **Structure** object. All **Displacement** objects currently use only the global co-ordinate system with ``axes='global'``, this will be improved later with the use of the local nodal system.

.. code-block:: python

    from compas_fea.structure import PinnedDisplacement

    mdl.add_displacement(PinnedDisplacement(name='disp_pinned', nodes='nset_base'))


=======================
Accessing displacements
=======================

To access the data stored on a **Displacement** object, use its string key and view or edit its attributes as needed:

.. code-block:: python

   >>> mdl.displacements['disp_pinned'].components
   {'x': 0, 'y': 0, 'z': 0, 'xx': None, 'yy': None, 'zz': None}

   >>> mdl.displacements['disp_pinned'].nodes
   'nset_base'

The example **PinnedDisplacement** object above restrains translations in all directions but allows rotations about any axis, as indicated by the automatic assignment of zero for ``x``, ``y`` and ``z``, and ``None`` for ``xx``, ``yy`` and ``zz``. Non-zero values for any of the six components could be given to simulate support settlements or to perform a displacement controlled analysis.


=====
Types
=====

Different displacement types are available from the classes in **compas_fea.structure.displacement**, these are detailed below:

-------
General
-------

A **GeneralDisplacement** object is used for defining all six spatial translations and rotations, and so is the most general type of **Displacement** object. The object has components ``x``, ``y``, ``z``, ``xx``, ``yy`` and ``zz`` all equal to ``None`` by default, defined automatically unless given otherwise. The ``name`` of the object, and the nodes it should act on must both be given.

.. code-block:: python

   from compas_fea.structure import GeneralDisplacement

   mdl.add_displacement(GeneralDisplacement(name='disp_general', nodes='nset_base', x=0.1, zz=0.05, z=0))

------
Pinned
------

A **PinnedDisplacement** object is used for restraining all spatial translations, but still allows rotations to occur. The object has components ``x=y=z=0`` and ``xx=yy=zz=None``, which are all defined automatically. The ``name`` of the object, and the nodes it should act on must both be given.

.. code-block:: python

   from compas_fea.structure import PinnedDisplacement

   mdl.add_displacement(PinnedDisplacement(name='disp_pinned', nodes='nset_base'))

-----
Fixed
-----

A **FixedDisplacement** object is used for restraining all spatial translations and rotations. The object has components ``x=y=z=xx=yy=zz=0``, which are all defined automatically. The ``name`` of the object, and the nodes it should act on must both be given.

.. code-block:: python

   from compas_fea.structure import FixedDisplacement

   mdl.add_displacement(FixedDisplacement(name='disp_fixed', nodes='nset_base'))

There are additionally three other types of fixed **Displacement** objects, **FixedDisplacementXX**, **FixedDisplacementYY** and **FixedDisplacementZZ**, which all posses zero translations ``x=y=z=0`` but with the rotations fixed for the indicated axis. So, **FixedDisplacementXX** additionally clamps ``xx=0``, **FixedDisplacementYY** clamps ``yy=0`` and **FixedDisplacementZZ** ``zz=0``. These objects are created in the same way, for example like:

.. code-block:: python

   from compas_fea.structure import FixedDisplacementXX

   mdl.add_displacement(FixedDisplacementXX(name='disp_fixedxx', nodes='nset_base'))

-------
Rollers
-------

There are six types of roller displacement objects, **RollerDisplacementX**, **RollerDisplacementY**,   **RollerDisplacementZ**, **RollerDisplacementXY**, **RollerDisplacementYZ** and **RollerDisplacementXZ**. These are all based on a **PinnedDisplacement** object, with the indicated translational degrees-of-freedom(s) released.  So for example, **RollerDisplacementX** is released in `x` with ``x=None``, and so has ``y=z=0``, while **RollerDisplacementXY** is released in both `x` and `y` with ``x=y=None`` leaving only ``z=0``.

.. code-block:: python

   from compas_fea.structure import RollerDisplacementXY

   mdl.add_displacement(RollerDisplacementXY(name='disp_roller', nodes='nset_base'))
