# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.address.internal.SearchLevel import SearchLevel
from pullenti.address.AddrLevel import AddrLevel
from pullenti.ner.TextToken import TextToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.address.internal.GarHelper import GarHelper

class AddrSearchFormal:
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.typname is not None): 
            print("{0} ".format(self.typname), end="", file=res, flush=True)
        for w in self.words: 
            print("{0} ".format(w), end="", file=res, flush=True)
        if (self.std_adj is not None): 
            print("{0} ".format(self.std_adj), end="", file=res, flush=True)
        if (self.number is not None): 
            print("{0} ".format(self.number), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def __init__(self, src_ : 'SearchAddressItem') -> None:
        self.src = None;
        self.words = list()
        self.std_adj = None;
        self.number = None;
        self.typname = None;
        self.reg_id = 0
        self.src = src_
        ar = None
        try: 
            ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(src_.text), None, None)
        except Exception as ex103: 
            pass
        if (ar is None): 
            return
        if (GarHelper.GAR_INDEX is None): 
            return
        t = ar.first_token
        first_pass3252 = True
        while True:
            if first_pass3252: first_pass3252 = False
            else: t = t.next0_
            if (not (t is not None)): break
            sit = StreetItemToken.try_parse(t, None, True, None)
            if ((sit is not None and ((sit.typ == StreetItemType.STDADJECTIVE or sit.typ == StreetItemType.STDPARTOFNAME)) and sit.termin is not None) and ((t.previous is not None or t.next0_ is not None))): 
                self.std_adj = NameAnalyzer.correct_adj(sit.termin.canonic_text)
                if (self.std_adj is None): 
                    self.words.append(sit.termin.canonic_text)
                t = sit.end_token
                continue
            if (sit is not None and sit.typ == StreetItemType.NUMBER): 
                self.number = sit.value
                t = sit.end_token
                continue
            if (self.typname is None and ((t != ar.first_token or t.next0_ is not None))): 
                if (sit is not None and sit.typ == StreetItemType.NOUN and self.src.level == SearchLevel.STREET): 
                    self.typname = sit.termin.canonic_text.lower()
                    t = sit.end_token
                    continue
                if (self.src.level == SearchLevel.CITY): 
                    cit = CityItemToken.try_parse(t, None, False, None)
                    if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                        self.typname = cit.value.lower()
                        t = cit.end_token
                        continue
                if (self.src.level == SearchLevel.DISTRICT): 
                    ter = TerrItemToken.try_parse(t, None, None)
                    if (ter is not None and ter.termin_item is not None): 
                        self.typname = ter.termin_item.canonic_text.lower()
                        t = ter.end_token
                        continue
            if ((isinstance(t, TextToken)) and t.length_char > 1): 
                self.words.append(t.term)
        if (len(self.words) > 1 and ((str.isdigit(self.words[0][0]) or len(self.words[0]) == 1))): 
            n = self.words[0]
            del self.words[0]
            self.words.append(n)
        i = 0
        while i < len(self.words): 
            self.words[i] = NameAnalyzer.corr_name(self.words[i])
            if (self.words[i] == "НА" and i > 0 and ((i + 1) < len(self.words))): 
                del self.words[i]
                i -= 1
            i += 1
    
    def check(self, ao : 'AreaObject', lite : bool) -> bool:
        return True
    
    def search(self) -> typing.List['AreaTreeObject']:
        if (len(self.words) == 0): 
            return list()
        res = list()
        if (len(self.words) > 1): 
            vars0_ = list()
            NameAnalyzer.create_search_variants(vars0_, None, None, "{0} {1}".format(self.words[0], self.words[1]), None, False)
            for v in vars0_: 
                res = GarHelper.GAR_INDEX.get_all_string_entries_by_start(v, self.std_adj, self.number, self.src.level == SearchLevel.STREET, self.reg_id)
                if (len(res) > 0): 
                    break
        else: 
            res = GarHelper.GAR_INDEX.get_all_string_entries_by_start(self.words[0], self.std_adj, self.number, self.src.level == SearchLevel.STREET, self.reg_id)
        if (len(self.words) > 1 and len(res) == 0): 
            res2 = GarHelper.GAR_INDEX.get_all_string_entries_by_start(self.words[1], self.std_adj, self.number, self.src.level == SearchLevel.STREET, self.reg_id)
            if (len(res) == 0): 
                res = res2
            elif (len(res2) > 0): 
                hash0_ = dict()
                for r in res2: 
                    if (not r.id0_ in hash0_): 
                        hash0_[r.id0_] = True
                res3 = list()
                for i in range(len(res) - 1, -1, -1):
                    if (res[i].id0_ in hash0_): 
                        res3.append(res[i])
                res = res3
        if (self.typname is not None): 
            for i in range(len(res) - 1, -1, -1):
                r = res[i]
                ok = False
                if (r.typs is not None): 
                    for ty in r.typs: 
                        if (self.typname in ty or ty in self.typname): 
                            ok = True
                            break
                if (not ok): 
                    del res[i]
        if (self.src.ignore_territories): 
            for i in range(len(res) - 1, -1, -1):
                r = res[i]
                if (r.level == AddrLevel.TERRITORY): 
                    del res[i]
        for i in range(len(res) - 1, -1, -1):
            r = res[i]
            if (self.src.level == SearchLevel.DISTRICT): 
                if (r.level == AddrLevel.TERRITORY or r.level == AddrLevel.DISTRICT or r.level == AddrLevel.CITYDISTRICT): 
                    continue
            elif (self.src.level == SearchLevel.CITY): 
                if (r.level == AddrLevel.CITY or r.level == AddrLevel.LOCALITY): 
                    continue
                if (r.level == AddrLevel.REGIONCITY): 
                    continue
            elif (self.src.level == SearchLevel.STREET): 
                if (r.level == AddrLevel.STREET or r.level == AddrLevel.TERRITORY): 
                    continue
            elif (self.src.level == SearchLevel.REGION): 
                if (r.level == AddrLevel.REGIONAREA or r.level == AddrLevel.REGIONCITY): 
                    continue
            else: 
                continue
            del res[i]
        return res