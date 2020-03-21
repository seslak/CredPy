# CredPy
Credit risk library for python enabling basic and advanced manipulation and
calculation of financial statements of datasets with companies.

## Installation

Installation can be done from te PyPi index:

`pip install credpy`

Or you can grab the source from GitHub and append it to your project:

`https://github.com/seslak/CredPy/`

## Usage
For the library to correctly calculate position from dataset firstly the
dataset has to be assigned to the class:

`import credpy as crp`
`x = crp.company[DATASET]`

where _DATASET_ is the dataset passed to the class with the financial positions
of companies as follows: 

Cash and Cash equivalents, Receivables, Inventory, Other short-term assets, Equipment,  Buildings and machinery, Land, Other long-term assets, Deffered Taxes, Loss above equity level, Payables, Shor-term loans, Long-term loans part maturing within a year, Other short-term obligations, Long-term loans, Other long-term obligations, Paid in capital, Retained earnings, Other capital, Total revenues, Costs of goods sold, General and administration costs, Total salaries, Amortization, Other operating expenses, Interest expanses, Other revenues, Other expenses, Taxes, Other P&L Changes

Following the above instructions is important for the library to be able to
manipulate balance positions correctly. Additional csv file with frame is in the examples folder.

Functions available:

- **position** - Retrieves designated balance sheet position.

`
x.position['equity']
`

Positions are labeled as follows (in square brakets are the labels for function):
            
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
            

Additional positions are:

            Total long-term assets [tlta]
            Total short-term assets [tsta]
            Total assets [ta]
            Total short-term obligations [tso]
            Total liabilites [tli]
            Equity [equity]
            
            Total costs [totalcosts]
            EBITDAR [ebitdar]
            EBITDA [ebitda]
            EBIT [ebit]
            EBT [ebt]
            Net Income [netincome]
            
- **weights** - Weights function is used for calculating weights in dataset.

`
x.weights('inventory', 80000, 'equity', 'ta', 'cash')
`
Retrieves weights fot equity, total assets, and cash for the inventory to be over the 80.000.

- **ratio** - Retrieves designated ratio

`
x.ratio['current']
`

Ratios are labeled as follows (in square brakets are the labels for function):

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
     

- **score** - Applies designated scoring model to the dataset

`
x.score['altman', 'revised']
`

Scoring models are labeled as follows (in square brakets are the labels for function):

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




## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

0.9.0 - First public release

## License
Apache License, Version 2.0