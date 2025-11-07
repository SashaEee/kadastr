# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.StroenType import StroenType
from pullenti.address.HouseType import HouseType
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.address.AddrObject import AddrObject
from pullenti.address.GarLevel import GarLevel
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.GarStatus import GarStatus
from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.internal.gar.AreaObject import AreaObject
from pullenti.address.GarObject import GarObject

class GarHelper:
    
    REGIONS = None
    
    __m_lock = None
    
    GAR_INDEX = None
    
    @staticmethod
    def init(index_path : str) -> None:
        from pullenti.address.internal.gar.FiasDatabase import FiasDatabase
        GarHelper.REGIONS = list()
        if (GarHelper.GAR_INDEX is not None): 
            GarHelper.GAR_INDEX.close()
            GarHelper.GAR_INDEX = (None)
        if (index_path is not None): 
            if (not pathlib.Path(index_path).is_dir()): 
                raise Utils.newException("Directory '{0}' not exists".format(index_path), None)
            GarHelper.GAR_INDEX = FiasDatabase()
            GarHelper.GAR_INDEX.initialize(index_path)
        if (GarHelper.GAR_INDEX is None): 
            return
        robj = GarHelper.GAR_INDEX.getao(1)
        if (robj is None): 
            return
        ga = list()
        for id0_ in robj.children_ids: 
            ao = GarHelper.GAR_INDEX.getao(id0_)
            if (ao is None): 
                continue
            if (ao.level != (1)): 
                continue
            g = GarHelper.create_gar_area(ao)
            if ((isinstance(g.attrs, AreaAttributes)) and g.level == GarLevel.REGION): 
                ga.append(g)
        i = 0
        while i < (len(ga) - 1): 
            j = 0
            while j < (len(ga) - 1): 
                if (ga[j].compareTo(ga[j + 1]) < 0): 
                    h = ga[j]
                    ga[j] = ga[j + 1]
                    ga[j + 1] = h
                j += 1
            i += 1
        for g in ga: 
            GarHelper.REGIONS.append(g)
    
    @staticmethod
    def get_object(sid : str) -> 'GarObject':
        if (sid is None or GarHelper.GAR_INDEX is None): 
            return None
        iid = 0
        wrapiid141 = RefOutArgWrapper(0)
        inoutres142 = Utils.tryParseInt(sid[1:], wrapiid141)
        iid = wrapiid141.value
        if (not inoutres142): 
            return None
        if (sid[0] == 'a'): 
            if (iid < 1): 
                return None
            nam = GarHelper.GAR_INDEX.getaoname(iid)
            prox = GarHelper.GAR_INDEX.getaoproxy(iid)
            if (nam is None or prox is None): 
                ao = GarHelper.GAR_INDEX.getao(iid)
                if (ao is None): 
                    return None
                return GarHelper.create_gar_area(ao)
            aa = AreaAttributes()
            res = GarObject(aa)
            if (nam.find('+') < 0): 
                aa.names.append(nam)
            else: 
                aa.names.extend(Utils.splitString(nam, '+', False))
            res.region_number = (prox.region)
            ty = GarHelper.GAR_INDEX.get_addr_type(prox.typ_id)
            if (ty is not None): 
                aa.types.append(ty.name)
            if (prox.alt_typ_id > (0)): 
                ty = GarHelper.GAR_INDEX.get_addr_type(prox.alt_typ_id)
                if (ty is not None): 
                    aa.types.append(ty.name)
            res.status = prox.status
            for pid in prox.parent_ids: 
                res.parent_ids.append("a{0}".format(pid))
            res.expired = prox.expired
            res.level = prox.glevel
            res.guid = GarHelper.GAR_INDEX.getaoguid(iid)
            res.id0_ = sid
            res.children_count = (prox.ch_count)
            return res
        if (sid[0] == 'h'): 
            ho = GarHelper.GAR_INDEX.get_house(iid)
            if (ho is None): 
                return None
            return GarHelper.create_gar_house(ho)
        if (sid[0] == 'r'): 
            ho = GarHelper.GAR_INDEX.get_room(iid)
            if (ho is None): 
                return None
            return GarHelper.create_gar_room(ho)
        return None
    
    @staticmethod
    def get_object_params(sid : str) -> typing.List[tuple]:
        if (GarHelper.GAR_INDEX is None): 
            return None
        iid = 0
        wrapiid143 = RefOutArgWrapper(0)
        inoutres144 = Utils.tryParseInt(sid[1:], wrapiid143)
        iid = wrapiid143.value
        if (not inoutres144): 
            return None
        if (sid[0] == 'a'): 
            return GarHelper.GAR_INDEX.getaoparams(iid)
        if (sid[0] == 'h'): 
            return GarHelper.GAR_INDEX.get_house_params(iid)
        if (sid[0] == 'r'): 
            return GarHelper.GAR_INDEX.get_room_params(iid)
        return None
    
    @staticmethod
    def get_children_objects(id0_ : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        if (Utils.isNullOrEmpty(id0_)): 
            return list(GarHelper.REGIONS)
        res = GarHelper.get_children_objects_by_id(id0_, ignore_houses)
        if (res is not None): 
            for r in res: 
                if (id0_ is not None and not id0_ in r.parent_ids): 
                    r.parent_ids.append(id0_)
        return res
    
    @staticmethod
    def get_children_objects_by_id(sid : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        if (GarHelper.GAR_INDEX is None or Utils.isNullOrEmpty(sid)): 
            return None
        res = list()
        iid = 0
        wrapiid145 = RefOutArgWrapper(0)
        inoutres146 = Utils.tryParseInt(sid[1:], wrapiid145)
        iid = wrapiid145.value
        if (not inoutres146): 
            return None
        if (sid[0] == 'a'): 
            ao = GarHelper.GAR_INDEX.getao(iid)
            if (ao is None): 
                return None
            if (ao.children_ids is not None): 
                areas = list()
                houses = list()
                rooms = list()
                for id0_ in ao.children_ids: 
                    mm = (id0_) & (AreaObject.ROOMMASK)
                    if (mm == AreaObject.ROOMMASK): 
                        if (ignore_houses): 
                            continue
                        ro = GarHelper.GAR_INDEX.get_room(((id0_) ^ (AreaObject.ROOMMASK)))
                        if (ro is not None): 
                            rooms.append(ro)
                    elif (mm == AreaObject.HOUSEMASK): 
                        if (ignore_houses): 
                            continue
                        ho = GarHelper.GAR_INDEX.get_house(((id0_) ^ (AreaObject.HOUSEMASK)))
                        if (ho is not None): 
                            houses.append(ho)
                    else: 
                        ch = GarHelper.create_gar_aby_id(id0_)
                        if (ch is not None): 
                            areas.append(ch)
                i = 0
                while i < (len(areas) - 1): 
                    j = 0
                    while j < (len(areas) - 1): 
                        if (areas[j].compareTo(areas[j + 1]) < 0): 
                            h = areas[j]
                            areas[j] = areas[j + 1]
                            areas[j + 1] = h
                        j += 1
                    i += 1
                i = 0
                while i < (len(houses) - 1): 
                    j = 0
                    while j < (len(houses) - 1): 
                        if (houses[j].compareTo(houses[j + 1]) < 0): 
                            h = houses[j]
                            houses[j] = houses[j + 1]
                            houses[j + 1] = h
                        j += 1
                    i += 1
                for a in areas: 
                    res.append(a)
                for h in houses: 
                    gh = GarHelper.create_gar_house(h)
                    if (gh is not None): 
                        res.append(gh)
                for r in rooms: 
                    rh = GarHelper.create_gar_room(r)
                    if (rh is not None): 
                        res.append(rh)
            return res
        if (sid[0] == 'h'): 
            ho = GarHelper.GAR_INDEX.get_house(iid)
            if (ho is None or ho.room_ids is None): 
                return None
            rooms = list()
            for id0_ in ho.room_ids: 
                ro = GarHelper.GAR_INDEX.get_room(id0_)
                if (ro is not None): 
                    rooms.append(ro)
            i = 0
            while i < (len(rooms) - 1): 
                j = 0
                while j < (len(rooms) - 1): 
                    if (rooms[j].compareTo(rooms[j + 1]) > 0): 
                        r = rooms[j]
                        rooms[j] = rooms[j + 1]
                        rooms[j + 1] = r
                    j += 1
                i += 1
            for r in rooms: 
                gr = GarHelper.create_gar_room(r)
                if (gr is not None): 
                    res.append(gr)
        if (sid[0] == 'r'): 
            ho = GarHelper.GAR_INDEX.get_room(iid)
            if (ho is None or ho.children_ids is None): 
                return None
            rooms = list()
            for id0_ in ho.children_ids: 
                ro = GarHelper.GAR_INDEX.get_room(id0_)
                if (ro is not None): 
                    rooms.append(ro)
            i = 0
            while i < (len(rooms) - 1): 
                j = 0
                while j < (len(rooms) - 1): 
                    if (rooms[j].compareTo(rooms[j + 1]) > 0): 
                        r = rooms[j]
                        rooms[j] = rooms[j + 1]
                        rooms[j + 1] = r
                    j += 1
                i += 1
            for r in rooms: 
                gr = GarHelper.create_gar_room(r)
                if (gr is not None): 
                    res.append(gr)
        return res
    
    @staticmethod
    def create_gar_aby_id(id0_ : int) -> 'GarObject':
        aa = GarHelper.GAR_INDEX.getao(id0_)
        if (aa is None): 
            return None
        return GarHelper.create_gar_area(aa)
    
    @staticmethod
    def create_gar_area(a : 'AreaObject') -> 'GarObject':
        aa = AreaAttributes()
        ga = GarObject(aa)
        ga.id0_ = "a{0}".format(a.id0_)
        ga.status = (a.status)
        ga.internal_byte = a.gps_mask
        aa.names.extend(a.names)
        if (a.typ is not None): 
            aa.types.append(a.typ.name)
        if (a.old_typ is not None): 
            aa.types.append(a.old_typ.name)
        ga.level = (Utils.valToEnum(a.level, GarLevel))
        ga.expired = not a.actual
        ga.guid = a.guid
        ga.region_number = (a.region)
        if (a.children_ids is not None): 
            ga.children_count = len(a.children_ids)
        if (a.actual_obj_id > 0): 
            ga.actual_object_id = "a{0}".format(a.actual_obj_id)
        for ii in a.parent_ids: 
            ga.parent_ids.append("a{0}".format(ii))
        return ga
    
    @staticmethod
    def create_gar_house(a : 'HouseObject') -> 'GarObject':
        if (a is None): 
            return None
        sid = "h" + str(a.id0_)
        ha = HouseAttributes()
        ga = GarObject(ha)
        ga.id0_ = sid
        ga.internal_byte = a.gps_mask
        ha.number = a.house_number
        if (a.house_typ == (1)): 
            ha.typ = HouseType.ESTATE
        elif (a.house_typ == (2)): 
            ha.typ = HouseType.HOUSE
        elif (a.house_typ == (3)): 
            ha.typ = HouseType.HOUSEESTATE
        elif (a.house_typ == (4)): 
            ha.typ = HouseType.GARAGE
        elif (a.house_typ == (5)): 
            ha.typ = HouseType.BOILER
        elif (a.house_typ == (6)): 
            ha.typ = HouseType.MINE
        elif (a.house_typ == (7)): 
            ha.typ = HouseType.UNFINISHED
        ha.build_number = a.build_number
        ha.stroen_number = a.struc_number
        ha.stroen_typ = (Utils.valToEnum(a.struc_typ, StroenType))
        ha.plot_number = a.plot_number
        ga.level = (GarLevel.PLOT if a.is_plot else GarLevel.BUILDING)
        ga.expired = not a.actual
        ga.guid = a.guid
        ga.status = a.status
        ga.source_text = a.source_text
        if (a.status != GarStatus.OK): 
            ha.number = a.source_text
        if (a.parent_id > 0): 
            ga.parent_ids.append("a" + str(a.parent_id))
        if (a.alt_parent_id > 0): 
            ga.parent_ids.append("a" + str(a.alt_parent_id))
        ga.children_count = (0 if a.room_ids is None else len(a.room_ids))
        return ga
    
    @staticmethod
    def create_gar_room(a : 'RoomObject') -> 'GarObject':
        sid = "r" + str(a.id0_)
        ra = RoomAttributes()
        ga = GarObject(ra)
        ga.id0_ = sid
        ra.number = a.number
        ra.typ = a.typ
        ra.misc = a.misc
        ga.status = a.status
        if (a.status != GarStatus.OK): 
            ra.number = a.source_text
        ga.level = GarLevel.ROOM
        ga.expired = not a.actual
        ga.guid = a.guid
        ga.source_text = a.source_text
        if (a.children_ids is not None): 
            ga.children_count = len(a.children_ids)
        if (a.house_id != (0) and (((a.house_id) & 0x80000000)) == 0): 
            ga.parent_ids.append("h" + str(a.house_id))
        elif (a.house_id != (0) and (((a.house_id) & 0x80000000)) != 0): 
            id0_ = (a.house_id) & 0x7FFFFFFF
            ga.parent_ids.append("r" + str(id0_))
        return ga
    
    @staticmethod
    def create_addr_object(g : 'GarObject') -> 'AddrObject':
        res = AddrObject(g.attrs)
        res.is_reconstructed = True
        res.gars.append(g)
        aa = Utils.asObjectOrNull(res.attrs, AreaAttributes)
        if (aa is not None): 
            i = 0
            while i < len(aa.names): 
                nn = aa.names[i]
                if (nn.startswith("поселок ")): 
                    aa.names[i] = nn[8:]
                ii = nn.find('/')
                if (ii > 0): 
                    aa.names[i] = nn[0:0+ii].strip()
                i += 1
        if (g.level == GarLevel.REGION): 
            res.level = AddrLevel.REGIONAREA
            if ((isinstance(g.attrs, AreaAttributes)) and "город" in g.attrs.types): 
                res.level = AddrLevel.REGIONCITY
        elif (g.level == GarLevel.ADMINAREA or g.level == GarLevel.MUNICIPALAREA or g.level == GarLevel.DISTRICT): 
            res.level = AddrLevel.DISTRICT
        elif (g.level == GarLevel.SETTLEMENT): 
            res.level = AddrLevel.SETTLEMENT
        elif (g.level == GarLevel.CITY): 
            res.level = AddrLevel.CITY
        elif (g.level == GarLevel.LOCALITY): 
            res.level = AddrLevel.LOCALITY
        elif (g.level == GarLevel.AREA): 
            res.level = AddrLevel.TERRITORY
        elif (g.level == GarLevel.STREET): 
            res.level = AddrLevel.STREET
        elif (g.level == GarLevel.PLOT): 
            res.level = AddrLevel.PLOT
        elif (g.level == GarLevel.BUILDING): 
            res.level = AddrLevel.BUILDING
        elif (g.level == GarLevel.ROOM): 
            res.level = AddrLevel.APARTMENT
        else: 
            return None
        return res
    
    @staticmethod
    def try_parse_double(str0_ : str, res : float) -> bool:
        res.value = (0)
        if (Utils.isNullOrEmpty(str0_)): 
            return False
        inoutres149 = Utils.tryParseFloat(str0_, res)
        if (inoutres149): 
            return True
        inoutres148 = Utils.tryParseFloat(str0_.replace(',', '.'), res)
        if (str0_.find(',') >= 0 and inoutres148): 
            return True
        inoutres147 = Utils.tryParseFloat(str0_.replace('.', ','), res)
        if (str0_.find('.') >= 0 and inoutres147): 
            return True
        return False
    
    @staticmethod
    def add_miss_address_items(addr : 'TextAddress') -> None:
        from pullenti.address.internal.AnalyzeHelper import AnalyzeHelper
        ah = AnalyzeHelper()
        AnalyzeHelper._add_miss_items(ah, addr)
    
    # static constructor for class GarHelper
    @staticmethod
    def _static_ctor():
        GarHelper.REGIONS = list()
        GarHelper.__m_lock = object()

GarHelper._static_ctor()