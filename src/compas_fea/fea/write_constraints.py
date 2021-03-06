
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'write_input_constraints',
]


comments = {
    'abaqus':   '**',
    'opensees': '#',
    'sofistik': '$',
    'ansys':    '!',
}


def write_input_constraints(f, software, constraints):

    """ Writes the constraints information to the input file.

    Parameters
    ----------
    f : obj
        The open file object for the input file.
    software : str
        Analysis software or library to use, 'abaqus', 'opensees', 'sofistik' or 'ansys'.
    constraints : dic
        Constraint dictionary from structure.constraints.

    Returns
    -------
    None

    """

    c = comments[software]

    f.write('{0} -----------------------------------------------------------------------------\n'.format(c))
    f.write('{0} ----------------------------------------------------------------- Constraints\n'.format(c))
    f.write('{0}\n'.format(c))

    for key, constraint in constraints.items():

        ctype = constraint.__name__

        f.write('{0} {1}\n'.format(c, key))
        f.write('{0} '.format(c) + '-' * len(key) + '\n')
        f.write('{0}\n'.format(c))

        # Tie constraint

        if ctype == 'TieConstraint':

            tol    = constraint.tol
            slave  = constraint.slave
            master = constraint.master

            if software == 'abaqus':

                f.write('*TIE, POSITION TOLERANCE={0}, NAME={1}, ADJUST=NO\n'.format(tol, key))
                f.write('** SLAVE, MASTER\n')
                f.write('{0}, {1}\n'.format(slave, master))

            elif software == 'opensees':

                pass

            elif software == 'sofistik':

                pass

            elif software == 'ansys':

                pass

        f.write('{0}\n'.format(c))

    f.write('{0}\n'.format(c))
