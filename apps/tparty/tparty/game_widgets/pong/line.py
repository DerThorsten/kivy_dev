




class LinearFunction(object):
    def __init__(self, p0, p1):

        dx = float(p1[0] - p0[0])
        dy = float(p1[1] - p0[1])

        self.m = dy / dx
        self.c = p0[1] - self.m * p0[0]


    def __call__(self, x):
        return self.m * x + self.c
