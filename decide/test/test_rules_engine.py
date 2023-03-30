import unittest
from unittest.mock import MagicMock
from decide.models.rules_engine import (
    ScorecardAPI,
    ScorecardRequest,
    ScorecardExecuteRequest,
    Status,
    Rule,
    RuleType,
    Condition,
    Operator,
    BooleanRuleSet,
    Affordability,
    Block,
    Duration,
    Outcome,
)


class TestScorecardAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client = MagicMock()
        cls.scorecard_api = ScorecardAPI()
        cls.scorecard_api.client = cls.mock_client

    def test_create_scorecard(self):
        mock_response = {
            "data": {
                "scorecard": {
                    "id": "123",
                    "name": "Test Scorecard",
                    "status": "enabled",
                    "affordability": {
                        "monthly_interest_rate": 10,
                        "monthly_duration": [{"duration": "3"}],
                    },
                    "booleanRulesetId": "6419b89806b22f001326e369",
                    "owner": "indicina",
                    "createdAt": "2023-03-21T14:00:56.683Z",
                    "updatedAt": "2023-03-21T14:00:56.683Z",
                }
            }
        }
        self.mock_client.post.return_value = mock_response

        # Create a list of rules for the scorecard
        rules = [
            Rule(
                order=1,
                rule_type=RuleType.AVERAGE_BALANCE,
                value="1000",
                condition=Condition.IS_EQUAL,
                operator=Operator.OPERATOR_AND,
            ),
            Rule(
                order=2,
                rule_type=RuleType.AVERAGE_CREDITS,
                value="500",
                condition=Condition.IS_EQUAL,
                operator=Operator.OPERATOR_AND,
            ),
            Rule(
                order=3,
                rule_type=RuleType.LOAN_AMOUNT,
                value="2000",
                condition=Condition.LESS_THAN_EQUAL_TO,
                operator=Operator.OPERATOR_AND,
            ),
        ]

        # Create a block from the list of rules
        block = Block(
            rules=rules,
            order=1,
            operator=Operator.OPERATOR_NONE,
            negative_outcome=Outcome.DECLINE,
        )

        # Create a boolean ruleset
        boolean_rule_set = BooleanRuleSet(
            name="Test Scorecard",
            positive_outcome=Outcome.ACCEPT,
            negative_outcome=Outcome.DECLINE,
            owner="indicina",
            blocks=[block],
        )

        # Create affordability logic
        affordability_logic = Affordability(20, [Duration(5), Duration(14)])

        # Create a scorecard request
        scorecard_request = ScorecardRequest(
            name="Test Scorecard",
            boolean_rule_set=boolean_rule_set,
            affordability=affordability_logic,
            status=Status.ENABLED,
        )

        scorecard = self.scorecard_api.create_scorecard(scorecard_request)
        self.assertEqual(scorecard.scorecard_id, "123")
        self.assertEqual(scorecard.name, "Test Scorecard")
        self.assertEqual(scorecard.status, "enabled")

    def test_read_scorecard_found(self):
        mock_response = {
            "statusCode": 200,
            "data": {
                "id": 123,
                "name": "Test Scorecard",
                "affordability": {
                    "monthly_duration": {"duration": [3]},
                    "monthly_interest_rate": 10,
                },
                "booleanRuleSet": {
                    "id": "640b840206b22f001326decf",
                    "name": "Test Scorecard",
                    "negativeOutcome": "OUTCOME_DECLINE",
                    "positiveOutcome": "OUTCOME_ACCEPT",
                    "blocks": [
                        {
                            "id": "640b840206b22f001326decd",
                            "negativeOutcome": "OUTCOME_MANUAL_REVIEW",
                            "rules": [
                                {
                                    "id": "640b840206b22f001326decb",
                                    "type": "cashFlowAnalysis.accountActivity",
                                    "order": 1,
                                    "value": "0.40",
                                    "condition": "CONDITION_GREATER_THAN",
                                    "operator": "OPERATOR_NONE",
                                    "createdAt": {},
                                    "updatedAt": {},
                                }
                            ],
                            "order": 1,
                            "operator": "OPERATOR_NONE",
                            "createdAt": {},
                            "updatedAt": {},
                        }
                    ],
                    "owner": "indicina",
                    "createdAt": {},
                    "updatedAt": {},
                    "types": ["cashFlowAnalysis.accountActivity"],
                },
                "booleanRulesetId": "640b840206b22f001326decf",
                "owner": "indicina",
                "status": "enabled",
                "createdAt": "2023-03-10T19:24:50.000Z",
                "updatedAt": "2023-03-10T19:24:50.000Z",
            },
            "message": "Scorecard fetched successfully",
        }
        self.mock_client.get.return_value = mock_response

        scorecard_id = 123
        scorecard = self.scorecard_api.read_scorecard(scorecard_id)

        self.assertIsNotNone(scorecard)
        self.assertEqual(scorecard.scorecard_id, 123)
        self.assertEqual(scorecard.name, "Test Scorecard")
        self.assertEqual(scorecard.status, "enabled")

    def test_read_scorecard_not_found(self):
        mock_response = {"statusCode": 404}
        self.mock_client.get.return_value = mock_response

        scorecard_id = 123
        scorecard = self.scorecard_api.read_scorecard(scorecard_id)

        self.assertIsNone(scorecard)

    def test_update_scorecard(self):
        mock_response = {
            "data": {
                "scorecard": {
                    "id": 123,
                    "name": "Test Scorecard",
                    "booleanRulesetId": "640b840206b22f001326decf",
                    "affordability": {
                        "monthly_interest_rate": 10,
                        "monthly_duration": {"duration": [3]},
                    },
                    "owner": "indicina",
                    "status": "enabled",
                    "createdAt": "2023-03-10T19:24:50.000Z",
                    "updatedAt": "2023-03-10T19:24:50.000Z",
                }
            },
        }
        self.mock_client.patch.return_value = mock_response

        scorecard_id = 123
        # Create a list of rules for the scorecard
        rules = [
            Rule(
                order=1,
                rule_type=RuleType.AVERAGE_BALANCE,
                value="1000",
                condition=Condition.IS_EQUAL,
                operator=Operator.OPERATOR_AND,
            ),
            Rule(
                order=2,
                rule_type=RuleType.AVERAGE_CREDITS,
                value="500",
                condition=Condition.IS_EQUAL,
                operator=Operator.OPERATOR_AND,
            ),
            Rule(
                order=3,
                rule_type=RuleType.LOAN_AMOUNT,
                value="2000",
                condition=Condition.LESS_THAN_EQUAL_TO,
                operator=Operator.OPERATOR_AND,
            ),
        ]

        # Create a block from the list of rules
        block = Block(
            rules=rules,
            order=1,
            operator=Operator.OPERATOR_NONE,
            negative_outcome=Outcome.DECLINE,
        )

        # Create a boolean ruleset
        boolean_rule_set = BooleanRuleSet(
            name="Test Scorecard",
            positive_outcome=Outcome.ACCEPT,
            negative_outcome=Outcome.DECLINE,
            owner="indicina",
            blocks=[block],
        )

        # Create affordability logic
        affordability_logic = Affordability(25, [Duration(5), Duration(14)])

        # Create a scorecard request
        scorecard_request = ScorecardRequest(
            name="Test Scorecard",
            boolean_rule_set=boolean_rule_set,
            affordability=affordability_logic,
            status=Status.ENABLED,
        )
        scorecard = self.scorecard_api.update_scorecard(scorecard_id, scorecard_request)

        self.assertEqual(scorecard.scorecard_id, 123)
        self.assertEqual(scorecard.name, "Test Scorecard")
        self.assertEqual(scorecard.status, "enabled")

    def test_delete_scorecard(self):
        mock_response = {"message": "Scorecard deleted successfully"}
        self.mock_client.delete.return_value = mock_response

        scorecard_id = 123
        message = self.scorecard_api.delete_scorecard(scorecard_id)

        self.assertEqual(message, "Scorecard deleted successfully")

    def test_execute_scorecard(self):
        mock_response = {
            "data": {
                "scorecardResults": [
                    {
                        "name": "Acc activity > 40",
                        "affordability": {},
                        "rules": {},
                        "analysisId": "f135b95792440ba774a78594bce00ab5f26428fc678c288370e3d1ecf25dc9bf2600aa8d4027e308613feebff95ae6e5d5b6c8a355e0fd4d04fd3406a620e180",
                        "scorecardId": 262,
                    },
                ],
                "bankStatementSummary": {},
            },
        }
        self.mock_client.post.return_value = mock_response

        scorecard_ids = ([262],)
        analysis_id = "f135b95792440ba774a78594bce00ab5f26428fc678c288370e3d1ecf25dc9bf2600aa8d4027e308613feebff95ae6e5d5b6c8a355e0fd4d04fd3406a620e180"

        scorecard_execute_request = ScorecardExecuteRequest(analysis_id, scorecard_ids)
        response = self.scorecard_api.execute_scorecard(scorecard_execute_request)

        self.assertIn("scorecardResults", response)

    def test_list_scorecards(self):
        mock_response = {
            "data": {
                "items": [
                    {
                        "id": 300,
                        "name": "Mercy Robert",
                        "booleanRulesetId": "640b840206b22f001326decf",
                        "affordability": {
                            "monthly_duration": {"duration": [3]},
                            "monthly_interest_rate": 10,
                        },
                        "owner": "indicina",
                        "status": "enabled",
                        "createdAt": "2023-03-10T19:24:50.000Z",
                        "updatedAt": "2023-03-10T19:24:50.000Z",
                    },
                    {
                        "id": 292,
                        "name": "ann",
                        "booleanRulesetId": "64076df76eb43c0013384336",
                        "affordability": {
                            "monthly_duration": {"duration": [3]},
                            "monthly_interest_rate": 10,
                        },
                        "owner": "indicina",
                        "status": "enabled",
                        "createdAt": "2023-03-07T17:01:44.000Z",
                        "updatedAt": "2023-03-07T17:01:44.000Z",
                    },
                ]
            }
        }
        self.mock_client.get.return_value = mock_response

        # Call the method with some parameters
        result = self.scorecard_api.list_scorecards(Status.ENABLED, 2, 1)

        # Assert that the correct URL was called
        expected_path = "scorecards?status=enabled&limit=2&page=1"
        actual_path = self.mock_client.path
        self.assertEqual(actual_path, expected_path)

        # Assert that the method returned the correct data
        expected_result = {
            "items": [
                {
                    "id": 300,
                    "name": "Mercy Robert",
                    "booleanRulesetId": "640b840206b22f001326decf",
                    "affordability": {
                        "monthly_duration": {"duration": [3]},
                        "monthly_interest_rate": 10,
                    },
                    "owner": "indicina",
                    "status": "enabled",
                    "createdAt": "2023-03-10T19:24:50.000Z",
                    "updatedAt": "2023-03-10T19:24:50.000Z",
                },
                {
                    "id": 292,
                    "name": "ann",
                    "booleanRulesetId": "64076df76eb43c0013384336",
                    "affordability": {
                        "monthly_duration": {"duration": [3]},
                        "monthly_interest_rate": 10,
                    },
                    "owner": "indicina",
                    "status": "enabled",
                    "createdAt": "2023-03-07T17:01:44.000Z",
                    "updatedAt": "2023-03-07T17:01:44.000Z",
                },
            ]
        }
        self.assertEqual(result, expected_result)
