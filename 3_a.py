class ScoreTracker:
    def __init__(self):
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def get_middle_value(self):
        self.scores.sort()
        mid_index = len(self.scores) // 2

        if len(self.scores) % 2 == 1:
            # Odd number of elements
            return self.scores[mid_index]
        else:
            # Even number of elements
            return self.scores[mid_index - 1], self.scores[mid_index]

score_tracker = ScoreTracker()
score_tracker.add_score(85.5)
score_tracker.add_score(92.3)
score_tracker.add_score(77.8)
score_tracker.add_score(90.1)
print(score_tracker.scores)
median1 = score_tracker.get_middle_value()
print(sum(median1)/2)
score_tracker.add_score(81.2)
score_tracker.add_score(88.7)
print(score_tracker.scores)
median2 = score_tracker.get_middle_value()
print(sum(median2)/2)

