# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import math
from pullenti.unisharp.Utils import Utils

from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.address.GarLevel import GarLevel
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.address.internal.RegionHelper import RegionHelper
from pullenti.address.DetailType import DetailType
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.address.AddrLevel import AddrLevel
from pullenti.ner.core.Termin import Termin
from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.ParamType import ParamType
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.AddressService import AddressService
from pullenti.address.internal.GarHelper import GarHelper

class CoefHelper:
    
    @staticmethod
    def calc_coef(ah : 'AnalyzeHelper', res : 'TextAddress', one : bool, txt : str, unknown_names : typing.List[str]) -> 'TextAddress':
        if (one): 
            res.text = txt
        elif (res.end_char > 0 and (res.end_char < len(txt))): 
            res.text = txt[res.begin_char:res.begin_char+(res.end_char + 1) - res.begin_char]
        dcoef = 100
        has_many_gars = False
        other_country = False
        msg = None
        if (res.error_message is not None): 
            if (not res.error_message.startswith("Смена")): 
                dcoef = (90)
            msg = io.StringIO()
            print(res.error_message, end="", file=msg)
        if (res.last_item is None): 
            res.coef = 0
            return res
        j = 0
        first_pass3274 = True
        while True:
            if first_pass3274: first_pass3274 = False
            else: j += 1
            if (not (j < len(res.items))): break
            it = res.items[j]
            no_msg = False
            if (j == 0 and AddressHelper.compare_levels(it.level, AddrLevel.CITY) > 0): 
                dcoef /= (2)
                no_msg = True
                if (msg is None): 
                    msg = io.StringIO()
                print("Первый объект '{0}' слишком низкого уровня ({1}). ".format(str(it), AddressHelper.get_addr_level_string(it.level)), end="", file=msg, flush=True)
            elif (it.level == AddrLevel.UNDEFINED): 
                dcoef /= (2)
                no_msg = True
                if (msg is None): 
                    msg = io.StringIO()
                print("Объект '{0}' имеет непонятный уровень. ".format(str(it)), end="", file=msg, flush=True)
            if ((j + 1) < len(res.items)): 
                if (not it.can_be_parent_for(res.items[j + 1], (res.items[j - 1] if j > 0 else None))): 
                    it1 = res.items[j + 1]
                    if (it.level == AddrLevel.DISTRICT and it1.level == AddrLevel.DISTRICT): 
                        if (len(it1.gars) > 0): 
                            if (msg is None): 
                                msg = io.StringIO()
                            print("Объект '{0}' указан в адресе неправильно. ".format(str(it)), end="", file=msg, flush=True)
                            dcoef *= 0.9
                            del res.items[j]
                            j -= 1
                            continue
                    if (((it.level == AddrLevel.CITY or it.level == AddrLevel.DISTRICT)) and ((it1.level == AddrLevel.DISTRICT or it1.level == AddrLevel.CITYDISTRICT))): 
                        if (len(it1.gars) == 0): 
                            del res.items[j + 1]
                            j -= 1
                            continue
                    if (it.level == AddrLevel.REGIONAREA and it1.level == AddrLevel.LOCALITY and "город" in it1.attrs.types): 
                        it1.level = AddrLevel.CITY
                    elif (it.level == AddrLevel.BUILDING and it1.level == AddrLevel.BUILDING): 
                        pass
                    elif (it.level == AddrLevel.DISTRICT and it1.level == AddrLevel.TERRITORY): 
                        pass
                    elif (it.level == AddrLevel.REGIONAREA and it1.level == AddrLevel.LOCALITY and res.alpha2 != "RU"): 
                        pass
                    else: 
                        dcoef /= (2)
                        no_msg = True
                        if (msg is None): 
                            msg = io.StringIO()
                        print("Объект '{0}' не может быть родителем для '{1}'. ".format(str(it), str(it1)), end="", file=msg, flush=True)
            if (GarHelper.GAR_INDEX is None): 
                continue
            if (it.level == AddrLevel.CITYDISTRICT): 
                continue
            par = (res.items[j - 1] if j > 0 else None)
            if (len(it.gars) == 0): 
                if (j == 0 and it.level == AddrLevel.COUNTRY): 
                    other_country = True
                    if (res.alpha2 is None): 
                        dcoef *= 0.5
                        if (msg is None): 
                            msg = io.StringIO()
                        print("Страна '{0}' неизвестная. ".format(it.to_string_min()), end="", file=msg, flush=True)
                    continue
                if (it.is_reconstructed): 
                    continue
                if (other_country): 
                    continue
                if (((par is not None and len(par.gars) > 0 and it.level == par.level) and it.level != AddrLevel.TERRITORY and it.level != AddrLevel.DISTRICT) and it.level != AddrLevel.BUILDING): 
                    del res.items[j]
                    j -= 1
                    continue
                if (par is not None): 
                    if (len(par.gars) == 0 and par.level != AddrLevel.DISTRICT): 
                        continue
                    if (len(par.gars) > 0 and par.gars[0].expired): 
                        if (it.level != AddrLevel.STREET and it.level != AddrLevel.TERRITORY): 
                            continue
                    if (it.level == AddrLevel.TERRITORY and ((j + 1) < len(res.items)) and len(res.items[j + 1].gars) > 0): 
                        str0_ = str(it)
                        if (str0_.startswith("территория")): 
                            str0_ = str0_[10:].strip()
                        if (not ParamType.ORGANIZATION in res.params): 
                            res.params[ParamType.ORGANIZATION] = str0_
                        del res.items[j]
                        j -= 1
                        continue
                    ha = Utils.asObjectOrNull(it.attrs, HouseAttributes)
                    if (ha is not None and ha.number is not None): 
                        if (ha.number == "б/н"): 
                            continue
                not0_ = False
                if (AddressHelper.compare_levels(it.level, AddrLevel.PLOT) >= 0): 
                    if (par is not None and len(par.gars) == 1 and par.gars[0].children_count == 0): 
                        pass
                    elif (it.level == AddrLevel.APARTMENT): 
                        not0_ = True
                    elif (it.level == AddrLevel.BUILDING or it.level == AddrLevel.PLOT): 
                        not0_ = True
                        if (par is not None and len(par.gars) > 0): 
                            if (par.level == AddrLevel.REGIONCITY): 
                                dcoef *= 0.9
                    else: 
                        dcoef *= 0.9
                        not0_ = True
                elif (AddressHelper.compare_levels(it.level, AddrLevel.TERRITORY) >= 0): 
                    aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
                    if (it.level == AddrLevel.STREET and aa.can_not_has_gar): 
                        pass
                    elif (it.level == AddrLevel.TERRITORY and (("лесничество" in aa.miscs or "месторождение" in aa.miscs or "участок" in aa.miscs))): 
                        pass
                    elif (("дорога" in aa.miscs and j > 0 and res.items[j - 1].level != AddrLevel.CITY) and res.items[j - 1].level != AddrLevel.LOCALITY and res.items[j - 1].level != AddrLevel.REGIONCITY): 
                        pass
                    elif (it.level == AddrLevel.TERRITORY and len(aa.names) == 0): 
                        pass
                    elif ((it.level == AddrLevel.STREET and len(aa.names) == 0 and aa.number is not None) and par is not None and len(par.gars) == 1): 
                        pass
                    elif ((par is not None and ((it.level == AddrLevel.TERRITORY or ((it.level == AddrLevel.STREET and ((par.level == AddrLevel.LOCALITY or par.level == AddrLevel.CITY)))))) and len(par.gars) > 0) and par.gars[0].expired): 
                        pass
                    elif (j > 0 and it.level == AddrLevel.TERRITORY and res.items[j - 1].detail_typ != DetailType.UNDEFINED): 
                        pass
                    elif (((j + 1) < len(res.items)) and res.items[j + 1].level == AddrLevel.TERRITORY and len(res.items[j + 1].gars) > 0): 
                        pass
                    elif (((j + 1) < len(res.items)) and res.items[j + 1].level == AddrLevel.STREET and len(res.items[j + 1].gars) == 1): 
                        pass
                    elif (it.level == AddrLevel.TERRITORY and ((("ВЧ" in aa.miscs or "ПЧ" in aa.miscs or "военный городок" in aa.miscs) or "администрация" in aa.miscs))): 
                        pass
                    elif (par is not None and len(par.gars) > 0 and ((par.level == AddrLevel.TERRITORY or par.level == AddrLevel.LOCALITY))): 
                        ok = par.gars[0].expired
                        if (ok or par.gars[0].children_count == 0): 
                            ok = True
                        elif (((j + 1) < len(res.items)) and len(res.items[j + 1].gars) == 1): 
                            ok = True
                        elif (len(par.gars) == 1): 
                            ok = True
                            chis = AddressService.get_children_objects(par.gars[0].id0_, True)
                            if (chis is not None and len(chis) > 0): 
                                ok = False
                        if (not ok): 
                            dcoef *= 0.8
                    else: 
                        dcoef *= 0.8
                    not0_ = True
                elif (((it.level == AddrLevel.LOCALITY or it.level == AddrLevel.SETTLEMENT)) and par is not None and len(par.gars) == 1): 
                    if (((j + 1) < len(res.items)) and len(res.items[j + 1].gars) > 0 and res.items[j].detail_typ != DetailType.UNDEFINED): 
                        pass
                    elif (((j + 1) < len(res.items)) and len(res.items[j + 1].gars) == 1 and ((res.items[j + 1].level == AddrLevel.LOCALITY or res.items[0].level == AddrLevel.REGIONCITY))): 
                        pass
                    elif (((not ah.create_alts_regime and it.level == AddrLevel.LOCALITY and ((j + 1) < len(res.items))) and len(res.items[j + 1].gars) == 1 and j > 0) and res.items[j - 1].level == AddrLevel.CITY and len(res.items[j - 1].gars) == 1): 
                        pass
                    else: 
                        dcoef *= 0.6
                    not0_ = True
                elif ((j > 0 and it.level == AddrLevel.DISTRICT and ((j + 1) < len(res.items))) and len(res.items[j + 1].gars) > 0): 
                    pass
                elif ((j > 0 and ((j + 1) < len(res.items)) and RegionHelper.is_big_citya(it) is not None) and len(res.items[j + 1].gars) > 0): 
                    del res.items[j]
                    j -= 1
                    continue
                elif (len(res.items) == 1): 
                    dcoef *= 0.2
                    not0_ = True
                else: 
                    dcoef *= 0.6
                    not0_ = True
                if (not0_ and not no_msg): 
                    if (msg is None): 
                        msg = io.StringIO()
                    print("Объект '{0}' не привязался к ГАР. ".format(str(it)), end="", file=msg, flush=True)
                continue
            elif (len(it.gars) > 5): 
                if (msg is None): 
                    msg = io.StringIO()
                print("К объекту '{0}' привязались {1} элементов ГАР. ".format(str(it), len(it.gars)), end="", file=msg, flush=True)
                dcoef *= 0.8
            if ((j + 1) < len(res.items)): 
                it1 = res.items[j + 1]
                if (len(it1.gars) > 0 and (isinstance(it.attrs, AreaAttributes)) and (isinstance(it1.attrs, AreaAttributes))): 
                    aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
                    aa1 = Utils.asObjectOrNull(it1.attrs, AreaAttributes)
                    ok = False
                    for g in it1.gars: 
                        if (it._find_gar_by_ids(g.parent_ids) is not None): 
                            ok = True
                        elif (len(g.parent_ids) > 0): 
                            for pid in g.parent_ids: 
                                pp = ah.get_gar_object(pid)
                                if (pp is not None): 
                                    if (it._find_gar_by_ids(pp.parent_ids) is not None): 
                                        ok = True
                    if (not ok and it.level == AddrLevel.DISTRICT and it1.level == AddrLevel.CITY): 
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
                    if (not ok and ((it.level == AddrLevel.DISTRICT or (((isinstance(it.tag, NameAnalyzer)) and it.tag.level == AddrLevel.DISTRICT)))) and ((it1.level == AddrLevel.STREET or it1.level == AddrLevel.CITY))): 
                        del res.items[j]
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
                    if (not ok and it.level == AddrLevel.LOCALITY and ((it1.level == AddrLevel.TERRITORY or it1.level == AddrLevel.STREET))): 
                        for g in it1.gars: 
                            p = ah.get_gar_object((g.parent_ids[0] if len(g.parent_ids) > 0 else None))
                            if (p is not None and it._find_gar_by_ids(p.parent_ids) is not None): 
                                ok = True
                                break
                    if (not ok and it.level == AddrLevel.TERRITORY and it1.level == AddrLevel.STREET): 
                        ok = True
                    if (not ok and it.level == AddrLevel.LOCALITY and it1.level == AddrLevel.LOCALITY): 
                        if (len(it.gars) > 0 and it1.find_gar_by_id(it.gars[0].id0_) is not None): 
                            ok = True
                    if (not ok and len(it1.gars) > 1): 
                        ok = True
                    elif ((not ok and len(it1.gars) == 1 and len(it.gars) > 0) and it.gars[0].expired): 
                        ok = True
                    elif (it.detail_typ != DetailType.UNDEFINED): 
                        ok = True
                    elif (it.level == it1.level and it.level == AddrLevel.LOCALITY and res.additional_items is None): 
                        kk = 0
                        kk = (j + 1)
                        while kk < len(res.items): 
                            if (res.items[kk].level != AddrLevel.LOCALITY): 
                                break
                            kk += 1
                        if (kk >= len(res.items)): 
                            ok = True
                            res.additional_items = list()
                            kk = (j + 1)
                            while kk < len(res.items): 
                                res.additional_items.append(res.items[kk])
                                kk += 1
                            del res.items[j + 1:j + 1+len(res.items) - j - 1]
                    if (not ok): 
                        if ((it.level == AddrLevel.DISTRICT and j == 1 and ((res.items[0].level == AddrLevel.REGIONAREA or res.items[0].level == AddrLevel.REGIONCITY))) and len(it1.gars) > 0 and (((it1.level == AddrLevel.CITY or it1.level == AddrLevel.DISTRICT or it1.level == AddrLevel.SETTLEMENT) or ((it1.level == AddrLevel.LOCALITY and len(it1.gars) == 1))))): 
                            pass
                        elif (((it.level == AddrLevel.TERRITORY or it.level == AddrLevel.LOCALITY)) and it1.level == AddrLevel.TERRITORY): 
                            pass
                        else: 
                            dcoef *= 0.9
                            if (not no_msg): 
                                if (msg is None): 
                                    msg = io.StringIO()
                                print("Похоже, объект '{0}' указан в адресе неправильно. ".format(str(it)), end="", file=msg, flush=True)
            if (it.level == AddrLevel.TERRITORY and it.gars[0].level == GarLevel.STREET): 
                if ((j + 1) == len(res.items) or AddressHelper.compare_levels(res.items[j + 1].level, AddrLevel.STREET) > 0): 
                    it.level = AddrLevel.STREET
            if (it.level == AddrLevel.STREET and it.cross_object is not None and len(it.cross_object.gars) == 0): 
                if (((j + 1) < len(res.items)) and res.items[j + 1].cross_object is not None): 
                    pass
                else: 
                    it.cross_object = (None)
            if (len(it.gars) == 1 or it.gars[1].expired): 
                continue
            if (AddressHelper.compare_levels(it.level, AddrLevel.BUILDING) >= 0): 
                continue
            pars = list()
            has_par = False
            for pid in it.gars[0].parent_ids: 
                kk = 0
                kk = 1
                while kk < len(it.gars): 
                    if (not pid in it.gars[kk].parent_ids): 
                        break
                    kk += 1
                if (kk >= len(it.gars)): 
                    has_par = True
                    break
            if (not has_par): 
                for g in it.gars: 
                    id0_ = (g.parent_ids[0] if len(g.parent_ids) > 0 else None)
                    if (len(g.parent_ids) > 1 and j > 0 and res.items[j - 1].find_gar_by_id(g.parent_ids[1]) is not None): 
                        id0_ = g.parent_ids[1]
                    if (id0_ is not None and not id0_ in pars): 
                        pars.append(id0_)
            co = 1 / (((1 if len(pars) == 0 else len(pars))))
            if (len(pars) > 1): 
                if (len(pars) == 2): 
                    co = 0.9
                elif (len(pars) == 3): 
                    co = 0.8
                else: 
                    co = 0.7
                nams = list()
                pars2 = list()
                for p in pars: 
                    oo = None
                    if (par is not None): 
                        oo = par.find_gar_by_id(p)
                    if (oo is None): 
                        oo = ah.get_gar_object(p)
                    if (oo is None): 
                        continue
                    ss = str(oo).upper()
                    if (ss.find('Ё') >= 0): 
                        ss = ss.replace('Ё', 'Е')
                    if (not ss in nams): 
                        nams.append(ss)
                    pp = (oo.parent_ids[0] if len(oo.parent_ids) > 0 else "")
                    if (not pp in pars2): 
                        pars2.append(pp)
                    if (len(nams) > 1 or len(pars2) > 1): 
                        break
                if (len(nams) == 1 and len(pars2) == 1): 
                    co = (1)
                else: 
                    if (msg is None): 
                        msg = io.StringIO()
                    print("К объекту '{0}' привязались {1} разные объекта ГАР. ".format(str(it), len(it.gars)), end="", file=msg, flush=True)
                    if (it.level == AddrLevel.CITY): 
                        co = 0.7
                    if (has_many_gars): 
                        co = (1)
                    has_many_gars = True
            dcoef *= co
        if (res.additional_items is not None): 
            li = list()
            for ai in res.additional_items: 
                if (len(ai.gars) == 0): 
                    li.append(ai)
            if (len(li) > 0): 
                if (msg is None): 
                    msg = io.StringIO()
                if (len(li) == 1): 
                    print("Объект '{0}' не привязался к ГАР. ".format(str(li[0])), end="", file=msg, flush=True)
                else: 
                    print("Объекты ".format(), end="", file=msg, flush=True)
                    for o in li: 
                        if (o != li[0]): 
                            print(", ", end="", file=msg)
                        print("'{0}'".format(str(o)), end="", file=msg, flush=True)
                    print(" не привязались к ГАР. ", end="", file=msg)
        j = 0
        first_pass3275 = True
        while True:
            if first_pass3275: first_pass3275 = False
            else: j += 1
            if (not (j < (len(res.items) - 1))): break
            it = res.items[j]
            if (it.level != AddrLevel.DISTRICT or res.items[j + 1].level != AddrLevel.CITY): 
                continue
            aa = Utils.asObjectOrNull(it.attrs, AreaAttributes)
            is_city_distr = False
            if (len(it.gars) == 0): 
                if ("район" in aa.types): 
                    is_city_distr = True
            else: 
                ga = Utils.asObjectOrNull(it.gars[0].attrs, AreaAttributes)
                if (len(ga.types) > 0 and "внутригородск" in ga.types[0]): 
                    is_city_distr = True
            if (is_city_distr): 
                it.level = AddrLevel.CITYDISTRICT
                del res.items[j]
                res.items.insert(j + 1, it)
            break
        j = 0
        while j < len(res.items): 
            it = res.items[j]
            if (it.detail_typ == DetailType.NEAR and it.detail_param is None): 
                it.detail_typ = DetailType.UNDEFINED
            j += 1
        total_char = 0
        not_char = 0
        max0_ = (0 if txt is None else len(txt))
        i = 0
        if (one and txt is not None): 
            if (res.begin_char > 0): 
                sub = txt[0:0+res.begin_char].strip().upper()
                if (sub.endswith(",")): 
                    sub = sub[0:0+len(sub) - 1].strip()
                rest = txt[res.begin_char:]
                if (sub in rest.upper()): 
                    res.begin_char = 0
                elif (sub in str(res).upper()): 
                    res.begin_char = 0
                elif (dcoef == 100): 
                    res.begin_char = 0
            i = txt.find("дом,корпус,кв.")
            if (((i)) > 0): 
                max0_ = i
            i = txt.find("ТП-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("РП-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("ВЛ-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("КЛ-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("КТПН-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("NULL")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            for i in range(max0_ - 1, 0, -1):
                if ((Utils.isWhitespace(txt[i]) or txt[i] == ',' or txt[i] == '-') or txt[i] == '.'): 
                    max0_ = i
                else: 
                    break
            else: i = 0
            i = 0
            first_pass3276 = True
            while True:
                if first_pass3276: first_pass3276 = False
                else: i += 1
                if (not (i < max0_)): break
                if (CoefHelper.__starts_with(txt, i, "РФ")): 
                    i += 2
                    continue
                if (CoefHelper.__starts_with(txt, i, "NULL")): 
                    i += 4
                    continue
                if (CoefHelper.__starts_with(txt, i, "РОССИЯ")): 
                    i += 6
                    continue
                if (CoefHelper.__starts_with(txt, i, "Г ")): 
                    i += 2
                    continue
                if (CoefHelper.__starts_with(txt, i, "Г.")): 
                    i += 2
                    continue
                if (str.isalpha(txt[i])): 
                    break
            i0 = i
            if (max0_ > 10 and txt[max0_ - 1] == '0'): 
                for ii in range(max0_ - 2, 0, -1):
                    if (str.isalnum(txt[ii])): 
                        break
                    elif (txt[ii] == ' ' or txt[ii] == ','): 
                        max0_ = ii
                        break
            if (max0_ > 10): 
                ii = max0_ - 1
                while ii > 4: 
                    if (str.upper(txt[ii]) == 'Т' and str.upper(txt[ii - 1]) == 'Е' and str.upper(txt[ii - 2]) == 'Н'): 
                        max0_ = (ii - 2)
                        ii -= 3
                    elif ((str.upper(txt[ii]) == 'П' and str.upper(txt[ii - 1]) == 'Р' and str.upper(txt[ii - 2]) == 'О') and str.upper(txt[ii - 2]) == 'К'): 
                        max0_ = (ii - 3)
                        ii -= 4
                    elif (str.upper(txt[ii]) == 'Р' and str.upper(txt[ii - 1]) == 'О' and str.upper(txt[ii - 2]) == 'К'): 
                        max0_ = (ii - 2)
                        ii -= 3
                    elif (str.upper(txt[ii]) == 'В' and str.upper(txt[ii - 1]) == 'К'): 
                        max0_ = (ii - 1)
                        ii -= 2
                    elif (str.upper(txt[ii]) == 'Л' and str.upper(txt[ii - 1]) == 'У' and not str.isalpha(txt[ii - 2])): 
                        max0_ = (ii - 1)
                        ii -= 2
                    elif (((txt[ii] == ' ' or txt[ii] == '.' or txt[ii] == ';') or txt[ii] == ',' or txt[ii] == '-') or txt[ii] == '\\' or txt[ii] == '/'): 
                        max0_ = ii
                    elif (txt[ii] == '0' and not str.isalnum(txt[ii - 1])): 
                        max0_ = ii
                    elif (str.upper(txt[ii]) == 'Д' and not str.isalnum(txt[ii - 1])): 
                        max0_ = ii
                    else: 
                        break
                    ii -= 1
            if ((res.end_char + 1) < max0_): 
                fff = txt[res.end_char + 1:res.end_char + 1+max0_ - res.end_char - 1].strip()
                aa = None
                if (res.last_item is not None): 
                    aa = (Utils.asObjectOrNull(res.last_item.attrs, AreaAttributes))
                if (aa is not None and len(aa.types) > 0 and Utils.startsWithString(aa.types[0], fff, True)): 
                    res.end_char = (max0_ - 1)
            while i < max0_: 
                if (str.isalnum(txt[i])): 
                    total_char += 1
                    if ((i < res.begin_char) or i > res.end_char): 
                        not_char += 1
                i += 1
            not_change_coef = False
            if (((res.end_char + 1) < max0_) and res.error_message is None): 
                if (msg is None): 
                    msg = io.StringIO()
                if (i0 < res.begin_char): 
                    print("Непонятные фрагменты: '{0}' и '{1}'. ".format(txt[i0:i0+res.begin_char - i0].strip(), txt[res.end_char + 1:res.end_char + 1+max0_ - res.end_char - 1].strip()), end="", file=msg, flush=True)
                else: 
                    ppp = txt[res.end_char + 1:res.end_char + 1+max0_ - res.end_char - 1].strip()
                    if (ppp.startswith(",")): 
                        ppp = ppp[1:].strip()
                    if (Utils.isNullOrEmpty(ppp)): 
                        not_change_coef = True
                    elif (Utils.startsWithString(ppp, "номер учетной", True)): 
                        not_change_coef = True
                    else: 
                        print("Непонятный фрагмент: '{0}'. ".format(ppp), end="", file=msg, flush=True)
                        if (ppp[0] == '/' or ppp[0] == '\\'): 
                            ppp = ppp[1:].strip()
                        if (Utils.startsWithString(ppp, "ММ", True) or Utils.startsWithString(ppp, "MM", True)): 
                            not_change_coef = True
            elif (i0 < res.begin_char): 
                if (msg is None): 
                    msg = io.StringIO()
                print("Непонятный фрагмент: '{0}'. ".format(txt[i0:i0+res.begin_char - i0].strip()), end="", file=msg, flush=True)
            if (total_char > 0 and not_char > 0 and not not_change_coef): 
                if ((not_char < 4) and AddressHelper.compare_levels(res.last_item.level, AddrLevel.PLOT) >= 0): 
                    pass
                else: 
                    dcoef *= (((total_char - not_char)) / (total_char))
        if (unknown_names is not None and len(unknown_names) > 0): 
            all0_ = str(res).upper()
            for k in range(len(unknown_names) - 1, -1, -1):
                if (unknown_names[k].upper() in all0_): 
                    del unknown_names[k]
            if (len(unknown_names) > 0): 
                alls = dict()
                for it in res.items: 
                    if (isinstance(it.attrs, AreaAttributes)): 
                        for g in it.gars: 
                            if (not g.id0_ in alls): 
                                alls[g.id0_] = g
                while True:
                    cou0 = len(alls)
                    gos = list(alls.values())
                    for g in gos: 
                        for id0_ in g.parent_ids: 
                            if (not id0_ in alls): 
                                gg = ah.get_gar_object(id0_)
                                if (gg is not None): 
                                    alls[gg.id0_] = gg
                    if (len(alls) <= cou0): 
                        break
                terms = TerminCollection()
                for n in unknown_names: 
                    terms.add(Termin._new124(n, n))
                for g in alls.values(): 
                    if (len(unknown_names) == 0): 
                        break
                    aa = Utils.asObjectOrNull(g.attrs, AreaAttributes)
                    if (len(aa.names) == 0): 
                        continue
                    ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(aa.names[0]), None, None)
                    tt = None
                    t = ar.first_token
                    while t is not None: 
                        tt = terms.try_parse(t, TerminParseAttr.NO)
                        if ((tt) is not None): 
                            n = Utils.asObjectOrNull(tt.termin.tag, str)
                            if (n in unknown_names): 
                                unknown_names.remove(n)
                        t = t.next0_
            if (len(unknown_names) > 0): 
                if (dcoef == 100 and len(unknown_names) == 1 and Utils.startsWithString(res.text, unknown_names[0], True)): 
                    if (res.find_item_by_level(AddrLevel.CITY) is not None or res.find_item_by_level(AddrLevel.LOCALITY) is not None): 
                        pass
                    else: 
                        dcoef *= 0.8
                elif ((dcoef == 100 and len(unknown_names) == 1 and ((res.find_item_by_level(AddrLevel.CITY) is not None or res.find_item_by_level(AddrLevel.REGIONCITY) is not None))) and res.find_item_by_level(AddrLevel.STREET) is not None and len(res.find_item_by_level(AddrLevel.STREET).gars) == 1): 
                    pass
                else: 
                    dcoef *= 0.8
                if (msg is None): 
                    msg = io.StringIO()
                if (len(unknown_names) == 1): 
                    print("Непонятный объект: '{0}'".format(unknown_names[0]), end="", file=msg, flush=True)
                else: 
                    print("Непонятные объекты: '{0}'".format(unknown_names[0]), end="", file=msg, flush=True)
                k = 1
                while k < len(unknown_names): 
                    print(", '{0}'".format(unknown_names[k]), end="", file=msg, flush=True)
                    k += 1
                print(". ", end="", file=msg)
        res.coef = (math.floor(dcoef))
        if (msg is not None): 
            res.error_message = Utils.toStringStringIO(msg).strip()
        return res
    
    @staticmethod
    def __starts_with(txt : str, i : int, sub : str) -> bool:
        j = 0
        while j < len(sub): 
            if ((i + j) >= len(txt)): 
                return False
            if (str.upper(txt[i + j]) != str.upper(sub[j])): 
                return False
            j += 1
        return True