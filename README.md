### Data Stream Simulation

The function `generate_data_stream` generates a continuous stream of floating-point numbers. It simulates a real-time data stream with the following features:
- A regular pattern based on a sine wave, representing seasonality.
- Random noise to introduce variability in the stream.
- Random anomalies, which occur with a certain probability (`anomaly_prob`), representing outliers (e.g., sudden spikes or drops).

The function yields data points one by one, simulating real-time data flow with a small delay (`time.sleep(0.01)`).

Parameters:
- `length` (int): Number of data points to generate.
- `anomaly_prob` (float): Probability of an anomaly occurring.
- `noise_level` (float): Amplitude of random noise.

Yields:
- `float`: The next value in the data stream.

### Anomaly Detection Algorithm

The `z_score_anomaly_detection` function uses the Z-Score method to detect anomalies in the data stream. It compares the latest value in the stream with the mean and standard deviation of the previous values (stored in a sliding window). If the Z-score exceeds a predefined threshold, the value is flagged as an anomaly.

Parameters:
- `window` (deque): A sliding window containing the most recent data points.
- `threshold` (float): The Z-score threshold above which a value is considered an anomaly (default is 3).

Returns:
- `bool`: True if the latest value is an anomaly, False otherwise.

The `monitor_stream` function is a simple real-time stream monitor that:
- Receives a data stream.
- Maintains a sliding window of the most recent data points.
- Detects and prints anomalies as they are streamed.

### Real-time Visualization

The `real_time_visualization` function displays the data stream and highlights any anomalies in real-time using **matplotlib**. It updates the plot as new data is streamed, marking detected anomalies in red.

Parameters:
- `stream` (generator): The real-time data stream.
- `window_size` (int): The size of the sliding window for anomaly detection.

