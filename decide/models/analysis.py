import json
from abc import ABC

from .enums import StatementType, PDFStatus
from .client import DecideClient
from .base import BaseModel
from .tagged_statement import DecideTaggedStatement


class Analysis(BaseModel):  # pylint: disable=too-few-public-methods

    behaviouralAnalysis: "BehaviouralAnalysis" = None
    cashFlowAnalysis: "CashFlowAnalysis" = None
    incomeAnalysis: "IncomeAnalysis" = None
    spendAnalysis: "SpendAnalysis" = None
    transactionPatternAnalysis: "TransactionPatternAnalysis" = None
    accountDetails = None

    def __init__(self, data: dict,
                 status,
                 statement_type: StatementType,
                 job_id: str = None) -> None:
        """
        Decide analysis

        :param data:
        :type data: dict
        :param status:
        :type status:
        :param statement_type:
        :type statement_type: StatementType
        :param job_id:
        :type job_id: str
        """
        super().__init__(data)
        if statement_type == StatementType.PDF:
            self.__status = PDFStatus[data["status"]]
            self.job_id = data["jobId"]
        self.__status = status

        self.statement_type = statement_type
        if self.statement_type == StatementType.PDF:
            self.pdf_client = DecideClient(path=f'pdf/extract/{job_id}/status',
                                           content_type="application/json")

    @property
    def transaction_tags(self) -> DecideTaggedStatement:
        tags = DecideTaggedStatement(request_id=self.id)
        tags.get()
        return tags

    @property
    def status(self) -> PDFStatus:
        """This method checks the status of Decide analyses"""

        if (self.statement_type == StatementType.PDF and
                self.__status not in (PDFStatus.DONE, PDFStatus.FAILED)):
            json_response = self.pdf_client.get()
            self.__status = PDFStatus[json_response["data"]["status"]]
            if self.__status == PDFStatus.DONE:
                super().__init__(data=json_response["data"]["decideResponse"])

            return self.__status
        return self.__status

    def __str__(self):
        return json.dumps(self._data)

    def build_dict_values(self, key, value):
        if key in _analysis_call_dict:
            return _analysis_call_dict[key](value)
        return value


class BehaviouralAnalysis(BaseModel):
    """
    For Behavioral Analysis
    """

    accountSweep = None
    gamblingRate = None
    inflowOutflowRate = None
    loanInflowRate = None
    loanRepaymentInflowRate = None
    loanRepayments = None
    topIncomingTransferAccount = None
    topTransferRecipientAccount = None

    def build_dict_values(self, key, value):
        return value


class CashFlowAnalysis(BaseModel):
    """
        For Cashflow Analysis
    """

    accountActivity = None
    averageBalance = None
    averageCredits = None
    averageDebits = None
    closingBalance = None
    firstDay = None
    lastDay = None
    monthPeriod = None
    netAverageMonthlyEarnings = None
    noOfTransactingMonths = None
    totalCreditTurnover = None
    totalDebitTurnover = None
    yearInStatement = None

    def __init__(self, values):
        super().__init__(values)

    def build_dict_values(self, key, value):
        return value


class IncomeAnalysis(BaseModel):
    """
        For Income Analysis
    """

    averageOtherIncome = None
    averageSalary = None
    confidenceIntervalOnSalaryDetection = None
    expectedSalaryDay = None
    lastSalaryDate = None
    medianIncome = None
    numberOtherIncomePayments = None
    numberOfSalaryPayments = None
    salaryEarner = None
    salaryFrequency = None
    gigWorker = None

    def build_dict_values(self, key, value):
        return value


class SpendAnalysis(BaseModel):
    """
        For Spend Analysis
    """

    expenseChannels: "ExpenseChannels" = None
    expenseCategories: "ExpenseCategories" = None
    averageRecurringExpense = None
    hasRecurringExpense = None
    totalExpenses = None

    def __init__(self, data):
        super().__init__(data)
        setattr(self, "expenseChannels", ExpenseChannels(data["expenseChannels"]))
        setattr(self, "expenseCategories", ExpenseCategories(data["expenseCategories"]))

    def build_dict_values(self, key, value):
        return value


class TransactionPatternAnalysis(BaseModel):
    """
        For TransPattern Analysis
    """

    highestMAWOCredit = None
    highestMAWODebit = None
    lastDateOfCredit = None
    lastDateOfDebit = None
    MAWWZeroBalanceInAccount = None
    mostFrequentBalanceRange = None
    mostFrequentTransactionRange = None
    NODWBalanceLess5000 = None
    recurringExpense = None
    transactionsBetween100000And500000 = None
    transactionsBetween10000And100000 = None
    transactionsGreater500000 = None
    transactionsLess10000 = None
    transactionRanges = None
    NODWBalanceLess = None

    def build_dict_values(self, key, value):
        if key in _analysis_call_dict:
            return _analysis_call_dict[key](value)
        return value


class AccountDetails(BaseModel):

    accountName = None
    accountNumber = None

    def build_dict_values(self, key, value):
        return value


class ExpenseChannels(BaseModel, ABC):

    atmSpend = None
    webSpend = None
    posSpend = None
    ussdTransactions = None
    mobileSpend = None
    spendOnTransfers = None
    internationalTransactionsSpend = None

    def __init__(self, data: list):
        super().__init__({})
        for __dict in data:
            setattr(self, __dict["key"], __dict["value"])


class ExpenseCategories(BaseModel, ABC):

    bills = None
    entertainment = None
    savingsAndInvestments = None
    gambling = None
    airtime = None
    bankCharges = None

    def __init__(self, data: list):
        super().__init__({})
        for __dict in data:
            setattr(self, __dict["key"], __dict["value"])


class Rule:
    condition = None
    name = None
    status = None


_analysis_call_dict = {
    "behaviouralAnalysis": BehaviouralAnalysis,
    "cashFlowAnalysis": CashFlowAnalysis,
    "incomeAnalysis": IncomeAnalysis,
    "spendAnalysis": SpendAnalysis,
    "transactionPatternAnalysis": TransactionPatternAnalysis,
    "accountDetails": AccountDetails
}
