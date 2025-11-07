# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import uuid
import datetime
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.GarStatus import GarStatus
from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.gar.AreaObject import AreaObject
from pullenti.address.GarParam import GarParam
from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.internal.gar.RoomsInHouse import RoomsInHouse
from pullenti.address.internal.gar.HousesInStreet import HousesInStreet
from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.util.repository.IRepository import IRepository
from pullenti.address.internal.gar.AreaType import AreaType
from pullenti.address.internal.gar.FiasHouseTable import FiasHouseTable
from pullenti.address.internal.gar.FiasAddrTable import FiasAddrTable
from pullenti.address.internal.gar.PTreeRoot import PTreeRoot
from pullenti.address.internal.gar.ParamsTable import ParamsTable
from pullenti.address.internal.gar.AreaTree import AreaTree
from pullenti.address.internal.gar.FiasRoomTable import FiasRoomTable

class FiasDatabase(IRepository):
    # База данных ФИАС (ГАР)
    
    def __init__(self) -> None:
        self.__basedir = None;
        self.id0_ = None;
        self.create_date = None;
        self.version = None;
        self.read_only = True
        self.__m_ao_by_regs = dict()
        self.__m_types = dict()
        self.__m_addr_table = None;
        self.__m_house_table = None;
        self.__m_room_table = None;
        self.__m_houses_in_ao = None;
        self.__m_rooms_in_house = None;
        self.__m_rooms_in_rooms = None;
        self.__m_zip_ao = None;
        self.__m_area_tree = None;
        self.__m_addr_params = None;
        self.__m_house_params = None;
        self.__m_room_params = None;
        self.__m_area_guids = None;
        self.__m_area_name_pos = None;
        self.__m_area_name_data = None;
        self.__m_params_maps = dict()
        self.__outlog = False
        self.__m_children = None;
    
    @property
    def base_dir(self) -> str:
        return self.__basedir
    @base_dir.setter
    def base_dir(self, value) -> str:
        self.__basedir = value
        return self.__basedir
    
    def initialize(self, dir_name : str) -> None:
        self.base_dir = dir_name
        if (not pathlib.Path(dir_name).is_dir()): 
            pathlib.Path(dir_name).mkdir(exist_ok=True)
        self.__m_addr_table = FiasAddrTable(self)
        if (self.read_only): 
            fi = pathlib.Path(pathlib.PurePath(self.base_dir).joinpath("areaobjects.ind"))
            self.__m_addr_table.open0_(self.read_only, (fi.stat().st_size if fi.is_file() else -1))
        else: 
            self.__m_addr_table.open0_(False, 0)
        self.__m_house_table = FiasHouseTable(self)
        if (not self.__m_house_table.open0_(self.read_only, 0)): 
            self.__m_house_table = (None)
        self.__m_room_table = FiasRoomTable(self)
        if (not self.__m_room_table.open0_(self.read_only, 0)): 
            self.__m_room_table = (None)
        self.__m_houses_in_ao = KeyBaseTable._new29(self, "houseinareas", True)
        if (not self.__m_houses_in_ao.open0_(self.read_only, 0)): 
            self.__m_houses_in_ao = (None)
        self.__m_rooms_in_house = KeyBaseTable._new29(self, "roominhouses", True)
        if (not self.__m_rooms_in_house.open0_(self.read_only, 0)): 
            self.__m_rooms_in_house = (None)
        self.__m_rooms_in_rooms = KeyBaseTable._new29(self, "roominrooms", True)
        if (not self.__m_rooms_in_rooms.open0_(self.read_only, 0)): 
            self.__m_rooms_in_rooms = (None)
        self.__m_addr_params = ParamsTable(self, "areaparams")
        if (not self.__m_addr_params.open0_(self.read_only, 0)): 
            self.__m_addr_params = (None)
        self.__m_house_params = ParamsTable(self, "houseparams")
        if (not self.__m_house_params.open0_(self.read_only, 0)): 
            self.__m_house_params = (None)
        self.__m_room_params = ParamsTable(self, "roomparams")
        if (not self.__m_room_params.open0_(self.read_only, 0)): 
            self.__m_room_params = (None)
        self.__m_zip_ao = (ParamsTable(self, "zipareas"))
        if (not self.__m_zip_ao.open0_(self.read_only, 0)): 
            self.__m_zip_ao = (None)
        vname = pathlib.PurePath(self.base_dir).joinpath("version.txt")
        if (pathlib.Path(vname).is_file()): 
            self.version = pathlib.Path(vname).read_bytes().decode("UTF-8", 'ignore')
        fname = pathlib.PurePath(self.base_dir).joinpath("types.xml")
        if (not pathlib.Path(fname).is_file()): 
            fname = pathlib.PurePath(self.base_dir).joinpath("types.dat")
        if (pathlib.Path(fname).is_file()): 
            id0__ = None
            dt = None
            wrapid32 = RefOutArgWrapper(id0__)
            wrapdt33 = RefOutArgWrapper(dt)
            typs = AreaType._load(fname, wrapid32, wrapdt33)
            id0__ = wrapid32.value
            dt = wrapdt33.value
            if (typs is not None): 
                self.__m_types = typs
            self.id0_ = id0__
            self.create_date = dt
        else: 
            self.id0_ = str(uuid.uuid4())
            self.create_date = "{0}.{1}.{2}".format(datetime.datetime.now().year, "{:02d}".format(datetime.datetime.now().month), "{:02d}".format(datetime.datetime.now().day))
        self.__m_area_tree = AreaTree()
        fname = pathlib.PurePath(self.base_dir).joinpath("areatree.dat")
        if (pathlib.Path(fname).is_file()): 
            self.__m_area_tree.load(fname)
        fname = pathlib.PurePath(self.base_dir).joinpath("areaguids.dat")
        if (pathlib.Path(fname).is_file()): 
            self.__m_area_guids = pathlib.Path(fname).read_bytes()
        fname = pathlib.PurePath(self.base_dir).joinpath("areanames.ind")
        if (pathlib.Path(fname).is_file()): 
            self.__m_area_name_pos = pathlib.Path(fname).read_bytes()
        fname = pathlib.PurePath(self.base_dir).joinpath("areanames.dat")
        if (pathlib.Path(fname).is_file()): 
            self.__m_area_name_data = pathlib.Path(fname).read_bytes()
        for ty in FiasDatabase.__m_param_types: 
            fname = pathlib.PurePath(self.base_dir).joinpath("paramap{0}.dat".format(ty))
            tn = PTreeRoot()
            if (ty == GarParam.KLADRCODE or ty == GarParam.KADASTERNUMBER or ty == GarParam.REESTERNUMBER): 
                tn.max_length = 8
            elif (ty == GarParam.GUID or ty == GarParam.OBJECTID): 
                tn.max_length = 5
            try: 
                if (pathlib.Path(fname).is_file()): 
                    tn.load(fname)
            except Exception as ex: 
                pass
            self.__m_params_maps[ty] = tn
        roots = self.getao(1)
        if (roots is not None and roots.children_ids is not None): 
            for id0__ in roots.children_ids: 
                if ((((id0__) & (AreaObject.ROOMMASK))) != 0): 
                    continue
                uid = id0__
                ao = self.getao(uid)
                if (ao is None or ao.typ is None): 
                    continue
                if (ao.level != (1) or ao.region == (0)): 
                    continue
                if (not ao.region in self.__m_ao_by_regs): 
                    self.__m_ao_by_regs[ao.region] = ao
    
    def add_addr_type(self, typ : str) -> 'AreaType':
        ty = None
        for kp in self.__m_types.items(): 
            if (kp[1].name == typ): 
                ty = kp[1]
                break
        if (ty is None): 
            ty = AreaType._new34(len(self.__m_types) + 1, typ)
            self.__m_types[ty.id0_] = ty
        return ty
    
    def get_addr_types(self) -> typing.List['AreaType']:
        return list(self.__m_types.values())
    
    def get_addr_type(self, id0__ : int) -> 'AreaType':
        res = None
        wrapres35 = RefOutArgWrapper(None)
        inoutres36 = Utils.tryGetValue(self.__m_types, id0__, wrapres35)
        res = wrapres35.value
        if (not inoutres36): 
            return None
        else: 
            return res
    
    @property
    def areas_count(self) -> int:
        if (self.__m_addr_table is None): 
            return 0
        return self.__m_addr_table.get_max_key()
    
    @property
    def houses_count(self) -> int:
        if (self.__m_house_table is None): 
            return 0
        return self.__m_house_table.get_max_key()
    
    @property
    def rooms_count(self) -> int:
        if (self.__m_room_table is None): 
            return 0
        return self.__m_room_table.get_max_key()
    
    __m_param_types = None
    
    def _close(self) -> None:
        if (self.__m_addr_table is not None): 
            self.__m_addr_table._close()
            self.__m_addr_table = (None)
        if (self.__m_area_tree is not None): 
            self.__m_area_tree.close0_()
            self.__m_area_tree = (None)
        if (self.__m_house_table is not None): 
            self.__m_house_table._close()
            self.__m_house_table = (None)
        if (self.__m_room_table is not None): 
            self.__m_room_table._close()
            self.__m_room_table = (None)
        if (self.__m_houses_in_ao is not None): 
            self.__m_houses_in_ao._close()
            self.__m_houses_in_ao = (None)
        if (self.__m_rooms_in_house is not None): 
            self.__m_rooms_in_house._close()
            self.__m_rooms_in_house = (None)
        if (self.__m_rooms_in_rooms is not None): 
            self.__m_rooms_in_rooms._close()
            self.__m_rooms_in_rooms = (None)
        if (self.__m_zip_ao is not None): 
            self.__m_zip_ao._close()
            self.__m_zip_ao = (None)
        if (self.__m_addr_params is not None): 
            self.__m_addr_params._close()
            self.__m_addr_params = (None)
        if (self.__m_house_params is not None): 
            self.__m_house_params._close()
            self.__m_house_params = (None)
        if (self.__m_room_params is not None): 
            self.__m_room_params._close()
            self.__m_room_params = (None)
        for kp in self.__m_params_maps.items(): 
            kp[1].close0_()
        self.__m_params_maps.clear()
        self.__m_area_guids = (None)
        self.__m_area_name_pos = (None)
        self.__m_area_name_data = (None)
    
    def collect(self) -> None:
        if (self.__m_area_tree is not None): 
            self.__m_area_tree.collect()
        for kp in self.__m_params_maps.items(): 
            kp[1].collect()
    
    def clear(self) -> None:
        pass
    
    @property
    def out_log(self) -> bool:
        return self.__outlog
    @out_log.setter
    def out_log(self, value) -> bool:
        self.__outlog = value
        return self.__outlog
    
    def close(self) -> None:
        self._close()
    
    def find_by_param(self, ty : 'GarParam', value : str) -> typing.List[int]:
        p = None
        wrapp39 = RefOutArgWrapper(None)
        inoutres40 = Utils.tryGetValue(self.__m_params_maps, ty, wrapp39)
        p = wrapp39.value
        if (not inoutres40): 
            return None
        if (ty == GarParam.GUID): 
            value = value.lower()
        elif (ty == GarParam.KADASTERNUMBER): 
            value = value.replace('-', ':')
            if (value.find(':') > 0): 
                value = value.replace(" ", "")
            else: 
                value = value.replace(' ', ':')
        tn = p.find(value)
        if (tn is None or tn.ids is None): 
            return None
        res = list()
        for ui in tn.ids: 
            pars = None
            if ((((ui) & 0x80000000)) == 0): 
                pars = self.getaoparams(ui)
            elif ((((ui) & 0x40000000)) == 0): 
                if (ty == GarParam.GUID): 
                    ho = self.get_house(((ui) & 0x3FFFFFFF))
                    if (ho is not None and ho.guid == value): 
                        res.append(ui)
                    continue
                pars = self.get_house_params(((ui) & 0x3FFFFFFF))
            else: 
                if (ty == GarParam.GUID): 
                    ho = self.get_room(((ui) & 0x3FFFFFFF))
                    if (ho is not None and ho.guid == value): 
                        res.append(ui)
                    continue
                pars = self.get_room_params(((ui) & 0x3FFFFFFF))
            if (pars is None): 
                continue
            val = None
            wrapval37 = RefOutArgWrapper(None)
            inoutres38 = Utils.tryGetValue(pars, ty, wrapval37)
            val = wrapval37.value
            if (not inoutres38): 
                continue
            if (val == value): 
                res.append(ui)
        return res
    
    def get_parent_id(self, sid : str) -> int:
        iid = 0
        wrapiid41 = RefOutArgWrapper(0)
        inoutres42 = Utils.tryParseInt(sid[1:], wrapiid41)
        iid = wrapiid41.value
        if (not inoutres42): 
            return 0
        if (iid < 0): 
            return 0
        if (sid[0] == 'a'): 
            with self.__m_addr_table.m_lock: 
                return self.__m_addr_table.get_parent_id(iid)
        if (sid[0] == 'h'): 
            with self.__m_house_table.m_lock: 
                return self.__m_house_table.get_parent_id(iid)
        if (sid[0] == 'r'): 
            with self.__m_room_table.m_lock: 
                return self.__m_room_table.get_parent_id(iid)
        return 0
    
    def get_status(self, id0__ : int) -> 'GarStatus':
        return self.__m_addr_table.get_status(id0__)
    
    def get_house_status(self, id0__ : int) -> 'GarStatus':
        return self.__m_house_table.get_status(id0__)
    
    def get_actual(self, sid : str) -> int:
        iid = 0
        wrapiid43 = RefOutArgWrapper(0)
        inoutres44 = Utils.tryParseInt(sid[1:], wrapiid43)
        iid = wrapiid43.value
        if (not inoutres44): 
            return -1
        if (iid < 0): 
            return -1
        if (sid[0] == 'a'): 
            with self.__m_addr_table.m_lock: 
                return self.__m_addr_table.get_actual(iid)
        if (sid[0] == 'h'): 
            with self.__m_house_table.m_lock: 
                return self.__m_house_table.get_actual(iid)
        if (sid[0] == 'r'): 
            with self.__m_room_table.m_lock: 
                return self.__m_room_table.get_actual(iid)
        return 0
    
    def getaoguid(self, id0__ : int) -> str:
        pos = id0__ * 16
        if (self.__m_area_guids is None or (pos < 0) or (pos + 16) > len(self.__m_area_guids)): 
            return None
        dat = Utils.newArrayOfBytes(16, 0)
        for i in range(16):
            dat[i] = self.__m_area_guids[pos + i]
        g = uuid.UUID(bytes_le=bytes(dat))
        return str(g)
    
    def getaoname(self, id0__ : int) -> str:
        pos = id0__ * 4
        if ((pos < 0) or self.__m_area_name_pos is None or (pos + 4) > len(self.__m_area_name_pos)): 
            return None
        ind = int.from_bytes(self.__m_area_name_pos[pos:pos+4], byteorder="little")
        if ((ind < 0) or self.__m_area_name_data is None or ind >= len(self.__m_area_name_data)): 
            return None
        return FiasHelper.decode_string1251(self.__m_area_name_data, ind, -1, True)
    
    def getaoproxy(self, id0__ : int) -> 'AreaTreeObject':
        if (self.__m_area_tree is None): 
            return None
        with self.__m_area_tree.m_lock: 
            return self.__m_area_tree.get_obj(id0__)
    
    def getao(self, id0__ : int) -> 'AreaObject':
        if (self.__m_addr_table is None): 
            return None
        with self.__m_addr_table.m_lock: 
            ao = AreaObject._new45(id0__)
            if (self.__m_addr_table.get(id0__, ao, self.__m_types)): 
                return ao
            else: 
                return None
    
    def getaochildren(self, ao : 'AreaObject') -> typing.List['AreaObject']:
        if (ao is None or ao.children_ids is None or len(ao.children_ids) == 0): 
            return None
        res = list()
        with self.__m_addr_table.m_lock: 
            for uid in ao.children_ids: 
                mm = (uid) & (AreaObject.ROOMMASK)
                if (mm != (0)): 
                    continue
                ao1 = AreaObject._new45(uid)
                if (self.__m_addr_table.get(ao1.id0_, ao1, self.__m_types)): 
                    res.append(ao1)
        return res
    
    def getaoby_reg(self, reg_id : int) -> 'AreaObject':
        res = None
        wrapres47 = RefOutArgWrapper(None)
        inoutres48 = Utils.tryGetValue(self.__m_ao_by_regs, reg_id, wrapres47)
        res = wrapres47.value
        if (inoutres48): 
            return res
        return None
    
    def getaoparams(self, id0__ : int) -> typing.List[tuple]:
        if (self.__m_addr_params is None): 
            return None
        with self.__m_addr_params.m_lock: 
            return self.__m_addr_params.get_params(id0__)
    
    def putaoparams(self, id0__ : int, pars : typing.List[tuple]) -> None:
        if (self.__m_addr_params is None): 
            return
        self.__m_addr_params.put_params(id0__, pars, False)
    
    def flush_all_params(self) -> None:
        self.__m_addr_params.flush()
        self.__m_house_params.flush()
        self.__m_room_params.flush()
    
    def putao(self, ao : 'AreaObject', only_attrs : bool=False) -> bool:
        if (self.__m_addr_table is None): 
            return False
        if (ao.id0_ == 0): 
            ao.id0_ = (self.__m_addr_table.get_max_key() + 1)
        self.__m_addr_table.add(ao.id0_, ao, only_attrs)
        return True
    
    def getaohouses(self, id0__ : int) -> 'HousesInStreet':
        if (self.__m_houses_in_ao is None): 
            return None
        dat = None
        with self.__m_houses_in_ao.m_lock: 
            dat = self.__m_houses_in_ao.read_key_data(id0__, 0)
        if (dat is None): 
            return None
        try: 
            res = HousesInStreet()
            res.load(dat)
            return res
        except Exception as ex: 
            return None
    
    def putaohouses(self, id0__ : int, dat : bytearray) -> None:
        self.__m_houses_in_ao.write_key_data(id0__, dat)
    
    def get_house(self, id0__ : int) -> 'HouseObject':
        if (self.__m_house_table is None): 
            return None
        with self.__m_house_table.m_lock: 
            ao = HouseObject._new49(id0__)
            if (self.__m_house_table.get(id0__, ao)): 
                return ao
            else: 
                return None
    
    def put_house(self, ao : 'HouseObject') -> bool:
        if (self.__m_house_table is None): 
            return False
        if (ao.parent_id == 0): 
            return False
        if (ao.id0_ == 0): 
            ao.id0_ = (self.__m_house_table.get_max_key() + 1)
        self.__m_house_table.add(ao.id0_, ao)
        return True
    
    def get_house_params(self, id0__ : int) -> typing.List[tuple]:
        if (self.__m_house_params is None): 
            return None
        with self.__m_house_params.m_lock: 
            return self.__m_house_params.get_params(id0__)
    
    def put_house_params(self, id0__ : int, pars : typing.List[tuple]) -> None:
        if (self.__m_house_params is None): 
            return
        self.__m_house_params.put_params(id0__, pars, False)
    
    def get_house_rooms(self, id0__ : int) -> 'RoomsInHouse':
        if (self.__m_rooms_in_house is None): 
            return None
        dat = None
        with self.__m_rooms_in_house.m_lock: 
            dat = self.__m_rooms_in_house.read_key_data(id0__, 0)
        if (dat is None): 
            return None
        try: 
            res = RoomsInHouse()
            res.load(dat)
            return res
        except Exception as ex: 
            return None
    
    def put_house_rooms(self, id0__ : int, rih : 'RoomsInHouse') -> None:
        if (rih is not None and rih.count > 0): 
            self.__m_rooms_in_house.write_key_data(id0__, rih.save())
    
    def put_string_entries(self, ao : 'AreaObject', na : 'NameAnalyzer') -> None:
        if ((ao.id0_ == 0 or na.status == GarStatus.ERROR or na.strings is None) or len(na.strings) == 0): 
            return
        if (na.status != GarStatus.OK2 and na.sec is not None): 
            return
        if (ao.id0_ == 25799): 
            pass
        ao.status = na.status
        is_street = na.level == AddrLevel.STREET or na.level == AddrLevel.TERRITORY
        for str0_ in na.strings: 
            if (ao.region > (0)): 
                self.__m_area_tree.add("{0}${1}".format(str0_, ao.region), ao, na)
            self.__m_area_tree.add(str0_, ao, na)
        if (na.strings_ex is not None): 
            for str0_ in na.strings_ex: 
                self.__m_area_tree.add(str0_, ao, na)
    
    def clear_string_entries(self) -> None:
        self.__m_area_tree.children = dict()
    
    def get_all_string_entries_by_start(self, start : str, adj : str, number : str, street : bool, reg_id : int) -> typing.List['AreaTreeObject']:
        res = list()
        suff = None
        if (adj is not None and number is not None): 
            suff = "{0}{1}".format(adj, number)
        elif (adj is not None): 
            suff = "{0}".format(adj)
        elif (number is not None): 
            suff = number
        root = None
        with self.__m_area_tree.m_lock: 
            if (suff is not None): 
                root = self.__m_area_tree.find(suff + start, False, True, False)
                if (root is None): 
                    root = self.__m_area_tree.find(suff + start, True, False, False)
                if (root is not None): 
                    suff = (None)
            if (root is None): 
                root = self.__m_area_tree.find(start, False, True, False)
            if (root is None): 
                root = self.__m_area_tree.find(start, True, False, False)
            ids = list()
            if (root is not None): 
                self.__m_area_tree.get_all_obj_ids(root, suff, street, ids)
            ids.sort()
            i = 0
            first_pass3248 = True
            while True:
                if first_pass3248: first_pass3248 = False
                else: i += 1
                if (not (i < len(ids))): break
                if (i > 0 and ids[i] == ids[i - 1]): 
                    continue
                o = self.__m_area_tree.get_obj(ids[i])
                if (o is None): 
                    continue
                if (reg_id != 0 and o.region != (reg_id)): 
                    continue
                if (street): 
                    if (AddressHelper.compare_levels(o.level, AddrLevel.TERRITORY) < 0): 
                        continue
                elif (AddressHelper.compare_levels(o.level, AddrLevel.TERRITORY) > 0): 
                    continue
                res.append(o)
        return res
    
    def _check_name(self, name : str, is_street : bool) -> bool:
        if (self.__m_area_tree is None): 
            return False
        with self.__m_area_tree.m_lock: 
            li = self.__m_area_tree.find(name, False, False, False)
            if (li is not None and li.obj_ids is not None and len(li.obj_ids) > 0): 
                return True
        return False
    
    def _get_string_entries(self, na : 'NameAnalyzer', regions : bytearray, par_ids : typing.List[int], max_count : int) -> typing.List['AreaTreeObject']:
        if (na is None or self.__m_area_tree is None): 
            return None
        if (regions is None or len(regions) == 0): 
            return self.__get_string_entriesr(na, 0, par_ids, max_count)
        if (len(regions) == 1): 
            return self.__get_string_entriesr(na, regions[0], par_ids, max_count)
        res = None
        for reg in regions: 
            re = self.__get_string_entriesr(na, reg, par_ids, max_count)
            if (re is None): 
                continue
            if (res is None): 
                res = re
            else: 
                res.extend(re)
            if (len(res) >= max_count): 
                break
        return res
    
    def __get_string_entriesr(self, na : 'NameAnalyzer', region : int, par_ids : typing.List[int], max_count : int) -> typing.List['AreaTreeObject']:
        if (na.strings is None): 
            return None
        is_street = na.level == AddrLevel.STREET or na.level == AddrLevel.TERRITORY
        res = None
        res2 = None
        with self.__m_area_tree.m_lock: 
            for k in range(3):
                if (na.strict_search and k > 0): 
                    break
                strs = (na.doubt_strings if k == 2 else na.strings)
                for s in strs: 
                    li = None
                    ss = s
                    if (region != (0)): 
                        ss = "{0}${1}".format(s, region)
                    li = self.__m_area_tree.find(ss, k == 1, False, k == 1)
                    if (li is not None and li.obj_ids is not None): 
                        for oid in li.obj_ids: 
                            if (len(li.obj_ids) > 1000 and region == (0)): 
                                return None
                            if (oid == 624846): 
                                pass
                            o = self.__m_area_tree.get_obj(oid)
                            if (o is None): 
                                continue
                            if (o.region == (52)): 
                                pass
                            if (region != (0) and o.region != region and o.region != (0)): 
                                continue
                            ok = False
                            ok2 = False
                            if (par_ids is None or len(par_ids) == 0): 
                                ok = True
                            elif (o.id0_ in par_ids): 
                                pass
                            else: 
                                for id0__ in par_ids: 
                                    if (id0__ in o.parent_ids): 
                                        ok = True
                                        break
                                    elif (o.parent_parent_ids is not None and id0__ in o.parent_parent_ids): 
                                        ok2 = True
                            if (not ok and not ok2): 
                                continue
                            if (o.level != AddrLevel.STREET): 
                                pass
                            co = o.check_type(na)
                            if (co >= 0): 
                                if (not ok): 
                                    if (res2 is None): 
                                        res2 = list()
                                    exi = False
                                    for oo in res2: 
                                        if (oo.id0_ == o.id0_): 
                                            exi = True
                                            break
                                    if (not exi): 
                                        res2.append(o)
                                else: 
                                    if (res is None): 
                                        res = list()
                                    res.append(o)
                                    if (len(res) >= max_count): 
                                        return res
                            elif (na.level == AddrLevel.STREET and o.level == AddrLevel.STREET): 
                                ok2 = False
                                if (len(na.types) == 1 and na.types[0] == "улица"): 
                                    if ("блок" in o.typs or "ряд" in o.typs or "линия" in o.typs): 
                                        pass
                                    else: 
                                        ok2 = True
                                elif (len(o.typs) == 1 and o.typs[0] == "улица"): 
                                    if ("блок" in na.types or "ряд" in na.types or "линия" in na.types): 
                                        pass
                                    else: 
                                        ok2 = True
                                elif (len(na.types) == 1 and len(o.typs) == 1): 
                                    if (na.types[0] == "проезд" or na.types[0] == "переулок"): 
                                        if (o.typs[0] == "проезд" or o.typs[0] == "переулок"): 
                                            ok2 = True
                                if (ok2): 
                                    if (res2 is None): 
                                        res2 = list()
                                    exi = False
                                    for oo in res2: 
                                        if (oo.id0_ == o.id0_): 
                                            exi = True
                                            break
                                    if (not exi): 
                                        res2.append(o)
                            elif (na.level == AddrLevel.STREET and o.level == AddrLevel.TERRITORY): 
                                if (res2 is None): 
                                    res2 = list()
                                exi = False
                                for oo in res2: 
                                    if (oo.id0_ == o.id0_): 
                                        exi = True
                                        break
                                if (not exi): 
                                    res2.append(o)
                            elif ((na.level == AddrLevel.CITY and o.level == AddrLevel.LOCALITY and par_ids is not None) and len(par_ids) > 0): 
                                if (res2 is None): 
                                    res2 = list()
                                exi = False
                                for oo in res2: 
                                    if (oo.id0_ == o.id0_): 
                                        exi = True
                                        break
                                if (not exi): 
                                    res2.append(o)
                    if (res is not None): 
                        return res
                    if (res2 is not None and k == 0): 
                        if (s[len(s) - 1] == '@'): 
                            pass
                        else: 
                            return res2
        return Utils.ifNotNull(res, res2)
    
    def put_room(self, ro : 'RoomObject') -> bool:
        if (ro.house_id == (0)): 
            return False
        self.__m_room_table.add(ro.id0_, ro)
        if ((((ro.house_id) & 0x80000000)) != 0): 
            return True
        return True
    
    def get_room(self, id0__ : int) -> 'RoomObject':
        if (self.__m_room_table is None): 
            return None
        with self.__m_room_table.m_lock: 
            return self.__m_room_table.get(id0__)
    
    def exists_room(self, id0__ : int) -> bool:
        if (self.__m_room_table is None): 
            return False
        return self.__m_room_table.read_key_data_len(id0__) > 0
    
    def get_room_params(self, id0__ : int) -> typing.List[tuple]:
        if (self.__m_room_params is None): 
            return None
        with self.__m_room_params.m_lock: 
            return self.__m_room_params.get_params(id0__)
    
    def put_room_params(self, id0__ : int, pars : typing.List[tuple]) -> None:
        if (self.__m_room_params is None): 
            return
        self.__m_room_params.put_params(id0__, pars, False)
    
    def get_room_rooms(self, id0__ : int) -> 'RoomsInHouse':
        if (self.__m_rooms_in_rooms is None): 
            return None
        dat = None
        with self.__m_rooms_in_rooms.m_lock: 
            dat = self.__m_rooms_in_rooms.read_key_data(id0__, 0)
        if (dat is None): 
            return None
        try: 
            res = RoomsInHouse()
            res.load(dat)
            return res
        except Exception as ex: 
            return None
    
    def put_rooms_rooms(self, id0__ : int, rih : 'RoomsInHouse') -> None:
        if (rih is not None and rih.count > 0): 
            self.__m_rooms_in_rooms.write_key_data(id0__, rih.save())
    
    def get_rooms_in_house(self, house_id : int) -> 'RoomsInHouse':
        if (house_id == 0 or self.__m_rooms_in_house is None): 
            return None
        dat = None
        with self.__m_rooms_in_house.m_lock: 
            dat = self.__m_rooms_in_house.read_key_data(house_id, 0)
        if (dat is None): 
            return None
        res = RoomsInHouse()
        res.load(dat)
        return res
    
    def get_rooms_in_rooms(self, room_id : int) -> 'RoomsInHouse':
        if (room_id == 0 or self.__m_rooms_in_rooms is None): 
            return None
        dat = None
        with self.__m_rooms_in_rooms.m_lock: 
            dat = self.__m_rooms_in_rooms.read_key_data(room_id, 0)
        if (dat is None): 
            return None
        res = RoomsInHouse()
        res.load(dat)
        return res
    
    def get_ao_ids_by_zip(self, zip0_ : int) -> typing.List[int]:
        if (self.__m_zip_ao is None): 
            return None
        zip0_ -= 99999
        if (zip0_ < 1): 
            return None
        dat = None
        with self.__m_zip_ao.m_lock: 
            dat = self.__m_zip_ao.read_key_data(zip0_, 0)
        if (dat is None or (len(dat) < 4)): 
            return None
        res = list()
        ind = 0
        while ind < len(dat): 
            res.append(int.from_bytes(dat[ind:ind+4], byteorder="little"))
            ind += 4
        return res
    
    def add_zip_aos(self, zip0_ : int, li : typing.List[int]) -> None:
        if (self.__m_zip_ao is None): 
            return
        li0 = self.get_ao_ids_by_zip(zip0_)
        if (zip0_ == 452451): 
            li.sort()
        zip0_ -= 99999
        if (zip0_ < 1): 
            return
        res = bytearray()
        for id0__ in li: 
            res.extend((id0__).to_bytes(4, byteorder="little"))
        if (li0 is not None): 
            for id0__ in li0: 
                if (not id0__ in li): 
                    res.extend((id0__).to_bytes(4, byteorder="little"))
        self.__m_zip_ao.write_key_data(zip0_, bytearray(res))
    
    # static constructor for class FiasDatabase
    @staticmethod
    def _static_ctor():
        FiasDatabase.__m_param_types = [GarParam.KADASTERNUMBER, GarParam.KLADRCODE, GarParam.OKATO, GarParam.OKTMO, GarParam.POSTINDEX, GarParam.REESTERNUMBER, GarParam.GUID, GarParam.OBJECTID]

FiasDatabase._static_ctor()