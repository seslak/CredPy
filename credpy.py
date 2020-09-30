
# -*- coding: utf-8 -*-

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


        ---
        Main library file for CredPy package (https://github.com/seslak/CredPy)

        Created on Fri Feb  7 00:29:32 2020

        @author: Sinisa Seslak
"""

# These functions have to be on top of module due to pickling for multiprocessing support. Do not move them within class functions.
from support_functions import weight
from support_functions import crappend
from ratios import getratio
from scoring import scores
#

class company:
    """
    Companies can have current balance positions and from previous periods. At this version of CredPy only three consequtive periods are supported.
    First dataset in input data is considered to be the current dataset, while the following ones are considered to be one period older.
    """
    def __init__(self, *args):
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
        self.dataset = [None] * len(args)
        import os
        if os.name == 'nt':
            """
            System test and branching for Windows based systems. Multiprocessing in CredPy has not been properly coded and tested for Windows machines.
            Due to that fact in case of Windows system the function moves on to single processing algorithm. It might influence performance dramatically
            on large datasets.
            """
            for c in range(len(args[:])):
                self.dataset[c] = crappend(args[c])

        else:
            """
            Multiprocessing for other systems beside Windows.
            """
            self.dataset = []
            import concurrent.futures            
            with concurrent.futures.ProcessPoolExecutor() as executor:
                self.results = [executor.submit(crappend, args[c]) for c in range(len(args[:]))]
                for f in concurrent.futures.as_completed(self.results):
                    self.dataset.append(f.result())

    def position(self, pos, n=0): # Getting distinguished balance sheet position
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
        return self.dataset[n][pos]

    # Weights function
    def weights(self, *args):
        """
        Weights function is used for calculating weights in dataset.

        For its usage it needs to have the target value (can be any of the dataset, but one),
        and weighted value (can be any of the dataset, and as many as wanted).

        Example:
            x.weights('inventory', 80000, 'equity', 'ta', 'cash')

            Retrieves weights for equity, total assets, and cash for the inventory to be
            over the 80.000.
        """

        import os
        if os.name == 'nt':
            """
            Single processing for Windows systems.
            """
            result  = [None] * len(self.dataset)
            self.modeldataset  = [None] * len(self.dataset)
            for c in range(len(self.dataset)):
                self.modeldataset[c] = self.dataset[c].loc[(self.dataset[c][args[0]] > args[1]), args[2:]].reset_index(drop=True)
                x  = [None] * len(args[2:])
                for i in args[2:]:
                    x[args.index(i)-2] = weight(args, i, self.dataset[c], self.modeldataset[c])
                result[c] = x
            return result
        else:
            """
            Multiprocessing for other systems beside Windows.
            """
            import concurrent.futures
            result  = [None] * len(self.dataset)
            self.modeldataset  = [None] * len(self.dataset)
            x = []
            for c in range(len(self.dataset)):
                self.modeldataset[c] = self.dataset[c].loc[(self.dataset[c][args[0]] > args[1]), args[2:]].reset_index(drop=True)
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    self.results = [executor.submit(weight, args, i, self.dataset[c], self.modeldataset[c]) for i in args[2:]]
                    for f in concurrent.futures.as_completed(self.results):
                        x.append(f.result())
                    result = x
            return result

    # Ratios function
    def ratio(self, ratiotype, n='all', days=365):
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
        self.ratiotype = ratiotype
        self.days = days

        import os
        if os.name == 'nt':
            """
            Single processing for Windows systems.
            """
            x  = [None] * len(self.dataset)
            for c in range(len(self.dataset)):
                x[c] = getratio(self.dataset[c], self.ratiotype, c, self.days)
            if n == 'all':
                return x
            else:
                return x[n]
        else:
            """
            Multiprocessing for other systems beside Windows.
            """
            import concurrent.futures
            result = []
            with concurrent.futures.ProcessPoolExecutor() as executor:
                self.results = [executor.submit(getratio, self.dataset[c], self.ratiotype, c, self.days) for c in range(len(self.dataset[:]))]
                for f in concurrent.futures.as_completed(self.results):
                    result.append(f.result())
                if n == 'all':
                    return result
                else:
                    return result[n]

    # Scoring function    
    """ 
    Ratios methods is used for applying ratio calculations on the appended dataset

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
    def score(self, model, modeltype="original", n='all', **kwargs):

        import os
        if os.name == 'nt':
            """
            Single processing for Windows systems.
            """
            x  = [None] * len(self.dataset)
            for c in range(len(self.dataset)): # This should be optimized to run only for the requested time series
                x[c] = scores(self.dataset[c], model, modeltype, kwargs)
            if n == 'all':
                return x
            else:
                return x[n]
        else:
            """
            Multiprocessing for other systems beside Windows.
            """
            import concurrent.futures
            result = []
            with concurrent.futures.ProcessPoolExecutor() as executor:
                self.results = [executor.submit(scores, self.dataset[c], model, modeltype, kwargs) for c in range(len(self.dataset[:]))] # Same here, can be optimized
                for f in concurrent.futures.as_completed(self.results):
                    result.append(f.result())
                if n == 'all':
                    return result
                else:
                    return result[n]

    # Machine learning framework
    """
    Machine learning methods are meant to easily use some of the popular statistical libraries and frameworks on financial datasets.
    This is more because CredPy has someone specific data structure so it is meant to make the work easier for the end user.
    Receantly added, should be rewritten soon in separate functions and with more comments.
    """
    
    def ml(self, model, xtestset, setnumber, targetvalue, *args, **kwargs):
        # Linear regression
        if (model[0] == "linreg"):
            import pandas as pd
            self.xtestset = crappend(xtestset)
            X_train = []
            X_test = []
            y_train = self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(targetvalue)].values
            for c in range(len(args)):
                X_train.append(self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(args[c])].values)
                X_test.append(self.xtestset.iloc[:, self.xtestset.columns.get_loc(args[c])].values)
            X_train = pd.DataFrame(X_train)
            X_train = X_train.transpose()
            y_train = pd.DataFrame(y_train)
            X_test = pd.DataFrame(X_test)
            X_test = X_test.transpose()

            if 'fit_intercept' not in kwargs:
                fit_intercept = True;
            else:
                fit_intercept = kwargs['fit_intercept']
                
            if 'normalize' not in kwargs:
                normalize = False;
            else:
                normalize = kwargs['normalize']
                
            if 'copy_X' not in kwargs:
                copy_X = True;
            else:
                copy_X = kwargs['copy_X']
                
            if 'n_jobs' not in kwargs:
                n_jobs = None;
            else:
                n_jobs = kwargs['n_jobs']

            from sklearn.linear_model import LinearRegression
            regressor = LinearRegression(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=n_jobs)
            regressor.fit(X_train, y_train)
            y_pred = regressor.predict(X_test)
            return y_pred
        
        # Polynomial regression
        if (model[0] == "polyreg"):
            import pandas as pd
            self.xtestset = crappend(xtestset)
            X_train = []
            X_test = []
            y_train = self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(targetvalue)].values
            for c in range(len(args)):
                X_train.append(self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(args[c])].values)
                X_test.append(self.xtestset.iloc[:, self.xtestset.columns.get_loc(args[c])].values)
            X_train = pd.DataFrame(X_train)
            X_train = X_train.transpose()
            y_train = pd.DataFrame(y_train)
            X_test = pd.DataFrame(X_test)
            X_test = X_test.transpose()
            
            if 'degree' not in kwargs:
                degree = 2;
            else:
                degree = kwargs['degree']
                
            if 'interaction_only' not in kwargs:
                interaction_only = False;
            else:
                interaction_only = kwargs['interaction_only']
                
            if 'include_bias' not in kwargs:
                include_bias = True;
            else:
                include_bias = kwargs['include_bias']
                
            if 'order' not in kwargs:
                order = 'C';
            else:
                order = kwargs['order']
                
            if 'fit_intercept' not in kwargs:
                fit_intercept = True;
            else:
                fit_intercept = kwargs['fit_intercept']
                
            if 'normalize' not in kwargs:
                normalize = False;
            else:
                normalize = kwargs['normalize']
                
            if 'copy_X' not in kwargs:
                copy_X = True;
            else:
                copy_X = kwargs['copy_X']
                
            if 'n_jobs' not in kwargs:
                n_jobs = None;
            else:
                n_jobs = kwargs['n_jobs']
            
            from sklearn.preprocessing import PolynomialFeatures
            from sklearn.linear_model import LinearRegression
            poly_reg = PolynomialFeatures(degree=degree, interaction_only=interaction_only, include_bias=include_bias, order=order)
            X_train = poly_reg.fit_transform(X_train)
            regressor = LinearRegression(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=n_jobs)
            regressor.fit(X_train, y_train)
            y_pred = regressor.predict(poly_reg.fit_transform(X_test))
            return y_pred
        
        # Support Vector Regression (SVR)
        if (model[0] == "SVR"):
            import pandas as pd
            self.xtestset = crappend(xtestset)
            X_train = []
            X_test = []
            y_train = self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(targetvalue)].values
            for c in range(len(args)):
                X_train.append(self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(args[c])].values)
                X_test.append(self.xtestset.iloc[:, self.xtestset.columns.get_loc(args[c])].values)
            X_train = pd.DataFrame(X_train)
            X_train = X_train.transpose()
            y_train = pd.DataFrame(y_train)
            X_test = pd.DataFrame(X_test)
            X_test = X_test.transpose()
            
            if 'kernel' not in kwargs:
                kernel = 'rbf';
            else:
                kernel = kwargs['kernel']
                
            if 'degree' not in kwargs:
                degree = 3;
            else:
                degree = kwargs['degree']
                
            if 'gamma' not in kwargs:
                gamma = 'scale';
            else:
                gamma = kwargs['gamma']
                
            if 'coef0' not in kwargs:
                coef0 = 0.0;
            else:
                coef0 = kwargs['coef0']
                
            if 'tol' not in kwargs:
                tol = 0.001;
            else:
                tol = kwargs['tol']

            if 'C' not in kwargs:
                C = 1.0;
            else:
                C = kwargs['C']

            if 'epsilon' not in kwargs:
                epsilon = 0.1;
            else:
                epsilon = kwargs['epsilon']
                                #### OVDE SAM STAO                
            if 'shrinking' not in kwargs:
                shrinking = True;
            else:
                shrinking = kwargs['shrinking']
                
            if 'cache_size' not in kwargs:
                cache_size = 200;
            else:
                cache_size = kwargs['cache_size']
                
            if 'verbose' not in kwargs:
                verbose = False;
            else:
                verbose = kwargs['verbose']
                
            if 'max_iter' not in kwargs:
                max_iter = -1;
            else:
                max_iter = kwargs['max_iter']

            from sklearn.preprocessing import StandardScaler
            sc_X = StandardScaler()
            sc_y = StandardScaler()
            X = sc_X.fit_transform(X_train)
            y = sc_y.fit_transform(y_train)
            from sklearn.svm import SVR
            regressor = SVR(kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, C=C, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose, max_iter=max_iter)
            regressor.fit(X, y)
            y_pred = sc_y.inverse_transform(regressor.predict(sc_X.transform(X_test)))            
            return y_pred
        
        # Decision Tree Regression
        if (model[0] == "decision_tree_reg"):
            import pandas as pd
            self.xtestset = crappend(xtestset)
            X_train = []
            X_test = []
            y_train = self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(targetvalue)].values
            for c in range(len(args)):
                X_train.append(self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(args[c])].values)
                X_test.append(self.xtestset.iloc[:, self.xtestset.columns.get_loc(args[c])].values)
            X_train = pd.DataFrame(X_train)
            X_train = X_train.transpose()
            y_train = pd.DataFrame(y_train)
            X_test = pd.DataFrame(X_test)
            X_test = X_test.transpose()
            
            if 'criterion' not in kwargs:
                criterion = 'mse';
            else:
                criterion = kwargs['criterion']
                
            if 'splitter' not in kwargs:
                splitter = 'best';
            else:
                splitter = kwargs['splitter']
                
            if 'max_depth' not in kwargs:
                max_depth = None;
            else:
                max_depth = kwargs['max_depth']

            if 'min_samples_split' not in kwargs:
                min_samples_split = 2;
            else:
                min_samples_split = kwargs['min_samples_split']
                
            if 'min_samples_leaf' not in kwargs:
                min_samples_leaf = 1;
            else:
                min_samples_leaf = kwargs['min_samples_leaf']
                
            if 'min_weight_fraction_leaf' not in kwargs:
                min_weight_fraction_leaf = 0.0;
            else:
                min_weight_fraction_leaf = kwargs['min_weight_fraction_leaf']
                
            if 'max_features' not in kwargs:
                max_features = None;
            else:
                max_features = kwargs['max_features']
                
            if 'random_state' not in kwargs:
                random_state = None;
            else:
                random_state = kwargs['random_state']
                
            if 'max_leaf_nodes' not in kwargs:
                max_leaf_nodes = None;
            else:
                max_leaf_nodes = kwargs['max_leaf_nodes']
                
            if 'min_impurity_decrease' not in kwargs:
                min_impurity_decrease = 0.0;
            else:
                min_impurity_decrease = kwargs['min_impurity_decrease']
                
            if 'min_impurity_split' not in kwargs:
                min_impurity_split = 0;
            else:
                min_impurity_split = kwargs['min_impurity_split']
                
            if 'ccp_alpha' not in kwargs:
                ccp_alpha = 0.0;
            else:
                ccp_alpha = kwargs['ccp_alpha']

            from sklearn.tree import DecisionTreeRegressor
            regressor = DecisionTreeRegressor(criterion=criterion, splitter=splitter, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features, random_state=random_state, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease, min_impurity_split=min_impurity_split, ccp_alpha=ccp_alpha)
            regressor.fit(X_train, y_train)

            # Predicting a new result
            y_pred = regressor.predict(X_test)
            return y_pred
        
        # Random Forest Regression
        if (model[0] == "random_forest_reg"):
            import pandas as pd
            self.xtestset = crappend(xtestset)
            X_train = []
            X_test = []
            y_train = self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(targetvalue)].values
            for c in range(len(args)):
                X_train.append(self.dataset[setnumber].iloc[:, self.dataset[setnumber].columns.get_loc(args[c])].values)
                X_test.append(self.xtestset.iloc[:, self.xtestset.columns.get_loc(args[c])].values)
            X_train = pd.DataFrame(X_train)
            X_train = X_train.transpose()
            y_train = pd.DataFrame(y_train)
            X_test = pd.DataFrame(X_test)
            X_test = X_test.transpose()
            
            if 'n_estimators' not in kwargs:
                n_estimators = 100;
            else:
                n_estimators = kwargs['n_estimators']
                
            if 'criterion' not in kwargs:
                criterion = 'mse';
            else:
                criterion = kwargs['criterion']
                
            if 'max_depth' not in kwargs:
                max_depth = None;
            else:
                max_depth = kwargs['max_depth']
                
            if 'min_samples_split' not in kwargs:
                min_samples_split = 2;
            else:
                min_samples_split = kwargs['min_samples_split']
                
            if 'min_samples_leaf' not in kwargs:
                min_samples_leaf = 1;
            else:
                min_samples_leaf = kwargs['min_samples_leaf']
                
            if 'min_weight_fraction_leaf' not in kwargs:
                min_weight_fraction_leaf = 0.0;
            else:
                min_weight_fraction_leaf = kwargs['min_weight_fraction_leaf']
                
            if 'max_features' not in kwargs:
                max_features = 'auto';
            else:
                max_features = kwargs['max_features']
                
            if 'max_leaf_nodes' not in kwargs:
                max_leaf_nodes = None;
            else:
                max_leaf_nodes = kwargs['max_leaf_nodes']
                
            if 'min_impurity_decrease' not in kwargs:
                min_impurity_decrease = 0.0;
            else:
                min_impurity_decrease = kwargs['min_impurity_decrease']
                
            if 'min_impurity_split' not in kwargs:
                min_impurity_split = None;
            else:
                min_impurity_split = kwargs['min_impurity_split']
                
            if 'bootstrap' not in kwargs:
                bootstrap = True;
            else:
                bootstrap = kwargs['bootstrap']
                
            if 'oob_score' not in kwargs:
                oob_score = False;
            else:
                oob_score = kwargs['oob_score']
                
            if 'n_jobs' not in kwargs:
                n_jobs = None;
            else:
                n_jobs = kwargs['n_jobs']
                
            if 'random_state' not in kwargs:
                random_state = None;
            else:
                random_state = kwargs['random_state']
                
            if 'verbose' not in kwargs:
                verbose = 0;
            else:
                verbose = kwargs['verbose']
                
            if 'warm_start' not in kwargs:
                warm_start = False;
            else:
                warm_start = kwargs['warm_start']
                
            if 'ccp_alpha' not in kwargs:
                ccp_alpha = 0.0;
            else:
                ccp_alpha = kwargs['ccp_alpha']
                
            if 'max_samples' not in kwargs:
                max_samples = None;
            else:
                max_samples = kwargs['max_samples']
                
            from sklearn.ensemble import RandomForestRegressor
            regressor = RandomForestRegressor(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features, min_impurity_decrease=min_impurity_decrease, min_impurity_split=min_impurity_split, bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs, random_state=random_state, verbose=verbose, warm_start=warm_start, ccp_alpha=ccp_alpha, max_samples=max_samples)
            regressor.fit(X_train, y_train)
            y_pred = regressor.predict(X_test)
            
            return y_pred

        
        
        
    
    