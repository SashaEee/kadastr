# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.gar.FiasHouseTable import FiasHouseTable
from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.address.internal.NumberAnalyzer import NumberAnalyzer
from pullenti.address.internal.FiasHelper import FiasHelper

class HousesInStreet:
    
    def __init__(self) -> None:
        self.__m_houses = None
        self.__refs = dict()
        self.__m_data = None;
        self.__m_houses_pos = None;
        self.m_lock = object()
    
    def __str__(self) -> str:
        return "{0} houses, {1} refs".format((len(self.__m_houses) if self.__m_houses is not None else (len(self.__m_houses_pos) if self.__m_houses_pos is not None else 0)), len(self.__refs))
    
    def load(self, dat : bytearray) -> None:
        if (dat is None or (len(dat) < 8)): 
            return
        self.__m_data = dat
        ind = 4
        cou = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        pos0 = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        self.__m_houses_pos = Utils.newArray(cou, 0)
        i = 0
        while i < cou: 
            self.__m_houses_pos[i] = int.from_bytes(dat[ind:ind+4], byteorder="little")
            i += 1; ind += 4
        ind = pos0
        cou = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        self.__refs.clear()
        i = 0
        while i < cou: 
            wrapind56 = RefOutArgWrapper(ind)
            key = FiasHelper.deserialize_string_from_bytes(dat, wrapind56, False)
            ind = wrapind56.value
            cou2 = int.from_bytes(dat[ind:ind+2], byteorder="little")
            ind += 2
            li = list()
            j = 0
            while j < cou2: 
                li.append(int.from_bytes(dat[ind:ind+2], byteorder="little"))
                j += 1; ind += 2
            self.__refs[key] = li
            i += 1
    
    def get_houses(self, na : 'NumberAnalyzer') -> typing.List['HouseObject']:
        inds = list()
        for it in na.items: 
            li = [ ]
            wrapli57 = RefOutArgWrapper(None)
            inoutres58 = Utils.tryGetValue(self.__refs, it.value, wrapli57)
            li = wrapli57.value
            if (not inoutres58): 
                break
            if (len(inds) == 0): 
                inds.extend(li)
            break
        if (len(inds) == 0): 
            return None
        res = list()
        for i in inds: 
            if ((i < 1) or i > len(self.__m_houses_pos)): 
                continue
            ho = HouseObject()
            ho.id0_ = int.from_bytes(self.__m_data[self.__m_houses_pos[i - 1]:self.__m_houses_pos[i - 1]+4], byteorder="little")
            if (FiasHouseTable._restore(self.__m_data, ho, self.__m_houses_pos[i - 1] + 4)): 
                res.append(ho)
        return res
    
    def save(self) -> bytearray:
        if (self.__m_houses is None or len(self.__m_houses) == 0): 
            return None
        with MemoryStream() as mem: 
            FiasHelper.serialize_int(mem, 0)
            FiasHelper.serialize_int(mem, len(self.__m_houses))
            FiasHelper.serialize_int(mem, 0)
            i = 0
            while i < len(self.__m_houses): 
                FiasHelper.serialize_int(mem, 0)
                i += 1
            self.__m_houses_pos = Utils.newArray(len(self.__m_houses), 0)
            i = 0
            while i < len(self.__m_houses): 
                self.__m_houses_pos[i] = (mem.position)
                FiasHelper.serialize_int(mem, self.__m_houses[i].id0_)
                dat = FiasHouseTable._store(self.__m_houses[i])
                mem.write(dat, 0, len(dat))
                i += 1
            pos = mem.position
            mem.position = 8
            FiasHelper.serialize_int(mem, pos)
            i = 0
            while i < len(self.__m_houses_pos): 
                FiasHelper.serialize_int(mem, self.__m_houses_pos[i])
                i += 1
            mem.position = mem.length
            FiasHelper.serialize_int(mem, len(self.__refs))
            for r in self.__refs.items(): 
                FiasHelper.serialize_string(mem, r[0], False)
                FiasHelper.serialize_short(mem, len(r[1]))
                for v in r[1]: 
                    FiasHelper.serialize_short(mem, v)
            return mem.toarray()
    
    def addho(self, ho : 'HouseObject') -> bool:
        num = NumberAnalyzer.try_parseho(ho)
        if (num is None or len(num.items) == 0): 
            return False
        if (self.__m_houses is None): 
            self.__m_houses = list()
        self.__m_houses.append(ho)
        ind = len(self.__m_houses)
        for it in num.items: 
            li = [ ]
            wrapli59 = RefOutArgWrapper(None)
            inoutres60 = Utils.tryGetValue(self.__refs, it.value, wrapli59)
            li = wrapli59.value
            if (not inoutres60): 
                li = list()
                self.__refs[it.value] = li
            if (not ind in li): 
                li.append(ind)
        return True