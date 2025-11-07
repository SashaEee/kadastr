# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import uuid
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.RoomType import RoomType
from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.address.GarStatus import GarStatus
from pullenti.util.repository.BaseTable import BaseTable
from pullenti.address.internal.gar.RoomObject import RoomObject

class FiasRoomTable(KeyBaseTable):
    
    def __init__(self, rep : 'IRepository', name_ : str="roomobjects") -> None:
        super().__init__(rep, name_, None)
    
    def add(self, id0_ : int, r : 'RoomObject') -> None:
        res = bytearray()
        FiasRoomTable._store(res, r)
        dat = bytearray(res)
        self.write_key_data(id0_, dat)
    
    @staticmethod
    def _store(res : bytearray, ao : 'RoomObject') -> None:
        attr = ((0 if ao.actual else 1))
        attr |= (2)
        if (ao.status != GarStatus.OK): 
            attr |= (4)
        attr |= (8)
        res.append(attr)
        res.extend((ao.house_id).to_bytes(4, byteorder="little"))
        res.append(ao.typ)
        BaseTable.get_bytes_for_string(res, ao.number, None)
        BaseTable.get_bytes_for_string(res, ao.misc, None)
        BaseTable.get_bytes_for_string(res, ao.source_text, None)
        res.extend((((0 if ao.children_ids is None else len(ao.children_ids)))).to_bytes(4, byteorder="little"))
        if (ao.children_ids is not None): 
            for id0_ in ao.children_ids: 
                res.extend((id0_).to_bytes(4, byteorder="little"))
        gg = uuid.UUID(ao.guid)
        res.extend(gg.bytes)
    
    def get(self, id0_ : int) -> 'RoomObject':
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return None
        r = RoomObject()
        r.id0_ = id0_
        ind = 0
        wrapind55 = RefOutArgWrapper(ind)
        FiasRoomTable._restore(dat, r, wrapind55)
        ind = wrapind55.value
        return r
    
    def get_parent_id(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 11)
        if (data is None): 
            return 0
        ind = 1
        return int.from_bytes(data[ind:ind+4], byteorder="little")
    
    def get_actual(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 1)
        if (data is None): 
            return -1
        return (0 if ((((data[0]) & 1)) != 0) else 1)
    
    @staticmethod
    def _get_room_typ(data : bytearray, ind : int) -> 'RoomType':
        ind += 5
        return Utils.valToEnum(data[ind], RoomType)
    
    @staticmethod
    def _restore(data : bytearray, ao : 'RoomObject', ind : int) -> bool:
        attr = data[ind.value]
        ind.value += 1
        if ((((attr) & 1)) != 0): 
            ao.actual = False
        else: 
            ao.actual = True
        ao.status = (GarStatus.OK if (((attr) & 4)) == 0 else GarStatus.ERROR)
        ao.house_id = int.from_bytes(data[ind.value:ind.value+4], byteorder="little")
        ind.value += 4
        typ = data[ind.value]
        ind.value += 1
        ao.typ = (Utils.valToEnum(typ, RoomType))
        ao.number = BaseTable.get_string_for_bytes(data, ind, False, None)
        if ((((attr) & 8)) != 0): 
            ao.misc = BaseTable.get_string_for_bytes(data, ind, False, None)
        if ((((attr) & 2)) != 0): 
            ao.source_text = BaseTable.get_string_for_bytes(data, ind, False, None)
        cou = int.from_bytes(data[ind.value:ind.value+4], byteorder="little")
        ind.value += 4
        while cou > 0: 
            if (ao.children_ids is None): 
                ao.children_ids = list()
            ao.children_ids.append(int.from_bytes(data[ind.value:ind.value+4], byteorder="little"))
            ind.value += 4
            cou -= 1
        dat = Utils.newArrayOfBytes(16, 0)
        for i in range(16):
            dat[i] = data[ind.value + i]
        gg = uuid.UUID(bytes_le=bytes(dat))
        ao.guid = str(gg)
        return True