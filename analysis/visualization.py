import matplotlib.pyplot as plt

def plot_signal(signal, step=1):
    sampled = signal[::step]
    plt.plot(sampled)
    plt.title("Market Sentiment Signal (Sampled)")
    plt.xlabel("Time")
    plt.ylabel("Signal Strength")
    plt.show()

