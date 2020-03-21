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
       Ratios file for CredPy package (https://github.com/seslak/CredPy)

@author: Sinisa Seslak
"""

# Ratios
def getratio(dataset, ratio, days=365):

    """
    These are liquidity ratios. 
    
    Currently available: current, quick, cashr, nwc, cashta, salestor, dayssales, costsales, ctr
    
    If you plan to commit, please follow this structure.
    
    """
    if ratio == "current": # Current ratio
        return dataset['tsta']/dataset['tso']
    
    if ratio == "quick": # Quick/Acid ratio
        return (dataset['tsta']-dataset['inventory'])/dataset['tso']
    
    if ratio == "cashr": # Cash ratio
        return dataset['cash']/(dataset['tso']+dataset['ltloansyear']+dataset['otherstobl']+dataset['ltloans']+dataset['otherltobl'])

    if ratio == "nwc": # Net-working capital
        return dataset['tsta']-dataset['tso']

    if ratio == "cashta": # Cash to assets ratio
        return dataset['cash']/dataset['ta']
    
    if ratio == "salestor": # Sales to receivables (or turnover ratio)
        return dataset['revenues']/dataset['receivables']
    
    if ratio == "dayssales": # Days sales outstanding
        return dataset['receivables']/dataset['revenues']*days
    
    if ratio == "costsales": # Cost of sales
        return (dataset['cogs']+dataset['gna']+dataset['salaries'])/dataset['receivables']
    
    if ratio == "ctr": # Cash turnover
        return dataset['revenues']/dataset['cash']    
    
    """
    These are leverage ratios. 
    
    Currently available: debtequ, debt, fatonw, ebitint, earnings, equityr
    
    If you plan to commit, please follow this structure.
    
    """
    
    if ratio == "debtequ": # Debt to equity ratio
        return dataset['tli']/dataset['paidincap']
    
    if ratio == "debt": # Debt ratio
        return dataset['tli']/dataset['ta']
    
    if ratio == "fatonw": # Fixed-assets to net-worth
        from errors import error
        error("fatonw")
        return (dataset['equipment']+dataset['buildings']+dataset['land']-dataset['amortization']*2)/(dataset['equipment']+dataset['buildings']+dataset['land']-dataset['tli'])
    
    if ratio == "ebitint": # Interest coverage
        return dataset['ebit']/dataset['interest']
    
    if ratio == "earnings": # Retained earnings ratio compared to equity
        return dataset['retainedear']/dataset['equity']
    
    if ratio == "equityr": # Equity ratio
        return dataset['equity']/dataset['ta'] 
    
        """
    These are efficiency ratios. 
    
    Currently available: invtr, invhp, invta, acctr, acccp, dpo
    
    If you plan to commit, please follow this structure.
    
    """
    
    if ratio == "invtr": # Inventory turnover
        return dataset['revenues']/dataset['inventory']
    
    if ratio == "invhp": # Inventory holding period
        return days/dataset['revenues']/dataset['inventory']
    
    if ratio == "invta": # Inventory to assets ratio
        return days/dataset['inventory']/dataset['ta']

    if ratio == "acctr": # Accounts receivable turnover
        return dataset['revenues']/dataset['receivables']
    
    if ratio == "acccp": # Accounts receivable collection period
        return days/dataset['revenues']/dataset['receivables']
    
    if ratio == "dpo": # Days payable outstanding
        return dataset['payables']/dataset['cogs']*days