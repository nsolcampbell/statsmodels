"""
This module provides various regression analysis techniques to model the
relationship between the dependent and independent variables.
"""

__docformat__ = 'restructuredtext'

import os

import numpy as N

from neuroimaging.core.api import Image

class LinearModelIterator(object):
    """
    TODO
    """

    def __init__(self, iterator, outputs=()):
        """
        :Parameters:
            iterator : TODO
                TODO
            outputs : TODO
                TODO
        """
        self.iterator = iter(iterator)
        self.outputs = [iter(output) for output in outputs]


    def model(self):
        """
        This method should take the iterator at its current state and
        return a LinearModel object.

        :Returns: ``None``
        """
        return None

    def fit(self):
        """
        Go through an iterator, instantiating model and passing data,
        going through outputs.

        :Returns: ``None``
        """

        for data in self.iterator:
            shape = data.shape[1:]
            data = data.reshape(data.shape[0], N.product(shape))

            results = self.model().fit(data)
            for output in self.outputs:
                out = output.extract(results)
                if output.nout > 1:
                    out.shape = (output.nout,) + shape
                else:
                    out.shape = shape

                output.set_next(data=out)


class RegressionOutput(object):

    """
    A generic output for regression. Key feature is that it has
    an \'extract\' method which is called on an instance of
    Results.
    """

    def __init__(self, grid, nout=1, outgrid=None):
        """
        :Parameters:
            grid : TODO
                TODO
            nout : ``int``
                TODO
            outgrid : TODO
                TODO
        """
        self.grid = grid
        self.nout = nout
        if outgrid is not None:
            self.outgrid = outgrid
        else:
            self.outgrid = grid
        self.img = NotImplemented
        self.it = NotImplemented

    def __iter__(self):
        """
        :Returns: ``self``
        """
        iter(self.it)
        return self

    def next(self):
        """
        :Returns: TODO
        """
        return self.it.next()

    def set_next(self, data):
        """
        :Parameters:
            data : TODO
                TODO

        :Returns: ``None``
        """
        self.it.next().set(data)

    def extract(self, results):
        """
        :Parameters:
            results : TODO
                TODO

        :Returns: ``None``

        :Raises: NotImplementedError
        """
        raise NotImplementedError

    def _setup_img(self, clobber, outdir, ext, basename):
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        outname = os.path.join(outdir, '%s%s' % (basename, ext))
        img = Image(outname, mode='w', grid=self.outgrid, clobber=clobber)
        if self.it is NotImplemented:
            it = img.slice_iterator('w')
        else:
            it = iter(self.it.copy(img))
        return img, it