#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2017, Ilya Etingof <etingof@gmail.com>
# License: http://pyasn1.sf.net/license.html
#
from pyasn1 import error


__all__ = ['ForwardRef']


class ForwardRef(object):
    # TODO: this is not thread-safe
    waitingList = {}

    def __init__(self, symbol, *args, **kwargs):
        self.__symbol = symbol
        self.args = args
        self.kwargs = kwargs

    def callLater(self, cbFun):
        if self.__symbol not in self.waitingList:
            self.waitingList[self.__symbol] = []
        self.waitingList[self.__symbol].append((self, cbFun))

    @classmethod
    def newTypeNotification(cls, name, obj):
        # TODO: name collision at different modules possible
        if name in cls.waitingList:
            for waitingObject, cbFun in cls.waitingList.pop(name):
                cbFun(obj(*waitingObject.args, **waitingObject.kwargs))

    def __getattr__(self, item):
        raise error.PyAsn1Error('Unresolved forward reference %s' % self.__symbol)

