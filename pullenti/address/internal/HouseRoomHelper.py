# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.internal.NumberItemClass import NumberItemClass
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.address.SearchParams import SearchParams
from pullenti.address.RoomType import RoomType
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.ner.TextToken import TextToken
from pullenti.address.ParamType import ParamType
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.address.DetailType import DetailType
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.address.AddrLevel import AddrLevel
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.address.StroenType import StroenType
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.address.HouseType import HouseType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.GarParam import GarParam
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.GarLevel import GarLevel
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.AddrObject import AddrObject
from pullenti.ner.geo.internal.NumToken import NumToken
from pullenti.address.AddressService import AddressService
from pullenti.address.internal.GarHelper import GarHelper

class HouseRoomHelper:
    
    @staticmethod
    def __get_nums_count(ha : 'HouseAttributes') -> int:
        if (ha is None): 
            return 0
        cou = 0
        if (ha.number is not None): 
            cou += 1
        if (ha.stroen_number is not None): 
            cou += 1
        if (ha.build_number is not None): 
            cou += 1
        if (ha.plot_number is not None): 
            cou += 1
        return cou
    
    @staticmethod
    def __get_house_type(ht : 'AddressHouseType') -> 'HouseType':
        if (ht == AddressHouseType.ESTATE): 
            return HouseType.ESTATE
        if (ht == AddressHouseType.HOUSE): 
            return HouseType.HOUSE
        if (ht == AddressHouseType.HOUSEESTATE): 
            return HouseType.HOUSEESTATE
        if (ht == AddressHouseType.SPECIAL): 
            return HouseType.SPECIAL
        if (ht == AddressHouseType.UNFINISHED): 
            return HouseType.UNFINISHED
        return HouseType.UNDEFINED
    
    @staticmethod
    def __get_stroen_type(bt : 'AddressBuildingType') -> 'StroenType':
        if (bt == AddressBuildingType.BUILDING): 
            return StroenType.BUILDING
        if (bt == AddressBuildingType.CONSTRUCTION): 
            return StroenType.CONSTRUCTION
        if (bt == AddressBuildingType.LITER): 
            return StroenType.LITER
        return StroenType.UNDEFINED
    
    @staticmethod
    def process_house_and_rooms(ah : 'AnalyzeHelper', ar : 'AddressReferent', addr : 'TextAddress') -> None:
        if (ar.box is not None and ((ar.house is not None or ar.building is not None or ar.corpus is not None))): 
            ar2 = AddressReferent()
            ar2.box = ar.box
            ar.box = None
            HouseRoomHelper.process_house_and_rooms(ah, ar, addr)
            ar.box = ar2.box
            HouseRoomHelper.process_house_and_rooms(ah, ar2, addr)
            return
        if (addr.last_item is None): 
            return
        add_nms = None
        if (ar.room is not None and ar.room.find(',') > 0): 
            add_nms = list(Utils.splitString(ar.room, ',', False))
            ar.room = add_nms[0]
        elif (ar.flat is not None and ar.flat.find(',') > 0): 
            add_nms = list(Utils.splitString(ar.flat, ',', False))
            ar.flat = add_nms[0]
        elif (ar.space is not None and ar.space.find(',') > 0): 
            add_nms = list(Utils.splitString(ar.space, ',', False))
            ar.space = add_nms[0]
        elif (ar.office is not None and ar.office.find(',') > 0): 
            add_nms = list(Utils.splitString(ar.office, ',', False))
            ar.office = add_nms[0]
        plot = None
        house = None
        add_house = None
        tr = None
        flat_num = None
        if (ar.field is not None and AddressHelper.compare_levels(addr.last_item.level, AddrLevel.TERRITORY) <= 0): 
            aa = AreaAttributes()
            aa.types.append("поле")
            aa.number = ar.field
            addr.items.append(AddrObject._new120(aa, AddrLevel.STREET))
        ao = None
        up_num = None
        for i in range(len(addr.items) - 1, -1, -1):
            ao0 = addr.items[i]
            if ((ao0.level == AddrLevel.TERRITORY or ao0.level == AddrLevel.STREET or ao0.level == AddrLevel.LOCALITY) or ao0.level == AddrLevel.CITY): 
                if (len(ao0.gars) > 0): 
                    ao = ao0
                    break
                if (ao0.level == AddrLevel.LOCALITY): 
                    break
                if (ao0.level == AddrLevel.STREET and not ao0.attrs.can_not_has_gar): 
                    if (i > 0 and len(addr.items[i - 1].gars) == 1 and addr.items[i - 1].gars[0].level == GarLevel.STREET): 
                        pass
                    else: 
                        break
                if (up_num is None): 
                    aaa = Utils.asObjectOrNull(ao0.attrs, AreaAttributes)
                    if (len(aaa.names) == 0 and aaa.number is not None): 
                        up_num = aaa.number
        house_gar_objects = None
        ar00 = Utils.asObjectOrNull(ar.clone(), AddressReferent)
        if (GarHelper.GAR_INDEX is not None and ao is not None and len(ao.gars) > 0): 
            hobjs = None
            for kk in range(2):
                for g in ao.gars: 
                    if (g.children_count == 0): 
                        continue
                    hinstr = ah.get_houses_in_street(g.id0_)
                    if (hinstr is None): 
                        continue
                    hobjs = (None)
                    has_slash = False
                    if (ah.litera_variant is not None and ar.building is None): 
                        arr = Utils.asObjectOrNull(ar.clone(), AddressReferent)
                        arr.building = ah.litera_variant.value
                        arr.building_type = AddressBuildingType.LITER
                        wraphas_slash151 = RefOutArgWrapper(has_slash)
                        hobjs = HouseRoomHelper.__find_houses_new(ah, hinstr, arr, (1 if ao.cross_object is not None else 0), up_num, wraphas_slash151)
                        has_slash = wraphas_slash151.value
                    if (hobjs is None): 
                        if (addr.items[len(addr.items) - 1].level == AddrLevel.STREET): 
                            aa = Utils.asObjectOrNull(addr.items[len(addr.items) - 1].attrs, AreaAttributes)
                            if (aa.number is not None and "блок" in aa.types and ar.box is not None): 
                                ar2 = Utils.asObjectOrNull(ar.clone(), AddressReferent)
                                ar2.box = "{0}/{1}".format(ar2.box, aa.number)
                                wraphas_slash152 = RefOutArgWrapper(has_slash)
                                hobjs = HouseRoomHelper.__find_houses_new(ah, hinstr, ar2, (1 if ao.cross_object is not None else 0), up_num, wraphas_slash152)
                                has_slash = wraphas_slash152.value
                        if (hobjs is None): 
                            wraphas_slash153 = RefOutArgWrapper(has_slash)
                            hobjs = HouseRoomHelper.__find_houses_new(ah, hinstr, ar, (1 if ao.cross_object is not None else 0), up_num, wraphas_slash153)
                            has_slash = wraphas_slash153.value
                    ar0 = ar
                    if (hobjs is not None): 
                        pass
                    if (hobjs is not None and ar.corpus_or_flat is None and ar00.corpus_or_flat is not None): 
                        if (ah.m_params is None or not ah.m_params.no_flats): 
                            ar1 = Utils.asObjectOrNull(ar00.clone(), AddressReferent)
                            ar1.corpus_or_flat = None
                            hsl = False
                            wraphsl154 = RefOutArgWrapper(hsl)
                            hobjs1 = HouseRoomHelper.__find_houses_new(ah, hinstr, ar1, (1 if ao.cross_object is not None else 0), up_num, wraphsl154)
                            hsl = wraphsl154.value
                            if (hobjs1 is not None): 
                                if (hobjs is not None and hobjs[0].id0_ == hobjs1[0].id0_): 
                                    pass
                                else: 
                                    addr.info_message = "Возможно, здесь '{0}' не корпус, а квартира.".format(ar00.corpus_or_flat)
                    if ((ar.flat is None and ar.corpus_or_flat is None and ao.cross_object is None) and ((ah.m_params is None or not ah.m_params.no_flats))): 
                        num = Utils.ifNotNull(ar.house, ar.house_or_plot)
                        ii = -1
                        hiph = False
                        if ((num is not None and ar.building is None and ar.corpus is None) and not has_slash and ((ah.m_params is None or not ah.m_params.strict_house_number))): 
                            ii = num.find('/')
                            if (((ii)) < 0): 
                                ii = num.find('-')
                                if (ii > 0): 
                                    hiph = True
                        if (hobjs is not None and HouseRoomHelper.__get_nums_count(Utils.asObjectOrNull(hobjs[0].attrs, HouseAttributes)) > 1): 
                            ii = -1
                        nn = 0
                        if (ii > 0): 
                            wrapnn155 = RefOutArgWrapper(0)
                            Utils.tryParseInt(num[ii + 1:], wrapnn155)
                            nn = wrapnn155.value
                        if (nn > 0 or ((ii > 0 and not hiph))): 
                            ar2 = AddressReferent()
                            ar2.house = num[0:0+ii]
                            ar2.flat = num[ii + 1:]
                            wraphas_slash156 = RefOutArgWrapper(has_slash)
                            hobjs2 = HouseRoomHelper.__find_houses_new(ah, hinstr, ar2, 0, up_num, wraphas_slash156)
                            has_slash = wraphas_slash156.value
                            if (hobjs2 is not None): 
                                hobjs = hobjs2
                                flat_num = num[ii + 1:]
                                ii = flat_num.find('-')
                                if (((ii)) > 0): 
                                    flat_num = flat_num[ii + 1:]
                                ar2.flat = flat_num
                                ar0 = ar2
                        elif (hiph): 
                            a1 = AddressReferent()
                            a1.house = num[ii + 1:]
                            wraphas_slash158 = RefOutArgWrapper(has_slash)
                            hobjs2 = HouseRoomHelper.__find_houses_new(ah, hinstr, a1, (1 if ao.cross_object is not None else 0), up_num, wraphas_slash158)
                            has_slash = wraphas_slash158.value
                            if (hobjs2 is not None and len(hobjs2) == 1): 
                                ao1 = AddrObject._new120(hobjs2[0].attrs, AddrLevel.BUILDING)
                                ao1.gars.append(hobjs2[0])
                                if (addr.additional_items is None): 
                                    addr.additional_items = list()
                                addr.additional_items.append(ao1)
                        elif (ar.plot is not None and hobjs is None and ((ar.house is not None or ar.building is not None or ar.corpus is not None))): 
                            ar2 = AddressReferent()
                            ar2.plot = ar.plot
                            wraphas_slash160 = RefOutArgWrapper(has_slash)
                            hobjs1 = HouseRoomHelper.__find_houses_new(ah, hinstr, ar2, (1 if ao.cross_object is not None else 0), up_num, wraphas_slash160)
                            has_slash = wraphas_slash160.value
                            ar3 = Utils.asObjectOrNull(ar.clone(), AddressReferent)
                            ar3.plot = None
                            wraphas_slash159 = RefOutArgWrapper(has_slash)
                            hobjs2 = HouseRoomHelper.__find_houses_new(ah, hinstr, ar3, (1 if ao.cross_object is not None else 0), up_num, wraphas_slash159)
                            has_slash = wraphas_slash159.value
                            if (hobjs1 is not None and hobjs2 is None): 
                                hobjs = hobjs1
                                ar0 = ar2
                            elif (hobjs2 is not None and hobjs1 is None): 
                                hobjs = hobjs2
                                ar0 = ar3
                    if (hobjs is not None): 
                        for gh in hobjs: 
                            if (gh.expired and ((ao.level == AddrLevel.CITY or ao.level == AddrLevel.LOCALITY))): 
                                continue
                            if (gh.attrs.plot_number is not None): 
                                if (plot is None): 
                                    plot = AddrObject._new120(gh.attrs.clone(), AddrLevel.PLOT)
                                plot.gars.append(gh)
                                continue
                            if (house is None): 
                                if (len(hobjs) == 1): 
                                    house = AddrObject._new120(gh.attrs.clone(), AddrLevel.BUILDING)
                                else: 
                                    if (house_gar_objects is None): 
                                        house_gar_objects = list()
                                    house_gar_objects.append(gh)
                            if (house is not None): 
                                house.gars.append(gh)
                                if (isinstance(gh.tag, list)): 
                                    gobjs2 = Utils.asObjectOrNull(gh.tag, list)
                                    add_house = AddrObject._new120(gobjs2[0].attrs.clone(), AddrLevel.BUILDING)
                                    add_house.gars.extend(gobjs2)
                                if (ar.house is not None and ar.flat is not None): 
                                    if (gh.attrs.number == "{0}/{1}".format(ar.house, ar.flat)): 
                                        ar.flat = None
                            if (house is not None and ar.corpus_or_flat is not None and gh.attrs.build_number == ar.corpus_or_flat): 
                                ar.corpus_or_flat = None
                                ar.corpus = gh.attrs.build_number
                            elif (gh.children_count > 0): 
                                rih = ah.get_rooms_in_object(gh.id0_)
                                gg = HouseRoomHelper.__find_room_new(ah, rih, ar0)
                                if (gg is not None): 
                                    if (tr is None): 
                                        tr = AddrObject._new120(gg.attrs, AddrLevel.APARTMENT)
                                    tr.gars.append(gg)
                if (ao.cross_object is not None): 
                    num = Utils.ifNotNull(ar.house, ar.house_or_plot)
                    for g in ao.cross_object.gars: 
                        if (g.children_count == 0): 
                            continue
                        hinstr = ah.get_houses_in_street(g.id0_)
                        if (hinstr is None): 
                            continue
                        bb = False
                        wrapbb168 = RefOutArgWrapper(bb)
                        hobjs = HouseRoomHelper.__find_houses_new(ah, hinstr, ar, 2, None, wrapbb168)
                        bb = wrapbb168.value
                        ah.index_read_count += 1
                        if (hobjs is not None): 
                            for gh in hobjs: 
                                if (house is None): 
                                    if (num is None or (num.find('/') < 0)): 
                                        continue
                                    house = AddrObject._new120(gh.attrs.clone(), AddrLevel.BUILDING)
                                    house.attrs.number = num[0:0+num.find('/')]
                                if (house.cross_object is None): 
                                    house.cross_object = AddrObject._new120(gh.attrs, AddrLevel.BUILDING)
                                house.cross_object.gars.append(gh)
                                gg = HouseRoomHelper.__find_room_new(ah, ah.get_rooms_in_object(gh.id0_), ar)
                                if (gg is not None): 
                                    if (tr is None): 
                                        tr = AddrObject._new120(gg.attrs, AddrLevel.APARTMENT)
                                    tr.gars.append(gg)
                    if (house is not None and house.cross_object is None): 
                        if (num is not None and num.find('/') > 0): 
                            house.cross_object = AddrObject._new120(house.attrs.clone(), AddrLevel.BUILDING)
                            house.cross_object.attrs.number = num[num.find('/') + 1:]
                if (hobjs is not None): 
                    break
                i = Utils.indexOfList(addr.items, ao, 0)
                if (i > 0 and addr.items[i - 1].level == AddrLevel.LOCALITY and len(addr.items[i - 1].gars) > 0): 
                    ao = addr.items[i - 1]
                else: 
                    break
        if (tr is not None and house_gar_objects is not None): 
            i = 0
            while i < len(house_gar_objects): 
                ok = False
                for gg in tr.gars: 
                    if (house_gar_objects[i].id0_ in gg.parent_ids): 
                        ok = True
                if (not ok): 
                    del house_gar_objects[i]
                    i -= 1
                i += 1
            if (len(house_gar_objects) == 1): 
                house = AddrObject._new120(house_gar_objects[0].attrs.clone(), AddrLevel.BUILDING)
                house.gars.append(house_gar_objects[0])
                house_gar_objects = (None)
        if (plot is not None and house is not None): 
            if (ar.house_or_plot is not None): 
                plot = (None)
        if (ar.plot is not None and ((ar.house is not None or ar.building is not None or ar.corpus is not None))): 
            aa = None
            if (plot is not None and len(plot.gars) > 0): 
                aa = (Utils.asObjectOrNull(plot.gars[0].attrs, HouseAttributes))
            if (aa is not None and ((aa.build_number is not None or aa.stroen_number is not None or aa.number is not None))): 
                pass
            else: 
                ar2 = AddressReferent()
                ar2.plot = ar.plot
                ar.plot = None
                HouseRoomHelper.process_house_and_rooms(ah, ar2, addr)
                HouseRoomHelper.process_house_and_rooms(ah, ar, addr)
                ar.plot = ar2.plot
                return
        if (plot is None and ar.plot is not None): 
            plot = AddrObject._new120(HouseAttributes._new171(("б/н" if ar.plot == "0" else ar.plot)), AddrLevel.PLOT)
        if (plot is not None): 
            plot._sort_gars()
            addr.items.append(plot)
            if (len(plot.gars) == 0 and ar.plot is not None and len(ar.plot) > 12): 
                sp = SearchParams._new173(GarParam.KADASTERNUMBER, ar.plot)
                sr = AddressService.search_objects(sp)
                if (len(sr.objects) == 1 and sr.objects[0].level == GarLevel.PLOT): 
                    plot.attrs = sr.objects[0].attrs.clone()
                    plot.gars.append(sr.objects[0])
        if (house is None and plot is None): 
            if (ar.house is not None): 
                house = AddrObject(HouseAttributes._new174(HouseRoomHelper.__get_house_type(ar.house_type), ("б/н" if ar.house == "0" else ar.house)))
            if (ar.house_or_plot is not None): 
                house = AddrObject(HouseAttributes._new174(HouseType.UNDEFINED, ("б/н" if ar.house_or_plot == "0" else ar.house_or_plot)))
            if (ar.building is not None and ((ar.building != "0" or house is None))): 
                if (house is None): 
                    house = AddrObject._new120(HouseAttributes(), AddrLevel.BUILDING)
                house.attrs.stroen_number = ("б/н" if ar.building == "0" else ar.building)
                house.attrs.stroen_typ = HouseRoomHelper.__get_stroen_type(ar.building_type)
            if (ar.corpus is not None and ((ar.corpus != "0" or house is None))): 
                if (house is None): 
                    house = AddrObject._new120(HouseAttributes(), AddrLevel.BUILDING)
                house.attrs.build_number = ("б/н" if ar.corpus == "0" else ar.corpus)
            if (house is None and ar.box is not None): 
                house = AddrObject(HouseAttributes._new174(HouseType.GARAGE, ("б/н" if ar.box == "0" else ar.box)))
            if (house is None and ar.well is not None): 
                house = AddrObject(HouseAttributes._new174(HouseType.WELL, ("б/н" if ar.well == "0" else ar.well)))
            if (house is not None): 
                house.level = AddrLevel.BUILDING
                if (house.attrs.typ == HouseType.UNDEFINED and house.attrs.number is not None): 
                    it = addr.find_item_by_level(AddrLevel.TERRITORY)
                    if (it is not None): 
                        aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
                        for m in aa.miscs: 
                            if ("гараж" in m): 
                                house.attrs.typ = HouseType.GARAGE
                                break
                if (ar.corpus_or_flat is not None): 
                    if (ah.m_params is not None and ah.m_params.no_flats): 
                        house.attrs.build_number = ar.corpus_or_flat
                    else: 
                        ar.flat = ar.corpus_or_flat
                        ar.corpus_or_flat = None
                if (house_gar_objects is not None): 
                    house.gars.extend(house_gar_objects)
        if (house is not None): 
            if (ao is not None and ao.cross_object is not None and house.cross_object is None): 
                num = house.attrs.number
                if (num is not None and num.find('/') > 0): 
                    house.cross_object = AddrObject(house.attrs.clone())
                    house.attrs.number = num[0:0+num.find('/')]
                    house.cross_object.attrs.number = num[num.find('/') + 1:]
            house._sort_gars()
            addr.items.append(house)
            if (add_house is not None): 
                if (addr.additional_items is None): 
                    addr.additional_items = list()
                addr.additional_items.append(add_house)
            if (house.attrs.typ == HouseType.SPECIAL and ar.well is not None): 
                addr.items.append(AddrObject._new120(HouseAttributes._new174(HouseType.WELL, ("б/н" if ar.well == "0" else ar.well)), AddrLevel.BUILDING))
        if (tr is None): 
            ra = HouseRoomHelper.create_apartment_attrs(ar, flat_num)
            if (ra is not None): 
                tr = AddrObject(ra)
                tr.level = AddrLevel.APARTMENT
        if (tr is not None): 
            tr._sort_gars()
            addr.items.append(tr)
            if (ar.carplace is not None and tr.attrs.typ != RoomType.CARPLACE): 
                addr.items.append(AddrObject._new120(RoomAttributes._new182(RoomType.CARPLACE, ar.carplace), AddrLevel.ROOM))
        if (ar.room is not None or ((ar.flat is not None and ar.space is not None))): 
            ra = RoomAttributes()
            room = AddrObject(ra)
            room.level = AddrLevel.ROOM
            ar0 = AddressReferent()
            if (ar.room is not None): 
                ra.typ = RoomType.ROOM
                ra.number = ar.room
                ar0.room = ar.room
            else: 
                ra.typ = RoomType.SPACE
                ra.number = ar.space
                ar0.space = ar.space
            if (str(room) == str(addr.last_item)): 
                room = addr.last_item
            else: 
                addr.items.append(room)
            if (tr is not None and len(tr.gars) == 1): 
                rih = ah.get_rooms_in_object(tr.gars[0].id0_)
                gg = HouseRoomHelper.__find_room_new(ah, rih, ar0)
                if (gg is not None): 
                    room.gars.append(gg)
        if (add_nms is not None): 
            del add_nms[0]
            HouseRoomHelper.__add_additional_numbers(ah, addr, add_nms)
    
    @staticmethod
    def create_apartment_attrs(ar : 'AddressReferent', flat_num : str) -> 'RoomAttributes':
        ra = RoomAttributes()
        if (ar.flat is not None): 
            ra.number = ar.flat
            ra.typ = RoomType.FLAT
        elif (ar.office is not None): 
            ra.number = ar.office
            ra.typ = RoomType.OFFICE
        elif (ar.space is not None): 
            ra.number = ar.space
            ra.typ = RoomType.SPACE
            ra.misc = ar.space_type
        elif (ar.room is not None): 
            ra.number = ar.room
            ra.typ = RoomType.ROOM
        elif (ar.pavilion is not None): 
            ra.number = ar.pavilion
            ra.typ = RoomType.PAVILION
        elif (ar.carplace is not None): 
            ra.number = ar.carplace
            ra.typ = RoomType.CARPLACE
        elif (flat_num is not None): 
            ra.number = flat_num
            ra.typ = RoomType.FLAT
        else: 
            return None
        if (ra.number == "НЕТ"): 
            return None
        if (ra.number == "0"): 
            ra.number = (None)
        return ra
    
    @staticmethod
    def __get_id(v : str) -> int:
        return int(v[1:])
    
    @staticmethod
    def __find_houses_new(ah : 'AnalyzeHelper', hinst : 'HousesInStreet', a : 'AddressReferent', cross_num : int, up_num : str, houses_has_slash : bool) -> typing.List['GarObject']:
        if (a.plot is None or a.house is None or a.plot == a.house): 
            inoutres184 = HouseRoomHelper.__find_houses_new0(ah, hinst, a, cross_num, up_num, houses_has_slash)
            return inoutres184
        pl = AddressReferent()
        pl.plot = a.plot
        res1 = HouseRoomHelper.__find_houses_new0(ah, hinst, pl, cross_num, up_num, houses_has_slash)
        a.plot = None
        res2 = HouseRoomHelper.__find_houses_new0(ah, hinst, a, cross_num, up_num, houses_has_slash)
        a.plot = pl.plot
        if (res1 is None): 
            return res2
        if (res2 is None): 
            return res1
        res1.extend(res2)
        return res1
    
    @staticmethod
    def __find_houses_new0(ah : 'AnalyzeHelper', hinst : 'HousesInStreet', a : 'AddressReferent', cross_num : int, up_num : str, houses_has_slash : bool) -> typing.List['GarObject']:
        from pullenti.address.internal.NumberAnalyzer import NumberAnalyzer
        if (hinst is None): 
            return None
        if (cross_num > 0 and ((a.house is not None or a.house_or_plot is not None))): 
            nnn = Utils.ifNotNull(a.house, a.house_or_plot)
            ii = nnn.find('/')
            if (ii > 0): 
                ar1 = AddressReferent()
                ar1.house = (nnn[0:0+ii] if cross_num == 1 else nnn[ii + 1:])
                res1 = HouseRoomHelper.__find_houses_new0(ah, hinst, ar1, 0, None, houses_has_slash)
                if (res1 is not None): 
                    if (cross_num == 1): 
                        res0 = HouseRoomHelper.__find_houses_new0(ah, hinst, a, 0, None, houses_has_slash)
                        if (res0 is not None and res0[0]._internal_tag >= res1[0]._internal_tag): 
                            return res0
                    return res1
        if (a.corpus_or_flat is not None): 
            aa1 = Utils.asObjectOrNull(a.clone(), AddressReferent)
            aa1.corpus_or_flat = None
            aa1.corpus = a.corpus_or_flat
            res1 = HouseRoomHelper.__find_houses_new0(ah, hinst, aa1, cross_num, None, houses_has_slash)
            aa1.corpus = None
            res2 = HouseRoomHelper.__find_houses_new0(ah, hinst, aa1, cross_num, None, houses_has_slash)
            if (res1 is not None): 
                if (res2 is None or (res2[0]._internal_tag < (res1[0]._internal_tag - 0.1)) or ((ah.m_params is not None and ah.m_params.no_flats))): 
                    a.corpus = a.corpus_or_flat
                    a.corpus_or_flat = None
                    return res1
            if (res2 is not None): 
                a.flat = a.corpus_or_flat
                a.corpus_or_flat = None
                return res2
            a.flat = a.corpus_or_flat
            a.corpus_or_flat = None
            return None
        if (a.house is not None and a.house.find('-') > 0): 
            ii = a.house.find('-')
            a1 = AddressReferent()
            a1.house = a.house[0:0+ii]
            a2 = AddressReferent()
            a2.house = a.house[ii + 1:]
            if (Utils.compareStrings(a1.house, a2.house, False) < 0): 
                res1 = HouseRoomHelper.__find_houses_new0(ah, hinst, a1, 0, None, houses_has_slash)
                res2 = HouseRoomHelper.__find_houses_new0(ah, hinst, a2, 0, None, houses_has_slash)
                if (res1 is not None and res2 is not None): 
                    res1[0].tag = (res2)
                    return res1
            if (a.flat is None): 
                res1 = HouseRoomHelper.__find_houses_new0(ah, hinst, a1, 0, None, houses_has_slash)
                if (res1 is not None): 
                    a.flat = a.house[ii + 1:]
                    return res1
        num = NumberAnalyzer.try_parse_referent(a, True)
        res = None
        max0_ = 0
        comp_not_equal = False
        for k in range(3):
            if (k > 0): 
                if (up_num is None): 
                    break
                if (a.plot is None): 
                    break
                aa = AddressReferent()
                aa.plot = ("{0}/{1}".format(up_num, a.plot) if k == 1 else "{0}/{1}".format(a.plot, up_num))
                num = NumberAnalyzer.try_parse_referent(aa, True)
            if (num is None): 
                continue
            hos = hinst.get_houses(num)
            if (hos is None or len(hos) == 0): 
                continue
            for ho in hos: 
                num1 = NumberAnalyzer.try_parseho(ho)
                if (num1 is None): 
                    continue
                for nn in num1.items: 
                    if (nn.slash): 
                        houses_has_slash.value = True
                co = num.calc_coef(num1, (False if ah.m_params is None else ah.m_params.strict_house_number))
                if (co <= 0): 
                    continue
                if (co < max0_): 
                    continue
                go = GarHelper.create_gar_house(ho)
                if (go is None): 
                    continue
                go._internal_tag = (0)
                if (go.expired): 
                    co *= 0.9
                if (co < max0_): 
                    continue
                if (co == max0_): 
                    res.append(go)
                else: 
                    if (res is None): 
                        res = list()
                    else: 
                        res.clear()
                    res.append(go)
                    max0_ = co
                    go._internal_tag = max0_
                    comp_not_equal = num.comp_not_equal
        if (comp_not_equal and res is not None and len(res) > 1): 
            res = (None)
        return res
    
    @staticmethod
    def __find_room_new(ah : 'AnalyzeHelper', rih : 'RoomsInHouse', a : 'AddressReferent') -> 'GarObject':
        from pullenti.address.internal.NumberAnalyzer import NumberAnalyzer
        if (rih is None): 
            return None
        num = NumberAnalyzer.try_parse_referent(a, False)
        if (num is None): 
            return None
        hos = rih.get_rooms(num)
        if (hos is None or len(hos) == 0): 
            return None
        res = None
        max0_ = 0
        has_flats_and_spaces = rih.check_has_flats_and_spaces()
        for ho in hos: 
            num1 = NumberAnalyzer.try_parsero(ho)
            if (num1 is None): 
                continue
            co = num.calc_coef(num1, False)
            if (co <= 0): 
                continue
            if (co < max0_): 
                continue
            if (has_flats_and_spaces): 
                if (num.items[0].cla == NumberItemClass.SPACE and num1.items[0].cla == NumberItemClass.FLAT): 
                    continue
                if (num.items[0].cla == NumberItemClass.FLAT and num1.items[0].cla == NumberItemClass.SPACE): 
                    continue
            go = GarHelper.create_gar_room(ho)
            if (go is None): 
                continue
            if (co == max0_): 
                res.append(go)
            else: 
                if (res is None): 
                    res = list()
                else: 
                    res.clear()
                res.append(go)
                max0_ = co
        if (res is None): 
            return None
        return res[0]
    
    @staticmethod
    def try_parse_list_items(ah : 'AnalyzeHelper', addr : 'TextAddress', ar : 'AnalysisResult') -> bool:
        t = None
        if (ar is not None): 
            t = ar.first_token
            while t is not None: 
                if (t.end_char == addr.end_char): 
                    t = t.next0_
                    break
                t = t.next0_
        if (t is None): 
            return False
        if (not t.is_comma_and and not t.is_hiphen and not t.is_value("ПО", None)): 
            return False
        it0 = addr.last_item
        room = Utils.asObjectOrNull(it0.attrs, RoomAttributes)
        house = Utils.asObjectOrNull(it0.attrs, HouseAttributes)
        if (house is None and room is None): 
            return False
        n0 = 0
        liter = None
        if (house is not None): 
            if (house.plot_number is not None): 
                if (house.number is not None or house.build_number is not None or house.stroen_number is not None): 
                    return False
                wrapn0185 = RefOutArgWrapper(0)
                Utils.tryParseInt(house.plot_number, wrapn0185)
                n0 = wrapn0185.value
            elif (house.number is not None): 
                if (house.build_number is not None or house.stroen_number is not None): 
                    return False
                wrapn0186 = RefOutArgWrapper(0)
                Utils.tryParseInt(house.number, wrapn0186)
                n0 = wrapn0186.value
            elif (house.build_number is not None): 
                if (house.stroen_number is not None): 
                    return False
                wrapn0187 = RefOutArgWrapper(0)
                Utils.tryParseInt(house.build_number, wrapn0187)
                n0 = wrapn0187.value
            elif (house.stroen_number is not None): 
                wrapn0188 = RefOutArgWrapper(0)
                inoutres189 = Utils.tryParseInt(house.stroen_number, wrapn0188)
                n0 = wrapn0188.value
                if (not inoutres189): 
                    liter = house.stroen_number
            else: 
                return False
        elif (room.number is None): 
            return False
        else: 
            wrapn0190 = RefOutArgWrapper(0)
            Utils.tryParseInt(room.number, wrapn0190)
            n0 = wrapn0190.value
        b0 = t.begin_char
        ar0 = None
        try: 
            ar0 = ProcessorService.get_empty_processor().process(SourceOfAnalysis._new129(addr.text[b0:], "ADDRESS"), None, None)
        except Exception as ex: 
            return False
        nums = list()
        if (liter is not None and ah.litera_variant is not None and liter != ah.litera_variant.value): 
            nums.append(ah.litera_variant.value)
        t = ar0.first_token
        first_pass3289 = True
        while True:
            if first_pass3289: first_pass3289 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not t.is_comma_and and not t.is_hiphen and not t.is_value("ПО", None)): 
                break
            hiph = t.is_hiphen or t.is_value("ПО", None)
            t = t.next0_
            if (t is None): 
                break
            if (not hiph and t.next0_ is not None and ((t.is_value("С", None) or t.is_value("C", None)))): 
                t = t.next0_
            if ((liter is not None and (isinstance(t, TextToken)) and t.length_char == 1) and t.chars.is_letter): 
                nums.append(t.term)
                addr.end_char = (t.end_char + b0)
                continue
            val = None
            et = None
            ait = AddressItemToken.try_parse_pure_item(t, None, None)
            if (ait is not None and ait.value is not None): 
                ok = ait.typ == AddressItemType.NUMBER
                if (ait.typ == AddressItemType.HOUSE and house is not None and house.plot_number is None): 
                    ok = True
                elif (ait.typ == AddressItemType.FLAT and room is not None): 
                    ok = True
                elif (ait.typ == AddressItemType.PLOT and house is not None and house.plot_number is not None): 
                    ok = True
                elif ((liter is not None and ait.typ == AddressItemType.BUILDING and not Utils.isNullOrEmpty(ait.value)) and not str.isdigit(ait.value[0])): 
                    ok = True
                if (ok): 
                    val = ait.value
                et = ait.end_token
            else: 
                nnn = NumToken.try_parse(t, GeoTokenType.HOUSE)
                if ((nnn is None and (isinstance(t, TextToken)) and t.length_char == 1) and t.chars.is_letter): 
                    nnn = NumToken.try_parse(t.next0_, GeoTokenType.HOUSE)
                    if (nnn is not None): 
                        nnn.value = (t.term + nnn.value)
                if (nnn is not None): 
                    val = nnn.value
                    et = nnn.end_token
            if (val is None): 
                break
            n1 = 0
            wrapn1192 = RefOutArgWrapper(0)
            Utils.tryParseInt(val, wrapn1192)
            n1 = wrapn1192.value
            if (hiph and n0 > 0 and n1 > n0): 
                if ((n1 - n0) > 100): 
                    break
                k = n0 + 1
                while k < n1: 
                    nums.append(str(k))
                    k += 1
            n0 = n1
            nums.append(val)
            t = et
            addr.end_char = (t.end_char + b0)
        if (len(nums) < 1): 
            return False
        if (len(nums) > 40): 
            return False
        HouseRoomHelper.__add_additional_numbers(ah, addr, nums)
        return True
    
    @staticmethod
    def __add_additional_numbers(ah : 'AnalyzeHelper', addr : 'TextAddress', nums : typing.List[str]) -> None:
        it0 = addr.last_item
        room = Utils.asObjectOrNull(it0.attrs, RoomAttributes)
        house = Utils.asObjectOrNull(it0.attrs, HouseAttributes)
        addr.additional_items = list()
        par = None
        rinh = None
        hinstr = None
        if (len(it0.gars) == 1 and len(it0.gars[0].parent_ids) > 0): 
            par = ah.get_gar_object(it0.gars[0].parent_ids[0])
            if (par is not None and ((par.level == GarLevel.BUILDING or par.level == GarLevel.ROOM))): 
                rinh = ah.get_rooms_in_object(par.id0_)
            elif (par is not None and (par.level) >= (GarLevel.LOCALITY)): 
                hinstr = ah.get_houses_in_street(par.id0_)
        for n in nums: 
            it = it0.clone()
            it.gars.clear()
            if (room is not None): 
                it.attrs.number = n
            elif (house.number is not None): 
                it.attrs.number = n
            elif (house.build_number is not None): 
                it.attrs.build_number = n
            else: 
                it.attrs.stroen_number = n
            addr.additional_items.append(it)
            if (room is not None): 
                a = AddressReferent()
                if (room.typ == RoomType.FLAT): 
                    a.flat = n
                elif (room.typ == RoomType.SPACE): 
                    a.space = n
                    if (room.misc is not None): 
                        a.space_type = room.misc
                elif (room.typ == RoomType.OFFICE): 
                    a.office = n
                elif (room.typ == RoomType.PAVILION): 
                    a.pavilion = n
                elif (room.typ == RoomType.ROOM): 
                    a.room = n
                else: 
                    continue
                gg = HouseRoomHelper.__find_room_new(ah, rinh, a)
                if (gg is not None): 
                    it.gars.append(gg)
            else: 
                a = AddressReferent()
                if (house.plot_number is not None): 
                    a.plot = n
                elif (house.number is not None): 
                    a.house = n
                elif (house.build_number is not None): 
                    a.corpus = n
                else: 
                    a.building = n
                bb = False
                wrapbb193 = RefOutArgWrapper(bb)
                gg = HouseRoomHelper.__find_houses_new(ah, hinstr, a, 0, None, wrapbb193)
                bb = wrapbb193.value
                if (gg is not None): 
                    it.gars.extend(gg)
    
    @staticmethod
    def create_dir_details(ar : 'AddressReferent', par : str) -> 'DetailType':
        par.value = ar.get_string_value(AddressReferent.ATTR_DETAILPARAM)
        return HouseRoomHelper.__create_dir_details(ar.detail)
    
    @staticmethod
    def __create_dir_details(dt : 'AddressDetailType') -> 'DetailType':
        ty = DetailType.UNDEFINED
        if (dt == AddressDetailType.NEAR): 
            ty = DetailType.NEAR
        elif (dt == AddressDetailType.EAST): 
            ty = DetailType.EAST
        elif (dt == AddressDetailType.NORTH): 
            ty = DetailType.NORTH
        elif (dt == AddressDetailType.NORTHEAST): 
            ty = DetailType.NORTHEAST
        elif (dt == AddressDetailType.NORTHWEST): 
            ty = DetailType.NORTHWEST
        elif (dt == AddressDetailType.SOUTH): 
            ty = DetailType.SOUTH
        elif (dt == AddressDetailType.SOUTHEAST): 
            ty = DetailType.SOUTHEAST
        elif (dt == AddressDetailType.SOUTHWEST): 
            ty = DetailType.SOUTHWEST
        elif (dt == AddressDetailType.WEST): 
            ty = DetailType.WEST
        elif (dt == AddressDetailType.RANGE): 
            ty = DetailType.KMRANGE
        elif (dt == AddressDetailType.CENTRAL): 
            ty = DetailType.CENTRAL
        elif (dt == AddressDetailType.LEFT): 
            ty = DetailType.LEFT
        elif (dt == AddressDetailType.RIGHT): 
            ty = DetailType.RIGHT
        return ty
    
    @staticmethod
    def process_other_details(addr : 'TextAddress', ar : 'AddressReferent') -> None:
        if (ar.floor0_ is not None): 
            if (not ParamType.FLOOR in addr.params): 
                addr.params[ParamType.FLOOR] = ar.floor0_
        if (ar.part is not None): 
            if (not ParamType.PART in addr.params): 
                addr.params[ParamType.PART] = ar.part
        if (ar.genplan is not None): 
            if (not ParamType.GENPLAN in addr.params): 
                addr.params[ParamType.GENPLAN] = (None if ar.genplan == "0" else ar.genplan)
        if (ar.delivery_area is not None): 
            if (not ParamType.DELIVERYAREA in addr.params): 
                addr.params[ParamType.DELIVERYAREA] = (None if ar.delivery_area == "0" else ar.delivery_area)
        if (ar.zip0_ is not None and ar.zip0_ != "000000" and ar.zip0_ != "0"): 
            if (not ParamType.ZIP in addr.params): 
                addr.params[ParamType.ZIP] = ar.zip0_
        if (ar.post_office_box is not None): 
            if (not ParamType.SUBSCRIBERBOX in addr.params): 
                addr.params[ParamType.SUBSCRIBERBOX] = ar.post_office_box
        if (ar.detail == AddressDetailType.ORG): 
            org0_ = Utils.asObjectOrNull(ar.get_slot_value(AddressReferent.ATTR_DETAILREF), Referent)
            if (org0_ is not None): 
                if (not ParamType.ORGANIZATION in addr.params): 
                    aa = AreaAttributes()
                    for s in org0_.slots: 
                        if (s.type_name == "TYPE"): 
                            aa.types.append(Utils.asObjectOrNull(s.value, str))
                        elif (s.type_name == "NAME"): 
                            aa.names.append(MiscHelper.convert_first_char_upper_and_other_lower(Utils.asObjectOrNull(s.value, str)))
                        elif (s.type_name == "NUMBER"): 
                            aa.number = (Utils.asObjectOrNull(s.value, str))
                    ss = str(aa)
                    if (len(ss) > 0): 
                        addr.params[ParamType.ORGANIZATION] = ss
    
    @staticmethod
    def try_process_details(addr : 'TextAddress', details : str) -> None:
        if (Utils.isNullOrEmpty(details) or addr.last_item is None or addr.last_item.detail_typ != DetailType.UNDEFINED): 
            return
        try: 
            ar0 = ProcessorService.get_empty_processor().process(SourceOfAnalysis._new129(details, "ADDRESS"), None, None)
            t = ar0.first_token
            first_pass3290 = True
            while True:
                if first_pass3290: first_pass3290 = False
                else: t = t.next0_
                if (not (t is not None)): break
                ait = AddressItemToken.try_parse_pure_item(t, None, None)
                if (ait is None or ait.typ != AddressItemType.DETAIL): 
                    continue
                addr.last_item.detail_typ = HouseRoomHelper.__create_dir_details(ait.detail_type)
                if (ait.detail_meters > 0): 
                    addr.last_item.detail_param = "{0}м".format(ait.detail_meters)
                break
        except Exception as ex195: 
            pass