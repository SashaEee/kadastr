# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import xml.etree
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream
from pullenti.unisharp.Xml import XmlWriter
from pullenti.unisharp.Xml import XmlWriterSettings

class AreaType:
    
    class Typs(IntEnum):
        UNDEFINED = 0
        REGION = 1
        CITY = 2
        VILLAGE = 3
        ORG = 4
        STREET = 5
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self) -> None:
        self.name = None;
        self.typ = AreaType.Typs.UNDEFINED
        self.id0_ = 0
        self.count = 0
        self.stat = dict()
    
    def __str__(self) -> str:
        return "{0}: {1}".format(Utils.enumToString(self.typ), self.name)
    
    def calc_typ(self) -> None:
        if (self.name == "территория"): 
            return
        max0_ = 10
        for s in self.stat.items(): 
            if (s[1] > max0_): 
                max0_ = s[1]
                self.typ = s[0]
    
    @staticmethod
    def _save(fname : str, typs : typing.List[tuple], id0__ : str, dt : str) -> None:
        settings = XmlWriterSettings()
        settings.indent = True
        settings.indentChars = (" ")
        settings.encoding = "UTF-8"
        with FileStream(fname, "wb") as f: 
            xml0_ = XmlWriter.create_stream(f, settings)
            xml0_.write_start_document()
            xml0_.write_start_element("types")
            if (id0__ is not None): 
                xml0_.write_attribute_string("guid", id0__)
            if (dt is not None): 
                xml0_.write_attribute_string("date", dt)
            for ty in typs.values(): 
                xml0_.write_start_element("type")
                xml0_.write_attribute_string("id", str(ty.id0_))
                xml0_.write_attribute_string("class", Utils.enumToString(ty.typ))
                xml0_.write_attribute_string("name", Utils.ifNotNull(ty.name, "?"))
                xml0_.write_attribute_string("count", str(ty.count))
                xml0_.write_end_element()
            xml0_.write_end_element()
            xml0_.write_end_document()
            xml0_.close()
    
    @staticmethod
    def _load(fname : str, id0__ : str, dt : str) -> typing.List[tuple]:
        res = dict()
        xdoc = None # new XmlDocument
        with FileStream(fname, "rb") as f: 
            xdoc = Utils.parseXmlFromStream(f)
        for a in xdoc.getroot().attrib.items(): 
            if (Utils.getXmlAttrLocalName(a) == "guid"): 
                id0__.value = a[1]
            elif (Utils.getXmlAttrLocalName(a) == "date"): 
                dt.value = a[1]
        for x in xdoc.getroot(): 
            if (Utils.getXmlLocalName(x) == "type"): 
                ty = AreaType()
                for a in x.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "id"): 
                        n = 0
                        wrapn18 = RefOutArgWrapper(0)
                        inoutres19 = Utils.tryParseInt(a[1], wrapn18)
                        n = wrapn18.value
                        if (inoutres19): 
                            ty.id0_ = n
                    elif (Utils.getXmlAttrLocalName(a) == "name"): 
                        ty.name = a[1]
                    elif (Utils.getXmlAttrLocalName(a) == "count"): 
                        n = 0
                        wrapn20 = RefOutArgWrapper(0)
                        inoutres21 = Utils.tryParseInt(a[1], wrapn20)
                        n = wrapn20.value
                        if (inoutres21): 
                            ty.count = n
                    elif (Utils.getXmlAttrLocalName(a) == "class"): 
                        try: 
                            ty.typ = (Utils.valToEnum(a[1], AreaType.Typs))
                        except Exception as ex22: 
                            pass
                if (ty.id0_ > 0 and not ty.id0_ in res): 
                    res[ty.id0_] = ty
        return res
    
    @staticmethod
    def _new34(_arg1 : int, _arg2 : str) -> 'AreaType':
        res = AreaType()
        res.id0_ = _arg1
        res.name = _arg2
        return res