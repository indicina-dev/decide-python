from abc import abstractmethod

from .analysis import Analysis
from .client import DecideClient
from .customer import Customer
from .enums import Currency, Bank, StatementType, StatementFormat
from typing import Optional, List


class DecideStatement:

    request_body: dict = None
    statement_type: StatementType = None
    job_id: str = None

    def __init__(self, path: str, content_type: str):
        self.client = DecideClient(f"client/{path}", content_type)

    def analyze(self) -> Analysis:
        """
        Example:
        statement = JSONStatement()
        analysis = statement.analyze()
        :return: returns an analysis of the bank statement using the Indicina Decide API
        :rtype: Analysis
        """

        """
        Make a call to the Indicina Decide API.
        Example:
            analysis = statement.analyze()
        """
        self.build_request_body()
        json_response = self.client.post(self.request_body)
        job_id = json_response["data"].get("jobId", None)
        return Analysis(data=json_response["data"],
                        status=json_response["status"],
                        statement_type=self.statement_type,
                        job_id=job_id)

    @abstractmethod
    def build_request_body(self) -> None:
        raise NotImplementedError()


class PDFStatement(DecideStatement):
    """
    Example:
        pdf  = PDFStatement("my_statement.pdf", bank=Bank.UBA, customer=customer,
                            password="pdf_pass", scorecard_ids=[1,2,3])
        analysis = pdf.analyze()
    """
    def __init__(self, pdf_path: str,
                 bank: Bank,
                 customer: Customer,
                 currency: Currency = Currency.NGN,
                 password: str = None, scorecard_ids: Optional[List[int]] = None):
        """
        To create a statement for PDF analysis
        :param pdf_path: Path to the bank statement in PDF format
        :type pdf_path: str
        :param bank: The bank from which the account originated
        :type bank: Bank
        :param customer: The customer who owns the statement
        :type customer: Customer
        :param currency: The currency used in the statement
        :type currency: Currency
        :param password: Password to the document (if required)
        :type password: str
        :param scorecard_ids: Optional list of scorecard ids to run on the statement
        :type scorecard_ids: list[int]
        """
        super().__init__("pdf/extract", "multipart/form-data")
        self.statement_type = StatementType.PDF

        self.pdf_path = pdf_path
        self.customer_id = customer.customer_id
        self.bank_code = bank
        self.currency = currency
        self.password = password
        self.scorecard_ids = scorecard_ids

    def build_request_body(self) -> None:
        self.request_body = {
            "pdf": self.pdf_path,
            "bank_code": self.bank_code.value,
            "currency": self.currency.value,
            "request_type": "score",
            "customer_id": self.customer_id
        }
        if self.scorecard_ids:
            self.request_body["scorecardIds"] = self.scorecard_ids

        if self.password:
            self.request_body["pdf_password"] = self.password


class CSVStatement(DecideStatement):
    """
    Example:
        csv = CSVStatement("statement.csv", customer=customer, scorecard_ids=[1,2,3])
        csv.analyze()
    """
    def __init__(self, csv_path: str,
                 customer: Customer, scorecard_ids: Optional[List[int]] = None):
        """
        To create a statement for CSV analysis

        :param csv_path: Path to the CSV file
        :type csv_path: str
        :param customer: The customer who owns the statement
        :type customer: Customer
        :param scorecard_ids: Optional list of scorecard ids to run on the statement
        :type scorecard_ids: list[int]
        """
        super().__init__("bsp/file", "multipart/form-data")
        self.statement_type = StatementType.CSV
        self.customer_id = customer.customer_id
        self.csv_path = csv_path
        self.scorecard_ids = scorecard_ids

    def build_request_body(self) -> None:
        self.request_body = {
            "file_statement": self.csv_path,
            "customer[id]": self.customer_id
        }
        if self.scorecard_ids:
            self.request_body["scorecardIds"] = self.scorecard_ids


class JSONStatement(DecideStatement):
    """
    Example:
        json_statement = JSONStatement(StatementFormat.MONO, json_statement, customer=customer, scorecard_ids=[1,2,3])
        json_statement.analyze()
    """
    def __init__(self, statement_format: StatementFormat, statement: dict,
                 customer: Customer, scorecard_ids: Optional[List[int]] = None):
        """
        To create a statement for JSON analysis
        :param statement_format: The bank statement format. This usually depends
        on the source of the statement (MONO, OKRA, MBS, CUSTOM)
        :type statement_format: StatementFormat
        :param statement: The bank statement
        :type statement: dict
        :param customer: The customer whose statement is to be analyzed.
        :type customer: Customer
        :param scorecard_ids: Optional list of scorecard ids to run on the statement
        :type scorecard_ids: list[int]
        """
        super().__init__("bsp", "application/json")
        self.statement_type = StatementType.JSON

        self.format = statement_format.value
        self.statement = statement
        self.customer = customer
        self.scorecard_ids = scorecard_ids

    def build_request_body(self) -> None:
        customer_json = {
            "id": self.customer.customer_id
        }
        self.request_body = {
            "customer": customer_json,
            "bankStatement": {
                "type": self.format,
                "content": self.statement
            }
        }
        if self.scorecard_ids:
            self.request_body["scorecardIds"] = self.scorecard_ids
