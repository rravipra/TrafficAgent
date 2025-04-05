# agents/fairness_agent.py

from collections import defaultdict


class FairnessAgent:
    def __init__(self):
        self.wait_times = defaultdict(int)

    def update_fairness(self, intersection, added_time):
        self.wait_times[intersection] += added_time

    def get_fair_signal_plan(self):
        return sorted(self.wait_times.items(), key=lambda x: -x[1])
