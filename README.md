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
      - [Supported Banks](#supported-banks)
      - [Analysis Result](#analysis)
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

- **Website:** https://developers.indicina.co
- **Documentation:** https://developers.indicina.co/docs/decide-python-library

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

statement = JSONStatement(statement_format=StatementFormat.MONO, statement=json_statement, customer=customer)
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

print(analysis)
print(f"Analysis status is: {analysis.status}")
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

#### Supported Banks
In selecting a bank to use for analysis, we maintain an ENUM of supported banks [here](decide/models/enums.py#L13). We have also provided a convenient method to fetch a current list of supported banks.

```
from decide import PDFStatement, Bank

# Enum selection of Bank
statement = PDFStatement(
            ...,
            bank=Bank.GTB,
            ...)
```

```
from decide import Bank

# Get bank list
supported_bank_list = Bank.get_bank_list()


print(supported_bank_list)

output: A list of tuples [(bank_name, bank_code)]
[('Guaranty Trust Bank', '058'), ('Access Bank', '044')...]
```

#### Analysis
When the Decide API sends a response, the response is represented in the Analysis class.

Anatomy of an Analysis
```
Analysis
|
|-- behaviouralAnalysis: `BehaviouralAnalysis`
|       |-- accountSweep
|       |-- gamblingRate
|       |-- inflowOutflowRate
|       |-- loanInflowRate
|       |-- loanRepaymentInflowRate
|       |-- loanRepayments
|       |-- topIncomingTransferAccount
|       |-- topTransferRecipientAccount
            |-- loanAmount
|
|-- cashFlowAnalysis: `CashFlowAnalysis`
|       |-- accountActivity
|       |-- averageBalance
|       |-- averageCredits
|       |-- averageDebits
|       |-- closingBalance
|       |-- firstDay
|       |-- lastDay
|       |-- monthPeriod
|       |-- netAverageMonthlyEarnings
|       |-- noOfTransactingMonths
|       |-- totalCreditTurnover
|       |-- totalDebitTurnover
|       |-- yearInStatement
|
|-- incomeAnalysis: `IncomeAnalysis`
|       |-- averageOtherIncome
|       |-- averageSalary
|       |-- confidenceIntervalOnSalaryDetection
|       |-- expectedSalaryDay
|       |-- lastSalaryDate
|       |-- medianIncome
|       |-- numberOtherIncomePayments
|       |-- numberOfSalaryPayments
|       |-- salaryEarner
|       |-- salaryFrequency
|       |-- gigWorker
|
|-- spendAnalysis: `SpendAnalysis`
|       |-- expenseChannels: `ExpenseChannels`
|       |       |-- atmSpend
|       |       |-- webSpend
|       |       |-- posSpend
|       |       |-- ussdTransactions
|       |       |-- mobileSpend
|       |       |-- spendOnTransfers
|       |       |-- internationalTransactionsSpend
|       |-- expenseCategories: `ExpenseCategories`
|       |       |-- bills
|       |       |-- entertainment
|       |       |-- savingsAndInvestments
|       |       |-- gambling
|       |       |-- airtime
|       |       |-- bankCharges
|       |-- averageRecurringExpense
|       |-- hasRecurringExpense
|       |-- totalExpenses
|-- transactionPatternAnalysis: `TransactionPatternAnalysis`
|       |-- highestMAWOCredit
|       |-- highestMAWODebit
|       |-- lastDateOfCredit
|       |-- lastDateOfDebit
|       |-- MAWWZeroBalanceInAccount
|       |-- mostFrequentBalanceRange
|       |-- mostFrequentTransactionRange
|       |-- NODWBalanceLess5000
|       |-- recurringExpense
|       |-- transactionsBetween100000And500000
|       |-- transactionsBetween10000And100000
|       |-- transactionsGreater500000
|       |-- transactionsLess10000
|       |-- transactionRanges
|       |-- NODWBalanceLess
|-- status
```

**Analysis Status**

Some bank statement analyses (e.g. PDF) are asynchronous. You may not get the results of the analysis immediately.

You may need to get the status of an analysis.

PDFStatus could take one of the following values.

| Status	  | Value	     | Description                       |
| ----------- | ------------ | --------------------------------- |
| DONE	      | DONE	     | The analysis is done              |
| FAILED	  | FAILED	     | The analysis failed               |
| IN_PROGRESS | IN_PROGRESS	 | The analysis is still in progress |

```
# Example usage on accessing the analysis response
analysis = statement.analyze()
print(f"Analysis status is: {analysis.status}")

# wait for analysis to be done
time.sleep(3)

print(analysis)
print(f"Analysis status is: {analysis.status}")
print(f"Credit turnover is: {analysis.cashFlowAnalysis.totalCreditTurnover}")
print(f"Average salary is: {analysis.incomeAnalysis.averageSalary}")
print(f"{analysis.behaviouralAnalysis}")
print(analysis.transaction_tags)
```

### Rules Engine Documentation

The Rules Engine enables merchants to set up an automated decisioning process for lending, based on pre-determined conditions tailored to their unique use case. It allows users to:

- Develop multiple rule-based conditions
- Analyze statements with pre-determined conditions and rules that automate the decision-making process
- Automatically filter qualifying applications based on the set rules
- Set up an affordability logic to reveal what applicants can pay back

#### Import Required Libraries
```python
from decide.models.rules_engine import (
    Rule, RuleType, Condition, Operator, Outcome, Block, Status, BooleanRuleSet, Affordability, Duration, ScorecardAPI, ScorecardRequest, ScorecardResponse, ScorecardExecuteRequest)
```

#### Set Environment Variables
```python
import os
os.environ["INDICINA_CLIENT_ID"] = "xxxxxx"
os.environ["INDICINA_CLIENT_SECRET"] = "xxxxx"
```

#### Initialize ScorecardAPI
```python 
sc = ScorecardAPI()
```

#### Create Scorecard
`Define Rules`

A Rule is defined as a condition to be evaluated on a certain value. You can have as many rules as you need. A Rule consists of several properties, including:

- order: an integer representing the order in which the rule is evaluated
- rule_type: an Enum representing the type of rule (e.g., average balance, loan amount, etc.)
- value: a string representing the value of the rule (e.g., "10000" for an average balance of 10,000)
- condition: an ENUM representing the condition to be evaluated (e.g., "is equal to", "less than or equal to", etc.)
- operator: an ENUM representing the logical operator to be used when evaluating the rule (e.g., "and", "or", etc.)

For example, the first rule defined in the code states that the average balance of an account must be exactly 10,000.

```python
rules = [
    Rule(order=1, rule_type=RuleType.AVERAGE_BALANCE, value="10000", condition=Condition.IS_EQUAL, operator=Operator.OPERATOR_AND),
    Rule(order=2, rule_type=RuleType.AVERAGE_CREDITS, value="5000", condition=Condition.IS_EQUAL, operator=Operator.OPERATOR_AND),
    Rule(order=3, rule_type=RuleType.LOAN_AMOUNT, value="20000", condition=Condition.LESS_THAN_EQUAL_TO, operator=Operator.OPERATOR_AND),]
```

`Create a Block`

A Block is a collection of Rule objects that are evaluated together using a logical operator (e.g., "and", "or", etc.). A Block consists of several properties, including:

rules: a list of Rule objects
order: an integer representing the order in which the block is evaluated
operator: an ENUM representing the logical operator to be used when evaluating the block (e.g., "and", "or", etc.)
negative_outcome: an Enum representing the outcome of the block if the evaluation is false
```python
block = Block(rules=rules, order=1, operator=Operator.OPERATOR_NONE, negative_outcome=Outcome.DECLINE)
```

`Create a Boolean Rule Set`

A BooleanRuleSet is a collection of Block objects that are evaluated together using a logical operator (e.g., "and", "or", etc.). A BooleanRuleSet consists of several properties, including:

- name: a string representing the name of the rule set
- positive_outcome: an ENUM representing the outcome of the rule set if the evaluation is true
- negative_outcome: an ENUM representing the outcome of the rule set if the evaluation is false
- owner: a string representing the owner of the rule set
- blocks: a list of Block objects
```python
boolean_rule_set = BooleanRuleSet(name="DPL", positive_outcome=Outcome.ACCEPT, negative_outcome=Outcome.DECLINE, owner="indicina", blocks=[block])
```

`Define Affordability Logic`

Affordability logic defines the logic to determine what the applicant can pay back. It is made up of two properties:

- monthly_interest_rate: interest rate per month
- monthly_durations: a list of Duration objects representing the tenures they wish to provide their service for
```python
affordability_logic = Affordability(monthly_interest_rate=10, monthly_durations=[Duration(3), Duration(4)])
```

`Create a Scorecard Request`

The ScorecardRequest object is the final object that is created and is used to make requests to the ScorecardAPI. It contains the name of the scorecard, the boolean rule set, the affordability logic, and the status of the scorecard (whether it is enabled or disabled).

```python
sc_request = ScorecardRequest(name="DPL", boolean_rule_set=boolean_rule_set, affordability=affordability_logic, status=Status.ENABLED)
scorecard = sc.create_scorecard(sc_request)
scorecard.scorecard_id
```

`Read Scorecard`

To retrieve an existing scorecard, we can use the get_scorecard method. The method takes the ID of the scorecard as input and returns a Scorecard object.

```python
card_61 = sc.read_scorecard("61")
```

`Update Scorecard`

We can create a new ScorecardRequest object with the updated information and use the update_scorecard method. The method takes the ID of the scorecard and the new ScorecardRequest object as input and updates the scorecard with the new information.

```python
rules = [
    Rule(order=1, rule_type=RuleType.AVERAGE_BALANCE, value="1000", condition=Condition.IS_EQUAL, operator=Operator.OPERATOR_AND),
    Rule(order=2, rule_type=RuleType.AVERAGE_CREDITS, value="500", condition=Condition.IS_EQUAL, operator=Operator.OPERATOR_AND),
    Rule(order=3, rule_type=RuleType.LOAN_AMOUNT, value="2000", condition=Condition.LESS_THAN_EQUAL_TO, operator=Operator.OPERATOR_AND),
]

block = Block(rules=rules, order=1, operator=Operator.OPERATOR_NONE, negative_outcome=Outcome.DECLINE)

boolean_rule_set = BooleanRuleSet(name="DPL", positive_outcome=Outcome.ACCEPT, negative_outcome=Outcome.DECLINE, owner="indicina", blocks=[block])

affordability_logic = Affordability(20, [Duration(5), Duration(14)])

sc_updated_request = ScorecardRequest(name="DPL_CHANGE_NAME", boolean_rule_set=boolean_rule_set, affordability=affordability_logic, status=Status.ENABLED)
card_61_updated = sc.update_scorecard(str(card_61.scorecard_id), sc_updated_request)
```

`Delete Scorecard`

To delete an existing scorecard, we can use the delete_scorecard method. The method takes the ID of the scorecard as input and deletes the scorecard.

```python
sc.delete_scorecard(str(card_61.scorecard_id))
```

`Execute Scorecard on Analysis`

To execute a scorecard on an existing Analysis, we can use the execute_scorecard method. The method takes the ID of the existing analysis as input and a list of scorecard IDs to run on the analysis.

```python
a_id = "xxxxxxxxxxxxxxxxxxx"
s_ids = [32, 45, 47]
scorecard_execute_request = ScorecardExecuteRequest(analysis_id=a_id, scorecard_ids=s_ids)
res = sc.execute_scorecard(scorecard_execute_request)
print(res['scorecardResults'])
```

`Analyse statement with Scorecard`

To analyse a statement with some already created scorecards/rules, pass in the ids of the scorecards as below:

```python
statement = JSONStatement(statement_format=StatementFormat.MONO, statement=statement, customer=customer, scorecard_ids=[47])
analysis: Analysis = statement.analyze()

print(analysis)
print(f"Analysis status is: {analysis.status}")
```

This concludes the documentation for using the Rules Engine, which covers creating, updating, deleting, and executing scorecards on existing analyses. Use this guide as a reference for implementing the automated decision-making process tailored to your specific lending use case.


# Contribution
## Setup Project
The link for this projects's repository can be found [here](https://github.com/indicina-dev/decide-python)
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


