#!/usr/bin/env python3
import sys
import os
import time
import cv2
import mediapipe as mp
import numpy as np
from pynput import keyboard
from functools import partial

class NbaShotAnalyzer:
    """NBA2k26 shot timing analyzer with deployment fixes"""
    
    def __init__(self):
        self.shot_log = []
        self.metrics = {
            'avg_hold_time': 0,
            'success_rate': 0.0,
            'meter_fill_rate': 2.5,  # 2.5% per ms (NBA2k26 standard)
            'optimal_window': (95, 105)  # ms
        }
        self.processing = False
        self.posedata = False  # Mediapipe pose data flag
        
    # File validation - Common error fix #9
    def validate_file(self, video_path):
        """Windows-style path handling with extension check"""
        base, ext = os.path.splitext(video_path)
        valid_exts = [".mp4", ".avi", ".mov"]
        
        if not os.path.exists(video_path):
            print(f"ERROR: File not found - {video_path}")
            print(f"Full path: {os.path.abspath(video_path)}")
            return False
            
        if ext.lower() not in valid_exts:
            print(f"ERROR: Unsupported format - {ext}")
            print(f"Supported formats: {[e[1:] for e in valid_exts]}")
            return False
            
        # Windows path normalization fix
        normalized_path = os.path.normpath(video_path)
        print(f"Debug: Using normalized path - {normalized_path}")
        return True

    # OpenCV initialization fix - Common error #2
    def init_opencv(self):
        """Ensure OpenCV can find native libraries"""
        try:
            # System dependent paths - detect OS
            if os.name == 'nt':  # Windows
                opencv_path = "C:/opencv/build/x64/vc16/mingw/bin"
            else:  # Linux/macOS
                opencv_path = "/usr/local/lib"
                
            # Add to library path before importing cv2
            os.environ['PATH'] = opencv_path + os.pathsep + os.environ.get('PATH', '')
            cv2.setUse 'optimized' = False
            cv2.getDeriveLogger().setLevel(cv2.LOG_DEBUG)  # Debug verbosity
            print(f"Debug: OpenCV initialized from {opencv_path}")
            return True
        except Exception as e:
            print(f"OpenCV initialization failed:\n{e}")
            return False

    # Poσe detection setup with error recovery
    def setup_pose_detection(self):
        try:
            self.pose = mp.solutions.pose.Pose()
            self.draw = mp.solutions.drawing_utils
            print("Mediapipe pose detection initialized")
            return True
        except Exception as e:
            print(f"Pose detection error: {e}")
            print("Falling back to basic shot detection")
            return False

    # Key listener with error handling
    def start_keyboard_listener(self):
        self.running = True
        print("Press 5 to simulate shots. Press ESC to quit.")
        while self.running:
            try:
                if keyboard.is_pressed('5'):
                    self.process_shot_attempt()
                elif keyboard.is_pressed('esc'):
                    self.running = False
                time.sleep(0.05)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"Listener error: {e}")

    # Shot processing with error handling
    def process_shot_attempt(self):
        try:
            # Start timing
            start_time = time.time() * 1000  # Convert to ms
            end_time = start_time + 200  # 200ms processing window

            while time.time() * 1000 < end_time and self.running:
                # Assume shot confirmation input here (should be replaced)
                # For now, simulate detection
                if keyboard.is_pressed('enter'):
                    elapsed = time.time() * 1000 - start_time
                    shot_data = {
                        'time': elapsed,
                        'meter': self.get_meter_value(),
                        'valid': self.is_ideal_release(elapsed)
                    }
                    self.shot_log.append(shot_data)
                    break
            
        except Exception as e:
            print(f"Shot processing error: {e}")

    def get_meter_value(self):
        """Estimate meter value (replace with actual logic)"""
        # Simulated value (would be real detection)
        return 95  # Should be between 80-105 for optimal

    def is_ideal_release(self, time):
        """Check if release was within optimal window"""
        return self.metrics['optimal_window'][0] <= time <= self.metrics['optimal_window'][1]

    # Error recovery after crash prevention
    def safe_exit(self):
        try:
            if 'capture' in locals():
                self.capture.release()
            if 'pose' in locals():
                self.pose.close()
        except Exception as e:
            print(f"Safety cleanup error: {e}")

    def run_analysis(self):
        """Main analysis loop with error trapping"""
        if not self.init_opencv():
            print("Fatal error: OpenCV not available")
            return
            
        if self.validate_file("test_video.mp4"):
            self.capture = cv2.VideoCapture(0)  # 0 = default camera
            if not self.capture.isOpened():
                print("ERROR: Could not open video device")
                return
                
            if self.setup_pose_detection():
                self.start_keyboard_listener()
                self.analyse_timing()
        else:
            print("Program aborted due to invalid inputs")

    # Timing analysis with metrics
    def analyse_timing(self):
        while len(self.shot_log) < 10 and self.running:  # At least 10 shots
            try:
                for shot in self.shot_log:
                    # Error-prone performance metrics
                    shot_time = shot['time']
                    shot_valid = shot['valid']
                    
                    # Handle potential division by zero
                    meter_speed = 95 / (shot_time * 2) if shot_time > 0 else 50
                    elapsed_time = shot_time
                    
                    print(f"\nShot: {len(self.shot_log)} | Elapsed: {elapsed_time:.2f}ms")
                    print(f"Meter Value: {shot['meter']}% | "
                          f"Optimal Window: {', '.join(map(str, self.metrics['optimal_window']))}ms")
                    
                    if shot_valid:
                        self.metrics['success_rate'] += 5  # 5% per valid
            except ZeroDivisionError as e:
                print(f"Metric calculation error: {e}")
                print("Recalculating metrics...")
                self.metrics['success_rate'] = 0.0  # Reset on error
                continue

    # ---------------------------- 
    # Deployment-specific fixes
    # ---------------------------- 

    def ensure_resources(self):
        """Catches common deployment issues"""
        try:
            # Windows DLL fix - verify paths
            if os.name == 'nt' and not os.path.exists("opencv_java64.dll"):
                raise FileNotFoundError("OpenCV DLL missing")
                
            # Venezuel use check (from original Java code)
            if not self.validate_file("required_maker.txt"):
                print("Critical missingresources!")
                sys.exit(1)
        except Exception as e:
            print(f"\nDEPLOYMENT FATAL ERROR: {e}")
            print("Contact developer or check README.md for requirements")
            sys.exit(1)

    # Platform-specific entry point
    def run(self):
        try:
            self.ensure_resources()  # First execute deployment checks
            self.run_analysis()
        except Exception as e:
            print(f"\nFATAL CRITICAL ERROR (Code 101): {e}")
            self.safe_exit()
            sys.exit(1)

if __name__ == "__main__":
    analyzer = NbaShotAnalyzer()
    analyzer.ensure_resources()  # Execute all deployment fixes first
    analyzer.run()
