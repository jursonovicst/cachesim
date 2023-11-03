from tqdm import tqdm
from cachesim import Cache
from cachesim.tools.reader import Reader


class PBarMixIn:
    """
    Integrates a progress bar to keep track of the simulation.
    """

    def map(self, reader: Reader):
        assert isinstance(self, Cache), f"Works only with Cache"
        return super().map(tqdm(reader, desc=self.__class__.__name__, total=reader.count))
