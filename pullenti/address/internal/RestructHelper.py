# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.address.SearchParams import SearchParams
from pullenti.address.AddressService import AddressService

class RestructHelper:
    
    @staticmethod
    def initialize() -> None:
        pass
    
    __m_moscow = None
    
    @staticmethod
    def __get_moscow() -> 'GarObject':
        if (RestructHelper.__m_moscow is not None): 
            return RestructHelper.__m_moscow
        sp = SearchParams()
        sp.city = "Москва"
        sp.region = 77
        sr = AddressService.search_objects(sp)
        if (len(sr.objects) != 1): 
            return None
        RestructHelper.__m_moscow = sr.objects[0]
        return RestructHelper.__m_moscow
    
    @staticmethod
    def restruct(ah : 'AnalyzeHelper', addr : 'TextAddress', i : int) -> bool:
        if (i == 0): 
            return False
        it0 = addr.items[0]
        if (len(it0.gars) == 0): 
            return False
        reg = it0.gars[0].region_number
        it = addr.items[i]
        it1 = addr.items[i - 1]
        regs = None
        if (reg == 50 and it.level == AddrLevel.CITY and "Юбилейный" in it.attrs.names): 
            txt = "область Московская, городской округ Королёв, город Королёв, микрорайон Юбилейный"
            addr1 = AddressService.process_single_address_text(txt, None)
            if (addr1 is None or addr1.coef != 100): 
                return False
            addr.info_message = "Смена объекта: '{0}' на '{1}'. ".format(str(it), str(addr1.last_item))
            del addr.items[0:0+i + 1]
            if (addr1.items[0].level == AddrLevel.COUNTRY): 
                del addr1.items[0]
            addr.items[0:0] = addr1.items
            return True
        if (reg == 50 and i == 2 and it.level == AddrLevel.STREET): 
            it00 = addr.items[1]
            if (it00.level == AddrLevel.CITY or it00.level == AddrLevel.LOCALITY): 
                mos = RestructHelper.__get_moscow()
                if (mos is None): 
                    return False
                pars = list()
                pars.append(int(mos.id0_[1:]))
                regs = bytearray()
                regs.append(77)
                r = Utils.asObjectOrNull(it00.tag, NameAnalyzer)
                probs = GarHelper.GAR_INDEX._get_string_entries(r, regs, pars, 10)
                if (probs is None or len(probs) != 1): 
                    return False
                pars.clear()
                pars.append(probs[0].id0_)
                probs2 = GarHelper.GAR_INDEX._get_string_entries(Utils.asObjectOrNull(it.tag, NameAnalyzer), regs, pars, 10)
                if (probs2 is None or len(probs2) != 1): 
                    return False
                addr.info_message = "Смена объекта: '{0}' на '{1}'. ".format(str(it0), str(mos))
                addr.items[0] = GarHelper.create_addr_object(mos)
                it00.gars.clear()
                return True
        if (reg == 50 and (((it.level == AddrLevel.CITY or it.level == AddrLevel.LOCALITY or it.level == AddrLevel.SETTLEMENT) or ((it.level == AddrLevel.STREET and i == 1))))): 
            mos = RestructHelper.__get_moscow()
            if (mos is None): 
                return False
            pars = list()
            pars.append(int(mos.id0_[1:]))
            regs = bytearray()
            regs.append(77)
            r = Utils.asObjectOrNull(it.tag, NameAnalyzer)
            probs = GarHelper.GAR_INDEX._get_string_entries(r, regs, pars, 10)
            if (probs is None): 
                return False
            distr = None
            if (it.level != AddrLevel.LOCALITY): 
                if (len(probs) != 1): 
                    return False
            else: 
                if (len(probs) > 10): 
                    return False
                ok = False
                for pr in probs: 
                    for pid in pr.parent_ids: 
                        par = AddressService.get_object("a{0}".format(pid))
                        if (par is None): 
                            continue
                        paa = Utils.asObjectOrNull(par.attrs, AreaAttributes)
                        if (len(paa.names) == 0): 
                            continue
                        nam = paa.names[0]
                        if (len(nam) < 4): 
                            continue
                        ii = 1
                        first_pass3300 = True
                        while True:
                            if first_pass3300: first_pass3300 = False
                            else: ii += 1
                            if (not (ii < i)): break
                            xaa = Utils.asObjectOrNull(addr.items[ii].attrs, AreaAttributes)
                            if (len(xaa.names) == 0): 
                                continue
                            if (xaa.names[0].startswith(nam[0:0+4])): 
                                ok = True
                                break
                            if ("Наро-Фоминский" in xaa.names): 
                                if ("Маруш" in nam): 
                                    ok = True
                        if (ok): 
                            if (len(probs) > 1): 
                                distr = GarHelper.create_addr_object(par)
                            break
                    if (ok): 
                        break
                if (not ok): 
                    return False
            addr.info_message = "Смена объекта: '{0}' на '{1}'. ".format(str(it0), str(mos))
            del addr.items[0:0+i]
            addr.items.insert(0, GarHelper.create_addr_object(mos))
            if (distr is not None): 
                addr.items.insert(1, distr)
            return True
        if ((reg == 72 and i == 1 and it.level == AddrLevel.DISTRICT) and (("Янао" in it.attrs.names or "Югра" in it.attrs.names))): 
            del addr.items[0]
            it.level = AddrLevel.REGIONAREA
            return True
        if (reg == 72 and it.level == AddrLevel.CITY): 
            regs = bytearray()
            regs.append(86)
            regs.append(89)
        elif (reg == 24 and it.level == AddrLevel.CITY): 
            regs = bytearray()
            regs.append(19)
        elif (reg == 23 and it.level == AddrLevel.CITY): 
            regs = bytearray()
            regs.append(1)
        if (reg == 22): 
            regs = bytearray()
            regs.append(4)
        if (reg == 4): 
            regs = bytearray()
            regs.append(22)
        if (regs is not None): 
            r = Utils.asObjectOrNull(it.tag, NameAnalyzer)
            probs = GarHelper.GAR_INDEX._get_string_entries(r, regs, None, 10)
            if (probs is not None): 
                if (((len(probs) == 1)) or ((len(probs) == 2 and probs[0].region == probs[1].region))): 
                    gar_ = AddressService.get_object("a{0}".format(probs[0].id0_))
                    if (gar_ is None): 
                        return False
                    addr.info_message = "Смена объекта: '{0}' на регион {1}. ".format(str(it0), probs[0].region)
                    it.gars.append(gar_)
                    if (len(probs) == 2): 
                        gar_ = AddressService.get_object("a{0}".format(probs[1].id0_))
                        if (gar_ is not None): 
                            it.gars.append(gar_)
                    del addr.items[0:0+i]
                    return True
        return False