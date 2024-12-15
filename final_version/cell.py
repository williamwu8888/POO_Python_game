class Cell:
    def __init__(self, type="empty", unit=None):
        self.type = type  # "empty", "water", "lava", "rock", etc.
        self.unit = unit  # Reference to a Unit or None
        self.traversable = True
        self.traversable_for_knight = False  # Ajout explicite pour les chevaliers

    def __str__(self):
        return self.type
