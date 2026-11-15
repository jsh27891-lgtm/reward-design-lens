"""Stage 1 · move(position, action) 테스트

실행: python -m unittest tests.test_1_move -v

이 파일은 미리 준비된 기준이에요. 고치지 말고, reward_lens/env.py를 직접 써서 통과시켜요.
"""

import unittest

from reward_lens.env import move


class TestMove(unittest.TestCase):
    def test_normal_moves(self):
        """정상 이동: 행동대로 위치가 바뀐다."""
        cases = [
            # (현재 위치, 행동, 기대 위치)
            (0, "right", 1),
            (1, "right", 2),
            (1, "left", 0),
            (2, "left", 1),
            (1, "wait", 1),
        ]
        for position, action, expected in cases:
            with self.subTest(position=position, action=action):
                self.assertEqual(move(position, action), expected)

    def test_walls(self):
        """경계: 벽 밖으로는 못 나가고 제자리에 머문다. 오류가 아니다!"""
        cases = [
            (0, "left", 0),
            (2, "right", 2),
            (0, "wait", 0),
            (2, "wait", 2),
        ]
        for position, action, expected in cases:
            with self.subTest(position=position, action=action):
                self.assertEqual(move(position, action), expected)

    def test_invalid_action(self):
        """정의되지 않은 행동은 ValueError."""
        for position in (0, 1, 2):
            with self.subTest(position=position):
                with self.assertRaises(ValueError):
                    move(position, "jump")

    def test_invalid_position(self):
        """격자(0~2) 밖의 위치에서는 어떤 행동이든 ValueError."""
        cases = [
            (3, "right"),
            (3, "left"),  # 지난번에 2로 '고쳐서' 돌려준 버그가 있었어요
            (3, "wait"),
            (-1, "right"),
            (-1, "wait"),
        ]
        for position, action in cases:
            with self.subTest(position=position, action=action):
                with self.assertRaises(ValueError):
                    move(position, action)


if __name__ == "__main__":
    unittest.main()
