import unittest

from app.intelligence.redmine_delivery import build_project_delivery


class WorkloadDeliveryTests(unittest.TestCase):
    def issue(self, owner, status):
        return {"assignee": owner, "status": status, "done": False, "pending": False}

    def test_assigned_unstarted_tasks_do_not_raise_risk(self):
        issues = [self.issue("Owner A", "New") for _ in range(92)]
        issues += [self.issue("Owner B", "New") for _ in range(40)]
        issues += [self.issue("Owner A", "In Progress") for _ in range(3)]
        issues += [self.issue("Owner B", "Doing") for _ in range(2)]
        risk, actions = build_project_delivery(issues, None)
        self.assertEqual(risk["level"], "GREEN")
        self.assertFalse(any(x["id"] == "workload-concentration" for x in actions))

    def test_active_concentration_still_raises_risk(self):
        issues = [self.issue("Owner A", "In Progress") for _ in range(5)]
        issues += [self.issue("Owner B", "In Review")]
        issues += [self.issue("Owner B", "New") for _ in range(100)]
        risk, actions = build_project_delivery(issues, None)
        self.assertEqual(risk["level"], "AT_RISK")
        workload = next(x for x in actions if x["id"] == "workload-concentration")
        self.assertEqual(workload["count"], 5)
        self.assertIn("5/6", workload["detail"])


if __name__ == "__main__":
    unittest.main()
