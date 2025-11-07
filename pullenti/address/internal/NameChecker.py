# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.geo.internal.INameChecker import INameChecker
from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.address.internal.GarHelper import GarHelper

class NameChecker(INameChecker):
    
    def check(self, name : str, is_street : bool) -> bool:
        if (GarHelper.GAR_INDEX is None): 
            return False
        vars0_ = list()
        vars2 = list()
        NameAnalyzer.create_search_variants(vars0_, None, vars2, name, None, False)
        for v in vars0_: 
            if (GarHelper.GAR_INDEX._check_name(v, is_street)): 
                return True
        for v in vars2: 
            if (GarHelper.GAR_INDEX._check_name(v, is_street)): 
                return True
        return False