# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 00:29:32 2020

@author: Sinisa Seslak
"""

import numpy as np
import pandas as pd

class company:
#    def __init__(self, cash, receivables, inventory, otherstassets, equipment, buildings, land, otherltassets, defferedtax, lossaboveq, defferdtax, lossaboveeq, payables, stloans, ltloansyear, otherstobl, ltloans, otherltobl, paidincap, retainedear, othcap, revenues, cogs, gna, salaries, amortization, othopexp, interest, othrev, othexp, taxes, othchg):
    def __init__(self, inputdata):
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
        self.dataset['ta'] = self.dataset['tlta'] + self.dataset['tsta'] # Total assets
        self.dataset['tso'] = self.dataset['payables'] + self.dataset['stloans'] + self.dataset['ltloansyear'] + self.dataset['otherstobl'] # Total shor-term obligations
        self.dataset['equity'] = self.dataset['paidincap'] + self.dataset['retainedear'] + self.dataset['othcap'] # Total equity

        # Basic P&L positions
        self.dataset['totalcosts'] = self.dataset['cogs'] + self.dataset['gna'] + self.dataset['salaries'] + self.dataset['amortization'] + self.dataset['othopexp'] # Total costs
        
        # Advanced P&L positions
        self.dataset['ebitdar'] = self.dataset['revenues'] - self.dataset['cogs'] - self.dataset['salaries']
        self.dataset['ebitda'] = self.dataset['ebitdar'] - self.dataset['gna'] - self.dataset['othopexp']
        self.dataset['ebit'] = self.dataset['ebitda'] - self.dataset['amortization']
        self.dataset['ebt'] = self.dataset['ebit'] - self.dataset['interest'] + self.dataset['othrev'] + self.dataset['othexp']
        self.dataset['netincome'] = self.dataset['ebt'] - self.dataset['taxes']
        
    # Scoring function    
    def score(self, model, modeltype="original"):
        
        # Altman's Z-Score model
        if model == "altman":
            if modeltype == "original":
                return 0.717*((self.dataset['tsta'] - self.dataset['tso'])/self.dataset['ta'])+0.847*(self.dataset['retainedear']/self.dataset['ta'])+3.107*(self.dataset['ebt']/self.dataset['ta'])+0.42*(self.dataset['equity']/(self.dataset['tso'] + self.dataset['ltloans'] + self.dataset['otherltobl']))+0.998*(self.dataset['revenues']/self.dataset['ta'])
            if modeltype == "emerging":
                return 3.25 + 6.56*((self.dataset['tsta'] - self.dataset['tso'])/self.dataset['ta'])+3.26*(self.dataset['retainedear']/self.dataset['ta'])+6.72*(self.dataset['ebt']/self.dataset['ta'])+1.05*(self.dataset['equity']/(self.dataset['tso'] + self.dataset['ltloans'] + self.dataset['otherltobl']))+0.998*(self.dataset['revenues']/self.dataset['ta'])
            if modeltype == "rev":
                return 0.717*((self.dataset['tsta'] - self.dataset['tso'])/self.dataset['ta'])+0.847*(self.dataset['retainedear']/self.dataset['ta'])+3.107*(self.dataset['ebt']/self.dataset['ta'])+0.42*(self.dataset['equity']/(self.dataset['tso'] + self.dataset['ltloans'] + self.dataset['otherltobl']))+0.998*(self.dataset['revenues']/self.dataset['ta'])
            
        # Bathory model
        if model == "bathory":
            return self.dataset['ebt']/self.dataset['tso']+self.dataset['ebt']/(self.dataset['tsta']-self.dataset['tso'])+self.dataset['equity']/self.dataset['tso']+((self.dataset['equipment']+self.dataset['buildings']+self.dataset['land'])/(self.dataset['tso']+self.dataset['ltloans']+self.dataset['otherltobl']))
        
        # Springate model
        if model == "springate":
            return 1.03*((self.dataset['tsta']/self.dataset['tso'])/self.dataset['ta'])+3.07*(self.dataset['ebit']/self.dataset['ta'])+0.66*(self.dataset['ebt']/self.dataset['tso'])+0.4*(self.dataset['revenues']/self.dataset['ta'])
        
        # Zmijewski model
        if model == "zmijewski":
            return -4.336 -4.513*((self.dataset['netincome']-self.dataset['othchg'])/self.dataset['ta'])+5.679*((self.dataset['ltloans']+self.odataset['therltobl']+self.dataset['tso'])/self.dataset['ta'])+0.004*(self.dataset['tsta']/self.dataset['tso'])
        
        # Grover model
        if model == "grover":
            return 1.650*((self.dataset['tsta']-self.dataset['tso'])/self.dataset['ta'])+3.404*(self.dataset['ebit']/self.dataset['ta'])-0.016*((self.dataset['netincome']-self.dataset['othchg'])/self.dataset['ta'])+0.057
        
        # Fulmer model
        if model == "fulmer":
            return 5.528*(self.dataset['retainedear']/self.dataset['ta'])+0.212*(self.dataset['revenues']/self.dataset['ta'])+0.73*(self.dataset['ebit']/self.dataset['equity'])+1.27*(self.dataset['ebit']+self.dataset['amortization']-self.dataset['taxes']+(self.dataset['cash']+self.dataset['receivables']+self.dataset['inventory']+self.dataset['otherstassets']-self.dataset['tso']))/(self.dataset['tso']+self.dataset['ltloans']+self.dataset['otherltobl'])-0.12*((self.dataset['tso']+self.dataset['ltloans']+self.dataset['otherltobl'])/self.dataset['equity'])+2.335*(self.dataset['tso']/self.dataset['ta'])
