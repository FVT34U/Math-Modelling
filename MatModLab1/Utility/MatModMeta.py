from PyQt5.sip import wrappertype as pyqtWrapperType
from abc import ABCMeta


class MatModMeta(pyqtWrapperType, ABCMeta):
    pass
