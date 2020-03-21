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
       Main library file for CredPy package (https://github.com/seslak/CredPy)

Created on Fri Feb  7 00:29:32 2020

@author: Sinisa Seslak
"""

import pandas as pd

class company:
    def __init__(self, inputdata):
        """
        Building balance sheet positions and profit and loss
        
        Initial dataset that is forwarded to class appends the data to corresponding
        balance sheet position. Data in dataset has to be arranged per columns in
        the following order (in brakets are the names of the columns in class'
        dataset, this is important for later):
            - Balance sheet
            Cash and Cash equivalents [cash]
            Receivables [receivables]
            Inventory [inventory]
            Other short-term assets [otherstassets]
            Equipment [equipment]
            Buildings and machinery [buildings]
            Land [land]
            Other long-term assets [otherltassets]
            Deffered Taxes [defferedtax]
            Loss above equity level [lossaboveq]
            Payables [payables]
            Shor-term loans [stloans]
            Long-term loans part maturing within a year [ltloansyear]
            Other short-term obligations [otherstobl]
            Long-term loans [ltloans]
            Other long-term obligations [otherltobl]
            Paid in capital [paidincap]
            Retained earnings [retainedear]
            Other capital [othcap]
            
            - Profit and loss                             
            Total revenues [revenues]
            Costs of goods sold [cogs]
            General and administration costs [gna]
            Total salaries [salaries]
            Amortization [amortization]
            Other operating expenses [othopexp]
            Interest expanses [interest]
            Other revenues [othrev]
            Other expenses [othexp]
            Taxes [taxes]
            Other P&L Changes [othchg]
        """
        self.dataset = pd.DataFrame(inputdata, columns = ['cash',            # Cash and Cash equivalents
                                                          'receivables',     # Receivables
                                                          'inventory',       # Inventory
                                                          'otherstassets',   # Other short-term assets
                                                          'equipment',       # Equipment
                                                          'buildings',       # Buildings and machinery
                                                          'land',            # Land
                                                          'otherltassets',   # Other long-term assets
                                                          'defferedtax',     # Deffered Taxes
                                                          'lossaboveq',      # Loss above equity level
                                                          'payables',        # Payables
                                                          'stloans',         # Shor-term loans
                                                          'ltloansyear',     # Long-term loans part maturing within a year 
                                                          'otherstobl',      # Other short-term obligations
                                                          'ltloans',         # Long-term loans 
                                                          'otherltobl',      # Other long-term obligations
                                                          'paidincap',       # Paid in capital
                                                          'retainedear',     # Retained earnings
                                                          'othcap',          # Other capital
                                                          
                                                          'revenues',        # Total revenues
                                                          'cogs',            # Costs of goods sold
                                                          'gna',             # General and administration costs
                                                          'salaries',        # Total salaries
                                                          'amortization',    # Amortization
                                                          'othopexp',        # Other operating expenses
                                                          'interest',        # Interest expanses
                                                          'othrev',          # Other revenues
                                                          'othexp',          # Other expenses
                                                          'taxes',           # Taxes
                                                          'othchg'])         # Other P&L Changes
      
        # Basic balance sheet positions
        self.dataset['tlta'] = self.dataset['equipment']+self.dataset['buildings']+self.dataset['land']+self.dataset['otherltassets'] # Total long-term assets
        
        self.dataset['tsta'] = self.dataset['cash'] + self.dataset['receivables'] + self.dataset['inventory'] + self.dataset['otherstassets'] # Total short-term assets
        
        self.dataset['ta'] = self.dataset['tlta'] + self.dataset['tsta'] - self.dataset['defferedtax'] - self.dataset['lossaboveq']# Total assets
        
        self.dataset['tso'] = self.dataset['payables'] + self.dataset['stloans'] + self.dataset['ltloansyear'] + self.dataset['otherstobl'] # Total shor-term obligations
        
        self.dataset['tli'] = self.dataset['tso'] + self.dataset['ltloans'] + self.dataset['otherltobl'] # Total liabilities
        
        self.dataset['equity'] = self.dataset['paidincap'] + self.dataset['retainedear'] + self.dataset['othcap'] # Total equity

        # Basic P&L positions
        self.dataset['totalcosts'] = self.dataset['cogs'] + self.dataset['gna'] + self.dataset['salaries'] + self.dataset['amortization'] + self.dataset['othopexp'] # Total costs
        
        # Advanced P&L positions
        self.dataset['ebitdar'] = self.dataset['revenues'] - self.dataset['cogs'] - self.dataset['salaries'] # EBITDAR
        
        self.dataset['ebitda'] = self.dataset['ebitdar'] - self.dataset['gna'] - self.dataset['othopexp'] # EBITDA
        
        self.dataset['ebit'] = self.dataset['ebitda'] - self.dataset['amortization'] # EBIT
        
        self.dataset['ebt'] = self.dataset['ebit'] - self.dataset['interest'] + self.dataset['othrev'] + self.dataset['othexp'] # EBT
        
        self.dataset['netincome'] = self.dataset['ebt'] - self.dataset['taxes'] # Net Income
    
    def position(self, pos): # Getting destinguished balance sheet position
        """
        Position is used for retrieving any accounting position from company's statements,
        or having it for all of the companies in the dataset.
        
        Example:
            x.position('equity')[3]
                will return equity position for the fourth company in the dataset,
                removing the index at the end will result in the retrievment of the
                entire 'equity' column.
        List of available positions:
            + Previously stated balance sheet and P&L positions
            Total long-term assets [tlta]
            Total short-term assets [tsta]
            Total assets [ta]
            Total short-term obligations [tso]
            Equity [equity]
            
            Total costs [totalcosts]
            EBITDAR [ebitdar]
            EBITDA [ebitda]
            EBIT [ebit]
            EBT [ebt]
            Net Income [netincome]
        """
        return self.dataset[pos]
    """
    Weights function is used for calculating weights in dataset.
    
    For its usage it needs to have the target value (can be any of the dataset, but one),
    and weighted value (can be any of the dataset, and as many as wanted).
    
    Example:
        x.weights('inventory', 80000, 'equity', 'ta', 'cash')
        
        Retrieves weights fot equity, total assets, and cash for the inventory to be
        over the 80.000.
    """
    def weights(self, *args):
        self.modeldataset = self.dataset.loc[(self.dataset[args[0]] > args[1]), args[2:]].reset_index(drop=True)
        x  = [None] * len(args[2:])
        for c in args[2:]:
            x[args.index(c)-2] = pd.DataFrame.std(self.modeldataset)[args[args.index(c)]]/pd.DataFrame.std(self.dataset)[args[args.index(c)]]
        return x
    
    # Ratios function
    """ 
    Ratios function is used for applying ratio calculations on the appended dataset
    
    Function is called from separated file ratios.py
    
    Example:
            x.ratio("dayssales", days=360)

    List of available ratios:
            Current ratio [current]
            Quick ratio [quick]
            Cash ratio [cashr]
            Net-working capital [nwr]
            Cash to total assets ratio [cashta]
            Sales to receivables (or turnover ratio) [salestor]
            Days sales outstanding [dayssales] {'days' is optional variable which can be defined, default is 365}
            Cost of sales [costsales]
            Cash turnover [ctr]
            
            Debt to equity ratio [debtequ]
            Debt ratio [debt]
            Fixed-assets to net-worth [fatonw]
            Interest coverage [ebitint]
            Retained earnings ratio compared to equity [earnings]
            Equity ratio  [equityr]
            
            Inventory turnover [invtr]
            Inventory holding period [invhp]
            Inventory to assets ratio [invta]
            Accounts receivable turnover [acctr]
            Accounts receivable collection period [acccp]
            Days payable outstanding [dpo]
    """
    def ratio(self, ratiotype, days=365):
        # we call the function from ratios file
        from ratios import getratio
        self.ratiotype = ratiotype
        self.days = days
        # and return the result for passing class' dataset to the function
        return getratio(self.dataset, self.ratiotype, self.days)
    
    # Scoring function    
    """ 
    Ratios function is used for applying ratio calculations on the appended dataset
    
    Function is called from separated file ratios.py
    
    Example:
        x.score("altman", "revised")
        
        You can also edit weights in scoring models. Example:
            x.score("fulmer", 1.1, 2.2, 0.5, 0.9, 5, 2.8)
            
    List of available scoring models:
        Altman's z-score [altman]
            Original (default model if not defined) [altman, original]
            Updated [altman, updated]
            Revised [altman, revised]
            Taffler's and Tisshaw's  [altman, tntmodel]
            Non-manufacturing [altman, non-man]
            Emerging markets [emerging]
        Bathory model [bathory]
        Springate model [springate]
        Zmijewski model [zmijewski]
        Kralicek DF indicator [kralicek]
        Grover model [grover]
        Fulmer model [fulmer]
    
    """
    def score(self, model, modeltype="original", **kwargs):
        from scoring import scores
        return scores(self.dataset, model, modeltype, **kwargs)


                

