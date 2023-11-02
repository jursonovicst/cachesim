from tqdm import tqdm

from cachesim import Reader


class PBarMixIn:
    """
    Integrates a progress bar to keep track of the simulation.
    """

    def map(self, reader: Reader):
        return map(super()._recv, tqdm(reader, desc=self.__class__.__name__, total=reader.count))
