from utils.vec import Vec2D


class Grid2D:
    """Automatically generates a dictionary grid (possibly sparse) from a 2D string"""

    def __init__(self, layout: str, relevant: callable = None):
        """Creates a grid from a 2D string with an optional functin to filter out relevant characters."""
        self.m_data = dict()
        self.m_maxx = 0
        self.m_maxy = 0
        for yidx, line in enumerate(layout.splitlines()):
            self.m_maxy = max(self.m_maxy, yidx)
            for xidx, ch in enumerate(line):
                self.m_maxx = max(xidx, self.m_maxx)
                if relevant is None or relevant(ch):
                    self.m_data[(xidx, yidx)] = ch

    @property
    def max_x(self) -> int:
        """Largest x in the grid (not necessarily populated if filtering)"""
        return self.m_maxx

    @property
    def max_y(self):
        """Largest y in the grid (not necessarily populated if filtering)"""
        return self.max_y

    def __getitem__(self, key: tuple | Vec2D):
        """Indexing support for grid, works with tuple or Vec2D"""
        return self.get(key)

    def get(self, key: tuple | Vec2D, default: str = None):
        """Indexing with optional default"""
        if not isinstance(key, tuple):
            key = key.as_tuple()
        if key not in self.m_data and default is not None:
            return default
        return self.m_data[key]

    def items(self, filter=lambda ch, pos: True):
        """Iterates through all present positions, yielding pos, character pairs"""
        for pos, ch in self.m_data.items():
            if filter(ch, pos):
                yield Vec2D(pos[0], pos[1]), ch
