import itertools
import statistics
from typing import List

from app.models.practice import Practice


class PracticeStats:

    def __init__(self, practices: List[Practice]):
        self.practices = practices
        self.practice_times = [sum([x.minutes for x in practice.exercises.all()]) for practice in practices]
        self.exercises_per_practice = [len(practice.exercises.all()) for practice in practices]
        self.exercises = [[x.minutes for x in practice.exercises.all()] for practice in practices]
        self.instruments = [practice.instrument.name.lower() for practice in self.practices]

    @property
    def total_practice_time(self):
        return sum([practice.length for practice in self.practices])

    @property
    def avg_practice_time(self):
        return round(self.__calculate(statistics.mean, self.practice_times))

    @property
    def median_practice_time(self):
        return self.__calculate(statistics.median, self.practice_times)

    @property
    def max_practice_time(self):
        return self.__calculate(max, self.practice_times)

    @property
    def min_practice_time(self):
        return self.__calculate(min, self.practice_times)

    @property
    def num_exercises(self):
        return self.__calculate(sum, self.exercises_per_practice)

    @property
    def avg_num_exercises(self):
        return self.__calculate(statistics.mean, self.exercises_per_practice)

    @property
    def median_num_exercises(self):
        return self.__calculate(statistics.median, self.exercises_per_practice)

    @property
    def avg_exercise_length(self):
        return self.__calculate(statistics.mean, list(itertools.chain(*self.exercises)))

    @property
    def median_exercise_length(self):
        return self.__calculate(statistics.median, list(itertools.chain(*self.exercises)))

    def __calculate(self, fnc, param):
        try:
            return fnc(param)
        except (statistics.StatisticsError, ValueError):
            return 0

    @property
    def most_practiced_instrument(self):
        return max(set(self.instruments), key=self.instruments.count)

    @property
    def least_practiced_instrument(self):
        return min(set(self.instruments), key=self.instruments.count)
