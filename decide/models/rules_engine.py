from enum import Enum
from typing import List, Dict, Optional
from .client import DecideClient


class Outcome(Enum):
    """
    An enumeration of possible outcomes of a Block or a Boolean rule set.
    """

    ACCEPT = "OUTCOME_ACCEPT"
    DECLINE = "OUTCOME_DECLINE"
    MANUAL_REVIEW = "OUTCOME_MANUAL_REVIEW"


class Condition(Enum):
    """
    An enumeration of possible conditions for a rule in a Boolean rule set.
    """

    UNSPECIFIED: str = "CONDITION_UNSPECIFIED"
    LESS_THAN: str = "CONDITION_LESS_THAN"
    LESS_THAN_EQUAL_TO: str = "CONDITION_LESS_THAN_EQUAL_TO"
    GREATER_THAN: str = "CONDITION_GREATER_THAN"
    GREATER_THAN_EQUAL_TO: str = "CONDITION_GREATER_THAN_EQUAL_TO"
    IS_BETWEEN: str = "CONDITION_IS_BETWEEN"
    IS_NOT_BETWEEN: str = "CONDITION_IS_NOT_BETWEEN"
    IS_EQUAL: str = "CONDITION_IS_EQUAL"
    IS_NOT_EQUAL: str = "CONDITION_IS_NOT_EQUAL"
    IS_IN: str = "CONDITION_IS_IN"


class Operator(Enum):
    """
    An enumeration of possible operators used in a Block or a Boolean rule set.
    """

    OPERATOR_NONE: str = "OPERATOR_NONE"
    OPERATOR_AND: str = "OPERATOR_AND"
    OPERATOR_OR: str = "OPERATOR_OR"


class Status(Enum):
    """
    An enumeration of possible statuses for a Scorecard.
    """

    ENABLED: str = "enabled"
    DISABLED: str = "disabled"


class RuleType(Enum):
    ACCOUNT_SWEEP: str = "behaviouralAnalysis.accountSweep"
    GAMBLING_RATE: str = "behaviouralAnalysis.gamblingRate"
    CONFIDENCE_INTERVAL_SALARY_DETECTION: str = (
        "incomeAnalysis.confidenceIntervalonSalaryDetection"
    )
    LOAN_INFLOW_RATE: str = "behaviouralAnalysis.loanInflowRate"
    LOAN_REPAYMENT_INFLOW_RATE: str = "behaviouralAnalysis.loanRepaymentInflowRate"
    SALARY_EARNER: str = "incomeAnalysis.salaryEarner"
    GIG_WORKER: str = "incomeAnalysis.gigWorker"
    AVERAGE_BALANCE: str = "cashFlowAnalysis.averageBalance"
    CLOSING_BALANCE: str = "cashFlowAnalysis.closingBalance"
    AVERAGE_CREDITS: str = "cashFlowAnalysis.averageCredits"
    AVERAGE_DEBITS: str = "cashFlowAnalysis.averageDebits"
    AVERAGE_OTHER_INCOME: str = "incomeAnalysis.averageOtherIncome"
    AVERAGE_SALARY: str = "incomeAnalysis.averageSalary"
    MEDIAN_INCOME: str = "incomeAnalysis.medianIncome"
    AVERAGE_RECURRING_EXPENSE: str = "spendAnalysis.averageRecurringExpense"
    TOTAL_EXPENSE: str = "spendAnalysis.totalExpenses"
    SAVING_AND_INVESTMENTS: str = "spendAnalysis.savingsAndInvestments"
    LOAN_AMOUNT: str = "behaviouralAnalysis.loanAmount"
    LOAN_REPAYMENTS: str = "behaviouralAnalysis.loanRepayments"
    FIRST_DAY: str = "cashFlowAnalysis.firstDay"
    LAST_DAY: str = "cashFlowAnalysis.lastDay"
    INFLOW_OUTFLOW_RATE: str = "behaviouralAnalysis.inflowOutflowRate"
    EXPECTED_SALARY_DAY: str = "incomeAnalysis.expectedSalaryDay"
    LAST_SALARY_DATE: str = "incomeAnalysis.lastSalaryDate"
    NO_OF_TRANSACTING_MONTHS: str = "cashFlowAnalysis.noOfTransactingMonths"
    ACCOUNT_ACTIVITY: str = "cashFlowAnalysis.accountActivity"
    NUMBER_SALARY_PAYMENTS: str = "incomeAnalysis.numberSalaryPayments"
    NO_OF_OTHER_INCOME_PAYMENTS: str = "incomeAnalysis.numberOtherIncomePayments"
    SALARY_FREQUENCY: str = "incomeAnalysis.salaryFrequency"


class Rule:
    """
    A class representing a rule in a block.
    Attributes:
    -----------
    order: int
        An integer representing the order of the rule in the block.
    rule_type: RuleType
        A RuleType object representing the type of the rule.
    value: str
        A string representing the value to be evaluated in the rule.
    condition: Condition
        A Condition object representing the condition to be evaluated in the rule.
    operator: Operator
        An Operator object representing the operator to be used in the rule.
    """

    def __init__(
        self,
        order: int,
        rule_type: RuleType,
        value: str,
        condition: Condition,
        operator: Operator,
    ):
        self.order = order
        self.rule_type = rule_type
        self.value = value
        self.condition = condition
        self.operator = operator

    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation of the rule.

        Returns:
        --------
        Dict:
            A dictionary representing the rule.
        """
        return {
            "order": self.order,
            "type": self.rule_type.value,
            "value": self.value,
            "condition": self.condition.value,
            "operator": self.operator.value,
        }


class Block:
    """
    A class representing a block of rules.
    Attributes:
    -----------
    rules: List[Rule]
        A list of Rule objects representing the rules in the block.
    order: int
        An integer representing the order of the block in a list of blocks.
    operator: Operator
        An Operator object representing the operator to be used to evaluate the rules in the block.
    negative_outcome: Outcome
        An Outcome object representing the outcome if the block evaluates to False.
    """

    def __init__(
        self,
        rules: List[Rule],
        order: int,
        operator: Operator,
        negative_outcome: Outcome,
    ):
        self.rules = rules
        self.order = order
        self.operator = operator
        self.negative_outcome = negative_outcome

    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation of the block.

        Returns:
        --------
        Dict:
            A dictionary representing the block.
        """
        return {
            "rules": [rule.to_dict() for rule in self.rules],
            "order": self.order,
            "operator": self.operator.value,
            "negativeOutcome": self.negative_outcome.value,
        }


class BooleanRuleSet:
    """
    A class representing a set of boolean rules.

    Attributes:
        name (str): The name of the rule set.
        positive_outcome (Outcome): The positive outcome of the rule set.
        negative_outcome (Outcome): The negative outcome of the rule set.
        owner (str): The owner of the rule set.
        blocks (List[Block]): The list of blocks that make up the rule set.
    """

    def __init__(
        self,
        name: str,
        positive_outcome: Outcome,
        negative_outcome: Outcome,
        owner: str,
        blocks: List[Block],
    ):
        self.name = name
        self.positive_outcome = positive_outcome
        self.negative_outcome = negative_outcome
        self.owner = owner
        self.blocks = blocks

    def to_dict(self):
        """
        Returns a dictionary representation of the BooleanRuleSet instance.

        Returns:
            Dict: A dictionary representation of the BooleanRuleSet instance.
        """
        return {
            "name": self.name,
            "positiveOutcome": self.positive_outcome.value,
            "negativeOutcome": self.negative_outcome.value,
            "owner": self.owner,
            "blocks": [block.to_dict() for block in self.blocks],
        }


class Duration:
    """
    A class representing a monthly duration.

    Attributes:
        duration (int): Monthly Duration.
    """

    def __init__(self, duration: int):
        self.duration = duration

    def to_dict(self):
        """
        Returns a dictionary representation of the Duration instance.

        Returns:
            Dict: A dictionary representation of the Duration instance.
        """
        return {"duration": self.duration}


class Affordability:
    """
    A class representing the affordability criteria.

    Attributes:
        monthly_interest_rate (float): The monthly interest rate.
        monthly_durations (List[Duration]): A list of duration objects representing monthly durations.
    """

    def __init__(self, monthly_interest_rate: float, monthly_durations: List[Duration]):
        self.monthly_interest_rate = monthly_interest_rate
        self.monthly_durations = monthly_durations

    def to_dict(self):
        """
        Returns a dictionary representation of the affordability object.
        """
        return {
            "monthly_interest_rate": self.monthly_interest_rate,
            "monthly_durations": [
                duration.to_dict() for duration in self.monthly_durations
            ],
        }


class ScorecardRequest:
    """
    A class representing a scorecard request.

    Attributes:
        name (str): The name of the scorecard request.
        boolean_rule_set (BooleanRuleSet): A BooleanRuleSet object representing the set of boolean rules.
        affordability (Affordability): An Affordability object representing the affordability criteria.
        status (Status): The status of the scorecard request.
    """

    def __init__(
        self,
        name: str,
        boolean_rule_set: BooleanRuleSet,
        affordability: Affordability,
        status: Status,
    ):
        self.name = name
        self.boolean_rule_set = boolean_rule_set
        self.affordability = affordability
        self.status = status

    def to_dict(self):
        """
        Returns a dictionary representation of the scorecard request object.
        """
        return {
            "name": self.name,
            "booleanRuleSet": self.boolean_rule_set.to_dict(),
            "affordability": self.affordability.to_dict(),
            "status": self.status.value,
        }


class ScorecardExecuteRequest:
    """
    A class representing a scorecard execute request.

    Attributes:
        analysis_id (str): The id of the analysis you wish to run the scorecard on.
        scorecard_ids (list[int]): A list of scorecard_ids to execute.
    """

    def __init__(
        self,
        analysis_id: str,
        scorecard_ids: list[int],
    ):
        self.analysis_id = analysis_id
        self.scorecard_ids = scorecard_ids

    def to_dict(self):
        """
        Returns a dictionary representation of the scorecard execute request object.
        """
        return {
            "analysisId": self.analysis_id,
            "scorecardIds": self.scorecard_ids,
        }


class ScorecardResponse:
    """
    A class representing a response from a scorecard API call.

    Attributes:
        name (str): The name of the scorecard.
        boolean_ruleset_id (str): The ID of the boolean rule set associated with the scorecard.
        affordability (Affordability): The affordability settings for the scorecard.
        owner (str): The owner of the scorecard.
        status (str): The status of the scorecard.
        created_at (str): The timestamp for when the scorecard was created.
        updated_at (str): The timestamp for when the scorecard was last updated.
        scorecard_id (int): The ID of the scorecard.
    """

    def __init__(
        self,
        name: str,
        boolean_ruleset_id: str,
        affordability: Affordability,
        owner: str,
        status: str,
        created_at: str,
        updated_at: str,
        scorecard_id: int,
    ):
        self.name = name
        self.boolean_ruleset_id = boolean_ruleset_id
        self.affordability = affordability
        self.owner = owner
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.scorecard_id = scorecard_id

    @staticmethod
    def from_dict(data):
        """
        Creates a ScorecardResponse object from a dictionary.

        Args:
            data (dict): The dictionary to create the object from.

        Returns:
            ScorecardResponse: The created ScorecardResponse object.
        """
        return ScorecardResponse(
            name=data["name"],
            boolean_ruleset_id=data["booleanRulesetId"],
            affordability=data["affordability"],
            owner=data["owner"],
            status=data["status"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"],
            scorecard_id=data["id"],
        )


class ScorecardAPI:
    """
    A class for interfacing with the scorecard API.

    Attributes:
        client (DecideClient): The DecideClient object used to make requests to the API.
    """

    def __init__(self) -> None:
        self.client: DecideClient = DecideClient("scorecards", "application/json")

    def create_scorecard(
        self, scorecard_request: ScorecardRequest
    ) -> ScorecardResponse:
        """
        Creates a new scorecard using the provided ScorecardRequest.

        Args:
            scorecard_request (ScorecardRequest): The ScorecardRequest to use for creating the scorecard.

        Returns:
            ScorecardResponse: The ScorecardResponse object representing the created scorecard.
        """
        data: dict = scorecard_request.to_dict()
        response = self.client.post(body=data)
        scorecard: ScorecardResponse = ScorecardResponse.from_dict(
            response["data"]["scorecard"]
        )
        return scorecard

    def read_scorecard(self, scorecard_id: str) -> Optional[ScorecardResponse]:
        """
        Retrieves a scorecard with the provided ID.

        Args:
            scorecard_id (str): The ID of the scorecard to retrieve.

        Returns:
            Optional[ScorecardResponse]: The ScorecardResponse object representing the retrieved scorecard, or None if not found.
        """
        self.client.path = f"scorecards/{scorecard_id}"
        response = self.client.get()
        scorecard: Optional[ScorecardResponse] = None
        if response.get("statusCode") == 200:
            scorecard = ScorecardResponse.from_dict(response["data"])
        return scorecard

    def update_scorecard(
        self, scorecard_id: str, scorecard_request: ScorecardRequest
    ) -> ScorecardResponse:
        """
        Update an existing scorecard by sending a PATCH request to the Scorecard API with the new scorecard request data.

        Args:
            scorecard_id (str): The ID of the scorecard to update.
            scorecard_request (ScorecardRequest): The new scorecard request data to update the scorecard with.

        Returns:
            ScorecardResponse: The updated scorecard response data.

        Raises:
            requests.exceptions.RequestException: If the request to the Scorecard API fails.
        """
        self.client.path = f"scorecards/{scorecard_id}"
        data: dict = scorecard_request.to_dict()
        response = self.client.patch(body=data)
        scorecard: ScorecardResponse = ScorecardResponse.from_dict(
            response["data"]["scorecard"]
        )
        return scorecard

    def delete_scorecard(self, scorecard_id: str) -> str:
        """
        Delete a scorecard by sending a DELETE request to the Scorecard API with the scorecard ID.

        Args:
            scorecard_id (str): The ID of the scorecard to delete.

        Returns:
            str: A message indicating the success of the deletion.
        """
        self.client.path = f"scorecards/{scorecard_id}"
        response = self.client.delete()
        response_data: dict = response
        return response_data["message"]

    def execute_scorecard(
        self, scorecard_execute_request: ScorecardExecuteRequest
    ) -> Dict:
        """
        Execute scorecard(s) on an already done analysis.

        Args:
            scorecard_execute_request (ScorecardRequest): The ScorecardExecuteRequest.

        Returns:
            Dict: A dictionary containing the scorecard results and bank statement summary.
        """
        self.client.path = "scorecards/execute"
        data: dict = scorecard_execute_request.to_dict()
        response = self.client.post(body=data)
        return response["data"]

    def list_scorecards(self, status: Status, limit: int, page: int):
        """
        List scorecards available to client in a paginated way

        Args:
            status (Enum): The Status of scorecard to filter by.
            limit (int): The max number of scorecards per page/call.
            page (int): The page number to retrieve

        Returns:
            Dict: A dictionary containing the scorecard results and bank statement summary.
        """
        self.client.path = f"scorecards?status={status.value}&limit={limit}&page={page}"
        response = self.client.get()
        return response["data"]
