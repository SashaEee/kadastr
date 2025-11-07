# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.address.GarStatus import GarStatus
from pullenti.address.internal.gar.HouseObject import HouseObject

class AreaObject(object):
    """ Адресный объект ГАР ФИАС """
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.parent_ids = list()
        self.parent_parent_ids = None;
        self.actual_obj_id = 0
        self.typ = None;
        self.names = list()
        self.old_typ = None;
        self.level = 0
        self.actual = False
        self.has_cross = False
        self.region = 0
        self.status = GarStatus.OK
        self.guid = None;
        self.gps_mask = 0
        self.children_ids = list()
        self.tag = None;
    
    HOUSEMASK = 0x80000000
    
    ROOMMASK = 0xC0000000
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.id0_ > 0): 
            print("{0}: ".format(self.id0_), end="", file=res, flush=True)
        if (not self.actual): 
            print("(*) ", end="", file=res)
        if (self.has_cross): 
            print("(+) ", end="", file=res)
        print("[{0}] ".format(self.level), end="", file=res, flush=True)
        if (self.typ is not None): 
            print("{0} ".format(self.typ.name), end="", file=res, flush=True)
        if (self.old_typ is not None): 
            print("(уст. {0}) ".format(self.old_typ.name), end="", file=res, flush=True)
        if (self.status != GarStatus.OK): 
            print("{0} ".format(Utils.enumToString(self.status)), end="", file=res, flush=True)
        i = 0
        while i < len(self.names): 
            print("{0}{1}".format(("/" if i > 0 else ""), self.names[i]), end="", file=res, flush=True)
            i += 1
        if (self.actual_obj_id > 0): 
            print(", ActualId = {0}".format(self.actual_obj_id), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def merge_with(self, ao : 'AreaObject') -> None:
        if (ao.actual == self.actual or ((self.actual and not ao.actual))): 
            for n in ao.names: 
                if (not n in self.names): 
                    self.names.append(n)
            if (ao.old_typ is not None and self.old_typ is None): 
                self.old_typ = ao.old_typ
            elif (self.typ is not None and ao.typ != self.typ and self.old_typ is None): 
                self.old_typ = ao.typ
            if (ao.level > (0) and self.level == (0)): 
                self.level = ao.level
        elif (not self.actual and ao.actual): 
            self.actual = True
            nams = list(ao.names)
            for n in self.names: 
                if (not n in nams): 
                    nams.append(n)
            self.names = nams
            if (self.typ != ao.typ): 
                self.old_typ = self.typ
                self.typ = ao.typ
            self.level = ao.level
        else: 
            pass
    
    def compareTo(self, other : 'AreaObject') -> int:
        if (self.level < other.level): 
            return -1
        if (self.level > other.level): 
            return 1
        if (len(self.names) > 0 and len(other.names) > 0): 
            i = HouseObject._comp_nums(self.names[0], other.names[0])
            if (i != 0): 
                return i
        return 0
    
    @staticmethod
    def _new45(_arg1 : int) -> 'AreaObject':
        res = AreaObject()
        res.id0_ = _arg1
        return res