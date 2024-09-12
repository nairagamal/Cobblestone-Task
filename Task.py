# Import necessary libraries
import numpy as np
import time
from collections import deque
import matplotlib.pyplot as plt

# Anomaly detection class using Z-Score with EWMA
class ZScoreEWMA_AnomalyDetector:
    def __init__(self, alpha=0.3, threshold=3):
        """
        Initialize the anomaly detector with given parameters.

        :param alpha: Smoothing factor for EWMA (0 < alpha < 1).
        :param threshold: Z-Score threshold beyond which an anomaly is flagged.
        """
        self.alpha = alpha
        self.mean_ewma = None
        self.variance_ewma = None
        self.threshold = threshold

    def detect(self, value):
        """
        Detect if the current value is an anomaly based on Z-Score and EWMA.
        
        :param value: Current data stream value.
        :return: True if an anomaly is detected, False otherwise.
        """
        # Initialize EWMA on first run
        if self.mean_ewma is None:
            self.mean_ewma = value
            self.variance_ewma = 0
            return False

        # Update EWMA for the mean
        self.mean_ewma = self.alpha * value + (1 - self.alpha) * self.mean_ewma

        # Update EWMA for variance (based on deviation from mean)
        deviation = value - self.mean_ewma
        self.variance_ewma = self.alpha * (deviation ** 2) + (1 - self.alpha) * self.variance_ewma

        # Compute Z-Score
        std = np.sqrt(self.variance_ewma)
        z_score = abs(deviation) / (std + 1e-6)  # Adding epsilon to avoid division by zero

        # Return True if the Z-Score exceeds the threshold (indicating an anomaly)
        return z_score > self.threshold


# Function to simulate a continuous data stream
def generate_data_stream(length=1000, anomaly_prob=0.05, noise_level=0.1):
    """
    Generates a stream of data simulating real-time input with some noise and occasional anomalies.
    
    :param length: Total number of data points to generate.
    :param anomaly_prob: Probability of an anomaly occurring.
    :param noise_level: Standard deviation of the added noise.
    :yield: Generated data point.
    """
    for i in range(length):
        # Regular sinusoidal data with added Gaussian noise
        regular_value = np.sin(i * 2 * np.pi / 100)
        noisy_value = regular_value + np.random.normal(0, noise_level)

        # Introduce anomalies based on probability
        if np.random.rand() < anomaly_prob:
            anomaly = np.random.choice([10, -10])
            yield noisy_value + anomaly
        else:
            yield noisy_value

        # Simulate real-time data streaming
        time.sleep(0.01)


# Function to visualize the real-time data stream with anomaly detection
def real_time_visualization(stream, anomaly_detector, window_size=30):
    """
    Visualizes the data stream in real time, highlighting anomalies as they are detected.
    
    :param stream: Data stream generator function.
    :param anomaly_detector: The anomaly detector object.
    :param window_size: Number of points to retain in the sliding window for visualization.
    """
    # Sliding window to keep recent data points
    window = deque(maxlen=window_size)
    data_points = []
    anomalies = []

    # Enable interactive plotting
    plt.ion()
    fig, ax = plt.subplots()

    for value in stream:
        # Append current value to the window and overall list of points
        window.append(value)
        data_points.append(value)

        # Detect if current value is an anomaly
        if anomaly_detector.detect(value):
            anomalies.append(len(data_points) - 1)

        # Clear and update the plot
        ax.clear()
        ax.plot(data_points, label="Data Stream")
        ax.scatter(anomalies, [data_points[i] for i in anomalies], color='red', label="Anomalies")
        ax.legend()

        # Redraw the plot
        plt.draw()
        plt.pause(0.01)

    # Disable interactive plotting and show the final result
    plt.ioff()
    plt.show()


# Main program
if __name__ == "__main__":
    # Step 1: Create the anomaly detector with given parameters
    anomaly_detector = ZScoreEWMA_AnomalyDetector(alpha=0.3, threshold=3)

    # Step 2: Simulate a real-time data stream
    stream = generate_data_stream()

    # Step 3: Visualize the data stream and detect anomalies in real-time
    real_time_visualization(stream, anomaly_detector)
