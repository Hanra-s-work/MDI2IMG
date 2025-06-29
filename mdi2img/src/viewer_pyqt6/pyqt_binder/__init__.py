"""
File in charge of grouping the elements of the window tools class
"""

from .add import AddPyQt
from .get import GetPyQt
from .set import SetPyQt
from .unsorted import UnsortedPyQt


class WindowTools(AddPyQt, GetPyQt, SetPyQt, UnsortedPyQt):
    """ The class in charge of grouping the window tools """

    def __init__(self, success: int = 0, error: int = 84) -> None:
        super(WindowTools, self).__init__()
        self.success = success
        self.error = error
        self._add = AddPyQt()
        self._get = GetPyQt()
        self._set = SetPyQt()
        self._unsorted = UnsortedPyQt()
        self.pyqt_add = self._add
        self.pyqt_get = self._get
        self.pyqt_set = self._set
        self.pyqt_unsorted = self._unsorted

    def test_window_tools(self) -> None:
        """ Test the window tools """
        print("Testing window tools")
        print(f"success = {self.success}")
        print(f"error = {self.error}")
        print(f"_add = {dir(self._add)}")
        print(f"_get = {dir(self._get)}")
        print(f"_set = {dir(self._set)}")
        print(f"_unsorted = {dir(self._unsorted)}")
