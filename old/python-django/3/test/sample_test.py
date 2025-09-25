import unittest
import time
from main import conditional_cache


class TestConditionalCache(unittest.TestCase):

    def setUp(self):
        self.mock_condition_true = lambda *args, **kwargs: True
        self.mock_condition_false = lambda *args, **kwargs: False

    def test_cache_before_expiry_with_condition_true(self):
        compute_count = 0

        @conditional_cache(expiry=5, condition=self.mock_condition_true)
        def add(a: int, b: int):
            nonlocal compute_count
            compute_count += 1
            return a + b

        result1 = add(1, 2)  # First call, should increment compute_count
        self.assertEqual(result1, 3)
        self.assertEqual(compute_count, 1)

        time.sleep(1)

        result2 = add(1, 2)  # Second call within expiry, should not increment compute_count
        self.assertEqual(result2, 3)
        self.assertEqual(compute_count, 1)


if __name__ == '__main__':
    unittest.main()
