import time
import logging

logging.basicConfig(level=logging.INFO)

def simulate_cpu_spike(duration=60, cpu_percent=80):
    logging.info(f"Starting CPU spike at {cpu_percent}%")

    end_time = time.time() + duration

    while time.time() < end_time:
        for _ in range(1000000):
            pass  # Busy loop

    logging.info("CPU spike completed")

if __name__ == "__main__":
    simulate_cpu_spike()