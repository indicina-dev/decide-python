## decide-python-package
![img.png](assets/img.png)

![PyPI](https://img.shields.io/pypi/v/indicina-decide)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/indicina-decide)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/indicina-dev/decide-python/ci-cd/v0.0.0)
---
**Table of contents**
- [About](#about)
- [Using the App](#using-the-app)
    - [Installation](#installation)
    - [Authorization](#authorization)
      - [sh](#sh)
      - [Python](#python)
    - [Sample Code](#sample-code)
      - [JSON STATEMENT](#json-statement)
      - [PDF Statement](#pdf-statement)
      - [CSV Statement](#csv-statement)
      - [Sample Response](#sample-response)
- [Contribution](#contribution)
  - [Setup Project](#setup-project)
    - [Cloning the project](#cloning-the-project)
        - [For HTTPS](#for-https)
        - [For SSH](#for-ssh)
      - [Running the project](#running-the-project)
  - [Contribute to Project](#contribute-to-project)
  - [Issues](#issues)

---
# About
Decide helps users make risk-free decisions based on an analysis of their banking transactions using extracted financial data.
The Decide SDK helps developers plug into the functionalities of Decide from their python projects.

# Using the App
### Installation
In your python project use the command `pip install indicina-decide` to install the Decide SDK

### Authorization
#### sh
```
export INDICINA_CLIENT_ID=my_id
export INDICINA_CLIENT_SECRET=my_secret
```
#### Python
```
import os

os.environ["INDICINA_CLIENT_ID"] = "my_id"
os.environ["INDICINA_CLIENT_SECRET"] = "my_secret"
```

You can get your `INDICINA_CLIENT_ID` and `INDICINA_CLIENT_SECRET` from [GitHub Pages](https://developers.indicina.co/docs/decide-api-keys).

### Sample Code
#### JSON STATEMENT
```
from decide.models.analysis import Analysis
from decide.models.customer import Customer
from decide.models.statement import JSONStatement
import json

statement = json.loads("""{
    "paging": {
        "total": 190,
        "page": 2,
        "previous": "https://api.withmono.com/accounts/:id/transactions?page=2",
        "next": "https://api.withmono.com/accounts/:id/transactions?page=3"
    },
    "data": [
        {
            "_id": "12345",
            "amount": 10000,
            "date": "2020-07-21T00:00:00.000Z",
            "narration": "TRANSFER from *************",
            "type": "debit",
            "category": "E-CHANNELS"
        },
        {
            "_id": "12345",
            "amount": 20000,
            "date": "2020-07-21T00:00:00.000Z",
            "narration": "TRANSFER from ***********",
            "type": "debit",
            "category": "E-CHANNELS"
        }
    ]
}""")

statement = JSONStatement(statement_format=StatementFormat.MBS, statement=json_statement, customer=customer)
analyis: Analysis = statement.analyze()

print(analysis)
print(f"Analysis status is: {analysis.status}")

```

#### PDF Statement

```
from decide import PDFStatement
from decide.models.analysis import Analysis
...
statement = PDFStatement(customer=customer,
                         pdf_path="statement.pdf",
                         bank=Bank.ACCESS,
                         currency=Currency.NGN)

analyis: Analysis = statement.analyze()

print(analysis)
print(f"Analysis status is: {analysis.status}")

```

#### CSV Statement
```
from decide import CSVStatement
from decide.models.analysis import Analysis

...
statement = CSVStatement(csv_path="AverageOtherIncome.csv",
                         customer=customer)
analyis: Analysis = statement.analyze()
```

#### Sample Response
```
{
    "status": "success",
    "data": {
        "country": "Nigeria",
        "currency": "NGN",
        "behaviouralAnalysis": {
            "accountSweep": "No",
            "gamblingRate": 0,
            "inflowOutflowRate": "Neutral Cash Flow",
            "loanAmount": 2000,
            "loanInflowRate": 0,
            "loanRepaymentInflowRate": 0,
            "loanRepayments": 54500,
            "topIncomingTransferAccount": "The",
            "topTransferRecipientAccount": "Day"
        },
        "cashFlowAnalysis": {
            "accountActivity": 0.84,
            "averageBalance": 1815942.46,
            "averageCredits": 153741.4861589404,
            "averageDebits": 31563.282248447216,
            "closingBalance": -202978.97,
            "firstDay": "2022-05-18",
            "lastDay": "2022-10-18",
            "monthPeriod": "May - October",
            "netAverageMonthlyEarnings": -1875144.8599999999,
            "noOfTransactingMonths": 6,
            "totalCreditTurnover": 23214964.409999996,
            "totalDebitTurnover": 25408442.21000001,
            "yearInStatement": "2022",
            "maxEmiEligibility": 48871,
            "emiConfidenceScore": 0.04
        },
        "incomeAnalysis": {
            "salaryEarner": "Yes",
            "medianIncome": 83150,
            "averageOtherIncome": 69187.43,
            "expectedSalaryDay": 25,
            "lastSalaryDate": "2022-08-25",
            "averageSalary": 2290408.08,
            "confidenceIntervalonSalaryDetection": 1,
            "salaryFrequency": "1",
            "numberSalaryPayments": 3,
            "numberOtherIncomePayments": 15,
            "gigWorker": "No"
        },
        "spendAnalysis": {
            "averageRecurringExpense": 360140.42,
            "hasRecurringExpense": "Yes",
            "averageMonthlyExpenses": 4234740.37,
            "expenseChannels": `expenseChannels`,(bills, entertainment,savingsAndInvestments,gambling,airtime,bankCharges,chequeWithdrawal,cashWithdrawal,shopping, eatingOut)
            "expenseCategories": `expenseCategories`
        },
        "transactionPatternAnalysis": {
            "MAWWZeroBalanceInAccount": {
                "month": null,
                "week_of_month": 0
            },
            "NODWBalanceLess5000": 35,
            "NODWBalanceLess": {
                "amount": 5000,
                "count": 35
            },
            "highestMAWOCredit": {
                "month": "August",
                "week_of_month": 3
            },
            "highestMAWODebit": {
                "month": "August",
                "week_of_month": 5
            },
            "lastDateOfCredit": "2022-10-17",
            "lastDateOfDebit": "2022-10-18",
            "mostFrequentBalanceRange": ">500000",
            "mostFrequentTransactionRange": "<10000",
            "recurringExpense": [
                {
                    "amount": 1650,
                    "description": "spend and save"
                },
                {
                    "amount": 4000,
                    "description": "airtime purchase 2347049215992"
                },
                {
                    "amount": 5000,
                    "description": "fuel"
                }
            ],
            "transactionsBetween100000And500000": 39,
            "transactionsBetween10000And100000": 176,
            "transactionsGreater500000": 24,
            "transactionsLess10000": 717,
            "transactionRanges": [
                {
                    "min": 10000,
                    "max": 100000,
                    "count": 176
                },
                {
                    "min": 100000,
                    "max": 500000,
                    "count": 39
                },
                {
                    "min": null,
                    "max": 10000,
                    "count": 717
                },
                {
                    "min": 500000,
                    "max": null,
                    "count": 24
                }
            ]
        }
    }
}

```

# Contribution
## Setup Project
The link for this projects's repository can be found [here](decide-python.git)
### Cloning the project

##### For HTTPS
Use this command `git clone https://github.com/indicina-dev/decide-python.git`

##### For SSH
Use this command `git clone git@github.com:indicina-dev/decide-python.git`

#### Running the project
- Create virtual enviroment
- Install the requirements.txt file `pip install -r requirements.txt`
- Run files

## Contribute to Project
Do you find the project interesting and you would like to contribute to our project?
- Fork the repository to your github account
- Clone the repository to your local machine
- Create a new branch for your fix (preferably descriptive to your contribution)
- Make appropriate changes and tests for the changes
- Use `git add insert-paths-of-changed-files-here` to add the file contents of the changed files to the "snapshot" git uses for project management
- Committing: As a means to create a seamless development and contribution flow, we require that commits be standardized, following the conventional [commits guideline](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

We have included the hook script to verify your commits, you will need to install it as follows:
```
pip install pre-commit
pre-commit install --hook-type commit-msg
```

Examples of good commits:
1. adding a new feature: `git commit -m "feat: allow provided config object to extend other configs"`

2. adding a breaking change, take note of the _!_ : `git commit -m "feat!: send an email to the customer when a product is shipped"`
- Push the changes to the remote repository using `git push origin branch-name-here`
- Submit a pull request to the upstream repository
- Title the pull request with a short description of the changes made and the issue or bug number associated with your change. For example, you can title an issue like so `Added more log outputting to resolve #4352`.
- Wait for our in-house developers to approve the merge requests or update the merge requests if changes were requested,

## Issues
To create an issue, simply click on the issues tab on the menu and create a new issue.


