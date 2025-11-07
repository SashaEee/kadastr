# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.GarStatus import GarStatus
from pullenti.address.RoomType import RoomType

class RoomObject(object):
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.house_id = 0
        self.number = None;
        self.typ = RoomType.UNDEFINED
        self.misc = None;
        self.actual = False
        self.guid = None;
        self.children_ids = None
        self.status = GarStatus.OK
        self.source_text = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        print(self.source_text, end="", file=res)
        if (self.status != GarStatus.OK): 
            print(" (ERROR)", end="", file=res)
        return Utils.toStringStringIO(res)
    
    def to_string_ex(self) -> str:
        res = io.StringIO()
        print("{0}{1}".format(AddressHelper.get_room_type_string(self.typ, True), Utils.ifNotNull(self.number, "б/н")), end="", file=res, flush=True)
        if (self.misc is not None): 
            print(" ({0})".format(self.misc), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __get_int(str0_ : str) -> int:
        if (str0_ is None): 
            return 0
        res = 0
        i = 0
        while i < len(str0_): 
            if (str.isdigit(str0_[i])): 
                res = (((res * 10) + (ord(str0_[i]))) - 0x30)
            else: 
                break
            i += 1
        return res
    
    @staticmethod
    def _comp_nums(str1 : str, str2 : str) -> int:
        n1 = RoomObject.__get_int(str1)
        n2 = RoomObject.__get_int(str2)
        if (n1 < n2): 
            return -1
        if (n1 > n2): 
            return 1
        if (str1 is not None and str2 is not None): 
            return Utils.compareStrings(str1, str2, False)
        return 0
    
    def compareTo(self, other : 'RoomObject') -> int:
        i = RoomObject._comp_nums(self.number, other.number)
        if (i != 0): 
            return i
        return 0
    
    @staticmethod
    def _new203(_arg1 : str) -> 'RoomObject':
        res = RoomObject()
        res.source_text = _arg1
        return res
    
    @staticmethod
    def _new244(_arg1 : str, _arg2 : int) -> 'RoomObject':
        res = RoomObject()
        res.source_text = _arg1
        res.house_id = _arg2
        return res