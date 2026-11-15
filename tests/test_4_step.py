"""Stage 4 · step(state, action, bonus) 테스트

실행: python -m unittest tests.test_4_step -v

step()은 (다음 상태, 보상, done)을 돌려줘요.
done은 이번 행동으로 에피소드가 끝났는지(도착했거나 남은 횟수가 0인지)예요.
"""

import unittest

from reward_lens.env import step


class TestStep(unittest.TestCase):
    def test_returns_three_values(self):
        """반환값은 (다음 상태, 보상, done) 세 개."""
        result = step((0, 6), "right", 6)
        self.assertEqual(len(result), 3)

    def test_normal_steps(self):
        cases = [
            # (현재 상태, 행동, bonus, 기대 (다음 상태, 보상, done))
            ((0, 6), "right", 6, ((1, 5), -1, False)),
            ((1, 5), "wait", 6, ((1, 4), 5, False)),
            ((1, 5), "wait", 0, ((1, 4), -1, False)),
            ((0, 6), "left", 6, ((0, 5), -1, False)),
        ]
        for state, action, bonus, expected in cases:
            with self.subTest(state=state, action=action, bonus=bonus):
                self.assertEqual(step(state, action, bonus), expected)

    def test_steps_that_end_the_episode(self):
        """이번 행동으로 끝나면 done=True."""
        cases = [
            ((1, 5), "right", 6, ((2, 4), 4, True)),   # 도착
            ((1, 1), "right", 6, ((2, 0), 4, True)),   # 마지막 행동으로 도착
            ((1, 1), "wait", 6, ((1, 0), 5, True)),    # 도장 찍고 횟수 소진
            ((0, 1), "wait", 6, ((0, 0), -1, True)),   # 횟수 소진
            ((1, 1), "left", 6, ((0, 0), -1, True)),
        ]
        for state, action, bonus, expected in cases:
            with self.subTest(state=state, action=action, bonus=bonus):
                self.assertEqual(step(state, action, bonus), expected)

    def test_errors_pass_through(self):
        """transition()의 오류가 step()까지 그대로 전달된다."""
        cases = [
            ((2, 4), "left"),   # 이미 도착
            ((1, 0), "right"),  # 이미 횟수 소진
            ((0, 6), "jump"),   # 없는 행동
            ((3, 6), "wait"),   # 격자 밖
        ]
        for state, action in cases:
            with self.subTest(state=state, action=action):
                with self.assertRaises(ValueError):
                    step(state, action, 6)


if __name__ == "__main__":
    unittest.main()
