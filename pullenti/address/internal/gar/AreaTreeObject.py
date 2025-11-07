# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.address.GarStatus import GarStatus
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.GarLevel import GarLevel

class AreaTreeObject(object):
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.region = 0
        self.level = AddrLevel.UNDEFINED
        self.glevel = GarLevel.UNDEFINED
        self.typs = None;
        self.miscs = None;
        self.parent_ids = list()
        self.parent_parent_ids = None;
        self.expired = False
        self.status = GarStatus.OK
        self.ch_count = 0
        self.typ_id = 0
        self.alt_typ_id = 0
    
    def check_type(self, na : 'NameAnalyzer') -> int:
        alev = self.level
        if (alev == AddrLevel.CITY or alev == AddrLevel.COUNTRY): 
            if (self.glevel == GarLevel.STREET): 
                alev = AddrLevel.STREET
        if (alev != na.level): 
            if (alev == AddrLevel.SETTLEMENT and ((na.level == AddrLevel.LOCALITY))): 
                pass
            elif (alev == AddrLevel.LOCALITY and na.level == AddrLevel.TERRITORY): 
                pass
            elif (alev == AddrLevel.LOCALITY and na.level == AddrLevel.CITY and "населенный пункт" in na.types): 
                pass
            elif (alev == AddrLevel.TERRITORY and ((na.level == AddrLevel.LOCALITY))): 
                pass
            elif ((alev == AddrLevel.TERRITORY and na.level == AddrLevel.DISTRICT and len(na.types) == 1) and na.types[0] == "муниципальный район"): 
                pass
            elif (alev == AddrLevel.STREET and na.level == AddrLevel.TERRITORY): 
                pass
            elif (alev == AddrLevel.CITY and ((na.level == AddrLevel.REGIONCITY or na.level == AddrLevel.LOCALITY))): 
                pass
            elif ((alev == AddrLevel.CITY and na.level == AddrLevel.LOCALITY and len(na.types) == 1) and na.types[0] == "населенный пункт"): 
                pass
            elif (alev == AddrLevel.TERRITORY and na.level == AddrLevel.STREET): 
                if (len(na.types) == 0 or ((len(na.types) == 1 and na.types[0] == "улица"))): 
                    if (self.miscs is not None): 
                        if ("гаражи" in self.miscs or "месторождение" in self.miscs or "дачи" in self.miscs): 
                            return -1
                else: 
                    ok = False
                    if (self.miscs is not None and na.miscs is not None): 
                        for m in self.miscs: 
                            if (m in na.miscs): 
                                ok = True
                    if (not ok): 
                        return -1
            elif ((alev == AddrLevel.DISTRICT and na.level == AddrLevel.SETTLEMENT and len(self.typs) > 0) and "округ" in self.typs[0]): 
                pass
            elif (alev == AddrLevel.LOCALITY and len(na.types) > 0 and "улус" in na.types): 
                pass
            elif (alev == AddrLevel.REGIONCITY and na.level == AddrLevel.CITY): 
                pass
            elif (((alev == AddrLevel.LOCALITY or alev == AddrLevel.CITY)) and len(na.types) == 0): 
                pass
            elif (alev == AddrLevel.DISTRICT and "улус" in self.typs and na.level == AddrLevel.LOCALITY): 
                pass
            else: 
                return -1
        if (self.typs is not None and na.types is not None and len(na.types) > 0): 
            for ty in self.typs: 
                if (ty in na.types): 
                    if (ty != "территория"): 
                        return (1 if alev == na.level else 0)
                    if (self.miscs is not None and na.miscs is not None): 
                        for m in self.miscs: 
                            if (m in na.miscs): 
                                return (1 if alev == na.level else 0)
                            if (str.islower(m[0])): 
                                ch0 = str.upper(m[0])
                                for mm in na.miscs: 
                                    if (mm[len(mm) - 1] == ch0): 
                                        return (1 if alev == na.level else 0)
            if (alev == AddrLevel.TERRITORY and na.level == AddrLevel.TERRITORY): 
                if ((len(self.typs) == 1 and len(na.types) == 1 and self.miscs is None) and len(na.miscs) == 0): 
                    return 0
                if (self.miscs is not None and len(self.miscs) == 1 and self.miscs[0] in na.miscs): 
                    return 0
                return -1
            if (alev == AddrLevel.STREET and na.level == AddrLevel.STREET): 
                if (len(self.typs) > 0 and len(na.types) > 0): 
                    return -1
            if (((alev == AddrLevel.STREET and na.level == AddrLevel.TERRITORY)) or ((alev == AddrLevel.TERRITORY and na.level == AddrLevel.STREET))): 
                if (self.miscs is not None and na.miscs is not None): 
                    for m in self.miscs: 
                        if (m in na.miscs): 
                            return 0
                if (len(na.types) == 1 and na.types[0] == "улица"): 
                    return 0
                if (self.status == GarStatus.OK2): 
                    return 0
                return -1
        return 0
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("{0}".format(self.id0_), end="", file=tmp, flush=True)
        if (self.typs is not None): 
            print(" (", end="", file=tmp)
            for ty in self.typs: 
                if (ty != self.typs[0]): 
                    print("/", end="", file=tmp)
                print(ty, end="", file=tmp)
            print(")", end="", file=tmp)
        if (self.miscs is not None): 
            print(" [", end="", file=tmp)
            for ty in self.miscs: 
                if (ty != self.miscs[0]): 
                    print("/", end="", file=tmp)
                print(ty, end="", file=tmp)
            print("]", end="", file=tmp)
        for p in self.parent_ids: 
            print("{0}{1}".format((" " if p == self.parent_ids[0] else "/"), p), end="", file=tmp, flush=True)
        if (self.parent_parent_ids is not None): 
            for id0__ in self.parent_parent_ids: 
                print("{0}{1}".format((" -" if id0__ == self.parent_parent_ids[0] else ","), id0__), end="", file=tmp, flush=True)
        print(",r={0},l={1}".format(self.region, Utils.enumToString(self.level)), end="", file=tmp, flush=True)
        if (self.expired): 
            print(",expired", end="", file=tmp)
        if (self.status != GarStatus.OK): 
            print(",{0}".format(Utils.enumToString(self.status)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def compareTo(self, other : 'AreaTreeObject') -> int:
        if (self.id0_ < other.id0_): 
            return -1
        if (self.id0_ > other.id0_): 
            return 1
        return 0
    
    def _serialize(self, f : Stream, tr : 'AreaTree') -> None:
        FiasHelper.serialize_int(f, self.id0_)
        f.writebyte(self.region)
        b = self.level
        if (self.expired): 
            b |= (0x80)
        if (self.status == GarStatus.ERROR): 
            b |= (0x40)
        if (self.status == GarStatus.WARNING): 
            b |= (0x20)
        if (self.status == GarStatus.OK2): 
            b |= (0x60)
        f.writebyte(b)
        f.writebyte(((0 if self.typs is None else len(self.typs))))
        if (self.typs is not None): 
            for ty in self.typs: 
                FiasHelper.serialize_short(f, tr.get_string_id(ty))
        f.writebyte(((0 if self.miscs is None else len(self.miscs))))
        if (self.miscs is not None): 
            for ty in self.miscs: 
                FiasHelper.serialize_short(f, tr.get_string_id(ty))
        f.writebyte(len(self.parent_ids))
        if (len(self.parent_ids) > 0): 
            for p in self.parent_ids: 
                FiasHelper.serialize_int(f, p)
            f.writebyte(((0 if self.parent_parent_ids is None else len(self.parent_parent_ids))))
            if (self.parent_parent_ids is not None): 
                for id0__ in self.parent_parent_ids: 
                    FiasHelper.serialize_int(f, id0__)
        f.writebyte(self.glevel)
        FiasHelper.serialize_short(f, self.ch_count)
        FiasHelper.serialize_short(f, self.typ_id)
        FiasHelper.serialize_short(f, self.alt_typ_id)
    
    def _deserialize(self, dat : bytearray, pos : int, tr : 'AreaTree') -> None:
        self.id0_ = int.from_bytes(dat[pos:pos+4], byteorder="little")
        pos += 4
        self.region = dat[pos]
        pos += 1
        b = dat[pos]
        pos += 1
        if ((((b) & 0x80)) != 0): 
            self.expired = True
            b &= (0x7F)
        if ((((b) & 0x40)) != 0): 
            if ((((b) & 0x20)) != 0): 
                self.status = GarStatus.OK2
                b &= (0x1F)
            else: 
                self.status = GarStatus.ERROR
                b &= (0x3F)
        if ((((b) & 0x20)) != 0): 
            self.status = GarStatus.WARNING
            b &= (0x1F)
        self.level = (Utils.valToEnum(b, AddrLevel))
        cou1 = dat[pos]
        pos += 1
        if (cou1 > 0): 
            self.typs = list()
            while cou1 > 0: 
                s = tr.get_string(int.from_bytes(dat[pos:pos+2], byteorder="little"))
                pos += 2
                if (s is not None): 
                    self.typs.append(s)
                cou1 -= 1
        cou1 = (dat[pos])
        pos += 1
        if (cou1 > 0): 
            self.miscs = list()
            while cou1 > 0: 
                s = tr.get_string(int.from_bytes(dat[pos:pos+2], byteorder="little"))
                pos += 2
                if (s is not None): 
                    self.miscs.append(s)
                cou1 -= 1
        cou1 = (dat[pos])
        pos += 1
        if (cou1 > 0): 
            while cou1 > 0: 
                self.parent_ids.append(int.from_bytes(dat[pos:pos+4], byteorder="little"))
                cou1 -= 1; pos += 4
            cou1 = (dat[pos])
            pos += 1
            if (cou1 > 0): 
                self.parent_parent_ids = list()
                while cou1 > 0: 
                    self.parent_parent_ids.append(int.from_bytes(dat[pos:pos+4], byteorder="little"))
                    cou1 -= 1; pos += 4
        if (pos >= len(dat)): 
            return
        b = dat[pos]
        pos += 1
        self.glevel = (Utils.valToEnum(b, GarLevel))
        self.ch_count = int.from_bytes(dat[pos:pos+2], byteorder="little")
        pos += 2
        self.typ_id = int.from_bytes(dat[pos:pos+2], byteorder="little")
        pos += 2
        self.alt_typ_id = int.from_bytes(dat[pos:pos+2], byteorder="little")
        pos += 2
    
    @staticmethod
    def _new1(_arg1 : int) -> 'AreaTreeObject':
        res = AreaTreeObject()
        res.id0_ = _arg1
        return res