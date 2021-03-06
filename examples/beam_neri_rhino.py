
from compas_fea.cad import rhino
from compas_fea.structure import ElasticIsotropic
from compas_fea.structure import ElementProperties as Properties
from compas_fea.structure import GeneralStep
from compas_fea.structure import GravityLoad
from compas_fea.structure import PinnedDisplacement
from compas_fea.structure import PipeSection
from compas_fea.structure import Structure

from compas_rhino.utilities import clear_layer

import rhinoscriptsyntax as rs


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


rs.EnableRedraw(False)

# Curves

ds = 0.05
lines = []
for i in range(2, 11):
    lid = 'lines-{0}'.format(i)
    lines.append(lid)
    rs.CurrentLayer(lid)
    clear_layer(lid)
    for curve in rs.ObjectsByLayer('curves-{0}'.format(i)):
        n = int(rs.CurveLength(curve) / ds)
        for i in range(n):
            sp = rs.CurveArcLengthPoint(curve, (i + 0) * ds)
            ep = rs.CurveArcLengthPoint(curve, (i + 1) * ds)
            rs.AddLine(sp, ep)
        rs.AddLine(ep, rs.CurveEndPoint(curve))

# Structure 

mdl = Structure(name='beam_neri', path='C:/Temp/')

# Beams

rhino.add_nodes_elements_from_layers(mdl, line_type='BeamElement', layers=lines)

# Materials

mdl.add_material(ElasticIsotropic(name='mat_asa', E=1.87*10**9, v=0.35, p=1050))

# Sctions

for i in range(2, 11):
    sname = 'sec_{0}'.format(i)
    ename = 'lines-{0}'.format(i)
    pname = 'ep_{0}'.format(i)
    mdl.add_section(PipeSection(name=sname, r=i/100, t=0.005))
    ep = Properties(name=pname, material='mat_asa', section=sname, elsets=ename)
    mdl.add_element_properties(ep)

# Displacements

rs.CurrentLayer('nset_pins')
clear_layer('nset_pins')
for nkey, node in mdl.nodes.items():
    if node['z'] < 0.001:
        rs.AddPoint(mdl.node_xyz(nkey))
rhino.add_sets_from_layers(mdl, layers=['nset_pins'])
mdl.add_displacement(PinnedDisplacement(name='disp_pins', nodes='nset_pins'))

# Loads

mdl.add_load(GravityLoad(name='load_gravity', elements=lines))

rs.EnableRedraw(True)

# Steps

mdl.add_steps([
    GeneralStep(name='step_bc', displacements=['disp_pins']),
    GeneralStep(name='step_load', loads=['load_gravity'], factor=1.2)])
mdl.steps_order = ['step_bc', 'step_load']

# Summary

mdl.summary()

# Run (Abaqus)

mdl.analyse_and_extract(software='abaqus', fields=['u', 's'])

rhino.plot_data(mdl, step='step_load', field='um', radius=0.02)
rhino.plot_data(mdl, step='step_load', field='smises', radius=0.02, nodal='max')
