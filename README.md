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
`x = crp.company(DATASET, [DATASET2], [DATASET3], ...)`

where _DATASET_ is the dataset passed to the class with the financial positions
of companies as follows: 

Cash and Cash equivalents, Receivables, Inventory, Other short-term assets, Equipment,  Buildings and machinery, Land, Other long-term assets, Deffered Taxes, Loss above equity level, Payables, Shor-term loans, Long-term loans part maturing within a year, Other short-term obligations, Long-term loans, Other long-term obligations, Paid in capital, Retained earnings, Other capital, Total revenues, Costs of goods sold, General and administration costs, Total salaries, Amortization, Other operating expenses, Interest expanses, Other revenues, Other expenses, Taxes, Other P&L Changes

Following the above instructions it is important for the library to be able to
manipulate balance positions correctly. Additional csv file with frame is in the examples folder.

You can serv csv file or dataset with lists and tupels, as long as it is a 1D set. It can have multiple dimesions within itself.

Adding _DATASET2_, _DATASET3_ etc. is adding time series into the company's information.

Functions available:

- **position** - Retrieves designated balance sheet position.

`
x.position('equity', 1)
`

Number one means it will use only second year from the dataset.
0 is the first year. Leaving blank calculates all the years.

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

It calculates weights on datasets for all of the years.

Retrieves weights fot equity, total assets, and cash for the inventory to be over the 80.000.

For its usage it needs to have the target value (can be any of the dataset, but only one), and weighted value (can be any of the dataset, and as many as wanted).


- **ratio** - Retrieves designated ratio

`
x.ratio('current', n=1)
`

Number one (n) means it will use only second year from the dataset.
0 is the first year. Leaving blank calculates all the years.

`
x.ratio("dayssales", 0, days=360)
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
x.score('altman', 'revised', 1)
`

Number one (n) means it will use only second year from the dataset.
0 is the first year. Leaving blank calculates all the years.

You can also edit weights in scoring models.

`
x.score('fulmer', 1.1, 2.2, 0.5, 0.9, 5, 2.8)
`

Scoring models are labeled as follows (in square brakets are the labels for functions):

        Altman's z-score [altman]
            Original (default model if not defined) [altman, original]
            Updated [altman, updated]
            Revised [altman, revised]
            Taffler's and Tisshaw's  [altman, tntmodel]
            Non-manufacturing [altman, non-man]
            Emerging markets [altman, emerging]
        Bathory model [bathory]
        Springate model [springate]
        Zmijewski model [zmijewski]
        Kralicek DF indicator [kralicek]
        Grover model [grover]
        Fulmer model [fulmer]
		
- **ml** - Basic machine learning calculations on prepared dataset

Machine learning methods are meant to easily use some of the popular statistical libraries and frameworks on financial datasets.
This is more because CredPy has someone specific data structure so it is meant to make the work easier for the end user.

`
x.ml(['linreg'], DATASETFORTESTING, 1, 'netincome','ebt', 'gna')
`

The following is the Simple linear regression for appended _DATASET2_ (because of number 1 in arguments) as a training set, where the targeted value is netincome and variables are EBT and GNA.
After that the predictions are applied on the _DATASETFORTESTING_ and returned. Because of that _DATASETFORTESTING_ has to comply to the CredPy data structure instructions.

It is possible to pass additional arguments into the functions:

`
x.ml(['linreg'], DATASETFORTESTING, 1, 'netincome','ebt', 'gna', fit_intercept=True, normalize=True, n_jobs=4)
`

All of the additional arguments are the ones available over the scikit-learn library so please see their documentation for additional info. If not specified, they are set to the defaults.

Currently suported modelling functions are:

        Simple linear regression [linreg] {it becomes multiple by adding more variables into the model, no need for different wording}
        Polynomial regression [polyreg]
        Support Vector Regression (SVR) [SVR]
        Decision Tree Regression [decision_tree_reg]
        Random Forest Regression [random_forest_reg]


## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

0.9.1 - Time series datasets enabled,
		Multiprocessing support re-coded for Linux (not tested on MAC OS, it should work), it is yet not implemented on Windows based systems,
		First machine learning functions incorporated into the ML framework,
		Loads of typos corrected. :)

0.9.0 - First public release

## License
Apache License, Version 2.0