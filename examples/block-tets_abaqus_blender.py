"""An example compas_fea package use for tetrahedron elements."""

from compas_fea.fea.abaq import abaq
from compas_fea.cad import blender

from compas_fea.structure import ElementProperties
from compas_fea.structure import GeneralStep
from compas_fea.structure import PinnedDisplacement
from compas_fea.structure import PointLoad
from compas_fea.structure import SolidSection
from compas_fea.structure import Steel
from compas_fea.structure import Structure

from compas.cad.blender.utilities import get_objects


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# Folders and Structure name

name = 'block-tets'
path = '/home/al/Temp/'

# Create an empty Structure object named mdl

mdl = Structure()

# Add tetrahedrons from bmesh

blender.add_tets_from_bmesh(mdl, name='elset_tets', bmesh=get_objects(layer=0)[0], draw_tets=False, volume=0.002)

# Add node sets to the Structure object

blender.add_nset_from_bmeshes(mdl, layer=1, name='nset_top')
blender.add_nset_from_bmeshes(mdl, layer=2, name='nset_bot')

# Add materials

mdl.add_material(Steel(name='mat_steel', fy=355))

# Add sections

mdl.add_section(SolidSection(name='sec_solid'))

# Add element properties

ep = ElementProperties(material='mat_steel', section='sec_solid', elsets='elset_tets')
mdl.add_element_properties(ep, name='ep_tets')

# Add loads

mdl.add_load(PointLoad(name='load_top', nodes='nset_top', y=1, z=1))

# Add displacements

mdl.add_displacement(PinnedDisplacement(name='disp_pinned', nodes='nset_bot'))

# Add steps

mdl.add_step(GeneralStep(name='step_bc', displacements=['disp_pinned']))
mdl.add_step(GeneralStep(name='step_loads', loads=['load_top']))
mdl.set_steps_order(['step_bc', 'step_loads'])

# Structure summary

mdl.summary()

# Generate .inp file

fnm = '{0}{1}.inp'.format(path, name)
abaq.inp_generate(mdl, filename=fnm)

# Run and extract data

exe = '/home/al/abaqus/Commands/abaqus cae '
mdl.analyse(path, name, software='abaqus', fields='U,S', exe=exe)

# Plot voxels

blender.plot_voxels(mdl, path, name, step='step_loads', vdx=0.02, cbar=[0, 300], cube_size=[10, 10, 20], layer=3)