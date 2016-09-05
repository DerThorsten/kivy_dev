import pybox2d as b2d



class AABBCallback(b2d.QueryCallback):
    def __init__(self, testPoint, ignoreSensorFixtures = True):
        super(AABBCallback,self).__init__()

        self.testPoint = b2d.vec2(testPoint)
        self.fixture  = None
        self.ignoreSensorFixtures = ignoreSensorFixtures

    def ReportFixture(self, fixture):
        if fixture.testPoint(self.testPoint):

            if not self.ignoreSensorFixtures:
                self.fixture  = fixture
                return False
            else:
                if not fixture.isSensor:
                    self.fixture  = fixture
                    return False
        else:
            return True

