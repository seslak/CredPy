# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 00:29:32 2020

@author: Sinisa Seslak
"""

class company:
    def __init__(self, cash, receivables, inventory, otherstassets, equipment, buildings, land, otherltassets, defferedtax, lossaboveq, defferdtax, lossaboveeq, payables, stloans, ltloansyear, otherstobl, ltloans, otherltobl, paidincap, retainedear, othcap, revenues, cogs, gna, salaries, amortization, othopexp, interest, othrev, othexp, taxes, othchg):
        self.cash = cash # Cash and Cash equivalents
        self.receivables = receivables # Receivables
        self.inventory = inventory # Inventory
        self.otherstassets = otherstassets # Other short-term assets
        self.equipment = equipment # Equipment
        self.buildings = buildings # Buildings and machinery
        self.land = land # Land
        self.otherltassets = otherltassets # Other long-term assets
        self.defferdtax = defferdtax # Deffered Taxes
        self.lossaboveeq = lossaboveeq # Loss above equity level
        self.payables = payables # Payables
        self.stloans = stloans # Shor-term loans
        self.ltloansyear = ltloansyear # Long-term loans part maturing within a year
        self.otherstobl = otherstobl # Other short-term obligations
        self.ltloans = ltloans # Long-term loans
        self.otherltobl = otherltobl # Other long-term obligations
        self.paidincap = paidincap # Paid in capital
        self.retainedear = retainedear # Retained earnings
        self.othcap = othcap # Other capital
        
        self.revenues = revenues # Total revenues
        self.cogs = cogs # Costs of goods sold
        self.gna = gna # General and administration costs
        self.salaries = salaries # Total salaries
        self.amortization = amortization # Amortization
        self.othopexp = othopexp # Other operating expenses
        self.interest = interest # Interest expanses
        self.othrev = othrev # Other revenues
        self.othexp = othexp # Other expenses
        self.taxes = taxes # Taxes
        self.othchg = othchg # Other P&L Changes
        
        # Basic balance sheet positions
        self.tlta = self.equipment + self.buildings + self.land + self.otherltassets # Total long-term assets
        self.tsta = self.cash + self.receivables + self.inventory + self.otherstassets # Total short-term assets
        self.ta = self.tlta + self.tsta # Total assets
        self.tso = self.payables + self.stloans + self.ltloansyear + self.otherstobl # Total shor-term obligations
        self.equity = self.paidincap + self.retainedear + self.othcap # Total equity
        
        # Basic P&L positions
        self.totalcosts = self.cogs + self.gna + self.salaries + self.amortization + self.othopexp # Total costs
        
        # Advanced P&L positions
        self.ebitdar = self.revenues - self.cogs - self.salaries
        self.ebitda = self.ebitdar - self.gna - self.othopexp
        self.ebit = self.ebitda - self.amortization
        self.ebt = self.ebit - self.interest + self.othrev + self.othexp
        self.netincome = self.ebt - self.taxes
        
    # Scoring function    
    def score(self, model, modeltype="original"):
        
        # Altman's Z-Score model
        if model == "altman":
            if modeltype == "original":
                return 0.717*((self.tsta - self.tso)/self.ta)+0.847*(self.retainedear/self.ta)+3.107*(self.ebt/self.ta)+0.42*(self.equity/(self.tso + self.ltloans + self.otherltobl))+0.998*(self.revenues/self.ta)
            if modeltype == "emerging":
                return 3.25 + 6.56*((self.tsta - self.tso)/self.ta)+3.26*(self.retainedear/self.ta)+6.72*(self.ebt/self.ta)+1.05*(self.equity/(self.tso + self.ltloans + self.otherltobl))+0.998*(self.revenues/self.ta)
            if modeltype == "rev":
                return 0.717*((self.tsta - self.tso)/self.ta)+0.847*(self.retainedear/self.ta)+3.107*(self.ebt/self.ta)+0.42*(self.equity/(self.tso + self.ltloans + self.otherltobl))+0.998*(self.revenues/self.ta)
            
        # Bathory model
        if model == "bathory":
            return self.ebt/self.tso+self.ebt/(self.tsta-self.tso)+self.equity/self.tso+((self.equipment+self.buildings+self.land)/(self.tso+self.ltloans+self.otherltobl))
        
        # Springate model
        if model == "springate":
            return 1.03*((self.tsta/self.tso)/self.ta)+3.07*(self.ebit/self.ta)+0.66*(self.ebt/self.tso)+0.4*(self.revenues/self.ta)
        
        # Zmijewski model
        if model == "zmijewski":
            return -4.336 -4.513*((self.netincome-self.othchg)/self.ta)+5.679*((self.ltloans+self.otherltobl+self.tso)/self.ta)+0.004*(self.tsta/self.tso)
        
        # Grover model
        if model == "grover":
            return 1.650*((self.tsta-self.tso)/self.ta)+3.404*(self.ebit/self.ta)-0.016*((self.netincome-self.othchg)/self.ta)+0.057
        
        # Fulmer model
        if model == "fulmer":
            return 5.528*(self.retainedear/self.ta)+0.212*(self.revenues/self.ta)+0.73*(self.ebit/self.equity)+1.27*(self.ebit+self.amortization-self.taxes+(self.))
