"""
.. _compas_fea.fea:

********************************************************************************
fea
********************************************************************************

.. module:: compas_fea.fea

The compas_fea package supports Abaqus, Ansys, Sofistik and OpenSees as analysis backends.


write_heading
=============

.. currentmodule:: compas_fea.fea.write_heading

:mod:`compas_fea.fea.write_heading`

.. autosummary::
    :toctree: generated/

    write_input_heading

write_constraints
=================

.. currentmodule:: compas_fea.fea.write_constraints

:mod:`compas_fea.fea.write_constraints`

.. autosummary::
    :toctree: generated/

    write_input_constraints

write_steps
===========

.. currentmodule:: compas_fea.fea.write_steps

:mod:`compas_fea.fea.write_steps`

.. autosummary::
    :toctree: generated/

    write_input_steps


write_elements
==============

.. currentmodule:: compas_fea.fea.write_elements

:mod:`compas_fea.fea.write_elements`

.. autosummary::
    :toctree: generated/

    write_input_elements


write_nodes
=============

.. currentmodule:: compas_fea.fea.write_nodes

:mod:`compas_fea.fea.write_nodes`

.. autosummary::
    :toctree: generated/

    write_input_nodes


write_bcs
=========

.. currentmodule:: compas_fea.fea.write_bcs

:mod:`compas_fea.fea.write_bcs`

.. autosummary::
    :toctree: generated/

    write_input_bcs


write_materials
===============

.. currentmodule:: compas_fea.fea.write_materials

:mod:`compas_fea.fea.write_materials`

.. autosummary::
    :toctree: generated/

    write_input_materials


write_misc
==========

.. currentmodule:: compas_fea.fea.write_misc

:mod:`compas_fea.fea.write_misc`

.. autosummary::
    :toctree: generated/

    write_input_misc


abaq
====

.. currentmodule:: compas_fea.fea.abaq

:mod:`compas_fea.fea.abaq`

.. autosummary::
    :toctree: generated/

    abaqus_launch_process
    extract_odb_data
    input_generate


ansys
=====

.. currentmodule:: compas_fea.fea.ansys

:mod:`compas_fea.fea.ansys`

.. autosummary::
    :toctree: generated/

    input_generate
    make_command_file_static
    make_command_file_modal
    make_command_file_harmonic
    ansys_launch_process
    ansys_launch_process_extract
    delete_result_files
    extract_rst_data
    write_results_from_rst
    load_to_results


opensees
========

.. currentmodule:: compas_fea.fea.opensees

:mod:`compas_fea.fea.opensees`

.. autosummary::
    :toctree: generated/

    input_generate
    opensees_launch_process


sofistik
========

.. currentmodule:: compas_fea.fea.sofistik

:mod:`compas_fea.fea.sofistik`

.. autosummary::
    :toctree: generated/

    input_generate

"""

from .write_heading import *
from .write_constraints import *
from .write_nodes import *
from .write_bcs import *
from .write_materials import *
from .write_elements import *
from .write_steps import *
from .write_misc import *
