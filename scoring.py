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
       Scoring file for CredPy package (https://github.com/seslak/CredPy)

@author: Sinisa Seslak
"""
def scores(dataset, model, modeltype="original", gnp = 1, **kwargs):
    # Altman's Z-Score model
    from errors import error
    error("scoringwarn")
    if model == "altman":
        if modeltype == "original": # Original
            x1 = kwargs.get('x1', 0.012)
            x2 = kwargs.get('x2', 0.014)
            x3 = kwargs.get('x3', 0.033)
            x4 = kwargs.get('x4', 0.006)
            x5 = kwargs.get('x5', 0.999)
            return x1*((dataset['tsta'] - dataset['tso'])/dataset['ta'])+x2*(dataset['retainedear']/dataset['ta'])+x3*(dataset['ebit']/dataset['ta'])+x4*(dataset['equity']/(dataset['tso'] + dataset['ltloans'] + dataset['otherltobl']))+x5*(dataset['revenues']/dataset['ta'])
        
        if modeltype == "updated": # Updated
            x1 = kwargs.get('x1', 1.2)
            x2 = kwargs.get('x2', 1.4)
            x3 = kwargs.get('x3', 3.3)
            x4 = kwargs.get('x4', 0.6)
            x5 = kwargs.get('x5', 1)
            return x1*((dataset['tsta'] - dataset['tso'])/dataset['ta'])+x2*(dataset['retainedear']/dataset['ta'])+x3*(dataset['ebit']/dataset['ta'])+x4*(dataset['equity']/(dataset['tso'] + dataset['ltloans'] + dataset['otherltobl']))+x5*(dataset['revenues']/dataset['ta'])
        
        if modeltype == "revised": # Revised
            x1 = kwargs.get('x1', 0.717)
            x2 = kwargs.get('x2', 0.847)
            x3 = kwargs.get('x3', 3.107)
            x4 = kwargs.get('x4', 0.420)
            x5 = kwargs.get('x5', 0.998)
            return x1*((dataset['tsta'] - dataset['tso'])/dataset['ta'])+x2*(dataset['retainedear']/dataset['ta'])+x3*(dataset['ebit']/dataset['ta'])+x4*(dataset['equity']/(dataset['tso'] + dataset['ltloans'] + dataset['otherltobl']))+x5*(dataset['revenues']/dataset['ta'])
        
        if modeltype == "tntmodel": # Taffler's and Tisshaw's model (1977)
            x1 = kwargs.get('x1', 0.53)
            x2 = kwargs.get('x2', 0.13)
            x3 = kwargs.get('x3', 0.18)
            x4 = kwargs.get('x4', 0.16)
            return x1*(dataset['ebit']/dataset['tso'])+x2*(dataset['tsta']/dataset['tli'])+x3*(dataset['tso']/dataset['ta'])+x4*((dataset['tsta']-dataset['inventory'])/(dataset['cogs']+dataset['gna']+dataset['salaries']))

        if modeltype == "non-man": # Non-manufacturing
            x1 = kwargs.get('x1', 6.56)
            x2 = kwargs.get('x2', 3.26)
            x3 = kwargs.get('x3', 6.72)
            x4 = kwargs.get('x4', 1.05)
            return x1*((dataset['tsta'] - dataset['tso'])/dataset['ta'])+x2*(dataset['retainedear']/dataset['ta'])+x3*(dataset['ebit']/dataset['ta'])+x4*(dataset['equity']/dataset['tli'])
        
        if modeltype == "emerging": # Emerging markets
            x1 = kwargs.get('x1', 3.25)
            x2 = kwargs.get('x2', 6.56)
            x3 = kwargs.get('x3', 3.26)
            x4 = kwargs.get('x4', 6.72)
            x5 = kwargs.get('x5', 1.05)
            return x1 + x2*((dataset['tsta'] - dataset['tso'])/dataset['ta'])+x3*(dataset['retainedear']/dataset['ta'])+x4*(dataset['ebit']/dataset['ta'])+x5*(dataset['equity']/dataset['tli'])
        
    # Bathory model
    if model == "bathory":
        return dataset['ebt']/dataset['tso']+dataset['ebt']/(dataset['tsta']-dataset['tso'])+dataset['equity']/dataset['tso']+((dataset['equipment']+dataset['buildings']+dataset['land'])/(dataset['tso']+dataset['ltloans']+dataset['otherltobl']))
    
    # Springate model
    if model == "springate":
        x1 = kwargs.get('x1', 1.03)
        x2 = kwargs.get('x2', 3.07)
        x3 = kwargs.get('x3', 0.66)
        x4 = kwargs.get('x4', 0.4)
        return x1*((dataset['tsta']/dataset['tso'])/dataset['ta'])+x2*(dataset['ebit']/dataset['ta'])+x3*(dataset['ebt']/dataset['tso'])+x4*(dataset['revenues']/dataset['ta'])
    
    # Zmijewski model
    if model == "zmijewski":
        x1 = kwargs.get('x1', -4.336)
        x2 = kwargs.get('x2', 4.513)
        x3 = kwargs.get('x3', 5.679)
        x4 = kwargs.get('x4', 0.004)
        return x1 - x2*((dataset['netincome']-dataset['othchg'])
                                  /dataset['ta'])+x3*((dataset['ltloans']
                                  +dataset['therltobl']+dataset['tso'])
                                  /dataset['ta'])+x4*(dataset['tsta']
                                  /dataset['tso'])


    # Kralicek DF indicator
    if model == "kralicek":
        x1 = kwargs.get('x1', 1.5)
        x2 = kwargs.get('x2', 0.08)
        x3 = kwargs.get('x3', 10)
        x4 = kwargs.get('x4', 5)
        x5 = kwargs.get('x5', 0.3)
        x6 = kwargs.get('x6', 0.1)
        return x1*(dataset['ebit']+dataset['amortization'])+x2*(dataset['ta']
                  /dataset['tli'])+x3*(dataset['ebit']
                  /dataset['ta'])+x4*(dataset['ebit']
                  /dataset['revenues'])+x5*(dataset['inventory']
                  /dataset['revenues'])+x6*(dataset['revenues']
                  /dataset['ta'])
        
        
    # Grover model
    if model == "grover":
        x1 = kwargs.get('x1', 1.650)
        x2 = kwargs.get('x2', 3.404)
        x3 = kwargs.get('x3', 0.016)
        x4 = kwargs.get('x4', 0.057)
        return x1*((dataset['tsta']-dataset['tso'])
                        /dataset['ta'])+x2*(dataset['ebit']
                        /dataset['ta'])-x3*((dataset['netincome']-dataset['othchg'])
                        /dataset['ta'])+x4

    # Fulmer model
    if model == "fulmer":
        x1 = kwargs.get('x1', 5.528)
        x2 = kwargs.get('x2', 0.212)
        x3 = kwargs.get('x3', 0.73)
        x4 = kwargs.get('x4', 1.27)
        x5 = kwargs.get('x5', 0.12)
        x6 = kwargs.get('x6', 2.335)
        return x1*(dataset['retainedear']
                        /dataset['ta'])+x2*(dataset['revenues']
                        /dataset['ta'])+x3*(dataset['ebit']
                        /dataset['equity'])+x4*(dataset['ebit']
                        +dataset['amortization']-dataset['taxes']
                        +(dataset['cash']+dataset['receivables']
                        +dataset['inventory']+dataset['otherstassets']
                        -dataset['tso']))/(dataset['tso']+dataset['ltloans']
                        +dataset['otherltobl'])-x5*((dataset['tso']
                        +dataset['ltloans']+dataset['otherltobl'])
                        /dataset['equity'])+x6*(dataset['tso']/dataset['ta']
                        )
        
