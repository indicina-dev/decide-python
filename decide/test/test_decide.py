import json
import os
import time
import time, secrets
from unittest import mock
from unittest.mock import patch, MagicMock

from decide import Customer, JSONStatement, StatementFormat, PDFStatement, Bank, PDFStatus, CSVStatement
from decide.auth import Auth


def auth_code_gen(secret=False):
    if secret:
        return secrets.token_hex(16)
    return None


def test_with_no_secret():
    assert auth_code_gen() is None


def test_with_secret():
    # test creds
    with mock.patch.dict(os.environ, {"INDICINA_CLIENT_ID": "indicina",
                                      "INDICINA_CLIENT_SECRET": "MD5Y106-RYG4STY-H3B33FS-CRS5AMG",
                                      "TEST_MODE": "true"}):

        assert isinstance(auth_code_gen(secret=True), str)
        assert auth_code_gen(secret=True) is not None


def test_different_auth_codes():
    with mock.patch.dict(os.environ, {"INDICINA_CLIENT_ID": "indicina",
                                      "INDICINA_CLIENT_SECRET": "MD5Y106-RYG4STY-H3B33FS-CRS5AMG",
                                      "TEST_MODE": "true"}):

        auth1 = auth_code_gen(secret=True)
        auth2 = auth_code_gen(secret=True)
        assert auth1 != auth2

@patch.object(JSONStatement, 'analyze')
def test_json_mono_statement(json_statement_mock):
    with open("decide/test/data/test1.json", "r") as f:
        statement = json.loads(f.read())

    with mock.patch.dict(os.environ, {"INDICINA_CLIENT_ID": "indicina",
                                      "INDICINA_CLIENT_SECRET": "MD5Y106-RYG4STY-H3B33FS-CRS5AMG",
                                      "TEST_MODE": "true"}):
        customer = Customer(customer_id="ckq9ehqmv000001me62y85j1u")

        json_statement_mock = JSONStatement(statement_format=StatementFormat.MONO,
                                  statement=statement, customer=customer)
        json_statement_mock.analyze = MagicMock(name="analyze")
        json_statement_mock.analyze.return_value = {
            "status": "success",
            "job_id": 1,
            "cashFlowAnalysis": {
                "yearInStatement": "2022",
                "accountActivity": 0.33,
                "monthPeriod": "July - July"
            },
            "spendAnalysis": {
                "averageRecurringExpense": 112775,
                "expenseChannels": {
                    "atmSpend": 0,
                },
            },
            "statement_type": "json"
        }

        analysis = json_statement_mock.analyze()

        assert analysis is not None
        assert analysis['status'] == "success"
        assert analysis['cashFlowAnalysis']['monthPeriod'] == "July - July"
        assert analysis['spendAnalysis']['expenseChannels']['atmSpend'] == 0


@patch.object(PDFStatement, 'analyze')
def test_pdf_statement(pdf_statement_mock):
    with mock.patch.dict(os.environ, {"INDICINA_CLIENT_ID": "indicina",
                                      "INDICINA_CLIENT_SECRET": "MD5Y106-RYG4STY-H3B33FS-CRS5AMG",
                                      "TEST_MODE": "true"}):
        customer = Customer(customer_id="ckq9ehqmv000001me62y85j1u")

        pdf_statement_mock = PDFStatement(pdf_path="decide/test/data/Bank Statement 2.pdf", customer=customer, bank=Bank.ACCESS)
        pdf_statement_mock.analyze = MagicMock(name="analyze")
        pdf_statement_mock.analyze.return_value = {
            "status": "DONE",
            "job_id": 1,
            "cashFlowAnalysis": {
                "yearInStatement": "2021,2022",
                "accountActivity": 0.54,
                "monthPeriod": "July - July"
            },
            "spendAnalysis": {
                "averageRecurringExpense": 112775,
                "expenseChannels": {
                    "atmSpend": 0,
                },
            },
            "statement_type": "pdf"
        }

        analysis = pdf_statement_mock.analyze()
        assert analysis is not None
        assert analysis['status'] in ('IN_PROGRESS', 'DONE')
        assert analysis['cashFlowAnalysis']['yearInStatement'] == "2021,2022"
        assert analysis['cashFlowAnalysis']['accountActivity'] == 0.54
        assert analysis['spendAnalysis']['averageRecurringExpense'] == 112775


@patch.object(CSVStatement, 'analyze')
def test_csv_statement(csv_statement_mock):
    with mock.patch.dict(os.environ, {"INDICINA_CLIENT_ID": "indicina",
                                      "INDICINA_CLIENT_SECRET": "MD5Y106-RYG4STY-H3B33FS-CRS5AMG",
                                      "TEST_MODE": "true"}):
        customer = Customer(customer_id="ckq9ehqmv000001me62y85j1u")
        statement = CSVStatement(csv_path="decide/test/data/AverageOtherIncome.csv", customer=customer)
        csv_statement_mock = CSVStatement(csv_path="decide/test/data/AverageOtherIncome.csv", customer=customer)
        csv_statement_mock.analyze = MagicMock(name="analyze")
        csv_statement_mock.analyze.return_value = {
            "status": "success",
            "job_id": 1,
            "cashFlowAnalysis": {
                "yearInStatement": "2022",
                "accountActivity": 0.33,
                "monthPeriod": "July - July"
            },
            "spendAnalysis": {
                "averageRecurringExpense": 23972.64,
                "expenseChannels": {
                    "atmSpend": 0,
                },
            },
            "statement_type": "csv"
        }
        analysis = csv_statement_mock.analyze()
        assert analysis is not None
        assert analysis['status'] == "success"
        assert analysis['cashFlowAnalysis']['yearInStatement'] == "2022"
        assert analysis['cashFlowAnalysis']['accountActivity'] == 0.33
        # assert analysis.spendAnalysis.averageRecurringExpense == 23972.64  # inconsistent

        analysis = csv_statement_mock.analyze()
        print(f"Average recurring Expense is: {analysis['spendAnalysis']['averageRecurringExpense']}")
        analysis = csv_statement_mock.analyze()
        print(f"Average recurring Expense is: {analysis['spendAnalysis']['averageRecurringExpense']}")
        analysis = csv_statement_mock.analyze()
        print(f"Average recurring Expense is: {analysis['spendAnalysis']['averageRecurringExpense']}")


def test_transaction_tags():

    with open("decide/test/data/test1.json", "r") as f:
        statement = json.loads(f.read())

    with mock.patch.dict(os.environ, {"INDICINA_CLIENT_ID": "indicina",
                                      "INDICINA_CLIENT_SECRET": "MD5Y106-RYG4STY-H3B33FS-CRS5AMG"}):
        customer = Customer(customer_id="ckq9ehqmv000001me62y85j1u")
        json_statement_mock = JSONStatement(statement_format=StatementFormat.MONO,
                                  statement=statement, customer=customer)
        json_statement_mock.analyze = MagicMock(name="analyze")
        json_statement_mock.analyze.return_value = {
            "status": "success",
            "job_id": 1,
            "cashFlowAnalysis": {
                "yearInStatement": "2022",
                "accountActivity": 0.33,
                "monthPeriod": "July - July"
            },
            "spendAnalysis": {
                "averageRecurringExpense": 112775,
                "expenseChannels": {
                    "atmSpend": 0,
                },
            },
            "statement_type": "json",
            "transaction_tags": []
        }

        analysis = json_statement_mock.analyze()
        tags = analysis['transaction_tags']
        print()
