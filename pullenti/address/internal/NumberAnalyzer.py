# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.address.internal.gar.RoomObject import RoomObject
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.GarLevel import GarLevel
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.address.internal.NumberItem import NumberItem
from pullenti.address.HouseType import HouseType
from pullenti.address.StroenType import StroenType
from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.internal.NumberItemClass import NumberItemClass
from pullenti.address.GarStatus import GarStatus
from pullenti.address.RoomType import RoomType
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.NumToken import NumToken
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.address.internal.HouseRoomHelper import HouseRoomHelper

class NumberAnalyzer:
    
    def __init__(self) -> None:
        self.items = list()
        self.comp_not_equal = False
    
    def __str__(self) -> str:
        if (len(self.items) == 0): 
            return "?"
        if (len(self.items) == 1): 
            return str(self.items[0])
        res = io.StringIO()
        print(str(self.items[0]), end="", file=res)
        i = 1
        while i < len(self.items): 
            print(", {0}".format(str(self.items[i])), end="", file=res, flush=True)
            i += 1
        return Utils.toStringStringIO(res)
    
    def calc_coef(self, num : 'NumberAnalyzer', strict : bool) -> float:
        res = 0
        self.comp_not_equal = False
        for it in num.items: 
            it.twix = (None)
        for it in self.items: 
            it.twix = (None)
            best = None
            max0_ = 0
            for it1 in num.items: 
                if (it1.twix is None): 
                    co = it.equal_coef(it1)
                    if (co > max0_): 
                        best = it1
                        max0_ = co
            if (best is None): 
                continue
            if (best.twix is not None): 
                continue
            if (strict and (max0_ < 0.1)): 
                continue
            it.twix = best
            best.twix = it
            res += max0_
        if (res == 0): 
            return 0
        cou = 0
        for it in self.items: 
            if (it.value == "0"): 
                continue
            cou += 1
            if (it.twix is None): 
                if (it == self.items[0]): 
                    return 0
                if (strict): 
                    return 0
                if (len(num.items) != 1): 
                    return 0
                self.comp_not_equal = True
                if (it.can_absent): 
                    res /= (2)
                elif (not Utils.isNullOrEmpty(it.value) and it.slash and str.isdigit(it.value[0])): 
                    res /= (2)
                else: 
                    return 0
            elif (Utils.indexOfList(self.items, it, 0) != Utils.indexOfList(num.items, it.twix, 0)): 
                return 0
        for it in num.items: 
            if (it.value == "0"): 
                continue
            cou += 1
            if (it.twix is None): 
                if (it == num.items[0]): 
                    return 0
                if (strict): 
                    return 0
                if (len(self.items) != 1): 
                    return 0
                self.comp_not_equal = True
                if (it.can_absent): 
                    res /= (2)
                elif (not Utils.isNullOrEmpty(it.value) and it.slash and str.isdigit(it.value[0])): 
                    res /= (2)
                else: 
                    return 0
        if (cou == 0): 
            cou = 1
        return res
    
    @staticmethod
    def try_parse_referent(ar : 'AddressReferent', house : bool) -> 'NumberAnalyzer':
        res = NumberAnalyzer()
        if (house): 
            if (ar.house_or_plot is not None): 
                nums = NumberItem.parse(ar.house_or_plot, None, NumberItemClass.UNDEFINED)
                if (nums is not None): 
                    res.items.extend(nums)
            elif (ar.plot is not None): 
                nums = NumberItem.parse(ar.plot, "уч.", NumberItemClass.PLOT)
                if (nums is not None): 
                    res.items.extend(nums)
            elif (ar.box is not None): 
                nums = NumberItem.parse(ar.box, "гар.", NumberItemClass.GARAGE)
                if (nums is not None): 
                    res.items.extend(nums)
                    if (ar.block is not None): 
                        nums2 = NumberItem.parse(ar.block, "бл.", NumberItemClass.UNDEFINED)
                        if (nums2 is not None and len(nums2) == 1): 
                            nums2[0].can_absent = True
                            res.items.append(nums2[0])
            if (ar.house is not None): 
                ty = ar.house_type
                nums = NumberItem.parse(ar.house, ("влад." if ty == AddressHouseType.ESTATE else ("дмвлд." if ty == AddressHouseType.HOUSEESTATE else "д.")), NumberItemClass.HOUSE)
                if (nums is not None): 
                    res.items.extend(nums)
            if (ar.corpus is not None): 
                nums = NumberItem.parse(ar.corpus, "корп.", NumberItemClass.HOUSE)
                if (nums is not None): 
                    res.items.extend(nums)
            if (ar.corpus_or_flat is not None): 
                nums = NumberItem.parse(ar.corpus_or_flat, "корп.", NumberItemClass.HOUSE)
                if (nums is not None): 
                    nums[0].can_be_flat = True
                    res.items.extend(nums)
            if (ar.building is not None): 
                ty = ar.building_type
                nums = NumberItem.parse(ar.building, ("сооруж." if ty == AddressBuildingType.CONSTRUCTION else ("лит." if ty == AddressBuildingType.LITER else "стр.")), NumberItemClass.HOUSE)
                if (nums is not None): 
                    res.items.extend(nums)
        else: 
            attr = HouseRoomHelper.create_apartment_attrs(ar, None)
            if (attr is not None): 
                nums = NumberItem.parse(attr.number, AddressHelper.get_room_type_string(attr.typ, True), (NumberItemClass.CARPLACE if attr.typ == RoomType.CARPLACE else (NumberItemClass.FLAT if attr.typ == RoomType.FLAT else NumberItemClass.SPACE)))
                if (nums is None): 
                    return None
                res.items.extend(nums)
        if (len(res.items) == 0): 
            return None
        return res
    
    @staticmethod
    def try_parse_gar_object(g : 'GarObject') -> 'NumberAnalyzer':
        if (GarHelper.GAR_INDEX is None): 
            return None
        if (g.id0_[0] == 'h'): 
            ho = GarHelper.GAR_INDEX.get_house(int(g.id0_[1:]))
            return NumberAnalyzer.try_parseho(ho)
        return None
    
    @staticmethod
    def try_parse_house_attrs(ha : 'HouseAttributes') -> 'NumberAnalyzer':
        res = NumberAnalyzer()
        if (ha.plot_number is not None): 
            nums = NumberItem.parse(ha.plot_number, "уч.", NumberItemClass.PLOT)
            if (nums is not None): 
                res.items.extend(nums)
        if (ha.number is not None): 
            nums = NumberItem.parse(ha.number, ("влад." if ha.typ == HouseType.ESTATE else ("д." if ha.typ == HouseType.HOUSE else ("дмвлд." if ha.typ == HouseType.HOUSEESTATE else ("гар." if ha.typ == HouseType.GARAGE else "д.")))), (NumberItemClass.GARAGE if ha.typ == HouseType.GARAGE else NumberItemClass.HOUSE))
            if (nums is not None): 
                res.items.extend(nums)
        if (ha.build_number is not None): 
            nums = NumberItem.parse(ha.build_number, "корп.", NumberItemClass.HOUSE)
            if (nums is not None): 
                res.items.extend(nums)
        if (ha.stroen_number is not None): 
            nums = NumberItem.parse(ha.stroen_number, ("сооруж." if ha.stroen_typ == StroenType.CONSTRUCTION else ("лит." if ha.stroen_typ == StroenType.LITER else "стр.")), NumberItemClass.HOUSE)
            if (nums is not None): 
                res.items.extend(nums)
        return res
    
    @staticmethod
    def try_parseho(ho : 'HouseObject') -> 'NumberAnalyzer':
        res = NumberAnalyzer()
        if (ho.plot_number is not None): 
            nums = NumberItem.parse(ho.plot_number, "уч.", NumberItemClass.PLOT)
            if (nums is not None): 
                res.items.extend(nums)
        if (ho.house_number is not None): 
            nums = NumberItem.parse(ho.house_number, ("влад." if ho.house_typ == (1) else ("д." if ho.house_typ == (2) else ("дмвлд." if ho.house_typ == (3) else ("гар." if ho.house_typ == (4) else "д.")))), (NumberItemClass.GARAGE if ho.house_typ == (4) else NumberItemClass.HOUSE))
            if (nums is not None): 
                res.items.extend(nums)
        if (ho.build_number is not None): 
            nums = NumberItem.parse(ho.build_number, "корп.", NumberItemClass.HOUSE)
            if (nums is not None): 
                res.items.extend(nums)
        if (ho.struc_number is not None): 
            nums = NumberItem.parse(ho.struc_number, ("сооруж." if ho.struc_typ == (2) else ("лит." if ho.house_typ == (3) else "стр.")), NumberItemClass.HOUSE)
            if (nums is not None): 
                res.items.extend(nums)
        return res
    
    @staticmethod
    def try_parsero(ro : 'RoomObject') -> 'NumberAnalyzer':
        nums = NumberItem.parse(ro.number, AddressHelper.get_room_type_string(ro.typ, True), (NumberItemClass.CARPLACE if ro.typ == RoomType.CARPLACE else (NumberItemClass.FLAT if ro.typ == RoomType.FLAT else NumberItemClass.SPACE)))
        if (nums is None): 
            return None
        res = NumberAnalyzer()
        res.items.extend(nums)
        return res
    
    @staticmethod
    def set_gar_loading_room_number_attrs(ro : 'RoomObject') -> None:
        num = Utils.ifNotNull(ro.source_text, "")
        if ("б/нб/н" in num): 
            num = num.replace("б/нб/н", "б/н")
        if (num == "-"): 
            num = "б/н"
        ii = 0
        while ii < (len(num) - 1): 
            if ((str.isalpha(num[ii]) and ((ord(num[ii])) < 0x80) and str.isalpha(num[ii + 1])) and (ord(num[ii + 1])) > 0x80): 
                num = "{0} {1}".format(num[0:0+ii + 1], num[ii + 1:])
            ii += 1
        if (len(num) > 1 and num[0] == 'Л' and str.isdigit(num[1])): 
            num = num[1:]
        elif ((len(num) > 2 and num[0] == 'Л' and num[1] == '-') and str.isdigit(num[2])): 
            num = num[2:]
        ro.status = GarStatus.OK
        ro.number = (None)
        ro.misc = (None)
        ro.typ = RoomType.UNDEFINED
        ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(num), None, None)
        t = None
        add_num = None
        t = ar.first_token
        first_pass3295 = True
        while True:
            if first_pass3295: first_pass3295 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char_of("\\/,.:")): 
                continue
            ait = AddressItemToken.try_parse_pure_item(t, None, None)
            if (ait is None): 
                break
            if (ro.number is None): 
                ro.number = ait.value
                if (ait.typ == AddressItemType.HOUSE and t.is_value("КВ", None) and ro.number.find('/') > 0): 
                    ro.typ = RoomType.FLAT
                    ro.number = ro.number[ro.number.find('/') + 1:]
            elif (ait.value is not None): 
                add_num = ait.value
            if (ro.typ == RoomType.UNDEFINED): 
                if (ait.typ == AddressItemType.FLAT): 
                    ro.typ = RoomType.FLAT
                elif (ait.typ == AddressItemType.CARPLACE): 
                    ro.typ = RoomType.CARPLACE
                elif (ait.typ == AddressItemType.OFFICE): 
                    ro.typ = RoomType.OFFICE
                elif (ait.typ == AddressItemType.ROOM): 
                    ro.typ = RoomType.ROOM
                elif (ait.typ == AddressItemType.BOX): 
                    ro.typ = RoomType.GARAGE
                elif (ait.typ == AddressItemType.PAVILION): 
                    ro.typ = RoomType.PAVILION
                elif (ait.typ == AddressItemType.SPACE or ait.typ == AddressItemType.NONUMBER): 
                    ro.typ = RoomType.SPACE
                elif (ait.typ == AddressItemType.NUMBER and ait.end_token.next0_ is None and t == ar.first_token): 
                    ro.typ = RoomType.SPACE
            if (ro.misc is None and ait.typ == AddressItemType.SPACE): 
                ro.misc = ait.detail_param
            t = ait.end_token
        if (add_num is not None): 
            if (ro.number is None): 
                ro.number = add_num
            else: 
                ro.number = "{0}/{1}".format(ro.number, add_num)
        while t is not None: 
            if (((not t.is_hiphen and not t.is_char_of("_,"))) or not (isinstance(t.next0_, NumberToken))): 
                break
            ait = AddressItemToken.try_parse_pure_item(t.next0_, None, None)
            if (ait is None or ait.typ != AddressItemType.NUMBER or ait.value is None): 
                break
            ro.number = "{0}/{1}".format(ro.number, ait.value)
            t = ait.end_token
            t = t.next0_
        while t is not None: 
            if (t.is_value("ПОДВАЛ", None)): 
                ro.misc = "подвал"
            elif (t.is_value("ТЕХЭТАЖ", None) or t.is_value("ЭТАЖТЕХ", None)): 
                ro.misc = "техэтаж"
            elif ((isinstance(t, TextToken)) and t.term.endswith("ЗАВОД")): 
                pass
            elif (t.is_value("МАШИНОМЕСТО", None) or t.is_value("ММ", None)): 
                if (ro.typ == RoomType.SPACE): 
                    ro.typ = RoomType.CARPLACE
            elif (t.is_value("ГАРАЖ", None)): 
                if (ro.typ == RoomType.SPACE): 
                    ro.typ = RoomType.GARAGE
            elif (t.is_value("ОИ", None)): 
                ro.misc = "МОП"
            t = t.next0_
        if ((ro.number is not None and ro.number.find('/') > 0 and GarHelper.GAR_INDEX is not None) and ro.house_id != (0)): 
            ii = ro.number.find('/')
            if ((((ro.house_id) & 0x80000000)) == 0x80000000): 
                ho = GarHelper.GAR_INDEX.get_room(((ro.house_id) & 0x7FFFFFFF))
                if (ho is not None and ho.number == ro.number[0:0+ii]): 
                    ro.number = ro.number[ii + 1:]
            else: 
                ho = GarHelper.GAR_INDEX.get_house(((ro.house_id) & 0x7FFFFFFF))
                if (ho is not None and ho.house_number == ro.number[0:0+ii]): 
                    ro.number = ro.number[ii + 1:]
        if (t is not None): 
            ro.status = GarStatus.ERROR
        if (ro.typ == RoomType.UNDEFINED): 
            ro.status = GarStatus.ERROR
    
    @staticmethod
    def set_gar_loading_house_number_attrs(ho : 'HouseObject', is_stead : bool) -> None:
        num = Utils.ifNotNull(ho.source_text, "")
        if (not is_stead and num.startswith("уч.")): 
            num = num[3:].strip()
        ho.status = GarStatus.OK
        ii = 0
        for kk in range(3):
            ii = num.lower().find(("стр" if kk == 0 else ("бокс" if kk == 1 else "поз")))
            if (ii > 0 and str.isalpha(num[ii - 1])): 
                num = "{0} {1}".format(num[0:0+ii], num[ii:])
        ii = num.find("кор")
        if (ii > 0): 
            ii0 = ii
            ii += 3
            if ((ii < len(num)) and num[ii] == 'п'): 
                ii += 1
                if ((ii < len(num)) and num[ii] == 'у'): 
                    ii += 1
                    if ((ii < len(num)) and num[ii] == 'с'): 
                        ii += 1
            if ((ii < len(num)) and str.isalpha(num[ii]) and str.isupper(num[ii])): 
                num = "{0} {1}".format(num[0:0+ii], num[ii:])
            if (str.isupper(num[ii0 - 1]) or str.isdigit(num[ii0 - 1])): 
                num = "{0} {1}".format(num[0:0+ii0], num[ii0:])
        if (num.find('|') > 0): 
            num = num.replace('|', '/')
        ii = num.find("лит")
        if (ii > 0): 
            ii0 = ii
            ii += 3
            if ((ii < len(num)) and num[ii] == 'е'): 
                ii += 1
                if ((ii < len(num)) and num[ii] == 'р'): 
                    ii += 1
                    if ((ii < len(num)) and num[ii] == 'а'): 
                        ii += 1
            if ((ii < len(num)) and str.isalpha(num[ii]) and str.isupper(num[ii])): 
                num = "{0} {1}".format(num[0:0+ii], num[ii:])
            if (str.isupper(num[ii0 - 1]) or str.isdigit(num[ii0 - 1])): 
                num = "{0} {1}".format(num[0:0+ii0], num[ii0:])
        ii = 0
        while ii < (len(num) - 1): 
            if ((str.isalpha(num[ii]) and str.islower(num[ii]) and str.isalpha(num[ii + 1])) and str.isupper(num[ii + 1])): 
                num = "{0} {1}".format(num[0:0+ii + 1], num[ii + 1:])
            elif (((is_stead and str.isalpha(num[ii]) and str.isupper(num[ii])) and num[ii + 1] == 'у' and ((ii + 2) < len(num))) and str.isdigit(num[ii + 2])): 
                num = "{0} {1}".format(num[0:0+ii + 1], num[ii + 1:])
            elif ((str.isalpha(num[ii]) and ((ii + 3) < len(num)) and num[ii + 1] == 'у') and num[ii + 2] == 'ч' and str.isdigit(num[ii + 3])): 
                num = "{0} {1}".format(num[0:0+ii + 1], num[ii + 1:])
            ii += 1
        ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(num), None, None)
        t = None
        add_num = None
        t = ar.first_token
        first_pass3296 = True
        while True:
            if first_pass3296: first_pass3296 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char_of("\\/,.:")): 
                continue
            if (t.is_char('(') and t != ar.first_token): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None and br.length_char > 10): 
                    t = br.end_token
                    continue
            ait = AddressItemToken.try_parse_pure_item(t, None, None)
            nt = None
            if (ait is not None and ait.typ == AddressItemType.NUMBER): 
                nt = NumToken.try_parse(t, GeoTokenType.STRONG)
                if (nt is not None and nt.length_char > ait.length_char): 
                    ait = (None)
            if ((ait is not None and ait.typ == AddressItemType.DETAIL and t.is_value("У", None)) and (isinstance(t.next0_, NumberToken))): 
                nt = NumToken.try_parse(t.next0_, GeoTokenType.STRONG)
                if (nt is not None): 
                    add_num = nt.value
                    t = nt.end_token
                    continue
            if (t.is_value2("ПОД", "ГАРАЖ")): 
                nt = NumToken.try_parse(t.next0_.next0_, GeoTokenType.STRONG)
                if (nt is not None): 
                    add_num = nt.value
                    t = nt.end_token
                    continue
            if (ait is None): 
                if (nt is None): 
                    nt = NumToken.try_parse(t, GeoTokenType.STRONG)
                if (nt is not None): 
                    ait = AddressItemToken._new201(AddressItemType.NUMBER, t, nt.end_token, nt.value)
                else: 
                    if ((((t.is_value("РЯД", None) or t.is_value("БЛОК", None) or t.is_value("ЛИНИЯ", None)) or t.is_value("АЛЛЕЯ", None) or t.is_value("ТЕРРИТОРИЯ", None)) or t.is_value("СЕКТОР", None) or t.is_value("ПРОЕЗД", None)) or t.is_value("ПЕРЕУЛОК", None) or t.is_value("ТУПИК", None)): 
                        nt = NumToken.try_parse(t.next0_, GeoTokenType.STRONG)
                        if (nt is not None): 
                            add_num = nt.value
                            t = nt.end_token
                            continue
                    sit = StreetItemToken.try_parse(t, None, False, None)
                    if (sit is not None and sit.typ == StreetItemType.NOUN): 
                        tt = sit.end_token.next0_
                        if (tt is not None and tt.is_hiphen): 
                            tt = tt.next0_
                        nt = NumToken.try_parse(tt, GeoTokenType.STRONG)
                        if (nt is not None): 
                            add_num = nt.value
                            t = nt.end_token
                            continue
                    if (t.is_value("УЧ", None) and is_stead): 
                        continue
                    break
            val = ("" if ait.typ == AddressItemType.NONUMBER or ait.value is None or ait.value == "0" else ait.value)
            if (ait.typ == AddressItemType.ZIP): 
                ait.typ = AddressItemType.NUMBER
            if ((not Utils.isNullOrEmpty(val) and ait.end_token.next0_ is not None and ((ait.end_token.next0_.is_hiphen or ait.end_token.next0_.is_char_of("_\\/")))) and not ait.end_token.next0_.is_whitespace_after): 
                nt = NumToken.try_parse(ait.end_token.next0_.next0_, GeoTokenType.STRONG)
                if (nt is not None): 
                    val = "{0}/{1}".format(val, nt.value)
                    ait.end_token = nt.end_token
            elif (not ait.is_whitespace_after): 
                nt = NumToken.try_parse(t, GeoTokenType.STRONG)
                if (nt is not None and nt.end_char > ait.end_char): 
                    val = nt.value
                    ait.end_token = nt.end_token
            if (ait.typ == AddressItemType.PLOT): 
                if (is_stead and ho.plot_number is None): 
                    ho.plot_number = val
                elif (add_num is None): 
                    add_num = val
                elif (ho.plot_number is None): 
                    ho.plot_number = val
            elif (ait.typ == AddressItemType.HOUSE): 
                if (is_stead and ho.plot_number is None): 
                    ho.plot_number = val
                elif (ho.house_number is not None): 
                    ho.status = GarStatus.ERROR
                else: 
                    ho.house_number = val
                    ho.house_typ = (2)
                    if (ait.house_type == AddressHouseType.ESTATE): 
                        ho.house_typ = (1)
                    elif (ait.house_type == AddressHouseType.HOUSE): 
                        ho.house_typ = (2)
                    elif (ait.house_type == AddressHouseType.HOUSEESTATE): 
                        ho.house_typ = (3)
                    elif (ait.house_type == AddressHouseType.SPECIAL): 
                        ho.house_typ = (2)
            elif (ait.typ == AddressItemType.BOX): 
                if (ho.house_number is not None): 
                    if (ho.house_typ == (4)): 
                        ho.house_number = "{0}/{1}".format(ho.house_number, ait.value)
                    else: 
                        ho.status = GarStatus.ERROR
                else: 
                    ho.house_number = val
                    ho.house_typ = (4)
            elif (ait.typ == AddressItemType.CORPUSORFLAT or ait.typ == AddressItemType.CORPUS): 
                if (ho.build_number is not None): 
                    ho.status = GarStatus.ERROR
                else: 
                    ho.build_number = val
            elif (ait.typ == AddressItemType.BUILDING): 
                if (ho.struc_number is None): 
                    ho.struc_number = val
                    if (ait.building_type == AddressBuildingType.CONSTRUCTION): 
                        ho.struc_typ = (2)
                    elif (ait.building_type == AddressBuildingType.LITER): 
                        ho.struc_typ = (3)
                    else: 
                        ho.struc_typ = (1)
                elif (ho.house_number is None): 
                    ho.house_number = ho.struc_number
                    ho.house_typ = (2)
                    ho.struc_number = val
                    if (ait.building_type == AddressBuildingType.CONSTRUCTION): 
                        ho.struc_typ = (2)
                    elif (ait.building_type == AddressBuildingType.LITER): 
                        ho.struc_typ = (3)
                    else: 
                        ho.struc_typ = (1)
                else: 
                    ho.status = GarStatus.ERROR
            elif (ait.typ == AddressItemType.FLAT and is_stead and ho.plot_number is not None): 
                add_num = val
            elif (((ait.typ == AddressItemType.BLOCK or ait.typ == AddressItemType.NUMBER or ait.typ == AddressItemType.PART)) and add_num is None): 
                add_num = ait.value
            elif (ait.typ == AddressItemType.NUMBER and is_stead and ho.plot_number is None): 
                ho.plot_number = ait.value
            else: 
                break
            t = ait.end_token
        if ((t is not None and t.is_char_of(".|") and (isinstance(t.next0_, NumberToken))) and t.next0_.next0_ is None and add_num is None): 
            add_num = t.next0_.value
            t = (None)
        if (add_num is not None): 
            if (ho.plot_number is not None): 
                ho.plot_number = "{0}/{1}".format(ho.plot_number, add_num)
            elif (is_stead): 
                ho.plot_number = add_num
            elif (ho.house_number is not None): 
                ho.house_number = "{0}/{1}".format(ho.house_number, add_num)
            elif (ho.struc_number is not None): 
                ho.struc_number = "{0}/{1}".format(ho.struc_number, add_num)
            else: 
                ho.status = GarStatus.ERROR
        if ((not Utils.isNullOrEmpty(ho.house_number) and ho.house_number[0] == 'К' and ho.build_number is None) and ho.house_typ != (4)): 
            ho.build_number = ho.house_number[1:]
            ho.house_number = (None)
            ho.house_typ = (0)
        if (t is None): 
            return
        if ((isinstance(t, TextToken)) and (t.length_char < 3) and t.next0_ is None): 
            return
        if (t.is_value2("В", "ГРАНИЦА") and ho.plot_number is not None): 
            return
        ho.status = GarStatus.ERROR
        ho.house_number = (None)
        ho.plot_number = (None)
        ho.struc_number = (None)
        ho.build_number = (None)
        ho.house_typ = (0)
        ho.struc_typ = (0)
    
    @staticmethod
    def recalc_status(go : 'GarObject') -> 'GarStatus':
        if (isinstance(go.attrs, HouseAttributes)): 
            ho = HouseObject._new202(go.source_text)
            NumberAnalyzer.set_gar_loading_house_number_attrs(ho, go.level == GarLevel.PLOT)
            return ho.status
        if (isinstance(go.attrs, RoomAttributes)): 
            ro = RoomObject._new203(go.source_text)
            if (len(go.parent_ids) > 0 and GarHelper.GAR_INDEX is not None and go.parent_ids[0][0] == 'h'): 
                ro.house_id = (int(go.parent_ids[0][1:]))
            NumberAnalyzer.set_gar_loading_room_number_attrs(ro)
            return ro.status
        return GarStatus.ERROR