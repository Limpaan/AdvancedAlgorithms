import matplotlib.pyplot as plt
import math
from DotSpace import DotSpace
from HomeExamHelpers import *
from tqdm import tqdm
from scipy.special import stdtrit

sample_means = []
sample_variance = []
confidence_thresholds = []
done_thresholds = []

# Interval and dot values
n = 100000
d = 0.000000005
interval_max = 1

# Sampling values
m_max = 6000
gamma = 0.1
alpha = 0.1

dot_interval = DotSpace(n, d, interval_max, DotSpace.UNIFORM_NORMAL_DIST)


def pure_uniform(dots, n_probes, g, a):
    top_sum = 0
    bot_sum = 0
    samples = []
    dots.soft_reset()
    for i in tqdm(range(n_probes)):
        left, right = dots.sample_value_uniform()
        dist = right - left
        top_sum += dots.max_val
        bot_sum += dots.max_val / dist
        samples.append((1 / dist, dist))

        mean = top_sum / bot_sum
        var = calculate_sample_variance(samples, mean)

        confidence_limit = stdtrit(i, 1 - a) * math.sqrt(var) / math.sqrt(i + 1)
        done_limit = g * mean

        sample_means.append(mean)
        sample_variance.append(var)
        confidence_thresholds.append(confidence_limit)
        done_thresholds.append(done_limit)

        if confidence_limit < done_limit:
            break
    return dots.max_val / mean


def ignore_long_uniform(dots, n_probes, g, a, long_threshold):
    top_sum = 0
    bot_sum = 0
    samples = []
    dots.soft_reset()
    for i in tqdm(range(n_probes)):
        left, right = dots.sample_value_uniform_ignore_long(long_threshold)
        dist = right - left
        if not dist > long_threshold:
            top_sum += dots.max_val
            bot_sum += dots.max_val / dist
            samples.append((1 / dist, dist))

        if len(samples) > 0:
            mean = top_sum / bot_sum
            var = calculate_sample_variance(samples, mean)

            number_long_intervals = dots.long_intervals.number_of_unique_intervals
            confidence_limit = stdtrit(i - number_long_intervals, 1 - a) * math.sqrt(var) / math.sqrt(i - number_long_intervals + 1)
            done_limit = g * mean

            sample_means.append(mean)
            sample_variance.append(var)
            confidence_thresholds.append(confidence_limit)
            done_thresholds.append(done_limit)

            if confidence_limit < done_limit:
                break
    dist_long_intervals = dots.long_intervals.total_space_occupied
    return (dots.max_val - dist_long_intervals) / mean + number_long_intervals


ignore_long_uniform(dot_interval, m_max, gamma, alpha, 0.0137)
plot_sample_true(sample_means, dot_interval.get_mean_no_longs(0.0137), "Sample Mean vs True Mean", 15)
plot_sample_true(sample_variance, dot_interval.get_var_no_longs(0.0137), "Sample Variance vs True Variance", 15)
plot_two(confidence_thresholds, done_thresholds, "Confidence threshold vs Gamma threshold", 15)