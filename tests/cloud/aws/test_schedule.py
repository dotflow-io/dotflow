"""Test AWS Schedule helpers."""

import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from dotflow.cloud.aws.schedule import AWSSchedule, _fix_step


class TestFixStep(unittest.TestCase):
    def test_star_slash_converts_to_zero_slash(self):
        self.assertEqual(_fix_step("*/5"), "0/5")

    def test_star_slash_large_number(self):
        self.assertEqual(_fix_step("*/30"), "0/30")

    def test_plain_star_unchanged(self):
        self.assertEqual(_fix_step("*"), "*")

    def test_fixed_value_unchanged(self):
        self.assertEqual(_fix_step("30"), "30")

    def test_range_unchanged(self):
        self.assertEqual(_fix_step("1-5"), "1-5")

    def test_explicit_start_step_unchanged(self):
        self.assertEqual(_fix_step("0/5"), "0/5")

    def test_question_mark_unchanged(self):
        self.assertEqual(_fix_step("?"), "?")


class TestAWSScheduleConvert(unittest.TestCase):
    def test_crontab_every_hour(self):
        result = AWSSchedule.convert("0 * * * *")

        self.assertEqual(result, "cron(0 * * * ? *)")

    def test_crontab_every_5_minutes(self):
        result = AWSSchedule.convert("*/5 * * * *")

        self.assertEqual(result, "cron(0/5 * * * ? *)")

    def test_crontab_every_30_minutes(self):
        result = AWSSchedule.convert("*/30 * * * *")

        self.assertEqual(result, "cron(0/30 * * * ? *)")

    def test_crontab_step_in_hours(self):
        result = AWSSchedule.convert("0 */6 * * *")

        self.assertEqual(result, "cron(0 0/6 * * ? *)")

    def test_crontab_step_in_minutes_and_hours(self):
        result = AWSSchedule.convert("*/10 */2 * * *")

        self.assertEqual(result, "cron(0/10 0/2 * * ? *)")

    def test_crontab_no_step_unchanged(self):
        result = AWSSchedule.convert("30 2 * * *")

        self.assertEqual(result, "cron(30 2 * * ? *)")

    def test_crontab_specific_day_of_week(self):
        result = AWSSchedule.convert("0 6 * * 1")

        self.assertEqual(result, "cron(0 6 ? * 1 *)")

    def test_crontab_specific_day_of_month(self):
        result = AWSSchedule.convert("0 0 1 * *")

        self.assertEqual(result, "cron(0 0 1 * ? *)")

    def test_rate_passthrough(self):
        result = AWSSchedule.convert("rate(6 hours)")

        self.assertEqual(result, "rate(6 hours)")

    def test_cron_aws_passthrough(self):
        result = AWSSchedule.convert("cron(0 * * * ? *)")

        self.assertEqual(result, "cron(0 * * * ? *)")

    def test_invalid_returns_as_is(self):
        result = AWSSchedule.convert("not a cron")

        self.assertEqual(result, "not a cron")

    def test_strips_whitespace(self):
        result = AWSSchedule.convert("  rate(1 day)  ")

        self.assertEqual(result, "rate(1 day)")


class TestAWSScheduleReadFromTemplate(unittest.TestCase):
    def test_reads_schedule_from_sam_template(self):
        content = """
Resources:
  Func:
    Type: AWS::Serverless::Function
    Properties:
      Events:
        Schedule:
          Type: Schedule
          Properties:
            Schedule: "0 */6 * * *"
"""
        with NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
            f.write(content)
            f.flush()
            result = AWSSchedule.read_from_template(Path(f.name))

        self.assertEqual(result, "0 */6 * * *")

    def test_returns_none_for_missing_file(self):
        result = AWSSchedule.read_from_template(Path("nonexistent.yaml"))

        self.assertIsNone(result)

    def test_returns_none_for_no_schedule(self):
        with NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
            f.write("key: value\n")
            f.flush()
            result = AWSSchedule.read_from_template(Path(f.name))

        self.assertIsNone(result)
