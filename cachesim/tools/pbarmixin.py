from tqdm import tqdm

from cachesim.tools.reader import Reader


class PBarMixIn:
    """
    Integrates a progress bar to keep track of the simulation.
    """

    def __init__(self, desc: str = None, **kwargs):
        super().__init__(**kwargs)
        self._desc = desc if desc is not None else self.__class__.__name__

    def map(self, reader: Reader):
        return super().map(tqdm(reader, desc=self._desc, total=reader.count))
