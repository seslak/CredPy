# -*- coding: utf-8 -*-
"""
       Copyright [2020] [Sinisa Seslak (seslaks@gmail.com)
    
       Licensed under the Apache License, Version 2.0 (the "License");
       you may not use this file except in compliance with the License.
       You may obtain a copy of the License at
    
       http://www.apache.org/licenses/LICENSE-2.0
    
       Unless required by applicable law or agreed to in writing, software
       distributed under the License is distributed on an "AS IS" BASIS,
       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
       See the License for the specific language governing permissions and
       limitations under the License.

---
       Errors and warnings file for CredPy package (https://github.com/seslak/CredPy)

@author: Sinisa Seslak
"""

def error(errortype):
    import warnings
    if errortype == "dayssales":
        warnings.warn("ATTENTION! After usage of this ratio company set has to be redefined! It will be fixed in coming version.", DeprecationWarning) # FIXED!
    
    if errortype == "scoringwarn":
        warnings.warn("Please have in mind this is undder development library. Double check the results!", Warning)
            
    if errortype == "fatonw":
        warnings.warn("For the ratio Fixed assets to Net worth the calculation of intangible assets has been done with Other long-term assets", Warning)