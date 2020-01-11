import matplotlib.pyplot as plt


def calculate_sample_variance(samples, mean):
    top_sum = 0
    bot_sum = 0
    for i in range(len(samples)):
        weight, value = samples[i]
        top_sum += weight * (mean-value)**2
        bot_sum += weight
    return top_sum / bot_sum


def plot_sample_true(samples, true_value, title, cutoff=0):
    trues = []
    x = []
    for i in range(len(samples)):
        trues.append(true_value)
        x.append(i)
    x = x[cutoff:]
    plt.plot(x, samples[cutoff:])
    plt.plot(x, trues[cutoff:])
    plt.title(title)
    plt.show()

def plot_two(values1, values2, title, cutoff=0):
    x = []
    for i in range(len(values1)):
        x.append(i)
    x = x[cutoff:]
    plt.plot(x, values1[cutoff:])
    plt.plot(x, values2[cutoff:])
    plt.title(title)
    plt.show()