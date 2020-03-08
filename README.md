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

`
import credpy as crp
x = crp.credpy[DATASET]
`

where DATASET is the dataset passed to the class with the financial positions
of companies as follows: 

Cash and Cash equivalents, Receivables, Inventory, Other short-term assets, Equipment,  Buildings and machinery, Land, Other long-term assets, Deffered Taxes, Loss above equity level, Payables, Shor-term loans, Long-term loans part maturing within a year, Other short-term obligations, Long-term loans, Other long-term obligations, Paid in capital, Retained earnings, Other capital, Total revenues, Costs of goods sold, General and administration costs, Total salaries, Amortization, Other operating expenses, Interest expanses, Other revenues, Other expenses, Taxes, Other P&L Changes

Following the above instructions is important for the library to be able to
manipulate balance positions correctly.

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
v0.91b - Feb, 2017.
changed source file name and added comments.

v0.91 - Feb, 2017.
Revived as a more complex idea for repository. README was created. Placed on GitHub.

v0.90 - March, 2015.
Basic IBAN validation algorithm was created.

## License
GNU GENERAL PUBLIC LICENSE v3
