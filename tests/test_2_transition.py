"""Stage 2 · transition(state, action) 테스트

실행: python -m unittest tests.test_2_transition -v

상태(state)는 (위치, 남은 행동 횟수) 튜플이에요.
"""

import unittest

from reward_lens.env import transition


class TestTransition(unittest.TestCase):
    def test_normal_transitions(self):
        """행동하면 위치가 바뀌고 남은 횟수가 1 줄어든다."""
        cases = [
            # (현재 상태, 행동, 기대 다음 상태)
            ((0, 6), "right", (1, 5)),
            ((1, 5), "wait", (1, 4)),
            ((1, 4), "left", (0, 3)),
            ((0, 6), "left", (0, 5)),  # 벽에 막혀도 행동 한 번은 쓴 것
        ]
        for state, action, expected in cases:
            with self.subTest(state=state, action=action):
                self.assertEqual(transition(state, action), expected)

    def test_actions_that_end_the_game(self):
        """게임을 '끝내는' 행동은 정상이다."""
        cases = [
            ((1, 1), "right", (2, 0)),  # 마지막 행동으로 도착
            ((1, 5), "right", (2, 4)),  # 일찍 도착
            ((0, 1), "wait", (0, 0)),   # 마지막 행동을 써 버림
            ((1, 1), "wait", (1, 0)),
        ]
        for state, action, expected in cases:
            with self.subTest(state=state, action=action):
                self.assertEqual(transition(state, action), expected)

    def test_actions_after_the_game_ended(self):
        """이미 '끝난' 게임에서 행동하면 ValueError."""
        cases = [
            ((2, 4), "left"),   # 이미 도착함
            ((2, 0), "wait"),   # 도착 + 횟수 소진
            ((1, 0), "right"),  # 횟수 소진
            ((0, 0), "wait"),
        ]
        for state, action in cases:
            with self.subTest(state=state, action=action):
                with self.assertRaises(ValueError):
                    transition(state, action)

    def test_invalid_inputs(self):
        """잘못된 행동이나 격자 밖 위치도 ValueError."""
        cases = [
            ((1, 5), "jump"),
            ((-1, 6), "right"),
            ((3, 6), "left"),
        ]
        for state, action in cases:
            with self.subTest(state=state, action=action):
                with self.assertRaises(ValueError):
                    transition(state, action)


if __name__ == "__main__":
    unittest.main()
