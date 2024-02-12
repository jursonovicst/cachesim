from typing import Iterable

from tqdm import tqdm


class PBarMixIn:
    """
    Integrates a progress bar to keep track of the simulation.
    """

    def map(self, reader: Iterable, desc=None, total=None):
        return super().map(tqdm(reader, desc=desc, total=total))
