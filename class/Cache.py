class Cache:
    def __init__(self):
        self.breakfast = None
        self.lunch = None
        self.dinner = None
        self.nextBreakfast = None
        self.nextLunch = None
        self.nextDinner = None

    def set_cache(self, name, value):
        if name == "breakfast":
            self.breakfast = value
        elif name == "lunch":
            self.lunch = value
        elif name == "dinner":
            self.dinner = value
        elif name == "nextBreakfast":
            self.nextBreakfast = value
        elif name == "nextLunch":
            self.nextLunch = value
        elif name == "nextDinner":
            self.nextDinner = value

    def get_cache(self, name):
        if name == "breakfast":
            return self.breakfast
        elif name == "lunch":
            return self.lunch
        elif name == "dinner":
            return self.dinner
        elif name == "nextBreakfast":
            return self.nextBreakfast
        elif name == "nextLunch":
            return self.nextLunch
        elif name == "nextDinner":
            return self.nextDinner
