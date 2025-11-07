# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import Stopwatch

from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.internal.PullentiAddressInternalResourceHelper import PullentiAddressInternalResourceHelper
from pullenti.address.SqlAddressHelper import SqlAddressHelper
from pullenti.ner.named.NamedEntityAnalyzer import NamedEntityAnalyzer
from pullenti.address.internal.CorrectionHelper import CorrectionHelper
from pullenti.address.ImageWrapper import ImageWrapper
from pullenti.address.AddressDbRecord import AddressDbRecord
from pullenti.address.internal.RegionHelper import RegionHelper
from pullenti.address.TextAddress import TextAddress
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.address.GarStatistic import GarStatistic
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.uri.UriAnalyzer import UriAnalyzer
from pullenti.ner.money.MoneyAnalyzer import MoneyAnalyzer
from pullenti.ner.phone.PhoneAnalyzer import PhoneAnalyzer
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.geo.internal.INameChecker import INameChecker
from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer

class AddressService:
    """ Сервис работы с адресами
    
    """
    
    VERSION = "4.31"
    """ Текущая версия """
    
    VERSION_DATE = "2025.08.24"
    """ Дата создания текущей версии """
    
    @staticmethod
    def initialize() -> None:
        """ Инициализация движка - необходимо вызывать один раз в начале работы. """
        from pullenti.address.internal.GarHelper import GarHelper
        from pullenti.address.internal.NameChecker import NameChecker
        from pullenti.address.internal.AnalyzeHelper import AnalyzeHelper
        if (AddressService.__m_inited): 
            return
        AddressService.__m_inited = True
        ProcessorService.initialize(None)
        MoneyAnalyzer.initialize()
        UriAnalyzer.initialize()
        PhoneAnalyzer.initialize()
        DateAnalyzer.initialize()
        GeoAnalyzer.initialize()
        MiscLocationHelper.NAME_CHECKER = (NameChecker())
        AddressAnalyzer.initialize()
        OrganizationAnalyzer.initialize()
        PersonAnalyzer.initialize()
        NamedEntityAnalyzer.initialize()
        AnalyzeHelper.init()
        GarHelper.init(None)
        CorrectionHelper.initialize0()
        SqlAddressHelper.initialize()
        AddressHelper.IMAGES.append(ImageWrapper("country", PullentiAddressInternalResourceHelper.get_bytes("country.png")))
        AddressHelper.IMAGES.append(ImageWrapper("region", PullentiAddressInternalResourceHelper.get_bytes("region.png")))
        AddressHelper.IMAGES.append(ImageWrapper("admin", PullentiAddressInternalResourceHelper.get_bytes("admin.png")))
        AddressHelper.IMAGES.append(ImageWrapper("municipal", PullentiAddressInternalResourceHelper.get_bytes("municipal.png")))
        AddressHelper.IMAGES.append(ImageWrapper("settlement", PullentiAddressInternalResourceHelper.get_bytes("settlement.png")))
        AddressHelper.IMAGES.append(ImageWrapper("city", PullentiAddressInternalResourceHelper.get_bytes("city.png")))
        AddressHelper.IMAGES.append(ImageWrapper("locality", PullentiAddressInternalResourceHelper.get_bytes("locality.png")))
        AddressHelper.IMAGES.append(ImageWrapper("district", PullentiAddressInternalResourceHelper.get_bytes("district.png")))
        AddressHelper.IMAGES.append(ImageWrapper("area", PullentiAddressInternalResourceHelper.get_bytes("area.png")))
        AddressHelper.IMAGES.append(ImageWrapper("street", PullentiAddressInternalResourceHelper.get_bytes("street.png")))
        AddressHelper.IMAGES.append(ImageWrapper("plot", PullentiAddressInternalResourceHelper.get_bytes("plot.png")))
        AddressHelper.IMAGES.append(ImageWrapper("building", PullentiAddressInternalResourceHelper.get_bytes("building.png")))
        AddressHelper.IMAGES.append(ImageWrapper("room", PullentiAddressInternalResourceHelper.get_bytes("room.png")))
        AddressHelper.IMAGES.append(ImageWrapper("carplace", PullentiAddressInternalResourceHelper.get_bytes("carplace.png")))
    
    __m_inited = False
    
    @staticmethod
    def set_gar_index_path(gar_path : str) -> None:
        """ Указание директории с индексом ГАР (если не задать, то выделяемые объекты привязываться не будут)
        
        Args:
            gar_path(str): папка с индексом ГАР
        """
        from pullenti.address.internal.ServerHelper import ServerHelper
        from pullenti.address.internal.GarHelper import GarHelper
        if (gar_path is not None): 
            ref_file = pathlib.PurePath(gar_path).joinpath("ref.txt")
            if (pathlib.Path(ref_file).is_file()): 
                real_path = pathlib.Path(ref_file).read_bytes().decode("UTF-8", 'ignore')
                if (not pathlib.Path(Utils.ifNotNull(real_path, "?")).is_dir()): 
                    raise Utils.newException("Gar path '{0}' not exists".format(real_path), None)
                if (Utils.compareStrings(real_path, gar_path, True) != 0): 
                    AddressService.set_gar_index_path(real_path)
                    return
        GarHelper.init(gar_path)
        if (gar_path is not None): 
            reg_file = pathlib.PurePath(gar_path).joinpath("regions.xml")
            RegionHelper.load_from_file(reg_file)
        CorrectionHelper.initialize()
        ServerHelper.SERVER_URI = (None)
    
    @staticmethod
    def get_gar_index_path() -> str:
        """ Получить папку с используемым ГАР-индексом (если null, то индекс не подгружен)
        
        """
        from pullenti.address.internal.GarHelper import GarHelper
        if (GarHelper.GAR_INDEX is None): 
            return None
        return GarHelper.GAR_INDEX.base_dir
    
    @staticmethod
    def get_gar_statistic() -> 'GarStatistic':
        """ Получить информацию по индексу и его объектам
        
        """
        from pullenti.address.internal.GarHelper import GarHelper
        from pullenti.address.internal.ServerHelper import ServerHelper
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.get_gar_statistic()
            if (GarHelper.GAR_INDEX is None): 
                return None
            res = GarStatistic()
            res.version = GarHelper.GAR_INDEX.version
            res.index_path = GarHelper.GAR_INDEX.base_dir
            res.area_count = GarHelper.GAR_INDEX.areas_count
            res.house_count = GarHelper.GAR_INDEX.houses_count
            res.room_count = GarHelper.GAR_INDEX.rooms_count
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def set_server_connection(uri : str) -> bool:
        """ Для работы установить связь с сервером и все запросы делать через него
        (используется для ускорения работы для JS и Python)
        
        Args:
            uri(str): например, http://localhost:2222, если null, то связь разрывается
        
        """
        from pullenti.address.internal.ServerHelper import ServerHelper
        if (uri is None): 
            ServerHelper.SERVER_URI = (None)
            return True
        if (not uri.startswith("http")): 
            uri = ("http://" + uri)
        ver = ServerHelper.get_server_version(uri)
        if (ver is None): 
            ServerHelper.SERVER_URI = (None)
            return False
        else: 
            AddressService.set_gar_index_path(None)
            ServerHelper.SERVER_URI = uri
            return True
    
    @staticmethod
    def get_server_uri() -> str:
        """ Если связь с сервером установлена, то вернёт адрес
        
        """
        from pullenti.address.internal.ServerHelper import ServerHelper
        return ServerHelper.SERVER_URI
    
    @staticmethod
    def get_server_version(uri : str) -> str:
        """ Получить версию SDK на сервере
        
        Args:
            uri(str): 
        
        Returns:
            str: версия или null при недоступности сервера
        """
        from pullenti.address.internal.ServerHelper import ServerHelper
        return ServerHelper.get_server_version(uri)
    
    @staticmethod
    def process_text(txt : str, pars : 'ProcessTextParams'=None) -> typing.List['TextAddress']:
        """ Обработать произвольный текст, в котором есть адреса
        
        Args:
            txt(str): текст
            pars(ProcessTextParams): дополнительные параметры (null - дефолтовые)
        
        Returns:
            typing.List[TextAddress]: результат - для каждого найденного адреса свой экземпляр
        
        """
        from pullenti.address.internal.AnalyzeHelper import AnalyzeHelper
        from pullenti.address.internal.ServerHelper import ServerHelper
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.process_text(txt, pars)
            ah = AnalyzeHelper()
            res = ah.analyze(txt, None, False, pars, False)
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_text(txt : str, pars : 'ProcessTextParams'=None) -> 'TextAddress':
        """ Обработать текст с одним адресом (адресное поле)
        
        Args:
            txt(str): исходный текст
            pars(ProcessTextParams): дополнительные параметры (null - дефолтовые)
        
        Returns:
            TextAddress: результат обработки
        
        """
        from pullenti.address.internal.AnalyzeHelper import AnalyzeHelper
        from pullenti.address.internal.ServerHelper import ServerHelper
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.process_single_address_text(txt, pars)
            sw = Stopwatch()
            sw.start()
            ah = AnalyzeHelper()
            objs = ah.analyze(txt, None, True, pars, False)
            res = None
            if (objs is None or len(objs) == 0): 
                res = TextAddress._new233("Адрес не выделен", txt)
            else: 
                res = objs[0]
                if (res.coef < 90): 
                    objs2 = ah.analyze(txt, None, True, pars, True)
                    if (objs2 is not None and len(objs2) == 1 and objs2[0].coef > objs[0].coef): 
                        res = objs2[0]
            res.read_count = ah.index_read_count
            sw.stop()
            res.milliseconds = (sw.elapsedMilliseconds)
            return res
        except Exception as ex: 
            return TextAddress._new233(str(ex), txt)
    
    @staticmethod
    def process_single_address_texts(txts : typing.List[str], pars : 'ProcessTextParams'=None) -> typing.List['TextAddress']:
        """ Обработать порцию адресов. Использовать в случае сервера, посылая ему порцию на обработку
        (не более 100-300 за раз), чтобы сократить время на издержки взаимодействия.
        Для обычной работы (не через сервер) это эквивалентно вызову в цикле ProcessSingleAddressText
        и особого смысла не имеет.
        
        Args:
            txts(typing.List[str]): список адресов
            pars(ProcessTextParams): дополнительные параметры (null - дефолтовые)
        
        Returns:
            typing.List[TextAddress]: результат (количество совпадает с исходным списком), если null, то какая-то ошибка
        """
        from pullenti.address.internal.ServerHelper import ServerHelper
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.process_single_address_texts(txts, pars)
            res = list()
            for txt in txts: 
                res.append(AddressService.process_single_address_text(txt, None))
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_texts_records(txts : typing.List[str], pars : 'ProcessTextParams'=None) -> typing.List['AddressDbRecord']:
        """ Пробразовать порцию адресов сразу в представление для записи в БД
        (фактически вызываются ProcessSingleAddressTexts и затем для каждого AddressDbRecord.AddressDbRecord,
        для случая взаимодействия с сервером так получится эффективнее)
        
        Args:
            txts(typing.List[str]): список адресов
            pars(ProcessTextParams): дополнительные параметры (null - дефолтовые)
        
        Returns:
            typing.List[AddressDbRecord]: результат (количество совпадает с исходным списком), если null, то какая-то ошибка
        """
        from pullenti.address.internal.ServerHelper import ServerHelper
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.process_single_address_texts_records(txts, pars)
            res = list()
            for txt in txts: 
                if (txt is None): 
                    res.append(None)
                else: 
                    a = AddressService.process_single_address_text(txt, pars)
                    if (a is None): 
                        res.append(None)
                    else: 
                        res.append(AddressDbRecord.create_from_address(a))
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def search_objects(search_pars : 'SearchParams') -> 'SearchResult':
        """ Искать объекты (для выпадающих списков)
        
        Args:
            search_pars(SearchParams): параметры запроса
        
        Returns:
            SearchResult: результат
        """
        from pullenti.address.internal.AddressSearchHelper import AddressSearchHelper
        from pullenti.address.internal.ServerHelper import ServerHelper
        try: 
            if (search_pars is None): 
                return None
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.search_objects(search_pars)
            return AddressSearchHelper.search(search_pars)
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_children_objects(obj_id : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        """ Получить список дочерних объектов для ГАР-объекта
        
        Args:
            obj_id(str): идентификатор объект ГАР (если null, то вернёт объекты первого уровня - регионы)
            ignore_houses(bool): игнорировать дома и помещения
        
        Returns:
            typing.List[GarObject]: дочерние объекты
        """
        from pullenti.address.internal.GarHelper import GarHelper
        from pullenti.address.internal.ServerHelper import ServerHelper
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.get_children_objects(obj_id, ignore_houses)
            return GarHelper.get_children_objects(obj_id, ignore_houses)
        except Exception as ex235: 
            return None
    
    @staticmethod
    def get_object(obj_id : str) -> 'GarObject':
        """ Получить объект по внутреннему идентификатору (он может меняться от версии к версии индекса,
        долгосрочно привязываться к нему НЕЛЬЗЯ)
        
        Args:
            obj_id(str): внутренний идентификатор объекта ГАР
        
        Returns:
            GarObject: объект
        """
        from pullenti.address.internal.GarHelper import GarHelper
        from pullenti.address.internal.ServerHelper import ServerHelper
        if (Utils.isNullOrEmpty(obj_id)): 
            return None
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.get_object(obj_id)
            return GarHelper.get_object(obj_id)
        except Exception as ex236: 
            return None
    
    @staticmethod
    def create_text_address_by_analysis_result(ar : 'AnalysisResult') -> typing.List['TextAddress']:
        from pullenti.address.internal.AnalyzeHelper import AnalyzeHelper
        ah = AnalyzeHelper()
        return ah._analyze1(ar, ar.sofa.text, None, False)
    
    @staticmethod
    def create_text_address_by_referent(r : 'Referent') -> 'TextAddress':
        from pullenti.address.internal.AnalyzeHelper import AnalyzeHelper
        ah = AnalyzeHelper()
        return ah.create_text_address_by_referent(r)