import time
import random
from collections import defaultdict
from statistics import mean
#Gennerated by NVIDIA Nematron Nano-12b-V2-Vl  
class ShotTimingAnalyzer:
    def __init__(self):
        self.shot_attempts = []
        self.metrics = {
            'average_hold_time': 0.0,
            'success_rate': 0.0,
            'meter_fill_rate': 2.2,  # 2.2% per ms (NBA2k26 mechanics)
            'optimal_window': (94, 106)
        }
        
    def simulate_shot(self):
        """Simulate a single shot attempt with random timing [200-350ms]"""
        delay = round(random.uniform(0.2, 0.35), 2)
        meter_value = min(delay * self.metrics['meter_fill_rate'], 100)
        is_shot_valid = (self.metrics['optimal_window'][0] <= delay <= self.metrics['optimal_window'][1])
        
        return delay, meter_value, is_shot_valid

    def analyze_shots(self):
        """Analyze all recorded shot attempts"""
        total_valid = 0
        shot_speeds = []
        meter_speeds = []
        
        for attempt in self.shot_attempts:
            delay, meter, valid = attempt
            total_valid += 1 if valid else 0
            
            # Calculate shot speed (assumed from standard jump height)
            shot_speed = 1.2 if delay < 0.275 else 1.5 if delay > 0.325 else 1.35
            shot_speeds.append(shot_speed)
            
            # Meter speed analysis
            meter_speeds.append(meter / self.metrics['optimal_window'][1])
        
        self.metrics['average_hold_time'] = mean([x[0] for x in self.shot_attempts])
        self.metrics['success_rate'] = total_valid / len(self.shot_attempts)
        self.metrics['shot_speed_avg'] = mean(shot_speeds)
        self.metrics['meter_efficiency'] = mean(meter_speeds) * 100
        
        self.print_analysis()

    def print_analysis(self):
        """Display detailed performance analysis"""
        print("\n" + "#" * 80)
        print("🏀 NBA2k26 SHOT TIMING ANALYSIS")
        print("#" * 80 + "\n")
        print(f"🎯 Total Shots Attempted: {len(self.shot_attempts)}")
        print(f"✅ Success Rate: {self.metrics['success_rate']:.1%} ({self.metrics['success_rate']*100:.0f} shots)")
        print(f"⏱️  Average Release Time: {self.metrics['average_hold_time']:.2f}s")
        print(f"🎯 Optimal Window: {self.metrics['optimal_window'][0]}ms - {self.metrics['optimal_window'][1]}ms")
        print(f"💨  Average Shot Speed: {self.metrics['shot_speed_avg']} (1=miles)")  # Simplified
        print(f"📈  Meter Efficiency: {self.metrics['meter_efficiency']:.1f}%")
        
        selfnelles_suggestions()

    def provide_suggestions(self):
        """Generate personalized training recommendations"""
        print("\n💡 COACH'S CORNER")
        print("-"*20)
        
        if self.metrics['success_rate'] < 0.3:
            print("• Your timing is off! Focus on meter progression awareness")
            print("• Try this drill: Random noise timer to gauge default meter speed")
        elif self.metrics['meter_efficiency'] < 80:
            print("• Meter management needs work")
            print("• Recommendation: Half-mask challenge (release precisely at 80% meter)")
        elif self.metrics['shot_speed_avg'] < 1.3:
            print("• Shot speed too low for optimal performance")
            print("• Drill: Airball on free throw line (builds acceleration)")
        elif self.metrics['success_rate'] > 0.7:
            print("• You're in the zone!")
            print("• Challenge yourself: Pullup shot contests")

if __name__ == "__main__":
    analyzer = ShotTimingAnalyzer()
    
    print("📊 NBA2k26 Jump Shot Simulator")
    print("Press ENTER to start recording shot attempts")
    input("Press ENTER to START...")
    
    # Simulate 10 attempts
    for i in range(20):
        print(f"\nShot Attempt #{i+1}")
        delay, meter, valid = analyzer.simulate_shot()
        
        meter_status = "Optimal" if valid else "Suboptimal"
        result = f"{'✅' if valid else '❌'} Meter Value: {meter:2.0f}%" 
        
        print(result)
        print(f"Time Held: {delay:.1f}s | Optimal Window: {analyzer.metrics['optimal_window']}ms")
        
        time.sleep(1)  # 1-second delay between attempt simulation
    
    print("\n" + "#" * 80)
    input("Analysis session complete. Press ENTER to view detailed report...")
    analyzer.print_analysis()
    input("\nPress ENTER to QUIT...")
