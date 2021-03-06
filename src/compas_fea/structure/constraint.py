
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'TieConstraint'
]


class TieConstraint(object):

    """ Tie constraint between two sets of nodes, elements or surfaces.

    Parameters
    ----------
    name : str
        TieConstraint name.
    master : str
        Master set name.
    slave : str
        Slave set name.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Returns
    -------
    None

    """

    def __init__(self, name, master, slave, tol):
        self.__name__ = 'TieConstraint'
        self.name = name
        self.master = master
        self.slave = slave
        self.tol = tol
