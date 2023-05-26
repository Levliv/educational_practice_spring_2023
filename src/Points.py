from Point import Point


class Points:
    def __init__(self, x, y):
        if len(x) != len(y):
            raise Exception("Длины векторов x и y должны быть одинаковыми")
        self.x = x[0 : len(x)]
        self.y = y[0 : len(y)]

    def __len__(self):
        return len(self.x)

    def __getitem__(self, item):
        return Point(self.x[item], self.y[item])
