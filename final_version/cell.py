class Cell:
    def __init__(self, type="empty", unit=None):
        self.type = type  # "empty", "water", "lava", "rock", etc.
        self.unit = unit  # Reference to a Unit or None

    def __str__(self):
        return self.type
