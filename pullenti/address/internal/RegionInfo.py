# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.internal.NameAnalyzer import NameAnalyzer

class RegionInfo:
    
    def __init__(self) -> None:
        self.attrs = AreaAttributes()
        self.names = None;
        self.acronims = list()
        self.capital = None;
        self.cities = list()
        self.districts = list()
        self.region_number = 0
        self.term_cities = None;
    
    def __str__(self) -> str:
        return "{0} ({1}) - {2} ({3}/{4})".format(str(self.attrs), (self.acronims[0] if len(self.acronims) > 0 else "?"), Utils.ifNotNull(self.capital, "?"), len(self.cities), len(self.districts))
    
    def add_city(self, nam : str) -> None:
        nam = nam.replace('ё', 'е')
        if (not nam in self.cities): 
            self.cities.append(nam)
    
    def add_district(self, nam : str) -> None:
        nam = nam.replace('ё', 'е')
        if (not nam in self.districts): 
            self.districts.append(nam)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("reg")
        self.attrs.serialize(xml0_)
        for a in self.acronims: 
            xml0_.write_element_string("acr", a)
        if (self.capital is not None): 
            xml0_.write_element_string("capital", self.capital)
        for c in self.cities: 
            xml0_.write_element_string("city", c)
        for d in self.districts: 
            xml0_.write_element_string("distr", d)
        if (self.region_number > 0): 
            xml0_.write_element_string("num", str(self.region_number))
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "area"): 
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "acr"): 
                self.acronims.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "capital"): 
                self.capital = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "city"): 
                self.cities.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "distr"): 
                self.districts.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "num"): 
                self.region_number = int(Utils.getXmlInnerText(x))
        self.names = NameAnalyzer()
        if (len(self.attrs.types) > 0): 
            self.names.process(self.attrs.names, self.attrs.types[0], (self.attrs.miscs[0] if len(self.attrs.miscs) > 0 else None))
        else: 
            pass
    
    def replace_capital_by_region(self, txt : str) -> str:
        if (self.capital is None): 
            return None
        ii = txt.upper().find(self.capital.upper())
        if (ii < 0): 
            return None
        if (ii > 0 and (ii < 7) and str.upper(txt[0]) == 'Г'): 
            ii += len(self.capital)
        elif (ii == 0): 
            ii += len(self.capital)
            j = ii + 1
            while j < len(txt): 
                if (txt[j] == ','): 
                    break
                elif (txt[j] == ' '): 
                    pass
                elif (txt[j] == 'Г' or txt[j] == 'г'): 
                    ss = txt[j:].upper()
                    if (ss.startswith("ГОРОД")): 
                        ii = (j + 5)
                    elif (ss.startswith("ГОР")): 
                        ii = (j + 3)
                    elif (ss.startswith("Г") and len(ss) > 1 and not str.isalpha(ss[1])): 
                        ii = (j + 1)
                    break
                else: 
                    break
                j += 1
        else: 
            return None
        res = "{0}, {1}".format(str(self.attrs), txt[ii:])
        return res