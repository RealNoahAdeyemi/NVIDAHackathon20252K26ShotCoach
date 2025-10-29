import time
import keyboard
from collections import deque
from statistics import mean
import numpy as np
import pynput
from pynput import keyboard as input
import sys

class Nba2k26Optimizer:
    def __init__(self):
        self.shot_attempts = []
        self.metrics = {
            'average_hold_time': 0.0,
            'success_rate': 0.0,
            'meter_fill_rate': 2.2,  # Adjust based on in-game meter speed
            'optimal_window': (94, 106),  # ms
            'win_rate': 0.0,
            'total_shots': 0
        }

    def key_listener(self):
        """Real-time key monitoring thread"""
        with input.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('5'):
            self.start_time = time.time()
            self.is_射击中 = True
        return True

    def on_release(self, key):
        if key == keyboard.KeyCode.from_char('5'):
            if self.is_射击中:
                release_time = time.time()
                hold_duration = (release_time - self.start_time) * 1000
                result = {
                    'time': hold_duration,
                    'valid': self._check_optimal(hold_duration)
                }
                self.shot_attempts.append(result)
                self.metrics['total_shots'] += 1
                if self.metrics['win_rate'] is not None:
                    self.metrics['success_rate'] = (self.metrics['win_rate'] + result['valid']) / 2
                input.Listener.stop()
                self.is_射击中 = False

    def _check_optimal(self, duration):
        """Check if shot timing was optimal"""
        return self.metrics['optimal_window'][0] <= duration <= self.metrics['optimal_window'][1]

    def analyze(self):
        """Calculate real-time metrics from shot data"""
        self.metrics.update({
            'average_hold_time': mean([s['time'] for s in self.shot_attempts]),
            'success_rate': sum(1 for s in self.shot_attempts if s['valid']),
            'pouring_meter_time': self._get_meter_fill_time()
        })

    def _get_meter_fill_time(self):
        """Calculate theoretical optimal hold time based on meter speed"""
        return len(self.shot_attempts) and (self.metrics['peak_meter']/self.metrics['meter_fill_rate'])

    def print_report(self):
        print(f"\n=== NBA2k26 SHOT OPTIMIZER FEEDBACK ===")
        print(f"Average Hold Time: {self.metrics['average_hold_time']:.1f}ms")
        print(f"Success Rate: {self.metrics['success_rate']*100:.1f}%")
        print(f"Optimal Window: {self.metrics['optimal_window']}ms")
        self._show_training_tips()

    def _show_training_tips(self):
        if self.metrics['success_rate'] < 0.6:
            print("\n🚨 IMPROVEMENT AREA:")
            print("• Practice timing drills with 2.2% meter fill simulations")
            print("• Use 3-tier release targets: 80% (clear), 95% (good), 100% (absorbed)")
        elif self.metrics['success_rate'] < 0.8:
            print("\n🏆 COMPETITIVE READY:")
            print("• Maintain 9-12 ms consistent variance")
            print("• Master 105-115 ms window for clutch servers")
        else:
            print("\n🏆 PRO LEVEL PERFORMANCE")
            print("• Focus on half-jump consistency and bailout shots")

def main():
    optimizer = Nba2k26Optimizer()
    print("【 NBA2k26 SHOT OPTIMIZER 】")
    print("• Shot timing analyzer for PC NBA2K26")
    print("• Press 'ESC' to quit at any time\n")

    # Start background key monitoring
    from threading import Thread
    thread = Thread(target=optimizer.key_listener)
    thread.start()

    # Main game analysis loop
    try:
        while True:
            time.sleep(0.5)
            optimizer.analyze()
            if len(optimizer.shot_attempts) > 0:
                optimizer.print_report()
    except KeyboardInterrupt:
        print("\nFinal metrics:")
        optimizer.print_report()
        sys.exit(0)

if __name__ == "__main__":
    main()
