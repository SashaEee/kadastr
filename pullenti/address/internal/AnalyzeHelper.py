# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.GarParam import GarParam
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.DetailType import DetailType
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.internal.CoefHelper import CoefHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.address.GarLevel import GarLevel
from pullenti.address.internal.RestructHelper import RestructHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.CanBeEqualsAttr import CanBeEqualsAttr
from pullenti.address.GarStatus import GarStatus
from pullenti.address.ParamType import ParamType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.address.AddrObject import AddrObject
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.address.AddrLevel import AddrLevel
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.Referent import Referent
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.address.TextAddress import TextAddress
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.internal.HouseRoomHelper import HouseRoomHelper
from pullenti.address.internal.RegionHelper import RegionHelper
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.address.internal.CorrectionHelper import CorrectionHelper
from pullenti.address.AddressService import AddressService

class AnalyzeHelper:
    
    def __init__(self) -> None:
        self.__m_gar_hash = dict()
        self.__m_houses = dict()
        self.__m_rooms = dict()
        self.index_read_count = 0
        self.litera_variant = None;
        self.house_number_variant = None;
        self.m_params = None;
        self.corrected_text = None;
        self.create_alts_regime = False
        self.zip0_ = None;
        self.zip_var_streets = None
        self.zip_var_cities = None
        self.__m_try_this_text_var = None;
        self.__m_try_this_text_var2 = None;
        self.__insert_street_before_substr = None
        self.__def_object_regime = None
    
    __m_proc0 = None
    
    __m_proc1 = None
    
    @staticmethod
    def init() -> None:
        AnalyzeHelper.__m_proc0 = ProcessorService.create_empty_processor()
        AnalyzeHelper.__m_proc1 = ProcessorService.create_processor()
        for a in AnalyzeHelper.__m_proc1.analyzers: 
            if (((a.name == "GEO" or a.name == "ADDRESS" or a.name == "NAMEDENTITY") or a.name == "DATE" or a.name == "PHONE") or a.name == "URI"): 
                pass
            else: 
                a.ignore_this_analyzer = True
    
    def get_gar_object(self, id0_ : str) -> 'GarObject':
        if (id0_ is None): 
            return None
        res = None
        wrapres104 = RefOutArgWrapper(None)
        inoutres105 = Utils.tryGetValue(self.__m_gar_hash, id0_, wrapres104)
        res = wrapres104.value
        if (inoutres105): 
            return res
        res = GarHelper.get_object(id0_)
        if (res is None): 
            return None
        self.__m_gar_hash[id0_] = res
        if (id0_[0] != 'a'): 
            self.index_read_count += 1
        return res
    
    def get_houses_in_street(self, id0_ : str) -> 'HousesInStreet':
        if (id0_ is None): 
            return None
        res = None
        wrapres106 = RefOutArgWrapper(None)
        inoutres107 = Utils.tryGetValue(self.__m_houses, id0_, wrapres106)
        res = wrapres106.value
        if (inoutres107): 
            return res
        res = GarHelper.GAR_INDEX.getaohouses(AnalyzeHelper.__get_id(id0_))
        if (res is not None): 
            self.index_read_count += 1
        self.__m_houses[id0_] = res
        return res
    
    def get_rooms_in_object(self, id0_ : str) -> 'RoomsInHouse':
        if (id0_ is None): 
            return None
        res = None
        wrapres108 = RefOutArgWrapper(None)
        inoutres109 = Utils.tryGetValue(self.__m_rooms, id0_, wrapres108)
        res = wrapres108.value
        if (inoutres109): 
            return res
        if (id0_[0] == 'h'): 
            res = GarHelper.GAR_INDEX.get_rooms_in_house(AnalyzeHelper.__get_id(id0_))
        elif (id0_[0] == 'r'): 
            res = GarHelper.GAR_INDEX.get_rooms_in_rooms(AnalyzeHelper.__get_id(id0_))
        if (res is not None): 
            self.index_read_count += 1
        self.__m_rooms[id0_] = res
        return res
    
    def analyze(self, txt : str, corr : typing.List[tuple], one_addr : bool, pars : 'ProcessTextParams', correct_keywords : bool) -> typing.List['TextAddress']:
        res = self.__analyze0(txt, corr, one_addr, pars, correct_keywords)
        if (not one_addr): 
            return res
        if (res is not None and len(res) == 1 and res[0].coef == 100): 
            return res
        if (self.zip_var_cities is not None): 
            for cit in self.zip_var_cities: 
                aa = Utils.asObjectOrNull(cit.attrs, AreaAttributes)
                if (len(aa.names) == 0): 
                    continue
                if (not aa.names[0].upper() in txt.upper()): 
                    continue
                ah1 = AnalyzeHelper()
                ah1.__def_object_regime = cit
                res1 = ah1.__analyze0(txt, corr, True, pars, correct_keywords)
                if (res1 is not None and len(res1) == 1 and res1[0].coef == 100): 
                    return res1
        return res
    
    def __analyze0(self, txt : str, corr : typing.List[tuple], one_addr : bool, pars : 'ProcessTextParams', correct_keywords : bool) -> typing.List['TextAddress']:
        if (Utils.isNullOrEmpty(txt)): 
            return None
        self.m_params = pars
        co = None
        if (corr is not None and "" in corr): 
            co = corr[""]
        detail = None
        vars0_ = None
        if (one_addr and ((pars is None or not pars.dont_correct_text))): 
            wrapdetail110 = RefOutArgWrapper(None)
            vars0_ = CorrectionHelper.correct(txt, pars is not None and pars.default_object is not None, wrapdetail110)
            detail = wrapdetail110.value
            if (vars0_ is None or len(vars0_) == 0): 
                return None
            txt = vars0_[0]
            del vars0_[0]
            if (correct_keywords): 
                ar0 = ProcessorService.get_empty_processor().process(SourceOfAnalysis(txt), None, None)
                subst = None
                t = ar0.first_token
                first_pass3253 = True
                while True:
                    if first_pass3253: first_pass3253 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if ((isinstance(t, TextToken)) and t.get_morph_class_in_dictionary().is_undefined and t.length_char > 4): 
                        vs = MorphologyService.correct_word_ex(t.term, None)
                        if (vs is None or len(vs) != 1): 
                            continue
                        t.tag = (vs[0])
                        if (subst is None): 
                            subst = list()
                        subst.insert(0, t)
                if (subst is None): 
                    return None
                tmp = Utils.newStringIO(txt)
                for t in subst: 
                    Utils.removeStringIO(tmp, t.begin_char, (t.end_char + 1) - t.begin_char)
                    Utils.insertStringIO(tmp, t.begin_char, Utils.asObjectOrNull(t.tag, str))
                txt = Utils.toStringStringIO(tmp)
            self.corrected_text = txt
        res = self.__analyze(txt, co, one_addr, None)
        src_addr = None
        if (len(res) == 1 and res[0].last_item is not None): 
            src_addr = res[0]
        if (one_addr and self.__insert_street_before_substr is not None): 
            ii = txt.upper().find(self.__insert_street_before_substr)
            if (ii > 0 and (Utils.indexOfList(txt.upper(), self.__insert_street_before_substr, ii + 1) < 0)): 
                txt = "{0}, ул.{1}".format(txt[0:0+ii], txt[ii:])
                self.corrected_text = txt
                res = self.__analyze(txt, co, one_addr, None)
        res2 = None
        if (vars0_ is not None): 
            for vtxt in vars0_: 
                vres = self.__analyze(vtxt, co, one_addr, None)
                if (res2 is None or len(res2) == 0): 
                    res2 = vres
                elif (vres is None or len(vres) != 1 or res2[0].coef >= vres[0].coef): 
                    continue
                else: 
                    res2 = vres
        if ((res is not None and one_addr and len(res) == 1) and len(res[0].items) > 0 and AddressHelper.compare_levels(res[0].items[0].level, AddrLevel.TERRITORY) >= 0): 
            ii = txt.find(' ')
            jj = txt.find(',')
            if (ii < 0): 
                ii = jj
            elif (jj > 0 and (jj < ii)): 
                ii = jj
            if (ii > 0 and ((pars is None or ((not pars.search_regime and not pars.dont_correct_text))))): 
                txt1 = "город {0}, {1}".format(txt[0:0+ii], txt[ii + 1:])
                res1 = self.__analyze(txt1, co, one_addr, src_addr)
                if (res1 is not None and len(res1) == 1 and res1[0].coef > res[0].coef): 
                    res = res1
        if (self.__m_try_this_text_var is not None and ((pars is None or ((not pars.search_regime and not pars.dont_correct_text))))): 
            res3 = self.__analyze(self.__m_try_this_text_var, co, one_addr, src_addr)
            if (self.__m_try_this_text_var2 is not None and ((res3 is None or len(res3) == 0 or (res3[0].coef < 80)))): 
                res4 = self.__analyze(self.__m_try_this_text_var2, co, one_addr, src_addr)
                if (res4 is not None and len(res4) == 1 and res4[0].coef >= 80): 
                    res3 = res4
            if (res3 is not None and len(res3) > 0 and (res3[0].coef < 60)): 
                res3 = (None)
            if (res3 is not None and len(res3) > 0): 
                is_best = False
                if (len(res3) == 1): 
                    if (len(res) == 0 or ((res3[0].coef == 100 and (res[0].coef < 100)))): 
                        is_best = True
                    elif ((res3[0].coef == 100 and res[0].coef == 100 and res3[0].error_message is None) and res[0].error_message is not None): 
                        is_best = True
                    elif (AnalyzeHelper.__has_nasel_punkt(res3[0]) and res3[0].coef > 80 and ((len(res) != 1 or not AnalyzeHelper.__has_nasel_punkt(res[0])))): 
                        is_best = True
                    elif (res[0].last_item_with_gar is not None and res3[0].last_item_with_gar is not None and res3[0].coef >= 60): 
                        ii = AddressHelper.compare_levels(res[0].last_item_with_gar.level, res3[0].last_item_with_gar.level)
                        if (ii < 0): 
                            is_best = True
                        elif (ii == 0): 
                            if (AddressHelper.compare_levels(res[0].last_item.level, res3[0].last_item.level) < 0): 
                                is_best = True
                if (is_best): 
                    HouseRoomHelper.try_process_details(res3[0], detail)
                    return res3
                if (res3[0].coef >= 80): 
                    if (res2 is None or len(res2) == 0 or res3[0].coef > res2[0].coef): 
                        res2 = res3
        if (res is not None and len(res) == 1 and res[0].last_item is not None): 
            if ((res2 is not None and len(res2) == 1 and AnalyzeHelper.__is_better_var(res2[0], res[0])) and res2[0].coef >= 80): 
                HouseRoomHelper.try_process_details(res2[0], detail)
                return res2
            if (len(res[0].last_item.gars) > 0): 
                HouseRoomHelper.try_process_details(res[0], detail)
                return res
        if (res2 is not None and len(res2) == 1 and res2[0].coef >= 80): 
            if (res is None or len(res) == 0 or (res[0].coef < res2[0].coef)): 
                HouseRoomHelper.try_process_details(res2[0], detail)
                return res2
        if (res is not None and detail is not None): 
            for r in res: 
                HouseRoomHelper.try_process_details(r, detail)
        return res
    
    @staticmethod
    def __is_better_var(better : 'TextAddress', wo : 'TextAddress') -> bool:
        if (better.coef > wo.coef): 
            return True
        if (better.coef < wo.coef): 
            return False
        if (better.last_item_with_gar is not None): 
            if (wo.last_item_with_gar is None): 
                return False
            if (AddressHelper.compare_levels(better.last_item_with_gar.level, wo.last_item_with_gar.level) > 0): 
                return True
            if (AddressHelper.compare_levels(better.last_item_with_gar.level, wo.last_item_with_gar.level) < 0): 
                return False
            if (better.error_message is None and wo.error_message is not None): 
                return True
        return False
    
    @staticmethod
    def __has_nasel_punkt(a : 'TextAddress') -> bool:
        for it in a.items: 
            if (it.level == AddrLevel.REGIONCITY or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY): 
                return True
        return False
    
    @staticmethod
    def __has_district(a : 'TextAddress') -> bool:
        for it in a.items: 
            if (it.level == AddrLevel.DISTRICT or it.level == AddrLevel.REGIONAREA or it.level == AddrLevel.REGIONCITY): 
                return True
        return False
    
    def __analyze(self, txt : str, co : typing.List[tuple], one_addr : bool, src_addr : 'TextAddress'=None) -> typing.List['TextAddress']:
        if (AnalyzeHelper.__m_proc1 is None): 
            return list()
        ar = None
        sofa = SourceOfAnalysis._new111(txt, co, False, ("ADDRESS" if one_addr else None))
        if (one_addr and self.m_params is not None and self.m_params.no_flats): 
            sofa.user_params += ";NOFLATS"
        ar = AnalyzeHelper.__m_proc1.process(sofa, None, None)
        res = self._analyze1(ar, txt, co, one_addr)
        if (len(res) > 0): 
            if ((src_addr is not None and res[0].coef > src_addr.coef and res[0].last_item is not None) and res[0].coef >= 80): 
                if (res[0].coef < 100): 
                    res[0].coef = (math.floor(((res[0].coef) * 0.8)))
                if (AddressHelper.compare_levels(res[0].last_item.level, AddrLevel.STREET) > 0 and res[0].last_item.level == src_addr.last_item.level): 
                    if (res[0].find_item_by_level(AddrLevel.STREET) is None and res[0].find_item_by_level(AddrLevel.TERRITORY) is None): 
                        res.clear()
            return res
        if ((isinstance(ar.first_token, TextToken)) and ar.first_token.length_char > 4 and one_addr): 
            txt = ("г." + txt)
            ar = AnalyzeHelper.__m_proc1.process(SourceOfAnalysis._new111(txt, co, False, ("ADDRESS" if one_addr else None)), None, None)
            res = self._analyze1(ar, txt, co, one_addr)
            if ((len(res) == 1 and res[0].last_item is not None and AddressHelper.compare_levels(res[0].last_item.level, AddrLevel.STREET) > 0) and res[0].find_item_by_level(AddrLevel.STREET) is None and res[0].find_item_by_level(AddrLevel.TERRITORY) is None): 
                res.clear()
            elif (len(res) > 0 and (res[0].coef < 60)): 
                res.clear()
        return res
    
    def _analyze1(self, ar : 'AnalysisResult', txt : str, co : typing.List[tuple], one_addr : bool) -> typing.List['TextAddress']:
        res = list()
        if (ar is None or ar.first_token is None): 
            return res
        reg_acr = None
        acr_end = None
        if (((one_addr and (isinstance(ar.first_token, TextToken)) and ar.first_token.chars.is_letter) and ar.first_token.length_char > 1 and (ar.first_token.length_char < 4)) and ar.first_token.next0_ is not None): 
            reg_acr = ar.first_token.term
            acr_end = ar.first_token
        elif ((((one_addr and (isinstance(ar.first_token, TextToken)) and ar.first_token.chars.is_letter) and ar.first_token.length_char == 1 and ar.first_token.next0_ is not None) and ar.first_token.next0_.is_char('.') and (isinstance(ar.first_token.next0_.next0_, TextToken))) and ar.first_token.next0_.next0_.chars.is_letter and ar.first_token.next0_.next0_.length_char == 1): 
            reg_acr = (ar.first_token.term + ar.first_token.next0_.next0_.term)
            acr_end = ar.first_token.next0_.next0_
            if (acr_end.next0_ is not None and acr_end.next0_.is_char('.')): 
                acr_end = acr_end.next0_
        if (reg_acr is not None and acr_end.next0_ is not None): 
            regs = RegionHelper.get_regions_by_abbr(reg_acr)
            if (regs is not None): 
                try: 
                    ar1 = ProcessorService.get_empty_processor().process(SourceOfAnalysis(txt), None, None)
                    for r in regs: 
                        ok = False
                        t = ar1.first_token
                        first_pass3254 = True
                        while True:
                            if first_pass3254: first_pass3254 = False
                            else: t = t.next0_
                            if (not (t is not None)): break
                            if (t.end_char <= acr_end.end_char): 
                                continue
                            toks = r.term_cities.try_parse_all(t, TerminParseAttr.NO)
                            if (toks is not None and len(toks) == 1): 
                                ok = True
                                break
                        if (not ok): 
                            continue
                        txt = "{0}, {1}".format(str(r.attrs), txt[acr_end.next0_.begin_char:])
                        ar = AnalyzeHelper.__m_proc1.process(SourceOfAnalysis._new111(txt, co, False, ("ADDRESS" if one_addr else None)), None, None)
                        break
                except Exception as ex114: 
                    pass
        if (ar.first_token.kit.corrected_tokens is not None): 
            for kp in ar.first_token.kit.corrected_tokens.items(): 
                if (isinstance(kp[0], TextToken)): 
                    pass
        unknown_names = None
        has_delim = False
        first_is_undef = False
        t = ar.first_token
        first_pass3255 = True
        while True:
            if first_pass3255: first_pass3255 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (isinstance(t, ReferentToken)): 
                r = t.get_referent()
                if (r is None): 
                    continue
                aaa = Utils.asObjectOrNull(r, AddressReferent)
                if (aaa is not None and aaa.zip0_ is not None and self.zip0_ is None): 
                    self.zip0_ = aaa.zip0_
                if (r.type_name == "PHONE" or r.type_name == "URI"): 
                    if (len(res) > 0): 
                        res[len(res) - 1].end_char = t.end_char
                    continue
                addr = TextAddress()
                addr.begin_char = t.begin_char
                addr.end_char = t.end_char
                AnalyzeHelper._create_address_items(addr, r, Utils.asObjectOrNull(t, ReferentToken), 0)
                if (len(addr.items) == 0): 
                    continue
                if ((len(addr.items) == 1 and addr.items[0].level == AddrLevel.TERRITORY and t == ar.first_token) and t.next0_ is None): 
                    continue
                addr.sort_items()
                if (len(addr.items) > 0 and (isinstance(addr.items[0].attrs, AreaAttributes)) and "Москва" in addr.items[0].attrs.names): 
                    i = 1
                    first_pass3256 = True
                    while True:
                        if first_pass3256: first_pass3256 = False
                        else: i += 1
                        if (not (i < (len(addr.items) - 1))): break
                        it = addr.items[i]
                        aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
                        if (aa is None): 
                            continue
                        if (it.level == AddrLevel.LOCALITY and "Олимпийская" in aa.names and "деревня" in aa.types): 
                            it.level = AddrLevel.TERRITORY
                            aa.names.clear()
                            aa.names.append("Олимпийская деревня")
                            aa.types.clear()
                            sr0 = StreetReferent()
                            sr0.add_slot("NAME", "ОЛИМПИЙСКАЯ ДЕРЕВНЯ", False, 0)
                            sr0.add_slot(StreetReferent.ATTR_TYPE, "территория", False, 0)
                            na = NameAnalyzer()
                            na.init_by_referent(sr0, False)
                            it.tag = (na)
                        elif ("Олимпийская Деревня" in aa.names): 
                            it.level = AddrLevel.TERRITORY
                add = True
                if (len(res) > 0 and ((addr.items[0].level == AddrLevel.STREET or addr.items[0].level == AddrLevel.TERRITORY))): 
                    a0 = res[len(res) - 1]
                    for ii in range(len(a0.items) - 1, -1, -1):
                        it = a0.items[ii]
                        if (not (isinstance(it.attrs, AreaAttributes))): 
                            continue
                        if (it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.REGIONCITY): 
                            add = False
                            if ((ii + 1) < len(a0.items)): 
                                del a0.items[ii + 1:ii + 1+len(a0.items) - ii - 1]
                            a0.end_char = addr.end_char
                            a0.items.extend(addr.items)
                            addr = a0
                        break
                if ((len(res) == 1 and t.previous is not None and t.previous.is_and) and res[0].last_item.level == AddrLevel.REGIONAREA): 
                    addr.begin_char = res[0].begin_char
                    del res[0]
                if (add): 
                    res.append(addr)
                    if (len(res) > 1 and t.previous is not None): 
                        if (t.previous.is_char(';')): 
                            has_delim = True
                r.tag = (addr)
                if (one_addr and t.next0_ is not None and t.next0_.is_char('(')): 
                    br = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 20)): 
                        t = br.end_token
                        addr.end_char = t.end_char
                tt = t.next0_
                if (tt is not None and tt.is_comma): 
                    tt = tt.next0_
                if (one_addr and (isinstance(tt, TextToken))): 
                    ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                    if ((ait is not None and ait.typ == AddressItemType.NUMBER and not Utils.isNullOrEmpty(ait.value)) and str.isalpha(ait.value[0])): 
                        ait.building_type = AddressBuildingType.LITER
                    if ((ait is None and tt.length_char == 1 and tt.chars.is_all_upper) and tt.chars.is_letter): 
                        ait = AddressItemToken._new115(AddressItemType.BUILDING, tt, tt, AddressBuildingType.LITER, tt.term)
                    if (ait is not None and ait.building_type == AddressBuildingType.LITER): 
                        self.litera_variant = ait
                        t = ait.end_token
                        addr.end_char = t.end_char
            elif ((isinstance(t, TextToken)) and t.length_char > 3 and one_addr): 
                if (self.__def_object_regime is not None and len(res) == 0): 
                    continue
                term = t.term
                if (((term == "ПРОП" or term.startswith("ПРОПИС") or term == "ПРОЖ") or term.startswith("ПРОЖИВ") or term.startswith("РЕГИСТР")) or term.startswith("ПОЧТОВЫЙ")): 
                    if (t.next0_ is not None and t.next0_.is_char(':')): 
                        has_delim = True
                    if (t.previous is not None and t.previous.is_char_of(";:\\/")): 
                        has_delim = True
                    continue
                mc = t.get_morph_class_in_dictionary()
                if (((((((((mc.is_verb or t.is_value("ТОВАРИЩЕСТВО", None) or t.is_value("МУНИЦИПАЛЬНЫЙ", None)) or t.is_value("ГОРОДСКОЙ", None) or t.is_value("СТРАНА", None)) or t.is_value("ПОЧТОВЫЙ", None) or t.is_value("ОКАТО", None)) or t.is_value("СУБЪЕКТ", None) or t.is_value("СТОЛИЦА", None)) or t.is_value("КОРДОН", None) or t.is_value("КОРПУС", None)) or t.is_value("НОМЕР", None) or t.is_value("УЧЕТНЫЙ", None)) or t.is_value("ЗАПИСЬ", None) or t.is_value("ГОСУДАРСТВЕННЫЙ", None)) or t.is_value("РЕЕСТР", None) or t.is_value("ЛЕСНОЙ", None)) or t.is_value("NULL", None) or t.is_value("НАРОДНЫЙ", None)): 
                    pass
                elif (t.is_value("ИНДЕКС", None)): 
                    if (len(res) > 0): 
                        if ((isinstance(t.next0_, NumberToken)) and t.next0_.length_char > 4): 
                            t = t.next0_
                        res[len(res) - 1].end_char = t.end_char
                else: 
                    if (NumberHelper.try_parse_roman(t) is not None): 
                        continue
                    uuu = t.get_source_text()
                    if (Utils.startsWithString(uuu, "РОС", True) or Utils.startsWithString(uuu, "ФЕДЕР", True)): 
                        pass
                    else: 
                        if (unknown_names is None): 
                            unknown_names = list()
                        if (t.begin_char < 6): 
                            first_is_undef = True
                        if (t.next0_ is not None and t.next0_.is_hiphen and (((isinstance(t.next0_.next0_, TextToken)) or (isinstance(t.next0_.next0_, NumberToken))))): 
                            t = t.next0_.next0_
                            uuu = "{0}-{1}".format(uuu, t.get_source_text())
                        unknown_names.append(uuu)
            elif ((one_addr and (isinstance(t, NumberToken)) and t == ar.first_token) and t.length_char == 6 and t.typ == NumberSpellingType.DIGIT): 
                self.zip0_ = t.get_source_text()
        if (unknown_names is None and len(res) > 0 and one_addr): 
            res[0].begin_char = 0
        i = 0
        first_pass3257 = True
        while True:
            if first_pass3257: first_pass3257 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if ((res[i].end_char + 30) > res[i + 1].begin_char): 
                if (len(res[i].items) == 1 and res[i].items[0].level == AddrLevel.COUNTRY and str(res[i].items[0]) == "Россия"): 
                    res[i + 1].begin_char = res[i].begin_char
                    del res[i]
                    i -= 1
                    continue
                if (str(res[i].last_item) == str(res[i + 1].items[0])): 
                    res[i].end_char = res[i + 1].end_char
                    res[i].items.remove(res[i].last_item)
                    res[i].items.extend(res[i + 1].items)
                    del res[i + 1]
                    i -= 1
                    continue
                str0 = str(res[i])
                str1 = str(res[i + 1])
                if (len(res[i].items) == len(res[i + 1].items) and str0 == str1 and res[i].last_item.tag == res[i + 1].last_item.tag): 
                    if ((res[i + 1].end_char - res[i + 1].begin_char) > 10): 
                        res[i].end_char = res[i + 1].end_char
                    del res[i + 1]
                    i -= 1
                    continue
                if (str1.startswith(str0)): 
                    if ((res[i + 1].end_char - res[i + 1].begin_char) < 10): 
                        del res[i + 1]
                        i -= 1
                        continue
                    res[i + 1].begin_char = res[i].begin_char
                    del res[i]
                    i -= 1
                    continue
                if (str0.startswith(str1)): 
                    if (res[i + 1].end_char > res[i].end_char): 
                        res[i].end_char = res[i + 1].end_char
                    del res[i + 1]
                    i -= 1
                    continue
                ok = res[i].last_item.can_be_parent_for(res[i + 1].items[0], None)
                if (len(res[i].items) == 1 and res[i].items[0].level == AddrLevel.CITY and res[i + 1].items[0].level == AddrLevel.CITY): 
                    ok = True
                    res[i].items[0].level = AddrLevel.REGIONCITY
                if (ok): 
                    res[i].end_char = res[i + 1].end_char
                    res[i].items.extend(res[i + 1].items)
                    del res[i + 1]
                    i -= 1
                    continue
                if (AddressHelper.compare_levels(res[i].items[0].level, res[i + 1].last_item.level) > 0): 
                    res[i].end_char = res[i + 1].end_char
                    res[i].items[0:0] = res[i + 1].items
                    res[i].alpha2 = res[i + 1].alpha2
                    del res[i + 1]
                    i -= 1
                    continue
        sec_address = False
        third_address = False
        k = 0
        first_pass3258 = True
        while True:
            if first_pass3258: first_pass3258 = False
            else: k += 1
            if (not (k < len(res))): break
            r = res[k]
            if (one_addr): 
                if (has_delim and ((len(res) == 2 or len(res) == 3))): 
                    sec_address = True
                    if (len(res) == 3): 
                        third_address = True
                    r.text = txt[r.begin_char:r.begin_char+(r.end_char + 1) - r.begin_char]
                    r.begin_char = 0
                    r.end_char = (len(r.text) - 1)
                else: 
                    r.text = txt
            ad = Utils.asObjectOrNull(r.last_item.tag, AddressReferent)
            if (ad is not None): 
                del r.items[len(r.items) - 1]
            if (self.__def_object_regime is not None): 
                while len(r.items) > 0:
                    if (AddressHelper.compare_levels(r.items[0].level, AddrLevel.CITY) <= 0): 
                        del r.items[0]
                    else: 
                        break
                if (len(r.items) == 0): 
                    return None
                oo = GarHelper.create_addr_object(self.__def_object_regime)
                if (oo is not None): 
                    r.items.insert(0, oo)
            r2 = r.clone()
            r3 = r.clone()
            has_sec_var = False
            has_alt_var = False
            self.create_alts_regime = False
            wraphas_sec_var117 = RefOutArgWrapper(False)
            ad2 = self._process_address(r, wraphas_sec_var117)
            has_sec_var = wraphas_sec_var117.value
            if (ad2 is not None and ad is not None): 
                ad2.merge_slots(ad, True)
            if (self.zip_var_streets is not None and len(r.items) > 0): 
                rvars = list()
                for g in self.zip_var_streets: 
                    zta = r.clone()
                    zta.items.clear()
                    zta.info_message = None
                    zta.error_message = zta.info_message
                    zta.items.append(GarHelper.create_addr_object(g))
                    AnalyzeHelper._add_miss_items(self, zta)
                    self._process_rest(zta, Utils.ifNotNull(ad2, ad), one_addr, ar)
                    CoefHelper.calc_coef(self, zta, one_addr, Utils.ifNotNull(r.text, txt), unknown_names)
                    CorrectionHelper.correct_country(zta)
                    hou = zta.find_item_by_level(AddrLevel.BUILDING)
                    if (hou is not None and len(hou.gars) > 0): 
                        if (hou.gars[0].get_param_value(GarParam.POSTINDEX) == self.zip0_): 
                            rvars.append(zta)
                if (len(rvars) == 1 and rvars[0].coef == 100): 
                    res[k] = rvars[0]
                    continue
            self._process_rest(r, Utils.ifNotNull(ad2, ad), one_addr, ar)
            CoefHelper.calc_coef(self, r, one_addr, Utils.ifNotNull(r.text, txt), unknown_names)
            if ((len(r2.items) == 2 and r2.items[0]._doubt_type and r2.items[1]._doubt_type) and ad is not None): 
                has_alt_var = True
                r2.items[0].level = AddrLevel.CITY
                r2.items[0].attrs.types.clear()
                r2.items[0].tag.level = AddrLevel.CITY
                r2.items[1].level = AddrLevel.STREET
                r2.items[1].attrs.types.clear()
                r2.items[1].tag.level = AddrLevel.STREET
                r2.items[1].tag.types.clear()
            if (r.coef == 100 and not has_sec_var): 
                if (not has_alt_var): 
                    continue
            if (has_sec_var or has_alt_var): 
                if (not has_alt_var): 
                    self.create_alts_regime = True
                wraphas_sec_var116 = RefOutArgWrapper(False)
                ad2 = self._process_address(r2, wraphas_sec_var116)
                has_sec_var = wraphas_sec_var116.value
                if (ad2 is not None and ad is not None): 
                    ad2.merge_slots(ad, True)
                self._process_rest(r2, Utils.ifNotNull(ad2, ad), one_addr, ar)
                CoefHelper.calc_coef(self, r2, one_addr, txt, unknown_names)
                if (r2.coef > r.coef): 
                    res[k] = r2
                    r = r2
                elif ((r2.coef == r.coef and ((((r2.error_message is None and r.error_message is not None)) or has_alt_var)) and r2.last_item_with_gar is not None) and r.last_item_with_gar is not None): 
                    if (AddressHelper.compare_levels(r2.last_item_with_gar.level, r.last_item_with_gar.level) > 0): 
                        res[k] = r2
                        r = r2
            if (r.coef >= 95): 
                continue
            if (not one_addr): 
                continue
            if ((len(r3.items) < 2) or len(res) > 1): 
                continue
            reg = RegionHelper.is_big_citya(r3.items[0])
            if (reg is not None and reg.capital is not None and r3.items[0].attrs.contains_name(reg.capital)): 
                pass
            elif (len(r3.items) > 1 and r3.items[0].level == AddrLevel.DISTRICT and r3.items[1].level == AddrLevel.CITY): 
                reg = RegionHelper.is_big_citya(r3.items[1])
                if (reg is not None and reg.capital is not None and r3.items[1].attrs.contains_name(reg.capital)): 
                    it = r3.items[0]
                    del r3.items[0]
                    r3.items.insert(1, it)
                else: 
                    continue
            else: 
                continue
            txt1 = reg.replace_capital_by_region(txt)
            if (txt1 is not None and txt != txt1): 
                res2 = self.analyze(txt1, None, True, self.m_params, False)
                if (res2 is not None and len(res2) == 1 and res2[0].coef > r.coef): 
                    return res2
        for r in res: 
            CorrectionHelper.correct_country(r)
        if (sec_address and ((len(res) == 2 or len(res) == 3)) and one_addr): 
            res[0].second_address = res[1]
            del res[1]
            if (len(res) == 2): 
                res[0].second_address.second_address = res[1]
                del res[1]
        if (len(res) > 1 and one_addr): 
            if (res[0].end_char > res[0].begin_char): 
                del res[1:1+len(res) - 1]
        if (len(res) > 1 and one_addr): 
            res[0].coef = math.floor(res[0].coef / len(res))
            msg = "В строке выделилось {0} адрес{1}, второй: {2}. ".format(len(res), ("а" if len(res) < 5 else "ов"), str(res[1]))
            if (res[0].error_message is None): 
                res[0].error_message = msg
            else: 
                res[0].error_message = "{0} {1}".format(res[0].error_message, msg)
        if ((one_addr and len(res) == 1 and ((first_is_undef or (res[0].coef < 90)))) and self.__m_try_this_text_var is None): 
            if (not AnalyzeHelper.__has_nasel_punkt(res[0])): 
                self.__m_try_this_text_var = ("н.п. " + txt)
                if (not AnalyzeHelper.__has_district(res[0])): 
                    self.__m_try_this_text_var2 = ("район " + txt)
            elif (txt.startswith("г.")): 
                self.__m_try_this_text_var = ("н.п. " + txt[2:])
            elif (first_is_undef): 
                self.__m_try_this_text_var = ("н.п. " + txt)
                if (not AnalyzeHelper.__has_district(res[0])): 
                    self.__m_try_this_text_var2 = ("район " + txt)
        if ((one_addr and len(res) == 0 and self.__m_try_this_text_var is None) and self.m_params is not None and self.m_params.default_object is not None): 
            self.__m_try_this_text_var = ("ул. " + txt)
        return res
    
    def create_text_address_by_referent(self, r : 'Referent') -> 'TextAddress':
        addr = TextAddress()
        AnalyzeHelper._create_address_items(addr, r, None, 0)
        if (len(addr.items) == 0): 
            return None
        addr.sort_items()
        r.tag = (addr)
        ad = Utils.asObjectOrNull(addr.last_item.tag, AddressReferent)
        if (ad is not None): 
            del addr.items[len(addr.items) - 1]
        r2 = r.clone()
        r3 = r.clone()
        has_sec_var = False
        self.create_alts_regime = False
        wraphas_sec_var118 = RefOutArgWrapper(False)
        ad2 = self._process_address(addr, wraphas_sec_var118)
        has_sec_var = wraphas_sec_var118.value
        self._process_rest(addr, Utils.ifNotNull(ad, ad2), True, None)
        CoefHelper.calc_coef(self, addr, True, None, None)
        CorrectionHelper.correct_country(addr)
        return addr
    
    @staticmethod
    def _create_address_items(addr : 'TextAddress', r : 'Referent', rt : 'ReferentToken', lev : int) -> None:
        if (lev > 10 or r is None): 
            return
        own = None
        own2 = None
        sown = None
        sown2 = None
        sown22 = None
        detail_typ = DetailType.UNDEFINED
        detail_param = None
        detail_org = None
        if (isinstance(r, GeoReferent)): 
            geo = Utils.asObjectOrNull(r, GeoReferent)
            if (geo.is_state and geo.alpha2 is not None): 
                if (((geo.alpha2 == "RU" or geo.alpha2 == "SU")) and lev > 0): 
                    return
                cou = CorrectionHelper.create_country(geo.alpha2, geo)
                if (cou is not None): 
                    addr.alpha2 = geo.alpha2
                    if (len(addr.items) > 0 and addr.items[0].level == AddrLevel.COUNTRY): 
                        pass
                    else: 
                        addr.items.append(cou)
                    return
            elif (geo.is_state and geo.find_slot("NAME", "РСФСР", True) is not None): 
                addr.alpha2 = "RU"
                return
            aa = AreaAttributes()
            res = AddrObject(aa)
            if ((isinstance(r, GeoReferent)) and Utils.compareStrings(str(r), "ДНР", True) == 0): 
                r = (GeoReferent())
                r.add_slot(GeoReferent.ATTR_TYPE, "республика", False, 0)
                r.add_slot(GeoReferent.ATTR_NAME, "ДОНЕЦКАЯ", False, 0)
                res.level = AddrLevel.REGIONAREA
            elif ((isinstance(r, GeoReferent)) and Utils.compareStrings(str(r), "ЛНР", True) == 0): 
                r = (GeoReferent())
                r.add_slot(GeoReferent.ATTR_TYPE, "республика", False, 0)
                r.add_slot(GeoReferent.ATTR_NAME, "ЛУГАНСКАЯ", False, 0)
                res.level = AddrLevel.REGIONAREA
            gstr = str(geo)
            is_reg = False
            if (gstr == "область Читинская"): 
                geo = GeoReferent()
                geo.add_slot(GeoReferent.ATTR_NAME, "ЗАБАЙКАЛЬСКИЙ", False, 0)
                geo.add_slot(GeoReferent.ATTR_TYPE, "край", False, 0)
                r = (geo)
            if (gstr == "область Крымская"): 
                geo = GeoReferent()
                geo.add_slot(GeoReferent.ATTR_NAME, "КРЫМ", False, 0)
                geo.add_slot(GeoReferent.ATTR_TYPE, "республика", False, 0)
                r = (geo)
                is_reg = True
            if (gstr == "Нагорный Карабах"): 
                is_reg = True
                addr.alpha2 = "AZ"
            if (gstr == "область Куйбышевская"): 
                geo = GeoReferent()
                geo.add_slot(GeoReferent.ATTR_NAME, "САМАРСКАЯ", False, 0)
                geo.add_slot(GeoReferent.ATTR_TYPE, "область", False, 0)
                r = (geo)
            if (gstr == "область Калининская"): 
                geo = GeoReferent()
                geo.add_slot(GeoReferent.ATTR_NAME, "ТВЕРСКАЯ", False, 0)
                geo.add_slot(GeoReferent.ATTR_TYPE, "область", False, 0)
                r = (geo)
            if (gstr.startswith("Донецкая") or gstr.startswith("Луганская")): 
                is_reg = True
            typs = r.get_string_values(GeoReferent.ATTR_TYPE)
            if ((geo.alpha2 == "UA" or geo.alpha2 == "BY" or geo.alpha2 == "KZ") or geo.alpha2 == "KG"): 
                aa.types.append("республика")
            elif (len(typs) > 0): 
                aa.types.extend(typs)
                if (is_reg and "государство" in aa.types): 
                    aa.types.remove("государство")
            nam = r.get_string_value(GeoReferent.ATTR_NAME)
            if (nam is not None and nam in RegionHelper.CITY_RENAMES): 
                r.add_slot(GeoReferent.ATTR_NAME, RegionHelper.CITY_RENAMES[nam], False, 0)
            AnalyzeHelper.__set_name(aa, r, GeoReferent.ATTR_NAME)
            AnalyzeHelper.__set_misc(aa, r, GeoReferent.ATTR_MISC)
            aa.number = r.get_string_value("NUMBER")
            na = NameAnalyzer()
            na.init_by_referent(r, False)
            res.tag = (na)
            if (is_reg): 
                na.level = AddrLevel.REGIONAREA
            res._doubt_type = geo.is_probable
            addr.items.append(res)
            own = geo.higher
            if (res.level == AddrLevel.UNDEFINED): 
                if (geo.alpha2 is None and na.level == AddrLevel.COUNTRY): 
                    res.level = AddrLevel.REGIONAREA
                else: 
                    res.level = na.level
            else: 
                na.level = res.level
            r.tag = (res)
            if (r.ontology_items is not None and len(r.ontology_items) > 0): 
                if (isinstance(r.ontology_items[0].ext_id, str)): 
                    res.ext_id = (Utils.asObjectOrNull(r.ontology_items[0].ext_id, str))
        elif (isinstance(r, StreetReferent)): 
            sown = r.higher
            uni = NameAnalyzer.merge_objects(sown, r)
            if (uni is not None): 
                AnalyzeHelper._create_address_items(addr, uni, rt, lev + 1)
                r.tag = (addr)
                sown.tag = (addr)
                return
            aa = AreaAttributes()
            res = AddrObject(aa)
            aa.types.extend(r.typs)
            if (len(aa.types) > 1 and "улица" in aa.types): 
                aa.types.remove("улица")
                aa.types.append("улица")
            AnalyzeHelper.__set_name(aa, r, StreetReferent.ATTR_NAME)
            AnalyzeHelper.__set_misc(aa, r, StreetReferent.ATTR_MISC)
            aa.number_param = r.get_string_value(StreetReferent.ATTR_PARAM)
            ki = r.kind
            if (ki == StreetKind.ROAD): 
                aa.miscs.append("дорога")
            aa.number = r.numbers
            if ((aa.number is not None and aa.number.endswith("км") and len(aa.names) == 0) and ki != StreetKind.ROAD): 
                aa.types.append("километр")
                aa.number = aa.number[0:0+len(aa.number) - 2]
            na = NameAnalyzer()
            na.init_by_referent(r, False)
            res.tag = (na)
            addr.items.append(res)
            own = (Utils.asObjectOrNull(r.get_slot_value(StreetReferent.ATTR_GEO), GeoReferent))
            res.level = na.level
            if (ki == StreetKind.ROAD and res.level == AddrLevel.STREET): 
                res.level = AddrLevel.TERRITORY
            r.tag = (res)
        elif (isinstance(r, AddressReferent)): 
            ar = Utils.asObjectOrNull(r, AddressReferent)
            sown = (Utils.asObjectOrNull(ar.get_slot_value(AddressReferent.ATTR_STREET), StreetReferent))
            streets = ar.streets
            if (len(streets) > 1): 
                if (ar.detail == AddressDetailType.CROSS): 
                    sown2 = (Utils.asObjectOrNull(streets[1], StreetReferent))
                elif ("очередь" in sown.typs or "очередь" in ar.streets[1].typs): 
                    sown2 = (Utils.asObjectOrNull(streets[1], StreetReferent))
                else: 
                    sown2 = (Utils.asObjectOrNull(streets[1], StreetReferent))
            if (len(streets) > 2): 
                sown22 = (Utils.asObjectOrNull(streets[2], StreetReferent))
            geos = ar.geos
            if (len(geos) > 0): 
                own = geos[0]
                if (len(geos) > 1): 
                    own2 = geos[1]
            if (ar.detail != AddressDetailType.UNDEFINED and ar.detail != AddressDetailType.CROSS): 
                wrapdetail_param119 = RefOutArgWrapper(None)
                detail_typ = HouseRoomHelper.create_dir_details(ar, wrapdetail_param119)
                detail_param = wrapdetail_param119.value
                own3 = Utils.asObjectOrNull(ar.get_slot_value(AddressReferent.ATTR_DETAILREF), GeoReferent)
                if (own3 is not None): 
                    if (own3.higher is None): 
                        own3.higher = own
                    if (own is None): 
                        own = own3
                    elif (own3.higher == own): 
                        own = own3
                    elif (own3.higher is not None and ((own3.higher.higher is None or own3.higher.higher == own)) and GeoOwnerHelper.can_be_higher(own, own3.higher, None, None)): 
                        own3.higher.higher = own
                        if (sown is not None and sown.parent_referent == own): 
                            sown.add_slot(StreetReferent.ATTR_GEO, own3, True, 0)
                            own = (None)
                        else: 
                            own = own3
            else: 
                org0_ = Utils.asObjectOrNull(ar.get_slot_value(AddressReferent.ATTR_DETAILREF), OrganizationReferent)
                if (org0_ is not None): 
                    aa = AreaAttributes()
                    detail_org = AddrObject(aa)
                    detail_org.level = AddrLevel.TERRITORY
                    aa.types.append("территория")
                    AnalyzeHelper.__set_name(aa, org0_, OrganizationReferent.ATTR_NAME)
                    AnalyzeHelper.__set_misc(aa, org0_, OrganizationReferent.ATTR_TYPE)
                    aa.number = org0_.number
                    na = NameAnalyzer()
                    na.init_by_referent(org0_, False)
                    detail_org.tag = (na)
                    addr.items.append(detail_org)
            if (ar.block is not None): 
                sr = StreetReferent()
                sr.add_slot(StreetReferent.ATTR_TYPE, "блок", False, 0)
                sr.add_slot(StreetReferent.ATTR_NUMBER, ar.block, False, 0)
                aa = AreaAttributes()
                aa.types.append("блок")
                aa.number = ar.block
                ao = AddrObject._new120(aa, AddrLevel.STREET)
                na = NameAnalyzer()
                na.init_by_referent(sr, False)
                ao.tag = (na)
                addr.items.append(ao)
            ha = HouseAttributes()
            res = AddrObject(ha)
            res.level = AddrLevel.BUILDING
            res.tag = (ar)
            r.tag = (res)
            addr.items.append(res)
        if (sown is not None): 
            addr1 = TextAddress()
            AnalyzeHelper._create_address_items(addr1, sown, None, lev + 1)
            if (len(addr1.items) > 0): 
                if (addr.alpha2 is None): 
                    addr.alpha2 = addr1.alpha2
                if (addr1.last_item.can_be_parent_for(addr.items[0], None)): 
                    addr.items[0:0] = addr1.items
                    if (sown2 is not None): 
                        addr2 = TextAddress()
                        AnalyzeHelper._create_address_items(addr2, sown2, None, lev + 1)
                        if (addr2.last_item is not None and addr2.last_item.can_be_equals_level(addr1.last_item)): 
                            a1 = Utils.asObjectOrNull(addr1.last_item.attrs, AreaAttributes)
                            a2 = Utils.asObjectOrNull(addr2.last_item.attrs, AreaAttributes)
                            if ("очередь" in a1.types and a1.number is not None and len(a1.names) == 0): 
                                addr.params[ParamType.ORDER] = a1.number
                                addr.items[len(addr1.items) - 1] = addr2.last_item
                            elif ("очередь" in a2.types and a2.number is not None and len(a2.names) == 0): 
                                addr.params[ParamType.ORDER] = a1.number
                            elif (addr2.last_item.level == AddrLevel.TERRITORY): 
                                addr.items.insert(len(addr1.items), addr2.last_item)
                                if (sown22 is not None): 
                                    addr3 = TextAddress()
                                    AnalyzeHelper._create_address_items(addr3, sown22, None, lev + 1)
                                    if (addr3.last_item is not None and addr3.last_item.level == addr1.last_item.level): 
                                        addr.items.insert(len(addr1.items) + 1, addr3.last_item)
                            else: 
                                addr1.last_item.cross_object = addr2.last_item
                elif (addr1.last_item.level == AddrLevel.STREET and ((addr.items[0].level == AddrLevel.TERRITORY or addr.items[0].level == AddrLevel.STREET))): 
                    addr.items[0:0] = addr1.items
        if (own is not None): 
            addr1 = TextAddress()
            AnalyzeHelper._create_address_items(addr1, own, None, lev + 1)
            if (len(addr1.items) > 0): 
                if (addr.alpha2 is None): 
                    addr.alpha2 = addr1.alpha2
                if (detail_typ != DetailType.UNDEFINED and sown is not None): 
                    addr1.last_item.detail_typ = detail_typ
                    addr1.last_item.detail_param = detail_param
                ins = False
                if (AddressHelper.compare_levels(addr1.last_item.level, addr.items[0].level) < 0): 
                    ins = True
                elif (addr1.last_item.can_be_parent_for(addr.items[0], None)): 
                    ins = True
                elif (addr1.last_item.level == AddrLevel.CITY and ((addr.items[0].level == AddrLevel.DISTRICT or addr.items[0].level == AddrLevel.SETTLEMENT))): 
                    ins = True
                elif (addr1.last_item.level == AddrLevel.DISTRICT and addr.items[0].level == AddrLevel.LOCALITY): 
                    ins = True
                if (ins): 
                    if (str(addr).startswith(str(addr1))): 
                        pass
                    else: 
                        addr.items[0:0] = addr1.items
                elif (((addr1.last_item.level == AddrLevel.SETTLEMENT or addr1.last_item.level == AddrLevel.LOCALITY)) and addr.items[0].level == AddrLevel.DISTRICT): 
                    if (str(addr).startswith(str(addr1))): 
                        pass
                    else: 
                        it0 = addr.items[0]
                        addr.items.clear()
                        addr.items.extend(addr1.items)
                        addr.items.insert(len(addr.items) - 1, it0)
                elif (detail_typ != DetailType.UNDEFINED and addr1.last_item.detail_typ != DetailType.UNDEFINED and (len(addr1.items) < len(addr.items))): 
                    i = 0
                    i = 0
                    while i < (len(addr1.items) - 1): 
                        if (str(addr1.items[i]) != str(addr.items[i])): 
                            break
                        i += 1
                    if (i == (len(addr1.items) - 1) and (AddressHelper.compare_levels(addr1.items[i].level, addr.items[i].level) < 0)): 
                        addr.items.insert(i, addr1.items[i])
        if (addr.last_item is not None): 
            aa = Utils.asObjectOrNull(addr.last_item.attrs, AreaAttributes)
            na = Utils.asObjectOrNull(addr.last_item.tag, NameAnalyzer)
            if ((aa is not None and len(aa.names) > 0 and aa.number is not None) and aa.number.endswith("км") and na.sec is not None): 
                aa1 = AreaAttributes()
                aa1.number = aa.number[0:0+len(aa.number) - 2]
                aa1.types.append("километр")
                km = AddrObject(aa1)
                km.level = AddrLevel.STREET
                addr.last_item.level = AddrLevel.TERRITORY
                km.tag = (na.sec)
                na.sec = (None)
                aa.number = (None)
                addr.items.append(km)
    
    @staticmethod
    def __set_name(a : 'AreaAttributes', r : 'Referent', typ : str) -> None:
        if (r is None): 
            return
        names = r.get_string_values(typ)
        if (names is None or len(names) == 0): 
            return
        long_name = None
        i = 0
        first_pass3259 = True
        while True:
            if first_pass3259: first_pass3259 = False
            else: i += 1
            if (not (i < len(names))): break
            nam = names[i]
            ii = nam.find('-')
            if (ii > 0 and ((ii + 1) < len(nam)) and str.isdigit(nam[ii + 1])): 
                a.number = nam[ii + 1:]
                r.add_slot("NUMBER", a.number, False, 0)
                ss = r.find_slot("NAME", nam, True)
                if (ss is not None): 
                    r.slots.remove(ss)
                nam = nam[0:0+ii]
                r.add_slot("NAME", nam, False, 0)
            if (nam == "МИКРОРАЙОН"): 
                if (not nam.lower() in a.types): 
                    a.types.append(nam.lower())
                del names[i]
                i -= 1
                continue
            names[i] = MiscHelper.convert_first_char_upper_and_other_lower(nam)
            if (long_name is None): 
                long_name = names[i]
            elif (len(long_name) > len(names[i])): 
                long_name = names[i]
        if (len(names) > 1 and names[0] != long_name): 
            names.remove(long_name)
            names.insert(0, long_name)
        a.names = names
    
    @staticmethod
    def __set_misc(a : 'AreaAttributes', r : 'Referent', nam : str) -> None:
        a.miscs = r.get_string_values(nam)
        if (len(a.miscs) > 0): 
            has_up = False
            for m in a.miscs: 
                if (str.isupper(m[0])): 
                    has_up = True
            if (has_up): 
                for i in range(len(a.miscs) - 1, -1, -1):
                    if (not str.isupper(a.miscs[i][0])): 
                        del a.miscs[i]
    
    @staticmethod
    def __get_id(v : str) -> int:
        return int(v[1:])
    
    @staticmethod
    def __add_par_ids(par_ids : typing.List[int], ao : 'AddrObject') -> None:
        for p in ao.gars: 
            id0_ = AnalyzeHelper.__get_id(p.id0_)
            if (not id0_ in par_ids): 
                par_ids.append(id0_)
    
    @staticmethod
    def __can_search_gars(r : 'NameAnalyzer', addr : 'TextAddress', i : int) -> bool:
        if (r.level == AddrLevel.TERRITORY or r.level == AddrLevel.STREET): 
            j = 0
            while j < i: 
                if (len(addr.items[j].gars) > 0): 
                    it = addr.items[j]
                    if (((it.level == AddrLevel.REGIONCITY or it.level == AddrLevel.CITY or it.level == AddrLevel.SETTLEMENT) or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.UNDEFINED) or it.level == AddrLevel.TERRITORY): 
                        return True
                    if (it.level == AddrLevel.DISTRICT): 
                        if ("улус" in it.attrs.types or "городской округ" in it.attrs.types or "муниципальный округ" in it.attrs.types): 
                            return True
                        if (len(it.gars) > 0): 
                            if ("городской округ" in it.gars[0].attrs.types): 
                                return True
                    if (r.level == AddrLevel.TERRITORY): 
                        if (j == (i - 1) and ((it.level == AddrLevel.DISTRICT or it.level == AddrLevel.SETTLEMENT))): 
                            return True
                        if (j == (i - 2) and it.level == AddrLevel.DISTRICT and ((addr.items[j + 1].detail_typ != DetailType.UNDEFINED or addr.items[j + 1].level == AddrLevel.TERRITORY))): 
                            return True
                    if (r.level == AddrLevel.STREET and i == 1): 
                        if (len(r.types) == 0): 
                            return True
                        nam = r.ref.get_string_value("NAME")
                        if (nam is not None and nam.find(' ') > 0): 
                            return True
                        if (it.gars[0].region_number == 50): 
                            return True
                j += 1
            return False
        if (r.level == AddrLevel.LOCALITY and i == 0): 
            return False
        return True
    
    def _process_address(self, addr : 'TextAddress', has_sec_var : bool) -> 'AddressReferent':
        has_sec_var.value = False
        if (len(addr.items) == 0): 
            return None
        ar = None
        regions = bytearray()
        other_country = False
        par_ids = list()
        ua_country = None
        rev = False
        dont_change_region = False
        i = 0
        first_pass3260 = True
        while True:
            if first_pass3260: first_pass3260 = False
            else: i += 1
            if (not (i < len(addr.items))): break
            it = addr.items[i]
            aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            if (aa is None): 
                break
            if (GarHelper.GAR_INDEX is None or other_country): 
                continue
            if (i == 0 and it.level == AddrLevel.COUNTRY): 
                if ("Украина" in aa.names): 
                    ua_country = it
                    del addr.items[0]
                    i -= 1
                    continue
                other_country = True
                continue
            if (len(it.gars) > 0): 
                if (len(regions) == 0): 
                    regions.append(it.gars[0].region_number)
                continue
            r = Utils.asObjectOrNull(it.tag, NameAnalyzer)
            if (r is None): 
                continue
            if ((it.level == AddrLevel.STREET and len(aa.types) == 0 and i > 0) and addr.items[i - 1].level == AddrLevel.REGIONAREA): 
                it.level = AddrLevel.LOCALITY
                aa.types.append("населенный пункт")
                r.level = AddrLevel.LOCALITY
            max_count = 50
            if (addr.items[0].level == AddrLevel.REGIONCITY): 
                max_count = 100
            elif (r.level == AddrLevel.TERRITORY): 
                max_count = 200
            par_ids.clear()
            pcou = 0
            for j in range(i - 1, -1, -1):
                it0 = addr.items[j]
                if (len(it0.gars) == 0): 
                    continue
                if (AddressHelper.compare_levels(it0.level, it.level) >= 0 and not AddressHelper.can_be_parent(it0.level, it.level)): 
                    break
                AnalyzeHelper.__add_par_ids(par_ids, it0)
                pcou += 1
                if (it0.level == AddrLevel.LOCALITY): 
                    break
                if (it.level == AddrLevel.TERRITORY and pcou > 1): 
                    break
                if (it0.level == AddrLevel.CITY): 
                    if (it.level == AddrLevel.LOCALITY): 
                        for g in it0.gars: 
                            if (len(g.parent_ids) == 0): 
                                continue
                            gg = self.get_gar_object(g.parent_ids[0])
                            if (gg is not None and gg.level == GarLevel.MUNICIPALAREA): 
                                par_ids.append(AnalyzeHelper.__get_id(gg.id0_))
                    break
            search_always = False
            if (len(par_ids) == 0): 
                if (i > 0): 
                    if (i == 1 and r.level == AddrLevel.CITY and len(addr.items[0].gars) == 0): 
                        cou = CorrectionHelper.find_country(it)
                        if (cou is not None): 
                            addr.items.insert(0, cou)
                            break
                    if (it.level == AddrLevel.CITY and RegionHelper.is_big_citya(it) is not None): 
                        pass
                    else: 
                        continue
                if (AddressHelper.compare_levels(it.level, AddrLevel.LOCALITY) >= 0 or it.level == AddrLevel.SETTLEMENT or it.level == AddrLevel.DISTRICT): 
                    r.strict_search = True
                    if (self.m_params is None or ((self.m_params.default_object is None and len(self.m_params.default_regions) == 0))): 
                        if (it.level != AddrLevel.LOCALITY and it.level != AddrLevel.SETTLEMENT and it.level != AddrLevel.DISTRICT): 
                            if (((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY)) and i == 0 and self.zip0_ is not None): 
                                pass
                            else: 
                                continue
                        else: 
                            probs2 = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, 30)
                            if (probs2 is None): 
                                if (it.level == AddrLevel.DISTRICT and len(addr.items) > 1 and addr.items[1].level == AddrLevel.CITY): 
                                    del addr.items[0]
                                    addr.items.insert(1, it)
                                    i = -1
                                continue
                            cou2 = 0
                            reg2 = 0
                            jj = 0
                            first_pass3261 = True
                            while True:
                                if first_pass3261: first_pass3261 = False
                                else: jj += 1
                                if (not (jj < len(probs2))): break
                                p = probs2[jj]
                                if ((i + 1) < len(addr.items)): 
                                    it1 = addr.items[i + 1]
                                    regions.append(p.region)
                                    probs3 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(it1.tag, NameAnalyzer), regions, par_ids, 3)
                                    regions.clear()
                                    if (probs3 is None): 
                                        del probs2[jj]
                                        jj -= 1
                                        continue
                                if (reg2 == (0)): 
                                    reg2 = p.region
                                    cou2 = 1
                                elif (reg2 != p.region): 
                                    cou2 += 1
                            if (cou2 == 1): 
                                regions.append(probs2[0].region)
                                search_always = True
                                self.__add_gars(addr, probs2, i, regions, False)
                                if (len(it.gars) > 0): 
                                    AnalyzeHelper._add_miss_items(self, addr)
                                continue
                            else: 
                                continue
                    if (self.m_params is not None and self.m_params.default_object is None): 
                        for rid in self.m_params.default_regions: 
                            regions.append(rid)
                        if (len(regions) == 0 and self.m_params.prev_address is None): 
                            continue
                    elif (self.m_params is not None and self.m_params.default_object is not None): 
                        to1 = GarHelper.create_addr_object(self.m_params.default_object)
                        if (AddressHelper.compare_levels(it.level, to1.level) > 0): 
                            par_ids.append(AnalyzeHelper.__get_id(self.m_params.default_object.id0_))
                            if (self.m_params.default_object.region_number > 0): 
                                regions.append(self.m_params.default_object.region_number)
                            addr.items.insert(0, to1)
                            i += 1
                            dont_change_region = True
                        elif (it.level == to1.level): 
                            eq = str(it) == str(to1)
                            if (not eq): 
                                na2 = NameAnalyzer()
                                na2.process_ex(self.m_params.default_object)
                                if (len(r.strings) > 0 and len(na2.strings) > 0 and na2.strings[0].startswith(r.strings[0])): 
                                    eq = True
                            if (eq): 
                                it.gars.append(self.m_params.default_object)
                                if (self.m_params.default_object.region_number > 0): 
                                    regions.append(self.m_params.default_object.region_number)
                                dont_change_region = True
                                continue
            if (((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY)) and self.zip0_ is not None): 
                has_loc = False
                for ii in range(i - 1, -1, -1):
                    it0 = addr.items[ii]
                    if ((it0.level == AddrLevel.CITY or it0.level == AddrLevel.REGIONCITY or it0.level == AddrLevel.LOCALITY) or it0.level == AddrLevel.SETTLEMENT): 
                        has_loc = True
                zip0__ = 0
                wrapzip121 = RefOutArgWrapper(0)
                Utils.tryParseInt(self.zip0_, wrapzip121)
                zip0__ = wrapzip121.value
                if (not has_loc and zip0__ > 0): 
                    cities = list()
                    locs = list()
                    gstreets = list()
                    streets = list()
                    ids = GarHelper.GAR_INDEX.get_ao_ids_by_zip(zip0__)
                    if (ids is not None): 
                        for id0_ in ids: 
                            go = self.get_gar_object("a{0}".format(id0_))
                            if (go is None): 
                                continue
                            if (go.level == GarLevel.CITY): 
                                cities.append(go)
                            elif (go.level == GarLevel.LOCALITY): 
                                locs.append(go)
                            if (i > 0): 
                                continue
                            if (go.level == GarLevel.STREET): 
                                sao = GarHelper.create_addr_object(go)
                                if (sao.attrs.can_be_equals(Utils.asObjectOrNull(it.attrs, AreaAttributes))): 
                                    streets.append(sao)
                                    gstreets.append(go)
                    if (len(streets) >= 1): 
                        if (it.level != AddrLevel.STREET): 
                            addr.items.insert(i, streets[0])
                            j = 1
                            while j < len(gstreets): 
                                addr.items[i].gars.append(gstreets[j])
                                j += 1
                        else: 
                            it.gars.extend(gstreets)
                        self.zip_var_streets = gstreets
                        continue
                    for ii in range(len(locs) - 1, -1, -1):
                        pars0 = list()
                        pars0.append(AnalyzeHelper.__get_id(locs[ii].id0_))
                        regs0 = bytearray()
                        regs0.append(locs[ii].region_number)
                        probs0 = GarHelper.GAR_INDEX._get_string_entries(r, regs0, pars0, max_count)
                        if (probs0 is None): 
                            del locs[ii]
                    if (len(locs) != 1): 
                        for ii in range(len(cities) - 1, -1, -1):
                            pars0 = list()
                            pars0.append(AnalyzeHelper.__get_id(cities[ii].id0_))
                            regs0 = bytearray()
                            regs0.append(cities[ii].region_number)
                            probs0 = GarHelper.GAR_INDEX._get_string_entries(r, regs0, pars0, max_count)
                            if (probs0 is None): 
                                del cities[ii]
                    ao = None
                    if (len(locs) == 1): 
                        ao = GarHelper.create_addr_object(locs[0])
                    elif (len(cities) == 1): 
                        ao = GarHelper.create_addr_object(cities[0])
                    elif (len(cities) > 0): 
                        self.zip_var_cities = cities
                    if (ao is not None): 
                        if (i == 0 or (AddressHelper.compare_levels(addr.items[i - 1].level, ao.level) < 0)): 
                            addr.items.insert(i, ao)
                            if (len(regions) == 0): 
                                regions.append(ao.gars[0].region_number)
                            continue
            if ((i == 0 and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.STREET)) and self.m_params is not None) and self.m_params.prev_address is not None): 
                for jj in range(len(self.m_params.prev_address.items) - 1, 0, -1):
                    it0 = self.m_params.prev_address.items[jj]
                    if (it0.level == AddrLevel.LOCALITY or it0.level == AddrLevel.CITY): 
                        pass
                    else: 
                        continue
                    if (len(it0.gars) != 1): 
                        continue
                    pars0 = list()
                    pars0.append(AnalyzeHelper.__get_id(it0.gars[0].id0_))
                    regs0 = bytearray()
                    regs0.append(it0.gars[0].region_number)
                    probs0 = GarHelper.GAR_INDEX._get_string_entries(r, regs0, pars0, max_count)
                    if (probs0 is None or len(probs0) > 2): 
                        continue
                    i = jj
                    kk = 0
                    while kk <= jj: 
                        addr.items.insert(kk, self.m_params.prev_address.items[kk].clone())
                        kk += 1
                    addr.alpha2 = self.m_params.prev_address.alpha2
                    break
                if (i > 0): 
                    continue
            if (not search_always and not AnalyzeHelper.__can_search_gars(r, addr, i)): 
                if (it.level == AddrLevel.STREET or (i > 0 and addr.items[i - 1].level == AddrLevel.DISTRICT)): 
                    pass
                elif (it.level == AddrLevel.TERRITORY and "СТ" in aa.miscs): 
                    pass
                elif (self.m_params is None or ((len(self.m_params.default_regions) == 0 and self.m_params.default_object is None))): 
                    continue
            probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
            if (probs is None and i > 0 and addr.items[i - 1].detail_typ != DetailType.UNDEFINED): 
                par_ids.clear()
                for g in addr.items[i - 1].gars: 
                    for p in g.parent_ids: 
                        if (not AnalyzeHelper.__get_id(p) in par_ids): 
                            par_ids.append(AnalyzeHelper.__get_id(p))
                if (len(par_ids) == 0 and i > 1): 
                    for g in addr.items[i - 2].gars: 
                        par_ids.append(AnalyzeHelper.__get_id(g.id0_))
                if (len(par_ids) > 0): 
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
            if ((probs is None and i == 0 and it.level == AddrLevel.DISTRICT) and len(addr.items) > 1 and addr.items[1].level == AddrLevel.CITY): 
                if (RegionHelper.is_big_citya(addr.items[1]) is not None and not rev): 
                    del addr.items[0]
                    addr.items.insert(1, it)
                    i -= 1
                    rev = True
                    continue
            if ((probs is None and i == 1 and it.level == AddrLevel.REGIONCITY) and addr.items[0].level == AddrLevel.REGIONAREA): 
                del addr.items[0]
                i = -1
                regions.clear()
                continue
            if ((probs is None and r.level == AddrLevel.CITY and "РОСТОВ" in r.strings) and 76 in regions): 
                r.strings.append("влРОСТОВ")
                probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                if (probs is not None): 
                    aa.names[0] = "Ростов Великий"
            if (probs is None and i == 0 and ((r.level == AddrLevel.CITY or r.level == AddrLevel.REGIONAREA or r.level == AddrLevel.DISTRICT))): 
                cou = CorrectionHelper.find_country(it)
                if (cou is not None): 
                    if (it.level == AddrLevel.DISTRICT): 
                        it.level = AddrLevel.REGIONAREA
                    addr.alpha2 = (Utils.asObjectOrNull(cou.tag, str))
                    addr.items.insert(0, cou)
                    break
            if (probs is not None and r.level == AddrLevel.DISTRICT and ((i + 1) < len(addr.items))): 
                if (addr.items[i + 1].level == AddrLevel.STREET or ((addr.items[i + 1].level == AddrLevel.LOCALITY and (i + 2) == len(addr.items)))): 
                    alt = r.try_create_alternative(False, (addr.items[i - 1] if i > 0 else None), (addr.items[i + 1] if (i + 1) < len(addr.items) else None))
                    if (alt is not None): 
                        par_ids0 = list()
                        for p in probs: 
                            par_ids0.append(p.id0_)
                        probs2 = GarHelper.GAR_INDEX._get_string_entries(alt, regions, par_ids0, max_count)
                        if (probs2 is not None): 
                            setls = 0
                            for p in probs2: 
                                if (p.level == AddrLevel.SETTLEMENT): 
                                    setls += 1
                            if (setls > 0 and (setls < len(probs2))): 
                                for jj in range(len(probs2) - 1, -1, -1):
                                    if (probs2[jj].level == AddrLevel.SETTLEMENT): 
                                        del probs2[jj]
                        if (probs2 is not None and len(probs2) == 1): 
                            it1 = addr.items[i + 1]
                            ok2 = True
                            if (it1.level == AddrLevel.LOCALITY and probs2[0].level == it1.level): 
                                ok2 = False
                                r2 = Utils.asObjectOrNull(it1.tag, NameAnalyzer)
                                alt2 = r2.try_create_alternative(True, None, None)
                                if (alt2 is not None): 
                                    par_ids2 = list()
                                    par_ids2.append(probs2[0].id0_)
                                    probs3 = GarHelper.GAR_INDEX._get_string_entries(alt2, regions, par_ids2, max_count)
                                    if (probs3 is not None and len(probs3) == 1): 
                                        ok2 = True
                            elif (it1.level == AddrLevel.STREET and ((alt.level == AddrLevel.LOCALITY or alt.level == AddrLevel.CITY))): 
                                ok2 = False
                                par_ids2 = list()
                                par_ids2.append(probs2[0].id0_)
                                probs3 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(it1.tag, NameAnalyzer), regions, par_ids2, max_count)
                                if (probs3 is not None and len(probs3) == 1): 
                                    ok2 = True
                            if (not ok2): 
                                pass
                            elif (not self.create_alts_regime): 
                                has_sec_var.value = True
                            else: 
                                probs = probs2
                                it.level = probs2[0].level
                                aa.types.clear()
                                aa.types.extend(alt.types)
                                aa.miscs.clear()
                                if (alt.miscs is not None): 
                                    aa.miscs.extend(alt.miscs)
                                it.tag = (alt)
                                r = alt
            if (probs is None): 
                alt = r.try_create_alternative(False, (addr.items[i - 1] if i > 0 else None), (addr.items[i + 1] if (i + 1) < len(addr.items) else None))
                if (alt is not None): 
                    if (not self.create_alts_regime): 
                        has_sec_var.value = True
                    else: 
                        if (AnalyzeHelper.__can_search_gars(alt, addr, i)): 
                            probs = GarHelper.GAR_INDEX._get_string_entries(alt, regions, par_ids, max_count)
                        if (probs is not None and ((len(probs) == 1 or it.level == AddrLevel.DISTRICT))): 
                            it.tag = (alt)
                            r = alt
                            it.level = probs[0].level
                            for p in probs: 
                                if (p.level != it.level): 
                                    it.level = AddrLevel.UNDEFINED
                                    break
                            aa.types.clear()
                            aa.types.extend(alt.types)
                            aa.miscs.clear()
                            if (alt.miscs is not None): 
                                aa.miscs.extend(alt.miscs)
                        else: 
                            alt2 = r.try_create_alternative(True, (addr.items[i - 1] if i > 0 else None), (addr.items[i + 1] if (i + 1) < len(addr.items) else None))
                            if (alt2 is not None): 
                                probs2 = None
                                if (AnalyzeHelper.__can_search_gars(alt2, addr, i)): 
                                    probs2 = GarHelper.GAR_INDEX._get_string_entries(alt2, regions, par_ids, max_count)
                                if (probs2 is not None and ((len(probs2) == 1 or ((len(probs2) == 2 and probs2[0].level == probs2[1].level))))): 
                                    probs = probs2
                                    it.tag = (alt2)
                                    r = alt2
                                    it.level = probs[0].level
                                    aa.types.clear()
                                    aa.types.extend(alt2.types)
                                    aa.miscs.clear()
                                    if (alt2.miscs is not None): 
                                        aa.miscs.extend(alt2.miscs)
            if (probs is not None and len(probs) == 1 and it.level != probs[0].level): 
                if (r.level == AddrLevel.TERRITORY or ((r.level == AddrLevel.LOCALITY and ((i == (len(addr.items) - 1) or addr.items[i + 1].level != AddrLevel.TERRITORY))))): 
                    par_ids2 = list()
                    par_ids2.append(probs[0].id0_)
                    probs2 = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids2, max_count)
                    if (probs2 is not None and ((i + 1) < len(addr.items))): 
                        prob3 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(addr.items[i + 1].tag, NameAnalyzer), regions, par_ids2, max_count)
                        if (prob3 is not None): 
                            probs2 = (None)
                    if (probs2 is not None): 
                        probs = probs2
                    elif (probs[0].level == AddrLevel.TERRITORY and len(addr.items) == 1): 
                        probs = (None)
            if ((probs is not None and len(probs) >= 2 and len(regions) == 0) and ((i + 1) < len(addr.items)) and RegionHelper.is_big_citya(addr.items[i + 1]) is not None): 
                probs1 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(addr.items[i + 1].tag, NameAnalyzer), regions, par_ids, max_count)
                if (probs1 is not None): 
                    for p in probs1: 
                        if (not p.region in regions): 
                            regions.append(p.region)
                if (len(regions) > 0): 
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
            if ((probs is None and len(regions) == 1 and len(par_ids) > 0) and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY))): 
                if ((i > 1 and RegionHelper.is_big_citya(addr.items[i - 1]) is not None and addr.items[i - 2].level == AddrLevel.DISTRICT) and len(addr.items[i - 2].gars) > 0): 
                    pars0 = list()
                    AnalyzeHelper.__add_par_ids(pars0, addr.items[i - 2])
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars0, max_count)
            all_terrs = True
            if (probs is not None): 
                for p in probs: 
                    if (p.level != AddrLevel.TERRITORY): 
                        all_terrs = False
            if (all_terrs): 
                if (len(regions) == 1 and len(par_ids) > 0 and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY))): 
                    if (probs is None): 
                        if (RestructHelper.restruct(self, addr, i)): 
                            regions.clear()
                            i = -1
                            continue
                    probs2 = GarHelper.GAR_INDEX._get_string_entries(r, regions, None, max_count)
                    if (it.level == AddrLevel.CITY and probs2 is None): 
                        probs2 = GarHelper.GAR_INDEX._get_string_entries(r, None, None, max_count)
                    if (probs2 is not None): 
                        for k in range(len(probs2) - 1, -1, -1):
                            pp = probs2[k]
                            ids = list()
                            for p in pp.parent_ids: 
                                ids.append("a{0}".format(p))
                            if (addr.find_gar_by_ids(ids) is None): 
                                del probs2[k]
                    if (probs2 is not None and ((len(probs2) == 0 or len(probs2) > 30))): 
                        probs2 = (None)
                    if ((probs2 is not None and len(probs2) <= 2 and i > 0) and RegionHelper.is_big_citya(addr.items[i - 1]) is not None): 
                        if (probs is not None and probs2[0] in probs): 
                            pass
                        else: 
                            del addr.items[i - 1]
                            i -= 1
                    if (probs is None): 
                        probs = probs2
                    if (probs is not None and len(probs) > 1): 
                        if (r.level == AddrLevel.CITY and "ТРОИЦК" in r.strings): 
                            for k in range(len(probs) - 1, -1, -1):
                                if (probs[k].region != (77)): 
                                    del probs[k]
                            if (len(probs) == 1): 
                                if (i > 0): 
                                    del addr.items[0:0+i]
                                    i = 0
                                    regions.clear()
                                    regions.append(77)
            if ((probs is None and ((it.level == AddrLevel.CITY or it.level == AddrLevel.REGIONCITY or it.level == AddrLevel.LOCALITY)) and aa.number is not None) and ((i + 1) < len(addr.items)) and addr.items[i + 1].level == AddrLevel.STREET): 
                num = aa.number
                cit = r.ref.clone()
                cit.add_slot("NUMBER", None, True, 0)
                naa = NameAnalyzer()
                naa.init_by_referent(cit, False)
                probs2 = GarHelper.GAR_INDEX._get_string_entries(naa, regions, par_ids, max_count)
                if (probs2 is not None): 
                    aa.number = (None)
                    it.tag = (naa)
                    r = naa
                    pars1 = list()
                    pars1.append(probs2[0].id0_)
                    probs3 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(addr.items[i + 1].tag, NameAnalyzer), regions, pars1, max_count)
                    if (probs3 is not None): 
                        pass
                    else: 
                        stret = addr.items[i + 1].tag.ref
                        stret.add_slot("NUMBER", num, False, 0)
                        addr.items[i + 1].attrs.number = num
                        naa = NameAnalyzer()
                        naa.init_by_referent(stret, False)
                        addr.items[i + 1].tag = (naa)
                    probs = probs2
            if (((len(regions) < 3) and i == (len(addr.items) - 1) and probs is None) and (((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.TERRITORY) or it.level == AddrLevel.STREET))): 
                cont = False
                for nn in it.attrs.names: 
                    ii = nn.find(' ')
                    if (ii < 0): 
                        continue
                    if (it.attrs.number is not None): 
                        break
                    rr = None
                    if (isinstance(r.ref, GeoReferent)): 
                        rr = (GeoReferent())
                        rr.add_slot(GeoReferent.ATTR_NAME, nn[0:0+ii].upper(), False, 0)
                        for ty in r.ref.typs: 
                            rr.add_slot(GeoReferent.ATTR_TYPE, ty, False, 0)
                    elif (isinstance(r.ref, StreetReferent)): 
                        rr = (StreetReferent())
                        rr.kind = r.ref.kind
                        rr.add_slot(StreetReferent.ATTR_NAME, nn[0:0+ii].upper(), False, 0)
                        for ty in r.ref.typs: 
                            rr.add_slot(StreetReferent.ATTR_TYPE, ty, False, 0)
                    else: 
                        continue
                    naa = NameAnalyzer()
                    naa.init_by_referent(rr, False)
                    probs2 = GarHelper.GAR_INDEX._get_string_entries(naa, regions, par_ids, max_count)
                    if (probs2 is None and i > 0 and (AddressHelper.compare_levels(addr.items[i - 1].level, AddrLevel.CITY) < 0)): 
                        rr = (GeoReferent())
                        rr.add_slot(StreetReferent.ATTR_NAME, nn[0:0+ii].upper(), False, 0)
                        rr.add_slot("TYPE", "город", False, 0)
                        naa = NameAnalyzer()
                        naa.init_by_referent(rr, False)
                        probs2 = GarHelper.GAR_INDEX._get_string_entries(naa, regions, par_ids, max_count)
                    if (probs2 is not None): 
                        for jj in range(len(probs2) - 1, -1, -1):
                            if (probs2[jj].level == AddrLevel.STREET): 
                                del probs2[jj]
                    if (probs2 is not None and len(probs2) > 0 and (len(probs2) < 20)): 
                        ss = StreetReferent()
                        ss.add_slot("NAME", nn[ii + 1:].upper(), False, 0)
                        ss.add_slot(StreetReferent.ATTR_TYPE, "улица", False, 0)
                        if (isinstance(rr, GeoReferent)): 
                            ss.add_slot("GEO", rr, False, 0)
                        else: 
                            ss.higher = Utils.asObjectOrNull(rr, StreetReferent)
                        naa2 = NameAnalyzer()
                        naa2.init_by_referent(ss, False)
                        ok = False
                        pars0 = list()
                        for pp in probs2: 
                            pars0.clear()
                            pars0.append(pp.id0_)
                            probs3 = GarHelper.GAR_INDEX._get_string_entries(naa2, regions, pars0, max_count)
                            if (probs3 is not None): 
                                ok = True
                                break
                        if (not ok): 
                            continue
                        tmp = TextAddress()
                        AnalyzeHelper._create_address_items(tmp, ss, None, 0)
                        if (len(tmp.items) == 2): 
                            del addr.items[i]
                            addr.items[i:i] = tmp.items
                            i -= 1
                            cont = True
                            break
                if (cont): 
                    continue
            if (((probs is None and i == 0 and it.level == AddrLevel.CITY) and ((i + 1) < len(addr.items)) and addr.items[i + 1].level == AddrLevel.DISTRICT) and not rev): 
                del addr.items[0]
                addr.items.insert(1, it)
                i -= 1
                rev = True
                continue
            if (((probs is None and ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY or it.level == AddrLevel.LOCALITY)) and i == (len(addr.items) - 1)) and aa.number is not None and len(aa.names) > 0) and ar is None): 
                last_num = False
                if (len(r.ref.occurrence) > 0): 
                    occ = r.ref.occurrence[0].get_text()
                    if (occ.endswith(aa.number)): 
                        last_num = True
                if (last_num): 
                    na2 = NameAnalyzer()
                    r.ref.add_slot(StreetReferent.ATTR_NUMBER, None, True, 0)
                    na2.init_by_referent(r.ref, False)
                    probs = GarHelper.GAR_INDEX._get_string_entries(na2, regions, par_ids, max_count)
                    r.ref.add_slot(StreetReferent.ATTR_NUMBER, aa.number, True, 0)
                    if (probs is not None): 
                        ar = AddressReferent()
                        ii = aa.number.find('-')
                        if (ii < 0): 
                            ar.house_or_plot = aa.number
                        else: 
                            ar.house = aa.number[0:0+ii]
                            ar.flat = aa.number[ii + 1:]
                        aa.number = (None)
            if ((probs is not None and len(probs) > 10 and i == 0) and len(regions) == 0): 
                probs = (None)
            if (it.level == AddrLevel.STREET and probs is not None and len(probs) > 5): 
                if (i == 0): 
                    probs = (None)
                else: 
                    it0 = addr.items[i - 1]
                    if (it0.level == AddrLevel.DISTRICT): 
                        if (len(it0.gars) > 0): 
                            for chi in GarHelper.get_children_objects(it0.gars[0].id0_, True): 
                                if (chi.level != GarLevel.CITY): 
                                    continue
                                if (len(chi.attrs.names) > 0 and chi.attrs.names[0] in it0.gars[0].attrs.names): 
                                    pass
                                else: 
                                    continue
                                pars = list()
                                pars.append(AnalyzeHelper.__get_id(chi.id0_))
                                probs1 = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars, max_count)
                                if (probs1 is not None and (len(probs1) < 3)): 
                                    probs = probs1
                        if (len(probs) > 3): 
                            if (i == 1): 
                                probs = (None)
                            elif (addr.items[i - 2].level != AddrLevel.CITY and addr.items[i - 2].level != AddrLevel.REGIONCITY): 
                                probs = (None)
            if (probs is None and i >= 2 and ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY))): 
                it0 = addr.items[i - 1]
                it00 = addr.items[i - 2]
                if (len(it0.gars) > 0 and it0.gars[0].expired and len(it00.gars) == 1): 
                    pars = list()
                    pars.append(AnalyzeHelper.__get_id(it00.gars[0].id0_))
                    probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars, max_count)
                    if (probs is None and ((it00.level == AddrLevel.CITYDISTRICT or it00.level == AddrLevel.TERRITORY)) and i > 2): 
                        it000 = addr.items[i - 3]
                        if (len(it000.gars) == 1 and ((it000.level == AddrLevel.CITY or it000.level == AddrLevel.REGIONCITY))): 
                            pars.clear()
                            pars.append(AnalyzeHelper.__get_id(it000.gars[0].id0_))
                            probs2 = GarHelper.GAR_INDEX._get_string_entries(r, regions, pars, max_count)
                            if (probs2 is not None and len(probs2) == 1): 
                                probs = probs2
            if ((probs is None and i >= 2 and it.level == AddrLevel.STREET) and addr.items[0].level == AddrLevel.REGIONCITY): 
                probs1 = GarHelper.GAR_INDEX._get_string_entries(r, regions, None, max_count)
                if (probs1 is not None and len(probs1) == 1): 
                    probs = probs1
                    if (len(addr.items[i - 1].gars) > 0): 
                        addr.items[i - 1].gars.clear()
            if (probs is None and len(regions) == 1 and it.level == AddrLevel.CITY): 
                r.level = AddrLevel.LOCALITY
                probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                r.level = AddrLevel.CITY
            if ((probs is None and it.level == AddrLevel.STREET and i > 0) and addr.items[i - 1].level == AddrLevel.TERRITORY and len(addr.items[i - 1].gars) == 0): 
                it0 = addr.items[i - 1]
                na = Utils.asObjectOrNull(it0.tag, NameAnalyzer)
                sr = StreetReferent()
                for n in na.ref.get_string_values("NAME"): 
                    sr.add_slot("NAME", n, False, 0)
                for s in r.ref.slots: 
                    if (s.type_name != "NAME"): 
                        sr.add_slot(s.type_name, s.value, False, 0)
                na1 = NameAnalyzer()
                na1.init_by_referent(sr, False)
                probs = GarHelper.GAR_INDEX._get_string_entries(na1, regions, par_ids, max_count)
                if (probs is not None): 
                    it.tag = (na1)
                    del addr.items[i - 1]
                    i -= 1
            if ((probs is None and it.level == AddrLevel.TERRITORY and len(par_ids) == 1) and i == (len(addr.items) - 1) and self.__insert_street_before_substr is None): 
                if ((r.miscs is not None and len(r.miscs) == 1 and r.ref.find_slot("NAME", None, True) is None) and len(r.types) == 1 and len(r.ref.occurrence) > 0): 
                    sr = StreetReferent()
                    sr.add_slot("NAME", r.miscs[0], False, 0)
                    na1 = NameAnalyzer()
                    na1.init_by_referent(sr, False)
                    probs1 = GarHelper.GAR_INDEX._get_string_entries(na1, regions, par_ids, max_count)
                    if (probs1 is not None): 
                        self.__insert_street_before_substr = r.miscs[0]
            if ((((probs is None and i == 1 and len(addr.items) == 2) and it.level == AddrLevel.STREET and len(r.types) == 0) and len(aa.names) > 0 and addr.items[0].level == AddrLevel.CITY) and len(addr.items[0].gars) == 1): 
                rrr = AddressService.process_single_address_text("{0} область".format(aa.names[0]), None)
                if (rrr.coef == 100 and rrr.last_item.level == AddrLevel.REGIONAREA): 
                    del addr.items[i]
                    addr.alpha2 = rrr.alpha2
                    addr.items[0:0] = rrr.items
                    break
            if (((probs is None and len(aa.names) == 1 and len(aa.miscs) == 1) and len(aa.miscs[0]) > 4 and str.isupper(aa.miscs[0][0])) and it.level == AddrLevel.STREET): 
                ar0 = ProcessorService.get_empty_processor().process(SourceOfAnalysis(aa.miscs[0]), None, None)
                if (ar0.first_token is not None and ar0.first_token.get_morph_class_in_dictionary().is_proper_name): 
                    sr = StreetReferent()
                    sr.add_slot("NAME", aa.miscs[0].upper(), False, 0)
                    sr.add_slot("MISC", aa.names[0].upper(), False, 0)
                    if (len(aa.types) > 0): 
                        sr.add_slot(StreetReferent.ATTR_TYPE, aa.types[0], False, 0)
                    na1 = NameAnalyzer()
                    na1.init_by_referent(sr, False)
                    na1.strict_search = True
                    probs1 = GarHelper.GAR_INDEX._get_string_entries(na1, regions, par_ids, max_count)
                    if (probs1 is not None): 
                        probs = probs1
                        aa.names[0] = MiscHelper.convert_first_char_upper_and_other_lower(aa.miscs[0])
                        aa.miscs[0] = sr.get_string_value("MISC").upper()
            if ((probs is None and it._doubt_type and it.level == AddrLevel.DISTRICT) and (i + 1) == len(addr.items) and "район" in aa.types): 
                r.level = AddrLevel.STREET
                probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                if (probs is not None): 
                    it.level = AddrLevel.STREET
                    aa.types.clear()
            if (probs is not None): 
                self.__add_gars(addr, probs, i, regions, False)
                if ((probs is not None and len(probs) > 0 and len(it.gars) == 0) and i > 0): 
                    it0 = addr.items[i - 1]
                    if (len(it0.gars) == 0 and it0.level == AddrLevel.DISTRICT and i > 1): 
                        it0 = addr.items[i - 2]
                    aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                    if ((((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY)) and it0.level == AddrLevel.DISTRICT and len(it0.gars) == 1) and len(aa0.names) > 0): 
                        nam = aa0.names[0]
                        if (len(nam) > 5): 
                            nam = nam[0:0+len(nam) - 3]
                        chils = AddressService.get_children_objects(it0.gars[0].id0_, True)
                        if (chils is not None): 
                            for ch in chils: 
                                ga = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                                if (ch.level != GarLevel.CITY and ch.level != GarLevel.LOCALITY): 
                                    continue
                                if (len(ga.names) == 0 or not Utils.startsWithString(ga.names[0], nam, True)): 
                                    continue
                                par_ids.clear()
                                par_ids.append(AnalyzeHelper.__get_id(ch.id0_))
                                probs0 = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                                if (probs0 is not None): 
                                    it00 = GarHelper.create_addr_object(ch)
                                    if (it00 is not None): 
                                        addr.items.insert(i, it00)
                                        i += 1
                                        self.__add_gars(addr, probs0, i, regions, False)
                                break
                if (((len(it.gars) == 1 and it.level == AddrLevel.CITY and i == 1) and len(addr.items) == 2 and len(addr.items[0].gars) == 0) and addr.items[0].level == AddrLevel.DISTRICT and ((addr.items[0]._doubt_type or "улус" in addr.items[0].attrs.types))): 
                    addr.items[0].level = AddrLevel.STREET
                    addr.items[0].attrs.types.clear()
                    del addr.items[1]
                    addr.items.insert(0, it)
                    i = 0
                    continue
            elif ((it.level == AddrLevel.TERRITORY and i > 0 and len(addr.items[i - 1].gars) == 1) and len(aa.names) > 0): 
                g0 = addr.items[i - 1].gars[0]
                if (g0.children_count < 500): 
                    childs = AddressService.get_children_objects(g0.id0_, True)
                    if (childs is not None): 
                        for ch in childs: 
                            if (ch.level != GarLevel.AREA or ch.expired): 
                                continue
                            aa0 = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                            if (aa0.number != aa.number): 
                                continue
                            if (aa.names[0].upper() in aa0.names[0].upper()): 
                                it.gars.append(ch)
                    if (len(it.gars) != 1): 
                        it.gars.clear()
            if (len(it.gars) == 0 and not dont_change_region): 
                if (RestructHelper.restruct(self, addr, i)): 
                    regions.clear()
                    i = -1
                    continue
            if (((len(it.gars) == 0 and it.level == AddrLevel.DISTRICT and i == 1) and len(addr.items[0].gars) == 1 and len(aa.names) > 0) and len(aa.names[0]) > 5): 
                nam = aa.names[0][0:0+5]
                chi = AddressService.get_children_objects(addr.items[0].gars[0].id0_, True)
                if (chi is not None): 
                    for ch in chi: 
                        if (ch.level != GarLevel.MUNICIPALAREA and ch.level != GarLevel.ADMINAREA): 
                            continue
                        aaa = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                        if (len(aaa.names) == 0): 
                            continue
                        if (aaa.names[0].startswith(nam)): 
                            if (" " in aa.names[0] == " " in aaa.names[0]): 
                                it.gars.append(ch)
                it._sort_gars()
            if (((len(it.gars) == 0 and i > 1 and it.level == AddrLevel.STREET) and addr.items[i - 1].level == AddrLevel.TERRITORY and len(addr.items[i - 1].gars) == 0) and len(addr.items[i - 2].gars) == 1 and ((addr.items[i - 2].level == AddrLevel.CITY or addr.items[i - 2].level == AddrLevel.REGIONCITY))): 
                aa0 = Utils.asObjectOrNull(addr.items[i - 1].attrs, AreaAttributes)
                if (len(aa0.names) > 0 and aa0.number is None and len(aa0.names[0]) > 5): 
                    chi = AddressService.get_children_objects(addr.items[i - 2].gars[0].id0_, True)
                    nam = aa0.names[0][0:0+5]
                    for ch in chi: 
                        if (ch.level != GarLevel.AREA): 
                            continue
                        aaa = Utils.asObjectOrNull(ch.attrs, AreaAttributes)
                        if (len(aaa.names) == 0): 
                            continue
                        if (aaa.names[0].startswith(nam)): 
                            if (" " in aa0.names[0] == " " in aaa.names[0]): 
                                addr.items[i - 1].gars.append(ch)
                    if (len(addr.items[i - 1].gars) == 1): 
                        i -= 1
                        continue
                    addr.items[i - 1].gars.clear()
            if (it.level == AddrLevel.DISTRICT and len(it.gars) > 0): 
                all_area = True
                for g in it.gars: 
                    if (g.level != GarLevel.AREA and g.level != GarLevel.DISTRICT): 
                        all_area = False
                if (all_area): 
                    it.level = AddrLevel.TERRITORY
                    if (((i + 1) < len(addr.items)) and addr.items[i + 1].level == AddrLevel.CITY): 
                        del addr.items[i]
                        addr.items.insert(i + 1, it)
                        it.gars.clear()
                        i -= 1
                        continue
            if (it.level == AddrLevel.LOCALITY and i > 0 and len(it.gars) == 1): 
                it0 = addr.items[i - 1]
                if (it0.level == AddrLevel.CITY and it0._find_gar_by_ids(it.gars[0].parent_ids) is None): 
                    del addr.items[i - 1]
                    i -= 1
            if ((it.level == AddrLevel.CITY and len(it.gars) == 1 and i > 0) and addr.items[i - 1].level == AddrLevel.DISTRICT and len(addr.items[i - 1].gars) == 0): 
                par_ids.clear()
                par_ids.append(AnalyzeHelper.__get_id(it.gars[0].id0_))
                probs2 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(addr.items[i - 1].tag, NameAnalyzer), regions, par_ids, max_count)
                if (probs2 is not None and (len(probs2) < 3)): 
                    del addr.items[i]
                    addr.items.insert(i - 1, it)
                    i -= 1
                    continue
            if (len(it.gars) == 0): 
                if (it.level == AddrLevel.COUNTRY): 
                    other_country = True
            if (it.cross_object is not None): 
                r = (Utils.asObjectOrNull(it.cross_object.tag, NameAnalyzer))
                probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, max_count)
                if (probs is not None): 
                    self.__add_gars(addr, probs, i, regions, True)
        j = 0
        first_pass3262 = True
        while True:
            if first_pass3262: first_pass3262 = False
            else: j += 1
            if (not (j < (len(addr.items) - 1))): break
            it0 = addr.items[j]
            it1 = addr.items[j + 1]
            if (len(it0.gars) > 0 or len(it1.gars) == 0): 
                continue
            ok = False
            if (it0.level == AddrLevel.LOCALITY and it1.level == AddrLevel.LOCALITY): 
                ok = True
            if (not ok): 
                continue
            par_ids.clear()
            for gg in it1.gars: 
                par_ids.append(AnalyzeHelper.__get_id(gg.id0_))
            probs = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(it0.tag, NameAnalyzer), regions, par_ids, 4)
            if (probs is not None): 
                addr.items[j] = it1
                addr.items[j + 1] = it0
                self.__add_gars(addr, probs, j + 1, regions, False)
        i = 0
        first_pass3263 = True
        while True:
            if first_pass3263: first_pass3263 = False
            else: i += 1
            if (not (i < len(addr.items))): break
            it = addr.items[i]
            if (it.level != AddrLevel.LOCALITY or len(it.gars) == 0 or it.gars[0].level != GarLevel.SETTLEMENT): 
                continue
            if ((i < (len(addr.items) - 1)) and addr.items[i + 1].level == AddrLevel.LOCALITY): 
                continue
            r = Utils.asObjectOrNull(it.tag, NameAnalyzer)
            if (r is None): 
                continue
            par_ids.clear()
            par_ids.append(AnalyzeHelper.__get_id(it.gars[0].id0_))
            probs = GarHelper.GAR_INDEX._get_string_entries(r, regions, par_ids, 10)
            if (probs is not None): 
                it.gars.clear()
                self.__add_gars(addr, probs, i, regions, False)
        self.__remove_items(addr)
        self.__remove_gars(addr)
        j = 0
        while j < len(addr.items): 
            it = addr.items[j]
            if (len(it.gars) > 1): 
                for g in it.gars: 
                    gg = it._find_gar_by_ids(g.parent_ids)
                    if (gg is not None): 
                        if (AddressHelper.can_be_equal_levels(it.level, gg.level)): 
                            it.gars.remove(g)
                        else: 
                            it.gars.remove(gg)
                        break
            j += 1
        j = 0
        first_pass3264 = True
        while True:
            if first_pass3264: first_pass3264 = False
            else: j += 1
            if (not (j < len(addr.items))): break
            it = addr.items[j]
            if (((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY)) and len(it.gars) > 0 and not it.gars[0].expired): 
                pass
            else: 
                continue
            j0 = j
            j -= 1
            has_ok = False
            for jj in range(j, 0, -1):
                it = addr.items[jj]
                if (((len(it.gars) > 0 and it.gars[0].expired)) or len(it.gars) == 0): 
                    pass
                else: 
                    has_ok = True
            if (has_ok or it.level == AddrLevel.CITY): 
                while j > 0: 
                    it = addr.items[j]
                    if (len(it.gars) > 0 and it.gars[0].expired): 
                        del addr.items[j]
                    elif (len(it.gars) == 0): 
                        if (it.level == AddrLevel.DISTRICT): 
                            it.level = AddrLevel.CITYDISTRICT
                            if ((j0 + 1) <= len(addr.items)): 
                                addr.items.insert(j0 + 1, it)
                            else: 
                                addr.items.append(it)
                        del addr.items[j]
                    j -= 1
            break
        AnalyzeHelper._add_miss_items(self, addr)
        self.__remove_items(addr)
        k = 0
        while k < (len(addr.items) - 1): 
            j = 0
            while j < (len(addr.items) - 1): 
                if (AddressHelper.compare_levels(addr.items[j].level, addr.items[j + 1].level) > 0): 
                    it = addr.items[j]
                    it1 = addr.items[j + 1]
                    addr.items[j] = addr.items[j + 1]
                    addr.items[j + 1] = it
                j += 1
            k += 1
        k = 0
        while k < (len(addr.items) - 1): 
            if (addr.items[k].level == addr.items[k + 1].level and addr.items[k].level != AddrLevel.TERRITORY): 
                it = addr.items[k]
                it1 = addr.items[k + 1]
                if (len(it.gars) == len(it1.gars) and len(it.gars) > 0 and it1.gars[0] in it.gars): 
                    del addr.items[k + 1]
                    k -= 1
                elif (len(it.gars) == 0 and len(it1.gars) > 0): 
                    del addr.items[k]
                    k -= 1
                elif (len(it.gars) > 0 and len(it1.gars) == 0): 
                    del addr.items[k + 1]
                    k -= 1
            k += 1
        if (ua_country is not None and ((len(addr.items) == 0 or addr.items[0].level != AddrLevel.COUNTRY))): 
            addr.items.insert(0, ua_country)
        if (addr.alpha2 is not None and len(addr.items) > 0 and addr.items[0].level != AddrLevel.COUNTRY): 
            cou = CorrectionHelper.create_country(addr.alpha2, None)
            if (cou is not None): 
                addr.items.insert(0, cou)
        return ar
    
    def _process_rest(self, addr : 'TextAddress', ar : 'AddressReferent', one : bool, aar : 'AnalysisResult') -> None:
        if (ar is not None): 
            if ((ar.house_or_plot is not None and self.m_params is not None and self.m_params.is_plot) and ar.plot is None): 
                ar.plot = ar.house_or_plot
                ar.house_or_plot = None
            HouseRoomHelper.process_house_and_rooms(self, ar, addr)
            has_details = False
            for it in addr.items: 
                if (it.detail_typ != DetailType.UNDEFINED): 
                    has_details = True
            if (not has_details): 
                par = None
                wrappar122 = RefOutArgWrapper(None)
                det = HouseRoomHelper.create_dir_details(ar, wrappar122)
                par = wrappar122.value
                if (det != DetailType.UNDEFINED and addr.last_item is not None): 
                    ao = addr.last_item
                    if (len(addr.items) > 1 and ((addr.items[len(addr.items) - 2].level == addr.last_item.level or ((addr.last_item.level == AddrLevel.PLOT and addr.last_item.attrs.number == "б/н"))))): 
                        if (par == "часть" and len(addr.items) > 2 and addr.items[len(addr.items) - 3].level == AddrLevel.TERRITORY): 
                            ao = addr.items[len(addr.items) - 3]
                        else: 
                            ao = addr.items[len(addr.items) - 2]
                    ao.detail_typ = det
                    ao.detail_param = par
            else: 
                j = 0
                first_pass3265 = True
                while True:
                    if first_pass3265: first_pass3265 = False
                    else: j += 1
                    if (not (j < (len(addr.items) - 1))): break
                    it = addr.items[j]
                    if (it.detail_typ == DetailType.UNDEFINED or len(it.gars) == 0): 
                        continue
                    it2 = addr.items[j + 1]
                    if (len(it2.gars) == 0): 
                        continue
                    for g in it2.gars: 
                        if (it._find_gar_by_ids(g.parent_ids) is not None): 
                            it.detail_typ = DetailType.UNDEFINED
                            it.detail_param = (None)
                            break
            HouseRoomHelper.process_other_details(addr, ar)
            ar.tag = (addr)
        elif (addr.text is not None): 
            i = addr.end_char + 1
            first_pass3266 = True
            while True:
                if first_pass3266: first_pass3266 = False
                else: i += 1
                if (not (i < len(addr.text))): break
                ch = addr.text[i]
                if (ch == ' ' or ch == ',' or ch == '.'): 
                    continue
                txt = addr.text[i:]
                rt = AddressItemToken.create_address(txt)
                if (rt is None and str.isdigit(txt[0])): 
                    rt = AddressItemToken.create_address("дом " + txt)
                if (rt is not None): 
                    ar = (Utils.asObjectOrNull(rt.referent, AddressReferent))
                    HouseRoomHelper.process_house_and_rooms(self, ar, addr)
                    addr.end_char = (i + rt.end_char)
                break
        if (addr.last_item is not None): 
            if (AddressHelper.compare_levels(addr.last_item.level, AddrLevel.STREET) > 0): 
                if (self.__remove_gars(addr)): 
                    AnalyzeHelper._add_miss_items(self, addr)
                    self.__remove_gars(addr)
                if (one): 
                    HouseRoomHelper.try_parse_list_items(self, addr, aar)
        AnalyzeHelper.__correct_levels(addr)
    
    def __remove_items(self, res : 'TextAddress') -> None:
        j = 0
        first_pass3267 = True
        while True:
            if first_pass3267: first_pass3267 = False
            else: j += 1
            if (not (j < (len(res.items) - 1))): break
            it = res.items[j]
            it1 = res.items[j + 1]
            if (len(it1.gars) == 0): 
                continue
            aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            aa1 = Utils.asObjectOrNull(it1.attrs, AreaAttributes)
            if (it.level == AddrLevel.DISTRICT and len(it.gars) == 0): 
                del res.items[j]
                j -= 1
                continue
            ok = False
            for g in it1.gars: 
                if (it._find_gar_by_ids(g.parent_ids) is not None): 
                    ok = True
            if (ok): 
                continue
            if (it.level == AddrLevel.DISTRICT and it1.level == AddrLevel.CITY): 
                if (len(aa.names) > 0 and len(aa1.names) > 0 and len(aa1.names[0]) > 3): 
                    if (aa.names[0].startswith(aa1.names[0][0:0+3])): 
                        ok = True
                if (not ok and ((j + 2) < len(res.items))): 
                    it2 = res.items[j + 2]
                    if (it2.level == AddrLevel.LOCALITY or it2.level == AddrLevel.CITY or it2.level == AddrLevel.SETTLEMENT): 
                        for g in it2.gars: 
                            if (it._find_gar_by_ids(g.parent_ids) is not None): 
                                ok = True
                        if (ok): 
                            del res.items[j + 1]
                            it1 = it2
                if (j == 0 and len(it1.gars) == 1): 
                    del res.items[0]
                    j -= 1
                    continue
            if ((not ok and it.level == AddrLevel.CITY and ((it1.level == AddrLevel.LOCALITY or it1.level == AddrLevel.TERRITORY))) and j > 0): 
                it0 = res.items[j - 1]
                aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                if (it0.level == AddrLevel.DISTRICT): 
                    for g in it1.gars: 
                        if (it0._find_gar_by_ids(g.parent_ids) is not None): 
                            ok = True
                    if (ok): 
                        del res.items[j]
                        j -= 1
                        continue
        if (len(res.items) > 2): 
            last = res.items[len(res.items) - 1]
            if ((last.level == AddrLevel.STREET and len(last.gars) == 0 and len(last.attrs.types) == 0) and res.items[len(res.items) - 2].level == AddrLevel.LOCALITY): 
                aa0 = Utils.asObjectOrNull(last.attrs, AreaAttributes)
                for i in range(len(res.items) - 3, 0, -1):
                    aa = Utils.asObjectOrNull(res.items[i].attrs, AreaAttributes)
                    if (len(aa.names) > 0 and aa.names[0] in aa0.names): 
                        res.items.remove(last)
                        break
    
    @staticmethod
    def _add_miss_items(ah : 'AnalyzeHelper', addr : 'TextAddress') -> None:
        j = 0
        first_pass3268 = True
        while True:
            if first_pass3268: first_pass3268 = False
            else: j += 1
            if (not (j < (len(addr.items) - 1))): break
            it0 = addr.items[j]
            it1 = addr.items[j + 1]
            if (len(it1.gars) == 0): 
                continue
            if (AnalyzeHelper.__contains_one_of_parent(addr, it1.gars)): 
                if (((it0.level == AddrLevel.REGIONCITY or it0.level == AddrLevel.REGIONAREA)) and it1.level == AddrLevel.LOCALITY): 
                    pass
                else: 
                    continue
            par = ah.__get_common_parent(addr, it1.gars)
            if (par is None): 
                continue
            if (addr.find_item_by_gar_level(par.level) is not None): 
                continue
            par2 = None
            par3 = None
            if (addr.find_gar_by_ids(par.parent_ids) is not None): 
                pass
            else: 
                if (len(par.parent_ids) == 0): 
                    continue
                par2 = ah.get_gar_object(par.parent_ids[0])
                if (par2 is None): 
                    continue
                if (addr.find_gar_by_ids(par2.parent_ids) is not None): 
                    pass
                else: 
                    if (len(par2.parent_ids) == 0): 
                        continue
                    par3 = ah.get_gar_object(par2.parent_ids[0])
                    if (par3 is None): 
                        continue
                    if (addr.find_gar_by_ids(par3.parent_ids) is not None): 
                        pass
                    else: 
                        continue
            to1 = GarHelper.create_addr_object(par)
            if (to1 is not None): 
                exi = addr.find_item_by_level(to1.level)
                if (exi is None): 
                    addr.items.insert(j + 1, to1)
                elif (not par in exi.gars): 
                    exi.gars.append(par)
            if (par2 is not None): 
                to2 = GarHelper.create_addr_object(par2)
                if (to2 is not None): 
                    exi = addr.find_item_by_level(to2.level)
                    if (exi is None): 
                        addr.items.insert(j + 1, to2)
                    elif (not par2 in exi.gars): 
                        exi.gars.append(par2)
                if (par3 is not None): 
                    to3 = GarHelper.create_addr_object(par3)
                    if (to3 is not None): 
                        exi = addr.find_item_by_level(to3.level)
                        if (exi is None): 
                            addr.items.insert(j + 1, to3)
                        elif (not par2 in exi.gars): 
                            exi.gars.append(par3)
        if (len(addr.items) > 0 and len(addr.items[0].gars) >= 1 and len(addr.items[0].gars[0].parent_ids) > 0): 
            addrs0 = list()
            for g in addr.items[0].gars: 
                ta = TextAddress()
                if (len(g.parent_ids) == 0): 
                    continue
                p = ah.get_gar_object(g.parent_ids[0])
                while p is not None: 
                    to1 = GarHelper.create_addr_object(p)
                    if (to1 is not None): 
                        ta.items.insert(0, to1)
                    if (len(p.parent_ids) == 0): 
                        break
                    p = ah.get_gar_object(p.parent_ids[0])
                if (len(ta.items) > 0): 
                    addrs0.append(ta)
            if (len(addrs0) > 0): 
                for i in range(len(addrs0[0].items) - 1, -1, -1):
                    ao = addrs0[0].items[i]
                    ok = True
                    j = 1
                    while j < len(addrs0): 
                        ao1 = addrs0[j].find_item_by_level(ao.level)
                        if (ao1 is None or ao1.gars[0].id0_ != ao.gars[0].id0_): 
                            ok = False
                            break
                        j += 1
                    if (ok): 
                        addr.items.insert(0, ao)
    
    @staticmethod
    def __contains_one_of_parent(a : 'TextAddress', gos : typing.List['GarObject']) -> bool:
        for g in gos: 
            if (a.find_gar_by_ids(g.parent_ids) is not None): 
                return True
        return False
    
    def __get_common_parent(self, a : 'TextAddress', gos : typing.List['GarObject']) -> 'GarObject':
        id0_ = None
        for g in gos: 
            if (len(g.parent_ids) > 0): 
                if (id0_ is None or id0_ in g.parent_ids): 
                    id0_ = (g.parent_ids[0] if len(g.parent_ids) > 0 else None)
                elif (id0_ is not None and id0_ in g.parent_ids): 
                    pass
                else: 
                    return None
        if (id0_ is None): 
            return None
        return self.get_gar_object(id0_)
    
    def __add_gars(self, addr : 'TextAddress', probs : typing.List['AreaTreeObject'], i : int, regions : bytearray, cross : bool) -> None:
        if (probs is None or len(probs) == 0): 
            return
        it = addr.items[i]
        if (cross): 
            it = it.cross_object
        it.gars.clear()
        aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
        if (it.level == AddrLevel.LOCALITY): 
            has_street = False
            j = i + 1
            while j < len(addr.items): 
                if (addr.items[j].level == AddrLevel.STREET): 
                    has_street = True
                j += 1
            if (has_street): 
                for j in range(len(probs) - 1, -1, -1):
                    if (probs[j].level == AddrLevel.STREET): 
                        del probs[j]
        if ((((it.level == AddrLevel.STREET or it.level == AddrLevel.LOCALITY)) and len(probs) > 1 and i > 0) and self.zip0_ is not None): 
            zip0__ = 0
            wrapzip123 = RefOutArgWrapper(0)
            Utils.tryParseInt(self.zip0_, wrapzip123)
            zip0__ = wrapzip123.value
            ids = GarHelper.GAR_INDEX.get_ao_ids_by_zip(zip0__)
            if (ids is not None): 
                probs0 = None
                for p in probs: 
                    if (p.id0_ in ids): 
                        if (probs0 is None): 
                            probs0 = list()
                        probs0.append(p)
                if (probs0 is not None): 
                    probs = probs0
        if (len(probs) > 1 and self.m_params is not None and len(self.m_params.default_regions) > 0): 
            has_reg = 0
            for g in probs: 
                if (Utils.indexOfList(self.m_params.default_regions, g.region, 0) >= 0): 
                    has_reg += 1
            if (has_reg > 0 and (has_reg < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (Utils.indexOfList(self.m_params.default_regions, probs[k].region, 0) < 0): 
                        del probs[k]
        if (len(probs) > 1 and len(aa.miscs) > 0 and it.level != AddrLevel.TERRITORY): 
            has_equ_misc = 0
            for g in probs: 
                if (aa.find_misc(g.miscs) is not None): 
                    has_equ_misc += 1
            if (has_equ_misc > 0 and (has_equ_misc < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (aa.find_misc(probs[k].miscs) is None): 
                        del probs[k]
        if (((len(probs) > 1 and it.level != AddrLevel.TERRITORY and it.level != AddrLevel.DISTRICT) and not "населенный пункт" in aa.types and not "станция" in aa.types) and ((not "поселение" in aa.types or len(aa.types) > 1))): 
            has_equ_type = 0
            for g in probs: 
                if (aa.has_equal_type(g.typs)): 
                    has_equ_type += 1
            if (has_equ_type > 0 and (has_equ_type < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (not aa.has_equal_type(probs[k].typs)): 
                        del probs[k]
        if (len(probs) > 1 and it.level != AddrLevel.UNDEFINED): 
            has_equ_level = 0
            gstat2 = 0
            loc_count = 0
            for g in probs: 
                if (it.level == g.level): 
                    has_equ_level += 1
                elif ((g.level == AddrLevel.LOCALITY and it.level == AddrLevel.STREET and ((i + 1) < len(addr.items))) and addr.items[i + 1].level == AddrLevel.STREET): 
                    loc_count += 1
                if (g.status == GarStatus.OK2): 
                    gstat2 += 1
            if (loc_count > 0): 
                for k in range(len(probs) - 1, -1, -1):
                    if (probs[k].level != AddrLevel.LOCALITY): 
                        del probs[k]
            elif (gstat2 == 0 and has_equ_level > 0 and (has_equ_level < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (it.level != probs[k].level): 
                        del probs[k]
        if (len(probs) > 1): 
            has_err = 0
            for g in probs: 
                if (g.status == GarStatus.ERROR): 
                    has_err += 1
            if (has_err > 0 and (has_err < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (probs[k].status == GarStatus.ERROR): 
                        del probs[k]
        if (len(probs) > 1): 
            has_act = 0
            oktyp = 0
            pars = list()
            for g in probs: 
                if (g.level == AddrLevel.DISTRICT or g.check_type(Utils.asObjectOrNull(it.tag, NameAnalyzer)) > 0): 
                    oktyp += 1
                if (g.expired): 
                    has_act += 1
                if (g.parent_ids is not None): 
                    for p in g.parent_ids: 
                        if (not p in pars): 
                            pars.append(p)
            if (has_act > 0 and (has_act < oktyp) and (len(pars) < 2)): 
                for k in range(len(probs) - 1, -1, -1):
                    if (probs[k].expired): 
                        del probs[k]
        if (i > 0 and len(probs) > 1): 
            it0 = addr.items[i - 1]
            if ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY or ((it.level == AddrLevel.LOCALITY and it0.level == AddrLevel.DISTRICT)))): 
                has_dir_parent = 0
                for g in probs: 
                    if (AnalyzeHelper.__find_parent_prob(it0, g) is not None and not g.expired): 
                        has_dir_parent += 1
                if (has_dir_parent > 0 and (has_dir_parent < len(probs))): 
                    for k in range(len(probs) - 1, -1, -1):
                        g = probs[k]
                        if (AnalyzeHelper.__find_parent_prob(it0, g) is not None): 
                            continue
                        del probs[k]
        if (i > 0 and len(probs) > 1): 
            it0 = addr.items[i - 1]
            aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
            if (len(aa0.names) > 0 and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.TERRITORY)) and it0.level == AddrLevel.DISTRICT): 
                probs0 = None
                for p in probs: 
                    if (p.parent_ids is None or len(p.parent_ids) == 0): 
                        continue
                    par = self.get_gar_object("a{0}".format(p.parent_ids[0]))
                    if (par is None): 
                        continue
                    for kk in range(2):
                        aa1 = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                        if (len(aa1.names) > 0 and len(aa1.names[0]) >= 4): 
                            if (aa0.names[0].startswith(aa1.names[0][0:0+4])): 
                                if (probs0 is None): 
                                    probs0 = list()
                                probs0.append(p)
                                break
                        if (kk > 0): 
                            break
                        if (par.parent_ids is None or len(par.parent_ids) == 0): 
                            break
                        par2 = self.get_gar_object(par.parent_ids[0])
                        if (par2 is None): 
                            break
                        par = par2
                if (probs0 is not None): 
                    probs.clear()
                    probs.extend(probs0)
        if ((len(probs) > 1 and it.level == AddrLevel.STREET and len(aa.types) > 1) and "улица" in aa.types): 
            typ0 = (aa.types[1] if aa.types[0] == "улица" else aa.types[0])
            has_typ = 0
            for p in probs: 
                if (p.typs is not None and typ0 in p.typs): 
                    has_typ += 1
            if (has_typ > 0 and (has_typ < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (not typ0 in probs[k].typs): 
                        del probs[k]
        if (len(probs) > 1 and it.level == AddrLevel.STREET and len(aa.types) > 0): 
            has_typ = 0
            for p in probs: 
                if (p.typs is not None and len(p.typs) == len(aa.types)): 
                    has_typ += 1
            if (has_typ > 0 and (has_typ < len(probs))): 
                for k in range(len(probs) - 1, -1, -1):
                    if (probs[k].typs is not None and len(probs[k].typs) != len(aa.types)): 
                        del probs[k]
        ignore_gars = False
        cross_gars = None
        for p in probs: 
            if ((len(probs) == 1 and it.level == AddrLevel.STREET and len(aa.types) == 0) and p.level != it.level): 
                it.level = p.level
            if (it.level == AddrLevel.STREET and i > 0): 
                ok = False
                ids = list()
                if (p.parent_ids is not None): 
                    for id0_ in p.parent_ids: 
                        ids.clear()
                        ids.append("a{0}".format(id0_))
                        gg = addr.find_gar_by_ids(ids)
                        if (gg is None): 
                            continue
                        if (gg.level == GarLevel.CITY or gg.level == GarLevel.LOCALITY or gg.level == GarLevel.AREA): 
                            ok = True
                            break
                        if (((gg.level == GarLevel.ADMINAREA or gg.level == GarLevel.REGION)) and "город" in gg.attrs.types): 
                            ok = True
                            break
                        if (gg.level == GarLevel.ADMINAREA or gg.level == GarLevel.MUNICIPALAREA or gg.level == GarLevel.SETTLEMENT): 
                            if (i > 0 and addr.items[i - 1].level == AddrLevel.DISTRICT): 
                                ok = True
                                break
                if (p.parent_parent_ids is not None and not ok and not "километр" in aa.types): 
                    for id0_ in p.parent_parent_ids: 
                        ids.clear()
                        ids.append("a{0}".format(id0_))
                        gg = addr.find_gar_by_ids(ids)
                        if (gg is None): 
                            continue
                        if ((gg.level == GarLevel.CITY or gg.level == GarLevel.LOCALITY or gg.level == GarLevel.AREA) or gg.level == GarLevel.SETTLEMENT): 
                            ok = True
                            break
                        if (((gg.level == GarLevel.ADMINAREA or gg.level == GarLevel.REGION)) and "город" in gg.attrs.types): 
                            ok = True
                            break
                if (not ok): 
                    continue
            g = self.get_gar_object("a{0}".format(p.id0_))
            if (g is None): 
                continue
            if (i == 0 and it.level == AddrLevel.DISTRICT): 
                if (g.level == GarLevel.REGION and g.attrs.types[0] in it.attrs.types): 
                    it.level = AddrLevel.REGIONAREA
                    it.gars.clear()
                    it.gars.append(g)
                    break
            if (p.miscs is not None and len(p.miscs) > 0): 
                g.attrs.miscs.extend(p.miscs)
            ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
            na = NameAnalyzer()
            na.process(ga.names, (ga.types[0] if len(ga.types) > 0 else None), None)
            co = na.calc_equal_coef(Utils.asObjectOrNull(it.tag, NameAnalyzer))
            if (co < 0): 
                continue
            if (((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.TERRITORY)) and i >= 2): 
                ok = False
                if (addr.find_gar_by_ids(g.parent_ids) is not None): 
                    ok = True
                else: 
                    for kk in range(i - 1, 0, -1):
                        it0 = addr.items[kk]
                        if (p.parent_parent_ids is not None): 
                            for ppid in p.parent_parent_ids: 
                                if (it0.find_gar_by_id("a{0}".format(ppid)) is not None): 
                                    ok = True
                                    break
                        if (ok): 
                            break
                        for pid in g.parent_ids: 
                            par = self.get_gar_object(pid)
                            if (par is None): 
                                continue
                            ga0 = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                            if (len(ga0.names) == 0 or (len(ga0.names[0]) < 4)): 
                                continue
                            sub = ga0.names[0][0:0+4]
                            aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                            if (len(aa0.names) > 0 and Utils.startsWithString(aa0.names[0], sub, True)): 
                                ok = True
                                break
                        if (ok): 
                            break
                        if (len(it0.gars) == 0 and len(probs) == 1): 
                            ok = True
                            break
                        if (p.parent_parent_ids is not None): 
                            for ppid in p.parent_parent_ids: 
                                par = self.get_gar_object("a{0}".format(ppid))
                                if (par is None): 
                                    continue
                                ga0 = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                                if (len(ga0.names) == 0 or (len(ga0.names[0]) < 4)): 
                                    continue
                                sub = ga0.names[0][0:0+4]
                                aa0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
                                if (len(aa0.names) > 0 and Utils.startsWithString(aa0.names[0], sub, True)): 
                                    ok = True
                                    break
                        if (ok): 
                            break
                if (not ok): 
                    continue
            if (na.sec is not None or p.status == GarStatus.OK2): 
                if (p.id0_ == 4001): 
                    pass
                if ((i + 1) >= len(addr.items) or na.sec is None): 
                    continue
                it1 = addr.items[i + 1]
                na1 = Utils.asObjectOrNull(it1.tag, NameAnalyzer)
                if (na1 is None): 
                    continue
                if (not na1.can_be_equals(na.sec)): 
                    continue
                it1.gars.append(g)
                ignore_gars = True
                it.gars.clear()
                it.is_reconstructed = True
            if (na.cross is not None): 
                if (it.cross_object is None): 
                    pass
                else: 
                    na1 = Utils.asObjectOrNull(it.cross_object.tag, NameAnalyzer)
                    if (na1 is None): 
                        continue
                    if (not na1.can_be_equals(na.cross)): 
                        continue
                    it.gars.clear()
                    it.gars.append(g)
                    break
            if (g.level == GarLevel.REGION and it.level == AddrLevel.CITY and i == 0): 
                it.level = AddrLevel.REGIONCITY
            elif (g.level == GarLevel.REGION and it.level != AddrLevel.REGIONCITY): 
                it.level = AddrLevel.REGIONAREA
            elif ((it.level == AddrLevel.STREET and g.level == GarLevel.LOCALITY and i > 0) and addr.items[i - 1].level == AddrLevel.DISTRICT): 
                it.level = AddrLevel.LOCALITY
            if (not it.can_be_equals_glevel(g)): 
                levs = list()
                for pp in probs: 
                    if (not pp.glevel in levs): 
                        levs.append(p.glevel)
                if (len(probs) == 1 and it.level == AddrLevel.STREET and g.level == GarLevel.AREA): 
                    pass
                elif (it.level == AddrLevel.CITY and g.level == GarLevel.LOCALITY): 
                    all_loc = True
                    for pp in probs: 
                        if (p.level != AddrLevel.LOCALITY): 
                            all_loc = False
                    if (not all_loc): 
                        if ("город" in ga.types): 
                            pass
                        else: 
                            continue
                elif (len(levs) == 1 and it.level == AddrLevel.TERRITORY and g.level == GarLevel.STREET): 
                    pass
                elif (len(levs) == 1 and it.level == AddrLevel.STREET and g.level == GarLevel.AREA): 
                    pass
                elif (len(levs) == 1 and it.level == AddrLevel.SETTLEMENT and ((g.level == GarLevel.MUNICIPALAREA or g.level == GarLevel.ADMINAREA))): 
                    pass
                elif ((len(levs) == 1 and it.level == AddrLevel.TERRITORY and g.level == GarLevel.LOCALITY) and "СТ" in aa.miscs and "станица" in ga.types): 
                    it.level = AddrLevel.LOCALITY
                    aa.types.clear()
                    aa.miscs.clear()
                    aa.types.extend(ga.types)
                elif (len(levs) == 1 and it.level == AddrLevel.LOCALITY and g.level == GarLevel.STREET): 
                    pass
                elif (len(levs) == 1 and it.level == AddrLevel.LOCALITY and g.level == GarLevel.AREA): 
                    if (len(aa.types) > 0 and aa.types[0] != "населенный пункт"): 
                        continue
                else: 
                    continue
            if (i == 0 and ((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY))): 
                nam_eq = False
                for n in ga.names: 
                    if (aa.contains_name(n)): 
                        nam_eq = True
                if (not nam_eq): 
                    continue
            if (not ignore_gars): 
                it.gars.append(g)
                if (na.cross is not None): 
                    if (cross_gars is None): 
                        cross_gars = list()
                    cross_gars.append(g)
        if (i == 0 and len(it.gars) > 1 and ((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY))): 
            ok = False
            for g in it.gars: 
                if (g.level == GarLevel.CITY): 
                    ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
                    for n in ga.names: 
                        if (RegionHelper.is_big_city(n) is not None): 
                            ok = True
                    if (ok): 
                        break
            if (ok): 
                for k in range(len(it.gars) - 1, -1, -1):
                    ga = Utils.asObjectOrNull(it.gars[k].attrs, AreaAttributes)
                    ok = False
                    if (it.gars[k].level == GarLevel.CITY): 
                        for n in ga.names: 
                            if (RegionHelper.is_big_city(n) is not None): 
                                ok = True
                    if (not ok): 
                        del it.gars[k]
                    if (len(aa.types) > 0 and aa.types[0] == "населенный пункт"): 
                        aa.types.clear()
                        aa.types.append(ga.types[0])
        if (len(it.gars) > 1 and it.level == AddrLevel.CITY): 
            g1 = it.find_gar_by_level(GarLevel.MUNICIPALAREA)
            if (g1 is not None and it.find_gar_by_level(GarLevel.CITY) is not None): 
                it.gars.remove(g1)
        if (len(it.gars) > 1 and i > 0 and ((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY or it.level == AddrLevel.TERRITORY))): 
            for j in range(i - 1, -1, -1):
                it0 = addr.items[j]
                if (len(it0.gars) == 0): 
                    continue
                ap = Utils.asObjectOrNull(it0.gars[0].attrs, AreaAttributes)
                if (ap is None or len(ap.names) == 0): 
                    break
                gars = None
                eq_parens = False
                lev = GarLevel.UNDEFINED
                for g in it.gars: 
                    if (len(g.parent_ids) == 0): 
                        continue
                    par = self.get_gar_object(g.parent_ids[0])
                    if (par is None): 
                        continue
                    if (lev == GarLevel.UNDEFINED or par.level == lev): 
                        lev = par.level
                    else: 
                        gars = (None)
                        break
                    pp = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                    if (pp is None or len(pp.names) == 0): 
                        continue
                    if (par in it.gars): 
                        gars = (None)
                        break
                    str0 = ap.names[0]
                    str1 = pp.names[0]
                    k = 0
                    k = 0
                    while (k < len(str0)) and (k < len(str1)): 
                        if (str0[k] != str1[k]): 
                            break
                        k += 1
                    if (k >= (len(str0) - 1) or k >= (len(str1) - 1)): 
                        if (gars is None): 
                            gars = list()
                        gars.append(g)
                        if (par in it0.gars): 
                            eq_parens = True
                if (gars is not None and (len(gars) < len(it.gars))): 
                    it.gars = gars
                    if (not eq_parens and j > 0): 
                        del addr.items[j]
                break
            if (len(it.gars) > 1): 
                for j in range(i - 1, -1, -1):
                    it0 = addr.items[j]
                    if (len(it0.gars) == 0): 
                        continue
                    gars = None
                    for g in it.gars: 
                        ok = False
                        if (it0._find_gar_by_ids(g.parent_ids) is not None): 
                            ok = True
                        else: 
                            for pid in g.parent_ids: 
                                p = self.get_gar_object(pid)
                                if (p is None): 
                                    continue
                                if (it0._find_gar_by_ids(p.parent_ids) is not None): 
                                    ok = True
                                    break
                        if (ok): 
                            if (gars is None): 
                                gars = list()
                            gars.append(g)
                    if (gars is None): 
                        continue
                    if (len(gars) < len(it.gars)): 
                        it.gars = gars
                    break
        if (len(it.gars) > 1 and ((it.level == AddrLevel.STREET or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.CITY)) and len(aa.names) > 0): 
            has_nam = 0
            for g in it.gars: 
                if (aa.names[0] in g.attrs.names or aa.names[0] in g.attrs.names[0]): 
                    has_nam += 1
            if (has_nam > 0 and (has_nam < len(it.gars))): 
                for k in range(len(it.gars) - 1, -1, -1):
                    if (not aa.names[0] in it.gars[k].attrs.names and not aa.names[0] in it.gars[k].attrs.names[0]): 
                        del it.gars[k]
        if ((i > 0 and len(it.gars) > 1 and it.level == AddrLevel.STREET) and addr.items[i - 1].level == AddrLevel.TERRITORY and len(addr.items[i - 1].gars) == 1): 
            g0 = addr.items[i - 1].gars[0]
            has_nam = 0
            for g in it.gars: 
                if (g.id0_ in g0.parent_ids): 
                    has_nam += 1
            if (has_nam > 0 and (has_nam < len(it.gars))): 
                for k in range(len(it.gars) - 1, -1, -1):
                    if (not it.gars[k].id0_ in g0.parent_ids): 
                        del it.gars[k]
        if (len(it.gars) > 1 and i > 0 and ((it.level == AddrLevel.STREET or "улица" in aa.types))): 
            if (len(aa.miscs) == 0): 
                has = 0
                for g in it.gars: 
                    if (len(g.attrs.miscs) > 0): 
                        has += 1
                if (has > 0 and (has < len(it.gars))): 
                    for k in range(len(it.gars) - 1, -1, -1):
                        if (len(it.gars[k].attrs.miscs) > 0): 
                            del it.gars[k]
                elif (has == len(it.gars) and it.tag.ref is not None and len(it.tag.ref.occurrence) > 0): 
                    txt = it.tag.ref.occurrence[0].get_text()
                    ii = txt.rfind(',')
                    if (ii > 0): 
                        txt = txt[ii + 1:].strip()
                    txt = txt.upper()
                    gars = list()
                    for g in it.gars: 
                        ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
                        if (len(ga.miscs) == 0): 
                            continue
                        mi = ga.miscs[0]
                        if (mi in txt or "{0}.".format(mi[0]) in txt): 
                            gars.append(g)
                    if (len(gars) > 0 and (len(gars) < len(it.gars))): 
                        it.gars = gars
            else: 
                has = 0
                for g in it.gars: 
                    if (aa.miscs[0] in g.attrs.miscs): 
                        has += 1
                if (has > 0 and (has < len(it.gars))): 
                    for k in range(len(it.gars) - 1, -1, -1):
                        if (not aa.miscs[0] in it.gars[k].attrs.miscs): 
                            del it.gars[k]
            if (len(it.gars) > 1 and len(aa.types) > 1 and "улица" in aa.types): 
                typ = (aa.types[1] if aa.types[0] == "улица" else aa.types[0])
                has = 0
                for g in it.gars: 
                    if (typ in g.attrs.types): 
                        has += 1
                if (has > 0 and (has < len(it.gars))): 
                    for k in range(len(it.gars) - 1, -1, -1):
                        if (not typ in it.gars[k].attrs.types): 
                            del it.gars[k]
        if ((len(it.gars) > 1 and i == 0 and it.level == AddrLevel.CITY) and len(aa.names) > 0): 
            gars1 = None
            for g in it.gars: 
                gg = g
                while gg is not None: 
                    if (gg.level != GarLevel.REGION): 
                        if (gg.parent_ids is None or len(gg.parent_ids) == 0): 
                            break
                        gg = self.get_gar_object(gg.parent_ids[0])
                        continue
                    aaa = Utils.asObjectOrNull(gg.attrs, AreaAttributes)
                    if (len(aaa.names) > 0 and len(aa.names[0]) > 3): 
                        if (aaa.names[0].startswith(aa.names[0][0:0+len(aa.names[0]) - 3])): 
                            if (gars1 is None): 
                                gars1 = list()
                            gars1.append(g)
                    break
            if (gars1 is not None): 
                it.gars = gars1
        if (len(it.gars) > 1 and ((it.level == AddrLevel.STREET or it.level == AddrLevel.TERRITORY))): 
            act = 0
            for g in it.gars: 
                if (not g.expired): 
                    act += 1
            if (act > 0): 
                for k in range(len(it.gars) - 1, -1, -1):
                    if (it.gars[k].expired): 
                        del it.gars[k]
        if (i == 0 or len(regions) == 0): 
            for g in it.gars: 
                if (g.region_number != 0 and not g.region_number in regions): 
                    regions.append(g.region_number)
        cou = len(it.gars)
        if (cross_gars is not None and (len(cross_gars) < len(it.gars)) and it.cross_object is None): 
            cou = (len(it.gars) - len(cross_gars))
            for ii in range(len(it.gars) - 1, -1, -1):
                if (it.gars[ii] in cross_gars): 
                    del it.gars[ii]
            it.gars.extend(cross_gars)
        if (cou > 11): 
            it.gars.clear()
        it._sort_gars()
    
    @staticmethod
    def __find_parent_prob(it : 'AddrObject', ato : 'AreaTreeObject') -> 'GarObject':
        if (len(ato.parent_ids) == 0): 
            return None
        for ii in ato.parent_ids: 
            go = it.find_gar_by_id("a{0}".format(ii))
            if (go is not None): 
                return go
        return None
    
    def __remove_gars(self, addr : 'TextAddress') -> bool:
        ret = False
        for j in range(len(addr.items) - 1, 0, -1):
            it1 = addr.items[j]
            if (len(it1.gars) < 2): 
                continue
            for k in range(j - 1, -1, -1):
                it0 = addr.items[k]
                if (len(it0.gars) == 0): 
                    continue
                cou = 0
                real = None
                is_actual = False
                for g in it1.gars: 
                    if (it0._find_gar_by_ids(g.parent_ids) is not None): 
                        cou += 1
                        real = g
                    elif (not g.expired): 
                        is_actual = True
                if (cou == 1): 
                    if (is_actual and real.expired): 
                        break
                    else: 
                        it1.gars.clear()
                        it1.gars.append(real)
                        ret = True
        for j in range(len(addr.items) - 1, -1, -1):
            it1 = addr.items[j]
            if (len(it1.gars) != 1): 
                continue
            if (AddressHelper.compare_levels(it1.level, AddrLevel.BUILDING) > 0): 
                continue
            for k in range(j - 1, -1, -1):
                it0 = addr.items[k]
                g1 = it1.gars[0]
                for i in range(len(it0.gars) - 1, -1, -1):
                    if (it0.gars[i].region_number != g1.region_number and g1.region_number > 0 and it0.gars[i].region_number > 0): 
                        del it0.gars[i]
                        ret = True
                if (len(it0.gars) == 0): 
                    break
                cou = 0
                par = None
                for g in it0.gars: 
                    if (g.id0_ in g1.parent_ids): 
                        cou += 1
                        par = g
                if (cou == 1 and len(it0.gars) > 1): 
                    it0.gars.clear()
                    it0.gars.append(par)
                    ret = True
                break
        i = 0
        first_pass3269 = True
        while True:
            if first_pass3269: first_pass3269 = False
            else: i += 1
            if (not (i < (len(addr.items) - 1))): break
            it0 = addr.items[i]
            if (len(it0.gars) < 2): 
                continue
            it1 = addr.items[i + 1]
            if (len(it1.gars) != 1): 
                continue
            has_par = 0
            for g in it0.gars: 
                if (it1._find_gar_by_ids(g.parent_ids) is not None): 
                    has_par += 1
            if (has_par > 0 and (has_par < len(it0.gars))): 
                for j in range(len(it0.gars) - 1, -1, -1):
                    if (it1._find_gar_by_ids(it0.gars[j].parent_ids) is None): 
                        del it0.gars[j]
        i = 0
        while i < (len(addr.items) - 1): 
            it0 = addr.items[i]
            it1 = addr.items[i + 1]
            if ((it0.level == AddrLevel.TERRITORY and it1.level == AddrLevel.STREET and len(it0.gars) == 0) and str(it0) == str(it1)): 
                del addr.items[i]
                break
            i += 1
        i = 0
        first_pass3270 = True
        while True:
            if first_pass3270: first_pass3270 = False
            else: i += 1
            if (not (i < len(addr.items))): break
            it = addr.items[i]
            if (len(it.gars) == 0): 
                continue
            if (len(it.gars) == 1 and i > 0 and it.level == AddrLevel.CITY): 
                del addr.items[0:0+i]
            break
        i = 1
        first_pass3271 = True
        while True:
            if first_pass3271: first_pass3271 = False
            else: i += 1
            if (not (i < len(addr.items))): break
            it = addr.items[i]
            if (len(it.gars) > 0): 
                continue
            it0 = addr.items[i - 1]
            if (len(it0.gars) == 0): 
                continue
            if (it.level == AddrLevel.LOCALITY and it0.level == AddrLevel.CITY): 
                pass
            else: 
                continue
            a = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            a0 = Utils.asObjectOrNull(it0.attrs, AreaAttributes)
            ok = False
            for n in a0.names: 
                if (n in a.names): 
                    ok = True
            if (ok): 
                del addr.items[i]
                i -= 1
        for it in addr.items: 
            if (it.level == AddrLevel.STREET and len(it.gars) > 2): 
                slash = 0
                for g in it.gars: 
                    ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
                    if (len(ga.names) > 0 and ga.names[0].find('/') > 0): 
                        slash += 1
                if (slash > 0 and slash <= (len(it.gars) - 1)): 
                    for i in range(len(it.gars) - 1, -1, -1):
                        ga = Utils.asObjectOrNull(it.gars[i].attrs, AreaAttributes)
                        if (len(ga.names) > 0 and ga.names[0].find('/') > 0): 
                            del it.gars[i]
        i = 1
        while i < (len(addr.items) - 1): 
            if (not addr.items[i].is_reconstructed): 
                if (((addr.items[i].level == AddrLevel.TERRITORY or addr.items[i].level == AddrLevel.LOCALITY)) and addr.items[i + 1].level == AddrLevel.STREET and len(addr.items[i + 1].gars) == 1): 
                    if (addr.items[i - 1].level == AddrLevel.CITY or addr.items[i - 1].level == AddrLevel.LOCALITY or addr.items[i - 1].level == AddrLevel.REGIONCITY): 
                        pars = addr.items[i + 1].gars[0].parent_ids
                        ok = False
                        for g in addr.items[i].gars: 
                            if (g.id0_ in pars): 
                                ok = True
                        if (not ok): 
                            del addr.items[i]
                        break
            i += 1
        i = 0
        first_pass3272 = True
        while True:
            if first_pass3272: first_pass3272 = False
            else: i += 1
            if (not (i < (len(addr.items) - 1))): break
            it1 = addr.items[i]
            it2 = addr.items[i + 1]
            if ((len(it1.gars) < 2) or len(it2.gars) == 0): 
                continue
            for g1 in it1.gars: 
                ok = False
                for g2 in it2.gars: 
                    if (g1.id0_ in g2.parent_ids): 
                        ok = True
                if (not ok): 
                    continue
                if (g1 != it1.gars[0]): 
                    it1.gars.remove(g1)
                    it1.gars.insert(0, g1)
                break
        return ret
    
    @staticmethod
    def __correct_object_by_gars(it : 'AddrObject') -> None:
        aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
        if (aa is None): 
            return
        typs = list()
        miscs = list()
        levs = list()
        if ("СТ" in aa.miscs and it.level == AddrLevel.LOCALITY): 
            aa.miscs.remove("СТ")
        for g in it.gars: 
            is_road = False
            for ty in g.attrs.types: 
                if (not ty in typs): 
                    typs.append(ty)
                    if ("дорога" in ty): 
                        is_road = True
            for ty in g.attrs.miscs: 
                if (not ty in miscs): 
                    miscs.append(ty)
            gl = g.level
            if (is_road and gl == GarLevel.LOCALITY): 
                gl = GarLevel.AREA
            if (not gl in levs): 
                levs.append(gl)
        if (len(aa.types) > 0 and ((aa.types[0] == "населенный пункт" or aa.types[0] == "почтовое отделение")) and len(typs) == 1): 
            aa.types[0] = typs[0]
            if (it.level == AddrLevel.LOCALITY and len(levs) == 1 and levs[0] == GarLevel.CITY): 
                it.level = AddrLevel.CITY
            elif (it.level == AddrLevel.CITY and len(levs) == 1 and levs[0] == GarLevel.LOCALITY): 
                it.level = AddrLevel.LOCALITY
        elif (len(typs) == 1 and len(aa.types) > 1 and Utils.indexOfList(aa.types, typs[0], 0) > 0): 
            aa.types.remove(typs[0])
            aa.types.insert(0, typs[0])
        if (len(aa.types) == 0 and len(typs) == 1): 
            aa.types.append(typs[0])
        if (len(aa.miscs) == 0 and len(miscs) > 0): 
            aa.miscs.append(miscs[0])
        if (len(aa.types) > 1 and len(typs) == 1): 
            if ("проезд" in aa.types and "проспект" in aa.types): 
                aa.types.clear()
                aa.types.append(typs[0])
        if (len(aa.types) == 1 and ((aa.types[0] == "район" or aa.types[0] == "город" or aa.types[0] == "населенный пункт")) and len(typs) == 1): 
            if ((it.level == AddrLevel.CITY and aa.types[0] == "город" and len(it.gars) == 1) and it.gars[0].level != GarLevel.CITY and typs[0] != "город"): 
                it.level = AddrLevel.LOCALITY
            aa.types.clear()
            aa.types.append(typs[0])
        elif ((len(aa.types) == 1 and aa.types[0] == "город" and len(levs) == 1) and levs[0] == GarLevel.LOCALITY and it.level == AddrLevel.CITY): 
            aa.types.clear()
            aa.types.extend(typs)
            it.level = AddrLevel.LOCALITY
        if (len(aa.types) == 0): 
            aa.types.extend(typs)
        if ((len(typs) == 1 and it.level == AddrLevel.STREET and aa.types[0] != typs[0]) and typs[0] != "территория"): 
            if ((len(aa.types) == 1 and aa.types[0] == "улица" and len(levs) == 1) and levs[0] == GarLevel.AREA and len(it.gars) == 1): 
                aa.types.clear()
                aa.types.append("территория")
                aa.miscs.extend(it.gars[0].attrs.miscs)
                it.level = AddrLevel.TERRITORY
            elif (not "километр" in aa.types): 
                if (typs[0] in aa.types): 
                    aa.types.remove(typs[0])
                aa.types.insert(0, typs[0])
        if (len(aa.types) > 1 and aa.types[0] == "улица"): 
            del aa.types[0]
            aa.types.append("улица")
        if (len(aa.names) == 0): 
            for g in it.gars: 
                ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
                if (len(ga.names) > 0): 
                    if (aa.number is not None and ga.names[0].replace(" ", "").find(aa.number) >= 0): 
                        pass
                    else: 
                        aa.names.append(ga.names[0])
                        if (len(aa.miscs) > 0 and Utils.compareStrings(aa.miscs[0], ga.names[0], True) == 0): 
                            del aa.miscs[0]
                        if (len(aa.types) > 1 and ga.names[0].lower() in aa.types): 
                            aa.types.remove(ga.names[0].lower())
                        break
            return
        for g in it.gars: 
            ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
            for n in aa.names: 
                for gn in ga.names: 
                    if (gn in aa.names or gn.replace('-', ' ') in aa.names): 
                        if (gn != aa.names[0]): 
                            aa.names.remove(gn)
                            aa.names.insert(0, gn)
                        elif (gn != ga.names[0] and not ga.names[0] in aa.names): 
                            aa.names.insert(0, ga.names[0])
                        return
                    elif (n in gn): 
                        if (len(gn) <= (len(n) + 1)): 
                            aa.names.insert(0, gn)
                        elif (n != aa.names[0]): 
                            aa.names.remove(n)
                            aa.names.insert(0, n)
                        return
        for g in it.gars: 
            ga = Utils.asObjectOrNull(g.attrs, AreaAttributes)
            na = NameAnalyzer()
            na.process(ga.names, (None if len(ga.types) == 0 else ga.types[0]), (None if len(ga.miscs) == 0 else ga.miscs[0]))
            aa2 = AreaAttributes()
            AnalyzeHelper.__set_name(aa2, na.ref, "NAME")
            if (len(aa2.names) > 0): 
                if (not aa2.names[0] in aa.names): 
                    if (MiscHelper.can_be_equals_ex(aa2.names[0], aa.names[0], CanBeEqualsAttr.NO)): 
                        aa.names.clear()
                    aa.names.insert(0, aa2.names[0])
                elif (len(ga.names[0]) == len(aa.names[0])): 
                    aa.names.insert(0, ga.names[0])
                break
        if (len(aa.types) == 0 and it.level == AddrLevel.STREET and len(aa.names) > 0): 
            if (aa.names[0].endswith("ая")): 
                aa.types.append("улица")
    
    @staticmethod
    def __correct_levels(addr : 'TextAddress') -> None:
        i = 0
        first_pass3273 = True
        while True:
            if first_pass3273: first_pass3273 = False
            else: i += 1
            if (not (i < len(addr.items))): break
            it = addr.items[i]
            AnalyzeHelper.__correct_object_by_gars(it)
            if (it.cross_object is not None): 
                AnalyzeHelper.__correct_object_by_gars(it.cross_object)
            aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            if ((i + 1) >= len(addr.items)): 
                if (it.level == AddrLevel.STREET and i == 1 and addr.items[0].level == AddrLevel.COUNTRY): 
                    if (len(aa.miscs) == 0 and len(aa.types) == 0): 
                        it.level = AddrLevel.UNDEFINED
                continue
            it1 = addr.items[i + 1]
            if (it.level == AddrLevel.DISTRICT): 
                if (it1.level == AddrLevel.TERRITORY or it1.level == AddrLevel.STREET): 
                    if ("улус" in it.attrs.types): 
                        it.level = AddrLevel.LOCALITY
            elif (it.level == AddrLevel.LOCALITY and it1.level == AddrLevel.LOCALITY): 
                if (len(it1.gars) > 0 and it1.gars[0].level == GarLevel.AREA): 
                    it1.level = AddrLevel.TERRITORY
            elif ((it.level == AddrLevel.LOCALITY and len(it.gars) > 0 and it.gars[0].level == GarLevel.CITY) and addr.find_item_by_level(AddrLevel.CITY) is None): 
                it.level = AddrLevel.CITY
            elif (((it.level == AddrLevel.TERRITORY and i > 0 and (AddressHelper.compare_levels(addr.items[i - 1].level, AddrLevel.LOCALITY) < 0)) and ((it1.level == AddrLevel.TERRITORY or it1.level == AddrLevel.STREET)) and len(it.gars) == 1) and ((it.gars[0].level == GarLevel.LOCALITY or it.gars[0].level == GarLevel.CITY))): 
                if (it.level == AddrLevel.TERRITORY and "дорога" in aa.miscs): 
                    pass
                else: 
                    it.level = AddrLevel.LOCALITY
                    if ("территория" in aa.types): 
                        aa.types.remove("территория")
                    ty = it.gars[0].attrs.types[0]
                    if (not ty in aa.types): 
                        aa.types.append(ty)
            elif ((it.level == AddrLevel.CITY and len(it.gars) > 0 and it.gars[0].level == GarLevel.SETTLEMENT) and it1.level == AddrLevel.LOCALITY): 
                it.level = AddrLevel.SETTLEMENT
                aa.types.clear()
                aa.types.extend(it.gars[0].attrs.types)
            elif ((it.level == AddrLevel.CITY and len(it.gars) == 1 and it.gars[0].level == GarLevel.LOCALITY) and AddressHelper.compare_levels(it1.level, AddrLevel.LOCALITY) > 0): 
                it.level = AddrLevel.LOCALITY
                aa.types.clear()
                aa.types.extend(it.gars[0].attrs.types)
            elif ((it.level == AddrLevel.LOCALITY and AddressHelper.compare_levels(it1.level, AddrLevel.STREET) >= 0 and i > 0) and addr.items[i - 1].level == AddrLevel.CITY): 
                if (len(it.gars) > 0 and it.gars[0].level == GarLevel.AREA): 
                    it.level = AddrLevel.TERRITORY
                    aa.types.clear()
                    aa.types.extend(it.gars[0].attrs.types)
            elif ((it.level == AddrLevel.LOCALITY and len(it.gars) == 1 and it1.level == AddrLevel.TERRITORY) and len(it1.gars) == 1 and it1.gars[0].level == GarLevel.DISTRICT): 
                is_distr = False
                for pid in it.gars[0].parent_ids: 
                    if (it1.gars[0].id0_ == pid): 
                        is_distr = True
                if (is_distr): 
                    it1.level = AddrLevel.CITYDISTRICT
                    addr.items[i] = it1
                    addr.items[i + 1] = it