"""Restricted reader for numeric NumPy pickle datasets, not model checkpoints."""
import pickle
import numpy as np


class NumpyUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        allowed = {
            ('numpy', 'ndarray'): np.ndarray,
            ('numpy', 'dtype'): np.dtype,
            ('numpy.core.multiarray', '_reconstruct'): np._core.multiarray._reconstruct,
            ('numpy._core.multiarray', '_reconstruct'): np._core.multiarray._reconstruct,
            ('numpy.core.multiarray', 'scalar'): np._core.multiarray.scalar,
            ('numpy._core.multiarray', 'scalar'): np._core.multiarray.scalar,
        }
        if (module, name) not in allowed:
            raise pickle.UnpicklingError(f'Unsupported pickle global: {module}.{name}')
        return allowed[module, name]


def load_numeric_pickle(path):
    # Restricts code globals; it is not a resource-limit sandbox.
    with open(path, 'rb') as stream:
        return NumpyUnpickler(stream).load()
