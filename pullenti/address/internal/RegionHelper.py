# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import xml.etree
import typing
import threading
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.internal.RegionInfo import RegionInfo
from pullenti.ner.core.Termin import Termin
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.ner.core.TerminCollection import TerminCollection

class RegionHelper:
    
    REGIONS = None
    
    REGIONS_BY_CODE = None
    
    CITY_RENAMES = None
    
    __m_lock = None
    
    @staticmethod
    def load_from_file(fname : str) -> None:
        if (not pathlib.Path(fname).is_file()): 
            return
        with RegionHelper.__m_lock: 
            RegionHelper.REGIONS.clear()
            RegionHelper.REGIONS_BY_CODE.clear()
            xml0_ = None # new XmlDocument
            xml0_ = xml.etree.ElementTree.parse(fname)
            for x in xml0_.getroot(): 
                if (Utils.getXmlLocalName(x) == "reg"): 
                    r = RegionInfo()
                    r.deserialize(x)
                    RegionHelper.REGIONS.append(r)
                    if (r.region_number > 0 and not r.region_number in RegionHelper.REGIONS_BY_CODE): 
                        RegionHelper.REGIONS_BY_CODE[r.region_number] = r
            RegionHelper.__init()
    
    @staticmethod
    def __init() -> None:
        RegionHelper.__m_city_regs.clear()
        RegionHelper.__m_adj_regs.clear()
        for r in RegionHelper.REGIONS: 
            r.term_cities = TerminCollection()
            for c in r.cities: 
                city = c.upper()
                if (not city in RegionHelper.__m_city_regs): 
                    RegionHelper.__m_city_regs[city] = r
                r.term_cities.add(Termin(city))
            for d in r.districts: 
                nam = d.upper()
                r.term_cities.add(Termin._new124(nam, d))
            if (r.names is not None and r.names.ref is not None): 
                for s in r.names.ref.slots: 
                    if (s.type_name == "NAME"): 
                        if (not Utils.asObjectOrNull(s.value, str) in RegionHelper.__m_adj_regs): 
                            RegionHelper.__m_adj_regs[Utils.asObjectOrNull(s.value, str)] = r
        RegionHelper.CITY_RENAMES.clear()
        for s in ["ГОРЬКИЙ;Нижний Новгород", "СВЕРДЛОВСК;Екатеринбург", "ОРДЖОНИКИДЗЕ;Владикавказ", "УСТИНОВ;Ижевск", "ВОРОШИЛОВГРАД;Луганск", "ЖДАНОВ;Мариуполь", "БРЕЖНЕВ;Набережные Челны", "АНДРОПОВ;Рыбинск", "КУЙБЫШЕВ;Самара", "ЛЕНИНГРАД;Санкт-Петербург", "ЗАГОРСК;Сергиев Посад", "КАЛИНИН;Тверь", "ЧЕРНЕНКО;Шарыпово", "ЛЕНИНОКАН;Гюмри", "КИРОВАБАД;Гюмжа", "ФРУНЗЕ;Бишкек", "ОКТЕМБЕРЯН;Армавир"]: 
            ii = s.find(';')
            RegionHelper.CITY_RENAMES[s[0:0+ii]] = s[ii + 1:].upper()
    
    __m_city_regs = None
    
    __m_adj_regs = None
    
    @staticmethod
    def is_big_city(nam : str) -> 'RegionInfo':
        if (nam is None): 
            return None
        res = None
        wrapres205 = RefOutArgWrapper(None)
        inoutres206 = Utils.tryGetValue(RegionHelper.__m_city_regs, nam.upper(), wrapres205)
        res = wrapres205.value
        if (inoutres206): 
            return res
        return None
    
    @staticmethod
    def is_big_citya(ao : 'AddrObject') -> 'RegionInfo':
        if (ao.level != AddrLevel.CITY and ao.level != AddrLevel.REGIONCITY): 
            return None
        aa = Utils.asObjectOrNull(ao.attrs, AreaAttributes)
        if (aa is None or len(aa.names) == 0): 
            return None
        if (aa.number is not None): 
            return None
        for n in aa.names: 
            r = RegionHelper.is_big_city(n)
            if (r is not None): 
                return r
        return None
    
    @staticmethod
    def get_regions_by_abbr(abbr : str) -> typing.List['RegionInfo']:
        res = None
        for r in RegionHelper.REGIONS: 
            if (abbr in r.acronims): 
                if (res is None): 
                    res = list()
                res.append(r)
        return res
    
    @staticmethod
    def find_region_by_adj(adj : str) -> 'RegionInfo':
        adj = adj.upper()
        ri = None
        wrapri207 = RefOutArgWrapper(None)
        inoutres208 = Utils.tryGetValue(RegionHelper.__m_adj_regs, adj, wrapri207)
        ri = wrapri207.value
        if (not inoutres208): 
            return None
        return ri
    
    # static constructor for class RegionHelper
    @staticmethod
    def _static_ctor():
        RegionHelper.REGIONS = list()
        RegionHelper.REGIONS_BY_CODE = dict()
        RegionHelper.CITY_RENAMES = dict()
        RegionHelper.__m_lock = threading.Lock()
        RegionHelper.__m_city_regs = dict()
        RegionHelper.__m_adj_regs = dict()

RegionHelper._static_ctor()