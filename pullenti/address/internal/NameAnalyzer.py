# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.address.internal.gar.AreaObject import AreaObject
from pullenti.ner.Referent import Referent
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.address.internal.gar.FiasAddrTable import FiasAddrTable
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.GarStatus import GarStatus
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis

class NameAnalyzer:
    
    def __init__(self) -> None:
        self.status = GarStatus.ERROR
        self.ref = None;
        self.types = None;
        self.strings = None;
        self.strings_ex = None;
        self.doubt_strings = None;
        self.miscs = None;
        self.level = AddrLevel.UNDEFINED
        self.sec = None;
        self.cross = None;
        self.strict_search = False
        self.ocr_regime = False
        self.ao = None;
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        self.out_info(tmp)
        return Utils.toStringStringIO(tmp)
    
    def __merge_with_other(self, na : 'NameAnalyzer') -> None:
        if (self.strings is None): 
            self.strings = na.strings
        else: 
            for s in na.strings: 
                if (not s in self.strings): 
                    self.strings.append(s)
        if (self.strings_ex is None): 
            self.strings_ex = na.strings_ex
        else: 
            for s in na.strings_ex: 
                if (not s in self.strings_ex): 
                    self.strings_ex.append(s)
        if (self.doubt_strings is None): 
            self.doubt_strings = na.doubt_strings
        else: 
            for s in na.doubt_strings: 
                if (not s in self.doubt_strings): 
                    self.doubt_strings.append(s)
        if (self.miscs is None): 
            self.miscs = na.miscs
        else: 
            for s in na.miscs: 
                if (not s in self.miscs): 
                    self.miscs.append(s)
    
    def init_by_referent(self, r : 'Referent', gar_regime : bool) -> None:
        self.ref = r
        self.strings = list()
        self.doubt_strings = list()
        if (gar_regime): 
            self.strings_ex = list()
        else: 
            self.strings_ex = (None)
        if ((isinstance(self.ref, GeoReferent)) and Utils.compareStrings(str(self.ref), "ДНР", True) == 0): 
            self.ref = (GeoReferent())
            self.ref.add_slot(GeoReferent.ATTR_TYPE, "республика", False, 0)
            self.ref.add_slot(GeoReferent.ATTR_NAME, "ДОНЕЦКАЯ", False, 0)
            self.level = AddrLevel.REGIONAREA
        elif ((isinstance(self.ref, GeoReferent)) and Utils.compareStrings(str(self.ref), "ЛНР", True) == 0): 
            self.ref = (GeoReferent())
            self.ref.add_slot(GeoReferent.ATTR_TYPE, "республика", False, 0)
            self.ref.add_slot(GeoReferent.ATTR_NAME, "ЛУГАНСКАЯ", False, 0)
            self.level = AddrLevel.REGIONAREA
        NameAnalyzer.__get_strings(self.ref, self.strings, self.doubt_strings, self.strings_ex, self.ocr_regime)
        self.types = self.ref.get_string_values((StreetReferent.ATTR_TYPE if isinstance(self.ref, StreetReferent) else GeoReferent.ATTR_TYPE))
        if (isinstance(self.ref, StreetReferent)): 
            num = self.ref.numbers
            if (num is not None and num.endswith("км")): 
                if (len(self.ref.names) > 0): 
                    self.sec = NameAnalyzer()
                    s1 = StreetReferent()
                    s1.add_slot(StreetReferent.ATTR_NUMBER, num, False, 0)
                    self.sec.init_by_referent(s1, gar_regime)
                    self.level = AddrLevel.TERRITORY
                    r.add_slot(StreetReferent.ATTR_NUMBER, None, True, 0)
                    self.strings.clear()
                    self.doubt_strings.clear()
                    if (self.strings_ex is not None): 
                        self.strings_ex.clear()
                    NameAnalyzer.__get_strings(r, self.strings, self.doubt_strings, self.strings_ex, self.ocr_regime)
                    r.add_slot(StreetReferent.ATTR_NUMBER, num, True, 0)
                else: 
                    self.types.append("километр")
        if (self.level == AddrLevel.UNDEFINED): 
            self.level = NameAnalyzer.calc_level(self.ref)
        self.miscs = self.ref.get_string_values("MISC")
        if (len(self.miscs) > 0): 
            add_misc = list()
            for m in self.miscs: 
                s = None
                if ("гараж" in m): 
                    s = "гаражи"
                elif ("садов" in m or "дачн" in m): 
                    s = "дачи"
                elif ("жилищ" in m): 
                    s = "жилье"
                elif ("месторожде" in m): 
                    s = "месторождение"
                if (s is not None and not s in add_misc): 
                    add_misc.append(s)
            has_up = False
            for m in self.miscs: 
                if (str.isupper(m[0])): 
                    has_up = True
            if (has_up): 
                for i in range(len(self.miscs) - 1, -1, -1):
                    if (not str.isupper(self.miscs[i][0]) and self.miscs[i].find(' ') > 0): 
                        del self.miscs[i]
            if (len(add_misc) > 0): 
                for m in add_misc: 
                    if (not m in self.miscs): 
                        self.miscs.append(m)
            if (isinstance(self.ref, StreetReferent)): 
                if (self.ref.kind == StreetKind.ROAD): 
                    self.miscs.append("дорога")
        self.status = GarStatus.OK
    
    @staticmethod
    def merge_objects(hi : 'Referent', lo : 'Referent') -> 'Referent':
        return None
    
    def try_create_alternative(self, sec_ : bool, prev : 'AddrObject', next0_ : 'AddrObject') -> 'NameAnalyzer':
        street = Utils.asObjectOrNull(self.ref, StreetReferent)
        if (street is not None): 
            name = street.get_string_value(StreetReferent.ATTR_NAME)
            typs = street.typs
            if (not sec_ and street.numbers is not None and name == "МИКРОРАЙОН"): 
                sr = StreetReferent()
                sr.add_slot(StreetReferent.ATTR_TYPE, name.lower(), False, 0)
                sr.numbers = street.numbers
                sr.kind = StreetKind.AREA
                alt = NameAnalyzer()
                alt.init_by_referent(sr, False)
                return alt
            elif ((name is None and not sec_ and street.numbers is not None) and (("микрорайон" in typs or "набережная" in typs))): 
                sr = StreetReferent()
                sr.add_slot(StreetReferent.ATTR_NAME, ("МИКРОРАЙОН" if "микрорайон" in typs else "НАБЕРЕЖНАЯ"), False, 0)
                sr.numbers = street.numbers
                alt = NameAnalyzer()
                alt.init_by_referent(sr, False)
                return alt
            if ((len(typs) == 1 and typs[0] == "территория" and name is None) and street.find_slot("NUMBER", None, True) is None): 
                miscs_ = street.get_string_values("MISC")
                if (len(miscs_) == 1): 
                    geo2 = GeoReferent()
                    geo2.add_slot(GeoReferent.ATTR_TYPE, "населенный пункт", False, 0)
                    geo2.add_slot(GeoReferent.ATTR_NAME, miscs_[0].upper(), False, 0)
                    alt = NameAnalyzer()
                    alt.init_by_referent(geo2, False)
                    return alt
        geo = Utils.asObjectOrNull(self.ref, GeoReferent)
        if (geo is not None): 
            typs = geo.typs
            if (len(typs) == 1 and ((typs[0] == "район" or typs[0] == "муниципальный район" or typs[0] == "населенный пункт"))): 
                num = geo.get_string_value("NUMBER")
                if (not sec_): 
                    geo2 = GeoReferent()
                    if (typs[0] != "населенный пункт"): 
                        geo2.add_slot(GeoReferent.ATTR_TYPE, "населенный пункт", False, 0)
                    else: 
                        geo2.add_slot(GeoReferent.ATTR_TYPE, "территория", False, 0)
                    for s in geo.get_string_values(GeoReferent.ATTR_NAME): 
                        geo2.add_slot(GeoReferent.ATTR_NAME, s, False, 0)
                    if (num is not None): 
                        geo2.add_slot("NUMBER", num, False, 0)
                    alt = NameAnalyzer()
                    alt.init_by_referent(geo2, False)
                    return alt
                else: 
                    if (prev is not None and prev.level == AddrLevel.REGIONAREA): 
                        return None
                    if (next0_ is not None and next0_.level == AddrLevel.STREET): 
                        return None
                    sr = StreetReferent()
                    for s in geo.get_string_values(GeoReferent.ATTR_NAME): 
                        sr.add_slot(StreetReferent.ATTR_NAME, s, False, 0)
                    if (num is not None): 
                        sr.add_slot(StreetReferent.ATTR_NUMBER, num, False, 0)
                    alt = NameAnalyzer()
                    alt.init_by_referent(sr, False)
                    return alt
            if (geo.is_city and not "город" in typs): 
                if (prev is not None and ((prev.level == AddrLevel.CITY or prev.level == AddrLevel.REGIONCITY or prev.level == AddrLevel.LOCALITY))): 
                    if (next0_ is not None and ((next0_.level == AddrLevel.STREET or next0_.level == AddrLevel.TERRITORY))): 
                        return None
                    sr = StreetReferent()
                    nam = str(geo)
                    ii = nam.find(';')
                    if (ii > 0): 
                        nam = nam[0:0+ii]
                    sr.add_slot(StreetReferent.ATTR_NAME, nam.upper(), False, 0)
                    for s in geo.get_string_values(GeoReferent.ATTR_NAME): 
                        sr.add_slot(StreetReferent.ATTR_NAME, s, False, 0)
                    for ty in typs: 
                        sr.add_slot(StreetReferent.ATTR_MISC, ty, False, 0)
                    num = geo.get_string_value("NUMBER")
                    if (num is not None): 
                        sr.add_slot(StreetReferent.ATTR_NUMBER, num, False, 0)
                    alt = NameAnalyzer()
                    alt.init_by_referent(sr, False)
                    return alt
        return None
    
    def process_ex(self, go : 'GarObject') -> None:
        aa = Utils.asObjectOrNull(go.attrs, AreaAttributes)
        self.process(aa.names, aa.types[0], (aa.miscs[0] if len(aa.miscs) > 0 else None))
    
    def process(self, names : typing.List[str], typ : str, misc : str) -> None:
        self.strings = (None)
        self.status = GarStatus.ERROR
        self.ref = (None)
        if (typ == "чувашия"): 
            typ = "республика"
            names[0] = "Чувашская Республика"
        best_coef = 10000
        best_ref = None
        best_sec_ref = None
        best_ref2 = None
        nn = 0
        first_pass3291 = True
        while True:
            if first_pass3291: first_pass3291 = False
            else: nn += 1
            if (not (nn < len(names))): break
            name = NameAnalyzer.correct_fias_name(names[nn])
            jj = nn + 1
            while jj < len(names): 
                if (names[jj] == name): 
                    del names[jj]
                    jj -= 1
                jj += 1
            if ("Капотня" in name): 
                pass
            if (name == "ЖСТ Чаевод квартал Питомник-2"): 
                pass
            if (misc is not None and not misc in name): 
                name = "{0} {1}".format(misc, name)
            iii = name.find('/')
            if (iii > 5 and ((iii + 4) < len(name))): 
                name2 = name[iii + 1:].strip()
                is_cross = False
                if (name[iii + 1] != ' ' or name[iii - 1] != ' '): 
                    ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(name2), None, None)
                    if (ar.first_token is not None): 
                        if (StreetItemToken.check_keyword(ar.first_token)): 
                            is_cross = True
                        elif (ar.first_token.chars.is_capital_upper): 
                            is_cross = True
                        elif ((isinstance(ar.first_token, NumberToken)) and name2.find('-') > 0): 
                            is_cross = True
                if (is_cross): 
                    cnames = list()
                    cnames.append(name2)
                    cross_ = NameAnalyzer()
                    cross_.process(cnames, None, None)
                    if (cross_.status != GarStatus.OK or cross_.level != AddrLevel.STREET or len(cross_.types) == 0): 
                        cross_.process(cnames, typ, misc)
                    if (cross_.status != GarStatus.OK): 
                        self.status = GarStatus.ERROR
                        return
                    self.cross = cross_
                    name = name[0:0+iii].strip()
                else: 
                    names.insert(nn + 1, name2)
                    name = name[0:0+iii].strip()
            if (Utils.isNullOrEmpty(name)): 
                continue
            name = NameAnalyzer.__corr_name(name)
            if (typ == "муниципальный округ"): 
                if (name.startswith("поселение ")): 
                    name = name[10:].strip()
            if ("Олимп.дер" in name): 
                name = "улица Олимпийская Деревня"
            elif (Utils.compareStrings("ЛЕНИНСКИЕ ГОРЫ", name, True) == 0): 
                name = ("улица " + name)
            for k in range(1):
                if (k > 0 and Utils.isNullOrEmpty(typ)): 
                    continue
                txt = (name if Utils.isNullOrEmpty(typ) else (("{0} \"{1}\"".format(typ, name) if k == 1 else "{0} {1}".format(typ, name))))
                if (Utils.compareStrings(Utils.ifNotNull(typ, ""), "километр", True) == 0 and (((len(name) < 6) or not str.isdigit(name[0])))): 
                    txt = "{0} {1}".format(name, typ)
                elif (("квартал" in name and not name.endswith("квартал") and str.isdigit(name[0])) and typ != "микрорайон"): 
                    txt = "{0} {1}".format(name, typ)
                txt0 = txt
                ncheck = MiscLocationHelper.NAME_CHECKER
                MiscLocationHelper.NAME_CHECKER = (None)
                ar = None
                try: 
                    ar = ProcessorService.get_standard_processor().process(SourceOfAnalysis._new129(txt, "GARADDRESS"), None, None)
                except Exception as ex: 
                    pass
                MiscLocationHelper.NAME_CHECKER = ncheck
                r = None
                r2 = None
                if (ar is None): 
                    continue
                for ii in range(len(ar.entities) - 1, -1, -1):
                    if (isinstance(ar.entities[ii], GeoReferent)): 
                        geo = Utils.asObjectOrNull(ar.entities[ii], GeoReferent)
                        if (geo.find_slot("NAME", "МОСКВА", True) is not None): 
                            if (Utils.compareStrings("МОСКВА", name, True) == 0): 
                                pass
                            else: 
                                continue
                        if (len(geo.occurrence) == 0 or geo.occurrence[0].begin_char > 8): 
                            continue
                        if (r is None): 
                            r = (geo)
                    elif (isinstance(ar.entities[ii], StreetReferent)): 
                        sr = Utils.asObjectOrNull(ar.entities[ii], StreetReferent)
                        is_olimp = sr.find_slot("NAME", "ОЛИМПИЙСКАЯ ДЕРЕВНЯ", True) is not None
                        if (r is None): 
                            r = (sr)
                            if (ii > 0 and is_olimp and (isinstance(ar.entities[ii - 1], StreetReferent))): 
                                ar.entities[ii - 1].higher = sr
                        elif (sr.higher == r): 
                            r = (sr)
                        elif (is_olimp): 
                            if (isinstance(r, StreetReferent)): 
                                r.higher = sr
                            else: 
                                pass
                    elif (isinstance(ar.entities[ii], AddressReferent)): 
                        aa = Utils.asObjectOrNull(ar.entities[ii], AddressReferent)
                        if (aa.block is not None): 
                            r2 = (StreetReferent())
                            r2.add_slot(StreetReferent.ATTR_TYPE, "блок", False, 0)
                            r2.add_slot(StreetReferent.ATTR_NUMBER, aa.block, False, 0)
                            r2.occurrence.extend(aa.occurrence)
                    else: 
                        pass
                co = 0
                if (r is None): 
                    if ((name.find(' ') < 0) and (name.find('.') < 0) and Utils.isNullOrEmpty(typ)): 
                        r = (StreetReferent())
                        r.add_slot(StreetReferent.ATTR_NAME, name.upper(), False, 0)
                        r.add_slot(StreetReferent.ATTR_TYPE, "улица", False, 0)
                        co = 10
                    else: 
                        ar1 = None
                        try: 
                            ar1 = ProcessorService.get_standard_processor().process(SourceOfAnalysis(txt0), None, None)
                        except Exception as ex197: 
                            pass
                        if (ar1 is not None and ar1.first_token is not None): 
                            if ("линия" in txt0): 
                                pass
                            strs = StreetItemToken.try_parse_list(ar1.first_token, 10, None)
                            rt = StreetDefineHelper.try_parse_ext_street(strs)
                            if (rt is not None and rt.end_token.next0_ is None): 
                                txt = txt0
                                r = rt.referent
                        if (r is None): 
                            continue
                elif (len(r.occurrence) > 0): 
                    if (r.occurrence[0].end_char < (len(txt) - 1)): 
                        ec = r.occurrence[0].end_char
                        if (r2 is not None and len(r2.occurrence) > 0 and r2.occurrence[0].end_char >= (len(txt) - 1)): 
                            pass
                        elif (ec == (len(txt) - 2) and txt[ec + 1] == '.'): 
                            pass
                        else: 
                            rest = txt[r.occurrence[0].end_char + 1:].strip()
                            if (rest == "-й"): 
                                pass
                            else: 
                                co += (len(txt) - 1 - r.occurrence[0].end_char)
                if (co < best_coef): 
                    best_coef = co
                    best_ref = r
                    best_sec_ref = r2
                    best_ref2 = (None)
                    if (best_coef == 0): 
                        break
                elif (co == best_coef): 
                    if (best_ref2 is None): 
                        best_ref2 = r
                    elif (not best_ref2.can_be_equals(best_ref, ReferentsEqualType.WITHINONETEXT)): 
                        best_ref2 = r
            if (best_ref is not None): 
                self.ref = best_ref
                self.init_by_referent(self.ref, True)
                if (best_coef > 0): 
                    self.status = GarStatus.WARNING
                sec_ref = None
                if (isinstance(self.ref, StreetReferent)): 
                    str0_ = Utils.asObjectOrNull(self.ref, StreetReferent)
                    if (str0_.higher is not None): 
                        sec_ref = (str0_.higher)
                    else: 
                        geo = Utils.asObjectOrNull(str0_.get_slot_value("GEO"), GeoReferent)
                        if (geo is not None and geo.find_slot("NAME", "Москва", True) is None): 
                            sec_ref = (geo)
                if (sec_ref is not None): 
                    self.sec = NameAnalyzer()
                    self.sec.init_by_referent(self.ref, True)
                    self.init_by_referent(sec_ref, True)
                elif (best_sec_ref is not None): 
                    self.sec = NameAnalyzer()
                    self.sec.init_by_referent(best_sec_ref, True)
                if (best_ref2 is not None and self.sec is None): 
                    na2 = NameAnalyzer()
                    na2.init_by_referent(best_ref2, True)
                    self.__merge_with_other(na2)
            if (self.status == GarStatus.OK and self.level == AddrLevel.UNDEFINED): 
                self.status = GarStatus.WARNING
            if (self.sec is not None): 
                if (self.sec.sec is not None): 
                    self.status = GarStatus.ERROR
                elif (self.sec.status != GarStatus.OK): 
                    self.status = self.sec.status
                if (self.status == GarStatus.OK): 
                    self.status = GarStatus.OK2
    
    def out_info(self, tmp : io.StringIO) -> None:
        if (self.status == GarStatus.ERROR and self.sec is None): 
            print("ошибка", end="", file=tmp)
            return
        print("{0} ".format(Utils.enumToString(self.level)), end="", file=tmp, flush=True)
        if (self.types is not None): 
            i = 0
            while i < len(self.types): 
                print("{0}{1}".format(("/" if i > 0 else ""), self.types[i]), end="", file=tmp, flush=True)
                i += 1
        if (self.strings is not None and len(self.strings) > 0): 
            print(" <", end="", file=tmp)
            i = 0
            while i < len(self.strings): 
                print("{0}{1}".format((", " if i > 0 else ""), self.strings[i]), end="", file=tmp, flush=True)
                i += 1
            print(">", end="", file=tmp)
        if (self.miscs is not None and len(self.miscs) > 0): 
            print(" [", end="", file=tmp)
            i = 0
            while i < len(self.miscs): 
                print("{0}{1}".format((", " if i > 0 else ""), self.miscs[i]), end="", file=tmp, flush=True)
                i += 1
            print("]", end="", file=tmp)
        if (self.sec is not None): 
            print(" + ", end="", file=tmp)
            self.sec.out_info(tmp)
        if (self.cross is not None): 
            print(" / ", end="", file=tmp)
            self.cross.out_info(tmp)
        if (self.status == GarStatus.WARNING): 
            print(" (неточность при анализе)", end="", file=tmp)
        elif (self.status == GarStatus.ERROR): 
            print(" (ОШИБКА)", end="", file=tmp)
    
    @staticmethod
    def calc_level(r : 'Referent') -> 'AddrLevel':
        from pullenti.address.internal.RegionHelper import RegionHelper
        geo = Utils.asObjectOrNull(r, GeoReferent)
        res = AddrLevel.UNDEFINED
        if (geo is not None): 
            if (geo.is_state): 
                return AddrLevel.COUNTRY
            if (geo.is_city): 
                res = AddrLevel.LOCALITY
                for ty in geo.typs: 
                    if (ty == "город" or ty == "місто"): 
                        res = AddrLevel.CITY
                        nam = geo.get_string_value(GeoReferent.ATTR_NAME)
                        if (nam == "МОСКВА" or nam == "САНКТ-ПЕТЕРБУРГ" or nam == "СЕВАСТОПОЛЬ"): 
                            res = AddrLevel.REGIONCITY
                        break
                    elif (ty == "городское поселение" or ty == "сельское поселение"): 
                        res = AddrLevel.SETTLEMENT
                        break
                    elif (ty == "населенный пункт" and len(geo.typs) == 1): 
                        nam = geo.get_string_value(GeoReferent.ATTR_NAME)
                        if (RegionHelper.is_big_city(nam) is not None): 
                            res = AddrLevel.CITY
                    elif (ty == "улус"): 
                        res = AddrLevel.DISTRICT
            elif (geo.is_region): 
                res = AddrLevel.DISTRICT
                for ty in geo.typs: 
                    if ((ty == "городской округ" or ty == "муниципальный район" or ty == "муниципальный округ") or ty == "федеральная территория"): 
                        res = AddrLevel.DISTRICT
                        break
                    elif (ty == "район" or ty == "автономный округ"): 
                        res = AddrLevel.DISTRICT
                        break
                    elif (ty.endswith("область") or ty == "край"): 
                        res = AddrLevel.REGIONAREA
                        break
                    elif (ty == "сельский округ"): 
                        res = AddrLevel.SETTLEMENT
                        break
                    elif (ty == "республика"): 
                        res = AddrLevel.REGIONAREA
                        break
            return res
        street = Utils.asObjectOrNull(r, StreetReferent)
        if (street is not None): 
            res = AddrLevel.STREET
            ki = r.kind
            if (ki == StreetKind.AREA or ki == StreetKind.ORG): 
                res = AddrLevel.TERRITORY
        if (isinstance(r, OrganizationReferent)): 
            return AddrLevel.TERRITORY
        return res
    
    @staticmethod
    def correct_fias_name(name : str) -> str:
        if (name is None): 
            return None
        ii = name.find(", находящ")
        if (ii < 0): 
            ii = name.find(",находящ")
        if (ii > 0): 
            name = name[0:0+ii].strip()
        if ("Г СК " in name): 
            name = name.replace("Г СК ", "ГСК ")
        return name
    
    @staticmethod
    def corr_name(str0_ : str) -> str:
        res = io.StringIO()
        NameAnalyzer.__corr_name2(res, str0_.upper())
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __corr_name2(res : io.StringIO, str0_ : str) -> int:
        corr = 0
        i = 0
        first_pass3292 = True
        while True:
            if first_pass3292: first_pass3292 = False
            else: i += 1
            if (not (i < len(str0_))): break
            ch = str0_[i]
            if (ch == 'Ь' or ch == 'Ъ'): 
                corr += 1
                continue
            if (str.isalnum(ch) or ch == ' ' or ch == '-'): 
                if (ch == '-'): 
                    ch = ' '
                    corr += 1
                if (i > 0 and res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) == ch): 
                    corr += 1
                    continue
                print(ch, end="", file=res)
        if (len(str0_) > 4 and res.tell() > 4): 
            ch1 = Utils.getCharAtStringIO(res, res.tell() - 1)
            ch2 = Utils.getCharAtStringIO(res, res.tell() - 2)
            ch3 = Utils.getCharAtStringIO(res, res.tell() - 3)
            if (LanguageHelper.is_cyrillic_vowel(ch1) or ch1 == 'Й'): 
                if (not LanguageHelper.is_cyrillic_vowel(ch2)): 
                    if (ch2 == 'Г' and ch3 == 'О'): 
                        Utils.setLengthStringIO(res, res.tell() - 2)
                    Utils.setCharAtStringIO(res, res.tell() - 1, '@')
                elif (not LanguageHelper.is_cyrillic_vowel(ch3)): 
                    Utils.setLengthStringIO(res, res.tell() - 1)
                    Utils.setCharAtStringIO(res, res.tell() - 1, '@')
        return corr
    
    @staticmethod
    def __corr_name(name : str) -> str:
        jj = name.find('(')
        if (jj > 0): 
            name = name[0:0+jj].strip()
        sec_var = None
        det = None
        if (str.isdigit(name[len(name) - 1])): 
            for i in range(len(name) - 1, 0, -1):
                if (not str.isdigit(name[i])): 
                    if (name[i] != '-'): 
                        name += "-й"
                    break
        if (name.endswith("-ад.")): 
            name = name[0:0+len(name) - 4]
        return name
    
    @staticmethod
    def create_search_variants(res : typing.List[str], res1 : typing.List[str], res2 : typing.List[str], name : str, num : str=None, ocr_regime_ : bool=False) -> None:
        if (name is None): 
            return
        items = list()
        sps = 0
        hiphs = 0
        i = 0
        while i < len(name): 
            ch = name[i]
            j = 0
            if (str.isalpha(ch)): 
                j = i
                while j < len(name): 
                    if (not str.isalpha(name[j])): 
                        break
                    j += 1
                if (i == 0 and j == len(name)): 
                    items.append(name)
                else: 
                    items.append(name[i:i+j - i])
                i = (j - 1)
            elif (ch == ' ' or ch == '.'): 
                sps += 1
            elif (ch == '-'): 
                hiphs += 1
            elif (str.isdigit(ch) and num is None): 
                j = i
                while j < len(name): 
                    if (not str.isdigit(name[j])): 
                        break
                    j += 1
                num = name[i:i+j - i]
                i = (j - 1)
            i += 1
        if ("НА" in items and len(items) > 2): 
            items.remove("НА")
        std_adj = None
        alt_std_adj = None
        if (len(items) > 1 and not ocr_regime_): 
            i = 0
            first_pass3293 = True
            while True:
                if first_pass3293: first_pass3293 = False
                else: i += 1
                if (not (i < len(items))): break
                it = items[i]
                if (it == "И"): 
                    del items[i]
                    i -= 1
                    if (len(items) == 1): 
                        break
                    continue
                if (it == "В"): 
                    std_adj = "ВР"
                    alt_std_adj = "ВЛ"
                    del items[i]
                    break
                if (it == "С"): 
                    std_adj = "СТ"
                    alt_std_adj = "СР"
                    del items[i]
                    break
                if (it == "Б"): 
                    std_adj = "БЛ"
                    alt_std_adj = "БЕ"
                    del items[i]
                    break
                if (it == "Н"): 
                    std_adj = "НВ"
                    alt_std_adj = "НЖ"
                    del items[i]
                    break
                if (it == "М"): 
                    std_adj = "МЛ"
                    del items[i]
                    break
                if (it == "К"): 
                    std_adj = "КР"
                    del items[i]
                    break
                if (it == "Г"): 
                    std_adj = "ГЛ"
                    del items[i]
                    break
                for k in range(2):
                    adjs = (NameAnalyzer.__m_std_arjso if k == 0 else NameAnalyzer.__m_std_arjse)
                    adjs_abbr = (NameAnalyzer.__m_std_arjs_oabbr if k == 0 else NameAnalyzer.__m_std_arjs_eabbr)
                    j = 0
                    first_pass3294 = True
                    while True:
                        if first_pass3294: first_pass3294 = False
                        else: j += 1
                        if (not (j < len(adjs))): break
                        a = adjs[j]
                        if (it.startswith(a)): 
                            if (len(it) == (len(a) + 2)): 
                                std_adj = adjs_abbr[j]
                                del items[i]
                                break
                            if (len(it) == (len(a) + 1)): 
                                if (k == 0 and it[len(a)] == 'О'): 
                                    pass
                                elif (k == 1 and it[len(a)] == 'Е'): 
                                    pass
                                else: 
                                    continue
                                std_adj = adjs_abbr[j]
                                del items[i]
                                break
                            if (len(it) > (len(a) + 3)): 
                                if (k == 0 and it[len(a)] == 'О'): 
                                    pass
                                elif (k == 1 and it[len(a)] == 'Е'): 
                                    pass
                                else: 
                                    continue
                                std_adj = adjs_abbr[j]
                                items[i] = it[len(a) + 1:]
                                break
                    if (std_adj is not None): 
                        break
                if (std_adj is not None): 
                    break
        if (len(items) > 1): 
            items.sort()
        full_std_adj = None
        if (std_adj is None and len(items) == 1 and not ocr_regime_): 
            nam = items[0]
            k = 0
            while k < len(NameAnalyzer.__m_std_arjso): 
                if (nam.startswith(NameAnalyzer.__m_std_arjso[k])): 
                    pr = NameAnalyzer.__m_std_arjso[k]
                    if (((len(pr) + 3) < len(nam)) and nam[len(pr)] == 'О'): 
                        std_adj = NameAnalyzer.__m_std_arjs_oabbr[k]
                        full_std_adj = (pr + "О")
                        nam = nam[len(pr) + 1:]
                        items[0] = nam
                        break
                k += 1
            if (std_adj is None): 
                k = 0
                while k < len(NameAnalyzer.__m_std_arjse): 
                    if (nam.startswith(NameAnalyzer.__m_std_arjse[k])): 
                        pr = NameAnalyzer.__m_std_arjse[k]
                        if (((len(pr) + 3) < len(nam)) and nam[len(pr)] == 'Е'): 
                            std_adj = NameAnalyzer.__m_std_arjs_eabbr[k]
                            full_std_adj = (pr + "Е")
                            nam = nam[len(pr) + 1:]
                            items[0] = nam
                            break
                    k += 1
        if (ocr_regime_): 
            if (num is not None): 
                res.append(num)
            res.extend(items)
            return
        pref = None
        if (std_adj is not None): 
            pref = std_adj.lower()
            if (num is not None): 
                pref += num
        elif (num is not None): 
            pref = num
        tmp = io.StringIO()
        tmp2 = None
        if (pref is not None): 
            print(pref, end="", file=tmp)
        i = 0
        while i < len(items): 
            NameAnalyzer.__corr_name2(tmp, items[i])
            i += 1
        if (len(items) > 1): 
            tmp2 = io.StringIO()
            if (pref is not None): 
                print(pref, end="", file=tmp2)
            for i in range(len(items) - 1, -1, -1):
                NameAnalyzer.__corr_name2(tmp2, items[i])
        r = Utils.toStringStringIO(tmp)
        if (len(r) > 0 and not r in res): 
            res.append(r)
            if (r == "ТАВРИЙСК@"): 
                res.append("ТАВРИЧЕСК@")
            if (full_std_adj is not None): 
                res.append(full_std_adj + r[2:])
            if (res1 is not None and r[len(r) - 1] == '@'): 
                res1.append(r[0:0+len(r) - 1])
        if (alt_std_adj is not None): 
            res.append(r.replace(std_adj, alt_std_adj))
        if (tmp2 is not None): 
            r2 = Utils.toStringStringIO(tmp2)
            if (len(r2) > 0 and not r2 in res): 
                res.append(r2)
                if (full_std_adj is not None): 
                    res.append(full_std_adj + r2[2:])
                if (res1 is not None and r2[len(r2) - 1] == '@'): 
                    res1.append(r2[0:0+len(r2) - 1])
        if (len(items) == 1 and items[0].endswith("ОГО")): 
            rr = r[0:0+len(r) - 1] + "ОГ@"
            if (not rr in res): 
                res.append(rr)
        if (res2 is not None and pref is not None): 
            Utils.removeStringIO(tmp, 0, len(pref))
            print(pref, end="", file=tmp)
            r = Utils.toStringStringIO(tmp)
            if (not r in res2): 
                res2.append(r)
    
    @staticmethod
    def correct_adj(val : str) -> str:
        i = 0
        while i < len(NameAnalyzer.__m_std_arjse): 
            if (val.startswith(NameAnalyzer.__m_std_arjse[i])): 
                return NameAnalyzer.__m_std_arjs_eabbr[i].lower()
            i += 1
        i = 0
        while i < len(NameAnalyzer.__m_std_arjso): 
            if (val.startswith(NameAnalyzer.__m_std_arjso[i])): 
                return NameAnalyzer.__m_std_arjs_oabbr[i].lower()
            i += 1
        return None
    
    __m_std_arjso = None
    
    __m_std_arjs_oabbr = None
    
    __m_std_arjse = None
    
    __m_std_arjs_eabbr = None
    
    @staticmethod
    def __get_strings(r : 'Referent', res : typing.List[str], doubts : typing.List[str], revs : typing.List[str], ocr_regime_ : bool) -> None:
        if (r is None): 
            return
        if ((isinstance(r, GeoReferent)) or (isinstance(r, OrganizationReferent))): 
            num = r.get_string_value("NUMBER")
            for s in r.slots: 
                if (s.type_name == GeoReferent.ATTR_NAME): 
                    str0_ = Utils.asObjectOrNull(s.value, str)
                    if (Utils.isNullOrEmpty(str0_)): 
                        continue
                    NameAnalyzer.create_search_variants(res, doubts, revs, str0_, num, ocr_regime_)
                    if ((len(str0_) > 3 and not LanguageHelper.is_cyrillic_vowel(str0_[len(str0_) - 1]) and str0_[len(str0_) - 1] != 'Й') and str0_[len(str0_) - 1] != 'Ь'): 
                        NameAnalyzer.create_search_variants(doubts, None, None, str0_ + "А", num, ocr_regime_)
                    add = r.get_string_value(GeoReferent.ATTR_MISC)
                    if (add is not None and (str0_.find(' ') < 0)): 
                        NameAnalyzer.create_search_variants(res, doubts, revs, "{0} {1}".format(str0_, add.upper()), num, ocr_regime_)
        elif (isinstance(r, StreetReferent)): 
            str0_ = Utils.asObjectOrNull(r, StreetReferent)
            num = str0_.numbers
            if (ocr_regime_): 
                name = None
                for s in r.slots: 
                    if (s.type_name == StreetReferent.ATTR_NAME): 
                        nn = Utils.asObjectOrNull(s.value, str)
                        if (name is None or (len(nn) < len(name))): 
                            name = nn
                if (name is not None): 
                    NameAnalyzer.create_search_variants(res, doubts, revs, name, num, ocr_regime_)
            else: 
                for s in r.slots: 
                    if (s.type_name == StreetReferent.ATTR_NAME): 
                        NameAnalyzer.create_search_variants(res, doubts, revs, Utils.asObjectOrNull(s.value, str), num, ocr_regime_)
                        misc = r.get_string_value(StreetReferent.ATTR_MISC)
                        if (misc is not None): 
                            NameAnalyzer.create_search_variants(doubts, None, None, "{0} {1}".format(misc.upper(), Utils.asObjectOrNull(s.value, str)), num, ocr_regime_)
            if (len(res) == 0 and num is not None): 
                if (num.endswith("км")): 
                    num = num[0:0+len(num) - 2]
                res.append(num)
            if (len(res) == 0): 
                ty = r.get_string_value(StreetReferent.ATTR_TYPE)
                if (ty is not None): 
                    res.append(NameAnalyzer.corr_name(ty.upper()))
        i = 0
        while i < len(res): 
            j = 0
            while j < (len(res) - 1): 
                if (len(res[j]) < len(res[j + 1])): 
                    s = res[j]
                    res[j] = res[j + 1]
                    res[j + 1] = s
                j += 1
            i += 1
    
    def calc_equal_coef(self, na : 'NameAnalyzer') -> int:
        if (na is None): 
            return -1
        if (((na.level == AddrLevel.TERRITORY or na.level == AddrLevel.STREET)) and ((self.level == AddrLevel.TERRITORY or self.level == AddrLevel.STREET))): 
            if (((na.ref.find_slot("NAME", None, True) is None or self.ref.find_slot("NAME", None, True) is None)) and len(self.miscs) > 0): 
                for m in self.miscs: 
                    if (m in na.miscs): 
                        return 0
                return -1
        if (na.level == AddrLevel.STREET and self.level == AddrLevel.STREET): 
            if ("километр" in na.types != "километр" in self.types): 
                return -1
        return 0
    
    def can_be_equals(self, na : 'NameAnalyzer') -> bool:
        if (na is None): 
            return False
        ok = False
        for s in self.strings: 
            if (s in na.strings): 
                ok = True
                break
        if (not ok): 
            return False
        return True
    
    def serialize(self) -> bytearray:
        res = bytearray()
        dat = FiasAddrTable._store(self.ao)
        res.extend((len(dat)).to_bytes(4, byteorder="little"))
        res.extend(dat)
        res.append(self.level)
        res.append(self.status)
        res.append(((0 if self.types is None else len(self.types))))
        if (self.types is not None): 
            for ty in self.types: 
                FiasAddrTable.get_bytes_for_string1251(res, ty)
        res.append(((0 if self.strings is None else len(self.strings))))
        if (self.strings is not None): 
            for ty in self.strings: 
                FiasAddrTable.get_bytes_for_string1251(res, ty)
        res.append(((0 if self.miscs is None else len(self.miscs))))
        if (self.miscs is not None): 
            for ty in self.miscs: 
                FiasAddrTable.get_bytes_for_string1251(res, ty)
        return bytearray(res)
    
    def deserialize(self, dat : bytearray, typs : typing.List[tuple]) -> None:
        ind = 0
        len0_ = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        self.ao = AreaObject()
        buf = Utils.newArrayOfBytes(len0_, 0)
        i = 0
        while i < len0_: 
            buf[i] = dat[ind]
            i += 1; ind += 1
        FiasAddrTable._restore(buf, self.ao, typs)
        self.level = (Utils.valToEnum(dat[ind], AddrLevel))
        ind += 1
        self.status = (Utils.valToEnum(dat[ind], GarStatus))
        ind += 1
        cou = dat[ind]
        ind += 1
        self.types = list()
        while cou > 0: 
            wrapind198 = RefOutArgWrapper(ind)
            self.types.append(FiasAddrTable.to_string1251(dat, wrapind198))
            ind = wrapind198.value
            cou -= 1
        cou = (dat[ind])
        ind += 1
        self.strings = list()
        while cou > 0: 
            wrapind199 = RefOutArgWrapper(ind)
            self.strings.append(FiasAddrTable.to_string1251(dat, wrapind199))
            ind = wrapind199.value
            cou -= 1
        cou = (dat[ind])
        ind += 1
        if (cou > 0): 
            self.miscs = list()
            while cou > 0: 
                wrapind200 = RefOutArgWrapper(ind)
                self.miscs.append(FiasAddrTable.to_string1251(dat, wrapind200))
                ind = wrapind200.value
                cou -= 1
    
    # static constructor for class NameAnalyzer
    @staticmethod
    def _static_ctor():
        NameAnalyzer.__m_std_arjso = ["СТАР", "НОВ", "МАЛ", "СЕВЕР", "ЮГ", "ЮЖН", "ЗАПАДН", "ВОСТОЧН", "КРАСН", "БЕЛ", "ГЛАВН", "ВЕЛИК"]
        NameAnalyzer.__m_std_arjs_oabbr = ["СТ", "НВ", "МЛ", "СВ", "ЮГ", "ЮГ", "ЗП", "ВС", "КР", "БЕ", "ГЛ", "ВЛ"]
        NameAnalyzer.__m_std_arjse = ["ВЕРХН", "НИЖН", "СРЕДН", "БОЛЬШ"]
        NameAnalyzer.__m_std_arjs_eabbr = ["ВР", "НЖ", "СР", "БЛ"]

NameAnalyzer._static_ctor()