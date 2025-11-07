# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import typing
import threading
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Misc import WebClient
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.GarParam import GarParam
from pullenti.address.AddressDbRecord import AddressDbRecord
from pullenti.address.GarObject import GarObject
from pullenti.address.SearchResult import SearchResult
from pullenti.address.ProcessTextParams import ProcessTextParams
from pullenti.address.GarStatistic import GarStatistic
from pullenti.address.TextAddress import TextAddress
from pullenti.address.AddressService import AddressService

class ServerHelper:
    """ Поддержка работы с сервером напрямую (лучше не использовать,
    а работать через функции класса AddressService, установив адрес через SetServerConnection). """
    
    __m_lock = None
    
    @staticmethod
    def get_server_version(address_ : str) -> str:
        if (address_ is None): 
            address_ = ServerHelper.SERVER_URI
        try: 
            with ServerHelper.__m_lock: 
                web = WebClient()
                res = web.download_data(Utils.ifNotNull(address_, "http://localhost:2222"))
                if (res is None or len(res) == 0): 
                    return None
                return res.decode("UTF-8", 'ignore')
        except Exception as ex: 
            return None
    
    SERVER_URI = None
    
    @staticmethod
    def get_gar_statistic() -> 'GarStatistic':
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetGarStatistic")
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 10): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = GarStatistic()
            res.deserialize(xml0_.getroot())
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def __get_dat_from_xml(tmp : io.StringIO) -> bytearray:
        i = 10
        while (i < (tmp.tell() - 4)) and (i < 100): 
            if ((Utils.getCharAtStringIO(tmp, i) == '-' and Utils.getCharAtStringIO(tmp, i + 1) == '1' and Utils.getCharAtStringIO(tmp, i + 2) == '6') and Utils.getCharAtStringIO(tmp, i + 3) == '\"'): 
                Utils.setCharAtStringIO(tmp, i + 1, '8')
                Utils.removeStringIO(tmp, i + 2, 1)
                break
            i += 1
        return Utils.toStringStringIO(tmp).encode("UTF-8", 'ignore')
    
    @staticmethod
    def __out_pars(xml0_ : XmlWriter, pars : 'ProcessTextParams') -> None:
        if (len(pars.default_regions) > 0): 
            val = str(pars.default_regions[0])
            i = 1
            while i < len(pars.default_regions): 
                val = "{0} {1}".format(val, pars.default_regions)
                i += 1
            xml0_.write_attribute_string("regs", val)
        if (pars.default_object is not None): 
            xml0_.write_attribute_string("defobj", pars.default_object.id0_)
        if (pars.is_plot): 
            xml0_.write_attribute_string("plot", "true")
        if (pars.strict_house_number): 
            xml0_.write_attribute_string("stricthousenumber", "true")
        if (pars.no_flats): 
            xml0_.write_attribute_string("noflats", "true")
        if (pars.dont_correct_text): 
            xml0_.write_attribute_string("dontcorrect", "true")
    
    @staticmethod
    def _parse_params(xml0_ : xml.etree.ElementTree.Element) -> 'ProcessTextParams':
        res = None
        if (xml0_.attrib is not None): 
            for x in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(x) == "regs"): 
                    if (res is None): 
                        res = ProcessTextParams()
                    for v in Utils.splitString(x[1], ' ', False): 
                        n = 0
                        wrapn228 = RefOutArgWrapper(0)
                        inoutres229 = Utils.tryParseInt(v, wrapn228)
                        n = wrapn228.value
                        if (inoutres229): 
                            res.default_regions.append(n)
                elif (Utils.getXmlAttrLocalName(x) == "defobj"): 
                    if (res is None): 
                        res = ProcessTextParams()
                    res.default_object = AddressService.get_object(x[1])
                elif (Utils.getXmlAttrLocalName(x) == "plot" and x[1] == "true"): 
                    if (res is None): 
                        res = ProcessTextParams()
                    res.is_plot = True
                elif (Utils.getXmlAttrLocalName(x) == "stricthousenumber" and x[1] == "true"): 
                    if (res is None): 
                        res = ProcessTextParams()
                    res.strict_house_number = True
                elif (Utils.getXmlAttrLocalName(x) == "dontcorrect" and x[1] == "true"): 
                    if (res is None): 
                        res = ProcessTextParams()
                    res.dont_correct_text = True
                elif (Utils.getXmlAttrLocalName(x) == "noflats" and x[1] == "true"): 
                    if (res is None): 
                        res = ProcessTextParams()
                    res.no_flats = True
        return res
    
    @staticmethod
    def create_process_text_data(txt : str, pars : 'ProcessTextParams') -> bytearray:
        """ Подготовить данные функции ProcessText для отправки на сервер
        
        Args:
            txt(str): обрабатываемый текст функцией ProcessText
            pars(ProcessTextParams): параметры обработки (может быть null)
        
        Returns:
            bytearray: байтовый массив, который нужно отправить как контент post-запроса
        """
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("ProcessText")
            if (pars is not None): 
                ServerHelper.__out_pars(wxml, pars)
            wxml.write_string(Utils.ifNotNull(txt, ""))
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        return dat
    
    @staticmethod
    def create_process_text_result(server_response : bytearray) -> typing.List['TextAddress']:
        """ Оформить объектами результат выполнения на сервере функции ProcessText
        
        Args:
            server_response(bytearray): ответ от сервера как байтовый массив
        
        Returns:
            typing.List[TextAddress]: список найденных адресов
        """
        xml0_ = None # new XmlDocument
        rstr = server_response.decode("UTF-8", 'ignore')
        xml0_ = Utils.parseXmlFromString(rstr)
        res = list()
        for x in xml0_.getroot(): 
            if (len(x) == 0): 
                continue
            to = TextAddress()
            to.deserialize(x)
            res.append(to)
        return res
    
    @staticmethod
    def process_text(txt : str, pars : 'ProcessTextParams') -> typing.List['TextAddress']:
        dat = ServerHelper.create_process_text_data(txt, pars)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            return ServerHelper.create_process_text_result(dat1)
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_texts(txts : typing.List[str], pars : 'ProcessTextParams') -> typing.List['TextAddress']:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("ProcessSingleAddressTexts")
            if (pars is not None): 
                ServerHelper.__out_pars(wxml, pars)
                if (pars.prev_address is not None): 
                    pars.prev_address.serialize(wxml, "prev")
            for txt in txts: 
                wxml.write_element_string("text", txt)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 5): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = list()
            for x in xml0_.getroot(): 
                if (len(x) == 0): 
                    continue
                r = TextAddress()
                r.deserialize(x)
                res.append(r)
            if (len(res) != len(txts)): 
                return None
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_texts_records(txts : typing.List[str], pars : 'ProcessTextParams'=None) -> typing.List['AddressDbRecord']:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("ProcessSingleAddressTextsRecords")
            if (pars is not None): 
                ServerHelper.__out_pars(wxml, pars)
                if (pars.prev_address is not None): 
                    pars.prev_address.serialize(wxml, "prev")
            for txt in txts: 
                wxml.write_element_string("text", Utils.ifNotNull(txt, ""))
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 5): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = list()
            for x in xml0_.getroot(): 
                if (len(x) == 0): 
                    res.append(None)
                    continue
                r = AddressDbRecord()
                r.deserialize(x)
                res.append(r)
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def create_process_single_address_text_data(txt : str, pars : 'ProcessTextParams') -> bytearray:
        """ Подготовить данные функции ProcessSingleAddressText для отправки на сервер
        
        Args:
            txt(str): обрабатываемый текст функцией ProcessSingleAddressText
            pars(ProcessTextParams): параметры обработки (может быть null)
        
        Returns:
            bytearray: байтовый массив, который нужно отправить как контент post-запроса
        """
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("ProcessSingleAddressText")
            if (pars is not None): 
                ServerHelper.__out_pars(wxml, pars)
                if (pars.prev_address is not None): 
                    pars.prev_address.serialize(wxml, "prev")
            wxml.write_string(Utils.ifNotNull(txt, ""))
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        return dat
    
    @staticmethod
    def create_process_single_address_text_result(server_response : bytearray) -> 'TextAddress':
        """ Оформить экземпляром TextAddress результат выполнения на сервере функции ProcessSingleAddressText
        
        Args:
            server_response(bytearray): ответ от сервера как байтовый массив
        
        Returns:
            TextAddress: экземпляр TextAddress
        """
        xml0_ = None # new XmlDocument
        rstr = server_response.decode("UTF-8", 'ignore')
        if (len(rstr) < 5): 
            return None
        xml0_ = Utils.parseXmlFromString(rstr)
        res = TextAddress()
        res.deserialize(xml0_.getroot())
        return res
    
    @staticmethod
    def process_single_address_text(txt : str, pars : 'ProcessTextParams') -> 'TextAddress':
        """ Обработать один адрес через сервер
        
        Args:
            txt(str): текст адреса
            pars(ProcessTextParams): параметры
        
        Returns:
            TextAddress: результат обработки
        """
        dat = ServerHelper.create_process_single_address_text_data(txt, pars)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            return ServerHelper.create_process_single_address_text_result(dat1)
        except Exception as ex: 
            return None
    
    @staticmethod
    def search_objects(search_pars : 'SearchParams') -> 'SearchResult':
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("SearchObjects")
            search_pars.serialize(wxml)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 5): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = SearchResult()
            res.deserialize(xml0_.getroot())
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_children_objects(id0_ : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetObjects")
            if (ignore_houses): 
                wxml.write_attribute_string("ignoreHouses", "true")
            if (id0_ is not None): 
                wxml.write_string(id0_)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            xml0_ = Utils.parseXmlFromString(rstr)
            res = list()
            if (len(rstr) < 10): 
                return res
            for x in xml0_.getroot(): 
                go = GarObject(None)
                go.deserialize(x)
                if (go.attrs is not None): 
                    res.append(go)
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_object(obj_id : str) -> 'GarObject':
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetObject")
            wxml.write_string(obj_id)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 10): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = GarObject(None)
            res.deserialize(xml0_.getroot())
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_object_params(sid : str) -> typing.List[tuple]:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetObjectParams")
            wxml.write_string(sid)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = [ ]
            with ServerHelper.__m_lock: 
                dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 10): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = dict()
            for x in xml0_.getroot(): 
                try: 
                    ty = Utils.valToEnum(Utils.getXmlLocalName(x), GarParam)
                    if (ty != GarParam.UNDEFINED): 
                        res[ty] = Utils.getXmlInnerText(x)
                except Exception as ex230: 
                    pass
            return res
        except Exception as ex: 
            return None
    
    # static constructor for class ServerHelper
    @staticmethod
    def _static_ctor():
        ServerHelper.__m_lock = threading.Lock()

ServerHelper._static_ctor()