"""
       Copyright [2020] [Sinisa Seslak (seslaks@gmail.com)]
    
       Licensed under the Apache License, Version 2.0 (the "License");
       you may not use this file except in compliance with the License.
       You may obtain a copy of the License at
    
       http://www.apache.org/licenses/LICENSE-2.0
    
       Unless required by applicable law or agreed to in writing, software
       distributed under the License is distributed on an "AS IS" BASIS,
       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
       See the License for the specific language governing permissions and
       limitations under the License.
"""

"""
       Support functions for modules in CredPy (https://github.com/seslak/CredPy)
"""

# Function for calculating weights in dataset
def weight(args, c, dataset, modeldataset):
    import pandas as pd
    x = pd.DataFrame.std(modeldataset)[args[args.index(c)]]/pd.DataFrame.std(dataset)[args[args.index(c)]]
    return (x)

# Function for building the balance sheet and P&L and appending it to the dataset
def crappend(args):
    import pandas as pd
    x = pd.DataFrame(args, columns = ['cash',            # Cash and Cash equivalents
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
    x['tlta'] = x['equipment']+x['buildings']+x['land']+x['otherltassets'] # Total long-term assets
        
    x['tsta'] = x['cash'] + x['receivables'] + x['inventory'] + x['otherstassets'] # Total short-term assets
        
    x['ta'] = x['tlta'] + x['tsta'] - x['defferedtax'] - x['lossaboveq']# Total assets
        
    x['tso'] = x['payables'] + x['stloans'] + x['ltloansyear'] + x['otherstobl'] # Total shor-term obligations
        
    x['tli'] = x['tso'] + x['ltloans'] + x['otherltobl'] # Total liabilities
        
    x['equity'] = x['paidincap'] + x['retainedear'] + x['othcap'] # Total equity

    # Basic P&L positions
    x['totalcosts'] = x['cogs'] + x['gna'] + x['salaries'] + x['amortization'] + x['othopexp'] # Total costs
        
    # Advanced P&L positions
    x['ebitdar'] = x['revenues'] - x['cogs'] - x['salaries'] # EBITDAR
         
    x['ebitda'] = x['ebitdar'] - x['gna'] - x['othopexp'] # EBITDA
        
    x['ebit'] = x['ebitda'] - x['amortization'] # EBIT
        
    x['ebt'] = x['ebit'] - x['interest'] + x['othrev'] + x['othexp'] # EBT
        
    x['netincome'] = x['ebt'] - x['taxes'] # Net Income
    
    return (x)
    