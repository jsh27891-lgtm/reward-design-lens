"""Stage 3 · calculate_reward(position, action, new_position, bonus) 테스트

실행: python -m unittest tests.test_3_reward -v

보상 규칙
- 모든 행동: -1
- 목적지(2)에 도착하는 행동: 추가 +5
- 가운데(1)에서 wait를 고르면: 추가 +bonus  (가운데에 '들어가는' 것만으로는 없음)
"""

import unittest

from reward_lens.env import calculate_reward


class TestCalculateReward(unittest.TestCase):
    def test_reward_rules(self):
        cases = [
            # (이전 위치, 행동, 새 위치, bonus, 기대 보상)
            (0, "right", 1, 6, -1),  # 가운데에 들어가기만 함: 보너스 없음
            (1, "right", 2, 6, 4),   # 도착: -1 + 5
            (1, "wait", 1, 6, 5),    # 가운데에서 기다림: -1 + 6
            (1, "wait", 1, 0, -1),   # 보너스를 끈 규칙
            (1, "wait", 1, 2, 1),    # 새 보너스 값: -1 + 2
            (0, "wait", 0, 6, -1),   # 시작 칸에서 기다림: 보너스 없음
            (0, "left", 0, 6, -1),   # 벽에 막혀 제자리. wait가 아니므로 보너스 없음
            (1, "left", 0, 6, -1),   # 가운데에서 떠남
        ]
        for position, action, new_position, bonus, expected in cases:
            with self.subTest(position=position, action=action, bonus=bonus):
                self.assertEqual(
                    calculate_reward(position, action, new_position, bonus), expected
                )


if __name__ == "__main__":
    unittest.main()
