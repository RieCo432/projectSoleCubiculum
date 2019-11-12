class CircularList(list):

    def __init__(self, data=None):
        super(CircularList, self).__init__(data)
        if data is not None:
            self._list = list(data)
        else:
            self._list = list()

    def shiftForward(self):
        last = self[-1]
        for i in range(len(self)).__reversed__():
            self[i] = self[i-1]
        self[0] = last

    def shiftForwardN(self, n):
        for i in range(n):
            self.shiftForward()

    def shiftBackward(self):
        first = self[0]
        for i in range(len(self)-1):
            self[i] = self[i+1]
        self[-1] = first

    def shiftBackwardN(self, n):
        for i in range(n):
            self.shiftBackward()



if __name__ == "__main__":
    ca = CircularList((1, 2, 3))
    print(ca)
    ca.shiftBackwardN(2)
    print(ca)
