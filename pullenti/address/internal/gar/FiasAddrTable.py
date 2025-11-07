# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.GarStatus import GarStatus

class FiasAddrTable(KeyBaseTable):
    
    def __init__(self, rep : 'IRepository', name_ : str="areaobjects") -> None:
        super().__init__(rep, name_, None)
    
    def add(self, id0_ : int, doc : 'AreaObject', only_attrs : bool) -> None:
        dat = FiasAddrTable._store(doc)
        self.write_key_data(id0_, dat)
    
    @staticmethod
    def _store(ao : 'AreaObject') -> bytearray:
        res = bytearray()
        attr = ((0 if ao.actual else 1))
        if (ao.status == GarStatus.WARNING): 
            attr |= (2)
        elif (ao.status == GarStatus.ERROR): 
            attr |= (4)
        elif (ao.status == GarStatus.OK2): 
            attr |= (8)
        if (ao.actual_obj_id > 0): 
            attr |= (0x10)
        if (ao.has_cross): 
            attr |= (0x20)
        res.append(attr)
        res.extend((((0 if ao.typ is None else ao.typ.id0_))).to_bytes(2, byteorder="little"))
        res.extend((((0 if ao.old_typ is None else ao.old_typ.id0_))).to_bytes(2, byteorder="little"))
        res.extend((len(ao.parent_ids)).to_bytes(2, byteorder="little"))
        if (len(ao.parent_ids) > 0): 
            for id0_ in ao.parent_ids: 
                res.extend((id0_).to_bytes(4, byteorder="little"))
            res.append(((0 if ao.parent_parent_ids is None else len(ao.parent_parent_ids))))
            if (ao.parent_parent_ids is not None): 
                for id0_ in ao.parent_parent_ids: 
                    res.extend((id0_).to_bytes(4, byteorder="little"))
        res.extend((ao.level).to_bytes(2, byteorder="little"))
        if (ao.actual_obj_id > 0): 
            res.extend((ao.actual_obj_id).to_bytes(4, byteorder="little"))
        res.extend((len(ao.names)).to_bytes(2, byteorder="little"))
        for n in ao.names: 
            FiasAddrTable.get_bytes_for_string1251(res, n)
        res.extend((len(ao.children_ids)).to_bytes(4, byteorder="little"))
        for id0_ in ao.children_ids: 
            res.extend((id0_).to_bytes(4, byteorder="little"))
        res.extend((0).to_bytes(4, byteorder="little"))
        res.append(ao.region)
        FiasAddrTable.get_bytes_for_string1251(res, ao.guid)
        res.append(ao.gps_mask)
        return bytearray(res)
    
    def get(self, id0_ : int, ao : 'AreaObject', typs : typing.List[tuple]) -> bool:
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return False
        ao.id0_ = id0_
        return FiasAddrTable._restore(dat, ao, typs)
    
    def get_parent_id(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 11)
        if (data is None): 
            return 0
        ind = 5
        cou = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        if (cou == 0): 
            return 0
        return int.from_bytes(data[ind:ind+4], byteorder="little")
    
    def get_actual(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 1)
        if (data is None): 
            return -1
        return (0 if ((((data[0]) & 1)) != 0) else 1)
    
    def get_status(self, id0_ : int) -> 'GarStatus':
        data = self.read_key_data(id0_, 1)
        if (data is None): 
            return GarStatus.ERROR
        if ((((data[0]) & 2)) != 0): 
            return GarStatus.WARNING
        if ((((data[0]) & 4)) != 0): 
            return GarStatus.ERROR
        if ((((data[0]) & 8)) != 0): 
            return GarStatus.OK2
        return GarStatus.OK
    
    @staticmethod
    def _restore(data : bytearray, ao : 'AreaObject', typs : typing.List[tuple]) -> bool:
        if ((((data[0]) & 1)) != 0): 
            ao.actual = False
        else: 
            ao.actual = True
        if ((((data[0]) & 2)) != 0): 
            ao.status = GarStatus.WARNING
        if ((((data[0]) & 4)) != 0): 
            ao.status = GarStatus.ERROR
        if ((((data[0]) & 8)) != 0): 
            ao.status = GarStatus.OK2
        if ((((data[0]) & 0x20)) != 0): 
            ao.has_cross = True
        ind = 1
        id0_ = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        ty = None
        wrapty27 = RefOutArgWrapper(None)
        inoutres28 = Utils.tryGetValue(typs, id0_, wrapty27)
        ty = wrapty27.value
        if (inoutres28): 
            ao.typ = ty
        id0_ = (int.from_bytes(data[ind:ind+2], byteorder="little"))
        ind += 2
        if (id0_ != 0): 
            wrapty23 = RefOutArgWrapper(None)
            inoutres24 = Utils.tryGetValue(typs, id0_, wrapty23)
            ty = wrapty23.value
            if (inoutres24): 
                ao.old_typ = ty
        cou = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        if (cou > 0): 
            while cou > 0: 
                ao.parent_ids.append(int.from_bytes(data[ind:ind+4], byteorder="little"))
                ind += 4
                cou -= 1
            cou = (data[ind])
            ind += 1
            if (cou > 0): 
                ao.parent_parent_ids = list()
                while cou > 0: 
                    ao.parent_parent_ids.append(int.from_bytes(data[ind:ind+4], byteorder="little"))
                    ind += 4
                    cou -= 1
        ao.level = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        if ((((data[0]) & 0x10)) != 0): 
            ao.actual_obj_id = int.from_bytes(data[ind:ind+4], byteorder="little")
            ind += 4
        cou = (int.from_bytes(data[ind:ind+2], byteorder="little"))
        ind += 2
        while cou > 0: 
            wrapind25 = RefOutArgWrapper(ind)
            ao.names.append(FiasAddrTable.to_string1251(data, wrapind25))
            ind = wrapind25.value
            cou -= 1
        cou = int.from_bytes(data[ind:ind+4], byteorder="little")
        ind += 4
        while cou > 0: 
            ao.children_ids.append(int.from_bytes(data[ind:ind+4], byteorder="little"))
            ind += 4
            cou -= 1
        ind += 4
        ao.region = data[ind]
        ind += 1
        if (ind < len(data)): 
            wrapind26 = RefOutArgWrapper(ind)
            ao.guid = FiasAddrTable.to_string1251(data, wrapind26)
            ind = wrapind26.value
        if (ind < len(data)): 
            ao.gps_mask = data[ind]
            ind += 1
        return True
    
    @staticmethod
    def to_string1251(data : bytearray, ind : int) -> str:
        if ((ind.value + 2) > len(data)): 
            return None
        len0_ = int.from_bytes(data[ind.value:ind.value+2], byteorder="little")
        ind.value += 2
        if (len0_ <= (0)): 
            return None
        if ((ind.value + (len0_)) > len(data)): 
            return None
        res = FiasHelper.decode_string1251(data, ind.value, len0_, False)
        ind.value += (len0_)
        return res
    
    @staticmethod
    def get_bytes_for_string1251(res : bytearray, str0_ : str) -> None:
        if (Utils.isNullOrEmpty(str0_)): 
            res.extend((0).to_bytes(2, byteorder="little"))
        else: 
            b = FiasHelper.encode_string1251(str0_)
            res.extend((len(b)).to_bytes(2, byteorder="little"))
            res.extend(b)