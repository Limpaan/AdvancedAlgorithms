import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
from IntervalCollection import IntervalCollection
import math


class DotSpace:
    UNIFORM_DIST = 0
    NORMAL_DIST = 1
    UNIFORM_NORMAL_DIST = 2
    DENSE_UNIFORM_DIST = 3
    EMPTY_NORMAL_DIST = 4
    RISING_DIST = 5
    CHISQUARE_DIST = 6

    max_val = 1

    def __init__(self, n, d, max_val=1, dot_distribution=random.randint(0, 11)):
        self.sampled_intervals = IntervalCollection()
        self.long_intervals = IntervalCollection()
        self.max_val = max_val
        self.dots = self.setup_dots(n, d, dot_distribution)

    def get_mean(self):
        mean = self.get_mean_no_longs(self.max_val + 1)
        return mean

    def get_mean_no_longs(self, long_threshold):
        total = 0
        longs = 0
        left = 0
        for i in range(len(self.dots)):
            dist = self.dots[i] - left
            left = self.dots[i]
            if dist > long_threshold:
                longs += 1
            else:
                total += dist
        dist = self.max_val - self.dots[-1]
        if dist > long_threshold:
            longs += 1
        else:
            total += dist

        return total / (len(self.dots) - longs)

    def get_var(self):
        return self.get_var_no_longs(self.max_val + 1)

    def get_var_no_longs(self, long_threshold):
        mean = self.get_mean_no_longs(long_threshold)
        total = 0
        longs = 0
        left = 0
        for i in range(len(self.dots)):
            dist = self.dots[i] - left
            left = self.dots[i]
            if dist > long_threshold:
                longs += 1
            else:
                total += (dist - mean)**2
        dist = self.max_val - self.dots[-1]
        if dist > long_threshold:
            longs += 1
        else:
            total += (dist - mean)**2

        return total / (len(self.dots) - longs)

    def soft_reset(self):
        self.sampled_intervals = IntervalCollection()
        self.long_intervals = IntervalCollection()

    def setup_dots(self, n, d, case):
        assert (n < self.max_val / d)

        if case == DotSpace.UNIFORM_DIST:
            # Uniform distribution
            print("Using uniform distribution")
            values = random.rand(n) * self.max_val
            values.sort()
        if case == DotSpace.NORMAL_DIST:
            # Normal distribution
            print("Using normal distribution")
            values = random.normal(0, 1, n)
            values.sort()
            values += values[0] * -1
            values /= values[n - 1]
            values = values * self.max_val
        if case == 2:
            # Half-Uniform-Half-Normal distribution
            print("Using Half-Uniform-Half-Normal distribution")
            values1 = random.rand(math.ceil(n / 2)) * self.max_val * 0.5
            values1.sort()
            values2 = random.normal(0, 1, math.floor(n / 2))
            values2.sort()
            values2 += values2[0] * -1
            values2 /= values2[-1]
            values2 = values2 * self.max_val * 0.5 + self.max_val * 0.5
            values = np.concatenate((values1, values2), axis=None)
            values.sort()
        if case == 3:
            # Dense-Uniform distribution
            # Hiding a quarter of the dots in as small a space as possible
            print("Using Dense-Uniform distribution")
            quarter_n = round(n / 4)
            values1 = random.rand(n - quarter_n) * (self.max_val - quarter_n * d)
            values1 += quarter_n * d
            values2 = np.zeros(quarter_n)
            for i in range(quarter_n):
                values2[i] = d * i
            values = np.concatenate((values1, values2), axis=None)
            values.sort()
        if case == 4:
            # Dense-Normal distribution
            print("Using Dense-Normal distribution")
            quarter_n = round(n / 4)
            values1 = random.normal(0, 1, n - quarter_n)
            values1.sort()
            values1 -= values1[0]
            values1 /= values1[len(values1) - 1]
            values1 *= (self.max_val - quarter_n * d)
            values1 += quarter_n * d
            values2 = np.zeros(quarter_n)
            for i in range(quarter_n):
                values2[i] = d * i
            values = np.concatenate((values1, values2), axis=None)
            values.sort()
        if case == 5:
            # Half-Empty-Half-Uniform distribution
            print("Using Half-Empty-Half-Uniform distribution")
            values = random.rand(n)
            values *= 0.5
            values[n - 1] = 1
            values *= self.max_val
            values.sort()
        if case == 6:
            # Half-Empty-Half-Normal distribution
            print("Using Half-Empty-Half-Normal distribution")
            values = random.normal(0, 1, n)
            values.sort()
            values -= values[0]
            values /= values[n - 1]
            values *= 0.5
            values[n - 1] = 1
            values *= self.max_val
            values.sort()
        if case == 7:
            # Half-Sparse-Uniform distribution
            print("Using Half-Sparse-Uniform distribution")
            part_n = round(n/10000.0)
            values1 = random.rand(n - part_n)
            values1 *= 0.5
            values2 = random.rand(part_n)
            values2 *= 0.5
            values2 += 0.5
            values = np.concatenate((values1, values2), axis=None)
            values.sort()
        if case == 8:
            # Half-Sparse-Normal distribution
            print("Using Half-Sparse-Normal distribution")
            part_n = round(n/10000.0)
            values1 = random.normal(0, 1, n-part_n)
            values1.sort()
            values1 -= values1[0]
            values1 /= values1[len(values1)-1]
            values1 *= 0.5
            values2 = random.normal(0, 1, part_n)
            values2.sort()
            values2 -= values2[0]
            values2 /= values2[len(values2)-1]
            values2 *= 0.5
            values2 += 0.5
            values = np.concatenate((values1, values2))
            values.sort()
        if case == 9:
            # Rising sizes distribution
            # Normal distribution that has a string of gaps, each twice the size of the previous
            print("Using rising sizes distribution")
            n_rising = math.floor(math.log2(1/d))
            values = random.normal(0, 1, n)
            values.sort()
            values -= values[0]
            values /= values[-1]
            values *= 0.5
            for i in range(n_rising):
                values[-(i + 1)] = 1 - d * math.pow(2, i)
        if case == 10:
            # Chi-Squared distribution
            print("Using Chi-Squared distribution")
            values = random.chisquare(2, n)
            values.sort()
            values += values[0] * -1
            values /= values[n - 1]
            values = values * self.max_val

        # Rescale so that we have at least d distance between each dot
        values *= (self.max_val - n * d) / self.max_val
        for i in range(n):
            values[i] += i * d

        assert (values[0] >= 0)
        assert (values[len(values) - 1] <= self.max_val)
        assert sorted(values)

        return values

    def plot_distribution(self, values, buckets):
        y = np.zeros(buckets)
        x = np.zeros(buckets)
        k = 1
        bucket_size = self.max_val / buckets
        for i in range(len(values)):
            if values[i] <= k * bucket_size:
                y[k-1] += 1
            else:
                y[k] += 1
                k += 1
        for i in range(buckets):
            x[i] = i * bucket_size
        plt.plot(x, y)
        plt.show()

    def is_sampled(self, value):
        return self.sampled_intervals.is_in_interval(value)

    def is_long(self, value):
        return self.long_intervals.is_in_interval(value)

    # Sample a random pair of dots
    def sample_dots_uniform(self):
        sample_index = random.randint(-1, len(self.dots))
        if sample_index == -1:
            left = 0
            right = self.dots[0]
        elif sample_index == len(self.dots) - 1:
            left = self.dots[len(self.dots) - 1]
            right = 1
        else:
            left = self.dots[sample_index]
            right = self.dots[sample_index + 1]
        return left, right

    # Sample a random value
    def sample_value_uniform(self):
        sample_spot = random.rand() * self.max_val
        return self.sample_value_bin(sample_spot)

    def sample_value(self, value):
        j = 0
        while self.dots[j] < value:
            j += 1
            if j >= len(self.dots):
                break
        if j == 0:
            left = 0
            right = self.dots[j]
        elif j == len(self.dots):
            left = self.dots[len(self.dots) - 1]
            right = self.max_val
        else:
            left = self.dots[j - 1]
            right = self.dots[j]
        return left, right

    def sample_value_bin(self, value):
        l_index = 0
        r_index = len(self.dots) - 1
        while True:
            m = math.floor((l_index + r_index)/2)
            left = self.dots[m]
            # If we are checking the last element
            if m == len(self.dots) - 1:
                return left, self.max_val
            # If we are checking the first element and value is to the left of it
            if m == 0 and value < self.dots[0]:
                return 0, self.dots[0]
            right = self.dots[m + 1]
            if value < left:
                r_index = m
            elif value >= right:
                l_index = m + 1
            else:
                return left, right

    # Samples a random value, but keeps track of and ignores values over the long_threshold
    def sample_value_uniform_ignore_long(self, long_threshold):
        value = random.rand() * (self.max_val - self.long_intervals.total_space_occupied)
        value = self.long_intervals.scale_value(value)
        left, right = self.sample_value_bin(value)
        # if long - add to long space, else to sampled intervals
        i = 0
        if right - left > long_threshold:
            self.long_intervals.append_sorted((left, right))
        else:
            self.sampled_intervals.append_sorted((left, right))
        return left, right

    def sample_uniform_remove_duplicates(self):
        value = random.rand() * (self.max_val - self.long_space)
        i = 0
        while i < len(self.long_intervals) and value > self.long_intervals[i][0]:
            value += self.long_intervals[i][2]
            i += 1
        left, right = self.sample_value_bin(value)
        # if long - add to long space, else to sampled intervals
        i = 0
        invert = 1
        if self.is_sampled(value):
            while i < len(self.long_intervals) and self.long_intervals[i][0] < left:
                i += 1
            self.long_intervals.insert(i, (left, right, right - left))
            self.long_space += right - left
            invert = -1
        else:
            while i < len(self.sampled_intervals) and self.sampled_intervals[i][0] < left:
                i += 1
            self.sampled_intervals.insert(i, (left, right, right - left))
        return left, right, invert, self.long_intervals
