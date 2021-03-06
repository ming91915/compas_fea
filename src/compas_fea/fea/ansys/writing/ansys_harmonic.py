import os
from .ansys_nodes_elements import write_constraint_nodes
from .ansys_nodes_elements import write_nodes
from .ansys_nodes_elements import write_elements
from .ansys_materials import write_all_materials
from .ansys_loads import write_loads
from compas_fea.fea.ansys.writing.ansys_process import *
from compas_fea.fea.ansys.writing.ansys_steps import *
from compas_fea.fea.ansys.writing.ansys_nodes_elements import *

__author__ = ['Tomas Mendez Echenagucia <mendez@arch.ethz.ch>']
__copyright__ = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'mendez@arch.ethz.ch'


def write_harmonic_analysis_request(structure, path, name, skey):
    # displacements = structure.steps[skey].displacements
    # factor = structure.steps[skey].factor
    # loads = structure.steps[skey].loads
    # ansys_open_post_process(output_path, filename)
    # write_all_materials(structure, output_path, filename)
    # write_nodes(structure, output_path, filename)
    # write_elements(structure, output_path, filename)
    # write_constraint_nodes(structure, output_path, filename, displacements)
    # write_loads(structure, output_path, filename, loads, factor)
    # write_harmonic_solve(structure, output_path, filename, skey)
    # write_request_element_nodes(output_path, filename)
    # write_harmonic_post_process(output_path, filename)
    # write_request_per_freq_nodal_displacements(structure, output_path, filename, skey)

    filename = name + '.txt'
    ansys_open_pre_process(path, filename)
    write_all_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    for skey in structure.steps_order:
        if structure.steps[skey].type == 'harmonic':
            displacements = structure.steps[skey].displacements
            factor = structure.steps[skey].factor
            loads = structure.steps[skey].loads
            write_harmonic_solve(structure, path, filename, skey)
            write_loads(structure, path, filename, loads, factor)
            write_constraint_nodes(structure, path, filename, displacements)
            write_request_load_step_file(structure, path, filename)
    write_request_solve_steps(structure, path, filename)


def write_harmonic_solve(structure, output_path, filename, skey):
    freq_range = structure.steps[skey].freq_range
    freq_steps = structure.steps[skey].freq_steps
    harmonic_damping = structure.steps[skey].damping

    cFile = open(output_path + "/" + filename, 'a')
    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('FINISH \n')
    cFile.write('/SOLU \n')
    cFile.write('ANTYPE,3            ! Harmonic analysis \n')
    cFile.write('HARFRQ,' + str(freq_range[0]) + ',' + str(freq_range[1]) + ',           ! Frequency range \n')
    cFile.write('NSUBST,' + str(freq_steps) + ',             ! Number of frequency steps \n')
    cFile.write('KBC,1                ! Stepped loads \n')

    if harmonic_damping:
        # cFile.write('ALPHAD,'+ str(harmonic_damping)+'   ! mass matrix multiplier for damping \n')
        cFile.write('BETAD,' + str(harmonic_damping) + '   ! stiffness matrix multiplier for damping \n')
        # cFile.write('DMPRAT,' + str(harmonic_damping) + '   ! constant modal damping ratio \n')

    # cFile.write('SOLVE \n')
    # cFile.write('FINISH \n')
    # cFile.write('!\n')
    # cFile.write('!\n')
    cFile.close()


def write_harmonic_results_from_ansys_rst(name, path, fields, freq_steps, step_index=0, step_name='step'):

    if not os.path.exists(path + name + '_output/harmonic_out/'):
        os.makedirs(path + name + '_output/harmonic_out/')

    # write_harmonic_post_process(path, name)

    if type(fields) == str:
        fields = [fields]
    if 'u' in fields or 'all' in fields:
        write_request_per_freq_nodal_displacements(path, name, freq_steps)
        # write_something(path, name)
    if 'geo' in fields or 'all' in fields:
        write_request_element_nodes(path, name)


def write_something(path, name):
    out_path = path + '/' + name + '_output/'
    filename = name + '_extract.txt'

    cFile = open(path + "/" + filename , 'a')
    cFile.write('!\n')
    cFile.write('/SOL \n')
    cFile.write('*cfopen,' + out_path + 'harmonic_out/something,txt \n')
    cFile.write('*vwrite, \'something\', \'something\', \'dark side...\' \n')
    cFile.write('(A, A, A,) \n')
    cFile.write('*cfclose \n')
    cFile.write('!\n')
    cFile.close()


def write_harmonic_post_process(path, name):
    filename = name + '_extract.txt'
    cFile = open(path + '/' + filename, 'a')
    cFile.write('/POST26 \n')
    cFile.write('PRCPLX, 0 \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_request_per_freq_nodal_displacements(path, name, freq_steps):
    filename = name + '_extract.txt'
    harmonic_outpath = path + '/' + name + '_output/harmonic_out/'

    cFile = open(path + '/' + filename, 'a')
    cFile.write('/POST1 \n')
    cFile.write('Set, FIRST, \n')
    cFile.write('*get,num_n,NODE,0,COUNT ! get number of nodes \n')
    cFile.write('*get,n_min,NODE,0,NUM,MIN ! get min node number \n')

    cFile.write('/POST26 \n')
    cFile.write('PRCPLX, 0 \n')
    cFile.write('!\n')
    cFile.write('!\n')

    cFile.write('*do,i,1,num_n,1   ! output to ascii by looping over nodes \n')
    cFile.write('curr_n=n_min \n')
    cFile.write('nsol,2,curr_n,u,x ! output UX \n')
    cFile.write('nsol,3,curr_n,u,y ! output UY \n')
    cFile.write('nsol,4,curr_n,u,z ! output UZ \n')

    cFile.write('*dim,N%curr_n%_output,array,' + str(freq_steps) + ',7 \n')

    cFile.write('vget,N%curr_n%_output(1,1),1 ! put time in array \n')
    cFile.write('vget,N%curr_n%_output(1,2),2,,0 ! put UX in array \n')
    cFile.write('vget,N%curr_n%_output(1,3),3,,0 ! put UY in array \n')
    cFile.write('vget,N%curr_n%_output(1,4),4,,0 ! put UZ in array \n')

    cFile.write('vget,N%curr_n%_output(1,5),2,,1 ! put UX in array \n')
    cFile.write('vget,N%curr_n%_output(1,6),3,,1 ! put UY in array \n')
    cFile.write('vget,N%curr_n%_output(1,7),4,,1 ! put UZ in array \n')

    cFile.write('*cfopen,' + harmonic_outpath + '/node_real_%curr_n%,txt \n')
    cFile.write('*vwrite,N%curr_n%_output(1,1),\',\' ,N%curr_n%_output(1,2),\',\' ,')
    cFile.write('N%curr_n%_output(1,3),\',\' ,N%curr_n%_output(1,4) \n')
    cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
    cFile.write('*cfclose\n')

    cFile.write('*cfopen,' + harmonic_outpath + '/node_imag_%curr_n%,txt \n')
    cFile.write('*vwrite,N%curr_n%_output(1,1),\',\' ,N%curr_n%_output(1,5),\',\' ')
    cFile.write(' ,N%curr_n%_output(1,6),\',\' ,N%curr_n%_output(1,7)\n')
    cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
    cFile.write('*cfclose\n')

    cFile.write('*get,n_min,NODE,curr_n,NXTH \n')
    cFile.write('*enddo \n')
    cFile.close()
