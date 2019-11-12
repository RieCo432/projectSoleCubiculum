from abc import abstractmethod
from collections import MutableSequence
from typing import overload


class CircularList(MutableSequence):

    @overload
    @abstractmethod
    def __delitem__(self, i: int) -> None: ...

    @overload
    @abstractmethod
    def __delitem__(self, i: slice) -> None: ...

    def __delitem__(self, i: int) -> None:
        pass

    def __init__(self, data=None):
        super(CircularList, self).__init__()
        if data is not None:
            self._data = list(data)
        else:
            self._data = list()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def insert(self, index, val):
        self._data[index] = val

    def append(self, val):
        self._data.append(val)

    def __setitem__(self, key, value):
        self._data[key] = value

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
