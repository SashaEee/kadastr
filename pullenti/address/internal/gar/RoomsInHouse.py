# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.address.RoomType import RoomType
from pullenti.address.internal.gar.RoomObject import RoomObject
from pullenti.address.internal.NumberAnalyzer import NumberAnalyzer
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.gar.FiasRoomTable import FiasRoomTable

class RoomsInHouse:
    
    def __init__(self) -> None:
        self.__m_rooms = None
        self.__refs = dict()
        self.__m_data = None;
        self.__m_rooms_pos = None;
        self.m_lock = object()
    
    @property
    def count(self) -> int:
        return (len(self.__m_rooms) if self.__m_rooms is not None else (len(self.__m_rooms_pos) if self.__m_rooms_pos is not None else 0))
    
    def __str__(self) -> str:
        return "{0} Rooms, {1} refs".format(self.count, len(self.__refs))
    
    def load(self, dat : bytearray) -> None:
        if (dat is None or (len(dat) < 8)): 
            return
        self.__m_data = dat
        ind = 4
        cou = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        pos0 = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        self.__m_rooms_pos = Utils.newArray(cou, 0)
        i = 0
        while i < cou: 
            self.__m_rooms_pos[i] = int.from_bytes(dat[ind:ind+4], byteorder="little")
            i += 1; ind += 4
        ind = pos0
        cou = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        self.__refs.clear()
        i = 0
        while i < cou: 
            wrapind73 = RefOutArgWrapper(ind)
            key = FiasHelper.deserialize_string_from_bytes(dat, wrapind73, False)
            ind = wrapind73.value
            cou2 = int.from_bytes(dat[ind:ind+2], byteorder="little")
            ind += 2
            li = list()
            j = 0
            while j < cou2: 
                li.append(int.from_bytes(dat[ind:ind+2], byteorder="little"))
                j += 1; ind += 2
            self.__refs[key] = li
            i += 1
    
    def get_rooms(self, na : 'NumberAnalyzer') -> typing.List['RoomObject']:
        inds = list()
        for it in na.items: 
            li = [ ]
            wrapli74 = RefOutArgWrapper(None)
            inoutres75 = Utils.tryGetValue(self.__refs, it.value, wrapli74)
            li = wrapli74.value
            if (not inoutres75): 
                continue
            if (len(inds) == 0): 
                inds.extend(li)
            else: 
                for v in li: 
                    if (not v in inds): 
                        inds.append(v)
        if (len(inds) == 0): 
            return None
        res = list()
        for i in inds: 
            if ((i < 1) or i > len(self.__m_rooms_pos)): 
                continue
            ho = RoomObject()
            ho.id0_ = int.from_bytes(self.__m_data[self.__m_rooms_pos[i - 1]:self.__m_rooms_pos[i - 1]+4], byteorder="little")
            ii = self.__m_rooms_pos[i - 1] + 4
            wrapii76 = RefOutArgWrapper(ii)
            inoutres77 = FiasRoomTable._restore(self.__m_data, ho, wrapii76)
            ii = wrapii76.value
            if (inoutres77): 
                res.append(ho)
        return res
    
    def check_has_flats_and_spaces(self) -> bool:
        has_flats = False
        has_spaces = False
        k = 0
        while k < len(self.__m_rooms_pos): 
            ty = FiasRoomTable._get_room_typ(self.__m_data, self.__m_rooms_pos[k] + 4)
            if (ty == RoomType.FLAT): 
                has_flats = True
            if (ty == RoomType.SPACE): 
                has_spaces = True
            if (has_flats and has_spaces): 
                return True
            k += 1
        return False
    
    def save(self) -> bytearray:
        if (self.__m_rooms is None or len(self.__m_rooms) == 0): 
            return None
        with MemoryStream() as mem: 
            FiasHelper.serialize_int(mem, 0)
            FiasHelper.serialize_int(mem, len(self.__m_rooms))
            FiasHelper.serialize_int(mem, 0)
            i = 0
            while i < len(self.__m_rooms): 
                FiasHelper.serialize_int(mem, 0)
                i += 1
            self.__m_rooms_pos = Utils.newArray(len(self.__m_rooms), 0)
            buf = bytearray()
            i = 0
            while i < len(self.__m_rooms): 
                self.__m_rooms_pos[i] = (mem.position)
                FiasHelper.serialize_int(mem, self.__m_rooms[i].id0_)
                buf.clear()
                FiasRoomTable._store(buf, self.__m_rooms[i])
                dat = bytearray(buf)
                mem.write(dat, 0, len(dat))
                i += 1
            pos = mem.position
            mem.position = 8
            FiasHelper.serialize_int(mem, pos)
            i = 0
            while i < len(self.__m_rooms_pos): 
                FiasHelper.serialize_int(mem, self.__m_rooms_pos[i])
                i += 1
            mem.position = mem.length
            FiasHelper.serialize_int(mem, len(self.__refs))
            for r in self.__refs.items(): 
                FiasHelper.serialize_string(mem, r[0], False)
                FiasHelper.serialize_short(mem, len(r[1]))
                for v in r[1]: 
                    FiasHelper.serialize_short(mem, v)
            return mem.toarray()
    
    def addro(self, ho : 'RoomObject') -> bool:
        num = NumberAnalyzer.try_parsero(ho)
        if (num is None or len(num.items) == 0): 
            return False
        if (self.__m_rooms is None): 
            self.__m_rooms = list()
        self.__m_rooms.append(ho)
        ind = len(self.__m_rooms)
        for it in num.items: 
            li = [ ]
            wrapli78 = RefOutArgWrapper(None)
            inoutres79 = Utils.tryGetValue(self.__refs, it.value, wrapli78)
            li = wrapli78.value
            if (not inoutres79): 
                li = list()
                self.__refs[it.value] = li
            if (not ind in li): 
                li.append(ind)
        return True