# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import uuid
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.BaseTable import BaseTable
from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.address.GarStatus import GarStatus

class FiasHouseTable(KeyBaseTable):
    
    def __init__(self, rep : 'IRepository', name_ : str="houseobjects") -> None:
        super().__init__(rep, name_, None)
    
    def add(self, id0_ : int, doc : 'HouseObject') -> None:
        dat = FiasHouseTable._store(doc)
        self.write_key_data(id0_, dat)
    
    def get_status(self, id0_ : int) -> 'GarStatus':
        data = self.read_key_data(id0_, 1)
        if (data is None): 
            return GarStatus.ERROR
        if ((((data[0]) & 4)) != 0): 
            return GarStatus.WARNING
        if ((((data[0]) & 8)) != 0): 
            return GarStatus.ERROR
        if ((((data[0]) & 0x10)) != 0): 
            return GarStatus.OK2
        return GarStatus.OK
    
    @staticmethod
    def _store(ao : 'HouseObject') -> bytearray:
        res = bytearray()
        attr = ((0 if ao.actual else 1))
        if (ao.alt_parent_id > 0): 
            attr |= (2)
        if (ao.status == GarStatus.WARNING): 
            attr |= (4)
        elif (ao.status == GarStatus.ERROR): 
            attr |= (8)
        elif (ao.status == GarStatus.OK2): 
            attr |= (0x10)
        attr |= (0x20)
        attr |= (0x40)
        if (ao.is_plot): 
            attr |= (0x80)
        res.append(attr)
        res.extend((ao.parent_id).to_bytes(4, byteorder="little"))
        res.append(ao.house_typ)
        res.append(ao.struc_typ)
        BaseTable.get_bytes_for_string(res, ao.house_number, None)
        BaseTable.get_bytes_for_string(res, ao.build_number, None)
        BaseTable.get_bytes_for_string(res, ao.struc_number, None)
        BaseTable.get_bytes_for_string(res, ao.plot_number, None)
        BaseTable.get_bytes_for_string(res, ao.source_text, None)
        res.extend(((0 if ao.room_ids is None else len(ao.room_ids))).to_bytes(4, byteorder="little"))
        if (ao.room_ids is not None): 
            for ii in ao.room_ids: 
                res.extend((ii).to_bytes(4, byteorder="little"))
        if (ao.alt_parent_id > 0): 
            res.extend((ao.alt_parent_id).to_bytes(4, byteorder="little"))
        gg = uuid.UUID(ao.guid)
        res.extend(gg.bytes)
        res.append(ao.gps_mask)
        return bytearray(res)
    
    def get(self, id0_ : int, ao : 'HouseObject') -> bool:
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return False
        ao.id0_ = id0_
        return FiasHouseTable._restore(dat, ao, 0)
    
    def get_parent_id(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 5)
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
    def _restore(data : bytearray, ao : 'HouseObject', ind : int=0) -> bool:
        if ((((data[ind]) & 1)) != 0): 
            ao.actual = False
        else: 
            ao.actual = True
        is_alt_parent = (((data[ind]) & 2)) != 0
        if ((((data[ind]) & 4)) != 0): 
            ao.status = GarStatus.WARNING
        if ((((data[ind]) & 8)) != 0): 
            ao.status = GarStatus.ERROR
        if ((((data[ind]) & 0x10)) != 0): 
            ao.status = GarStatus.OK2
        is_plot = (((data[ind]) & 0x20)) != 0
        has_source = (((data[ind]) & 0x40)) != 0
        ao.is_plot = (((data[ind]) & 0x80)) != 0
        ind += 1
        ao.parent_id = int.from_bytes(data[ind:ind+4], byteorder="little")
        ind += 4
        ao.house_typ = data[ind]
        ind += 1
        ao.struc_typ = data[ind]
        ind += 1
        wrapind54 = RefOutArgWrapper(ind)
        ao.house_number = BaseTable.get_string_for_bytes(data, wrapind54, False, None)
        ind = wrapind54.value
        wrapind53 = RefOutArgWrapper(ind)
        ao.build_number = BaseTable.get_string_for_bytes(data, wrapind53, False, None)
        ind = wrapind53.value
        wrapind52 = RefOutArgWrapper(ind)
        ao.struc_number = BaseTable.get_string_for_bytes(data, wrapind52, False, None)
        ind = wrapind52.value
        if (is_plot): 
            wrapind50 = RefOutArgWrapper(ind)
            ao.plot_number = BaseTable.get_string_for_bytes(data, wrapind50, False, None)
            ind = wrapind50.value
        if (has_source): 
            wrapind51 = RefOutArgWrapper(ind)
            ao.source_text = BaseTable.get_string_for_bytes(data, wrapind51, False, None)
            ind = wrapind51.value
        if (ao.house_typ == (5)): 
            ao.plot_number = ao.house_number
            ao.house_number = (None)
            ao.house_typ = (0)
        cou = int.from_bytes(data[ind:ind+4], byteorder="little")
        ind += 4
        if (cou > 0): 
            ao.room_ids = list()
            while cou > 0: 
                ao.room_ids.append(int.from_bytes(data[ind:ind+4], byteorder="little"))
                ind += 4
                cou -= 1
        if (is_alt_parent): 
            ao.alt_parent_id = int.from_bytes(data[ind:ind+4], byteorder="little")
            ind += 4
        if ((ind + 16) <= len(data)): 
            dat = Utils.newArrayOfBytes(16, 0)
            for i in range(16):
                dat[i] = data[ind + i]
            ind += 16
            gg = uuid.UUID(bytes_le=bytes(dat))
            ao.guid = str(gg)
        if (ind < len(data)): 
            ao.gps_mask = data[ind]
            ind += 1
        return True