#!/usr/bin/env python3
"""
RSVP Experiment Launcher with Environment Selection
===================================================

Advanced launcher that allows you to select between Hospital and Lab environments
with appropriate hardware configurations.
"""

import sys
import os
from rsvp_experiment import RSVPExperiment

def display_environment_info():
    """Display information about the two environments"""
    print("RSVP Experiment Environment Selector")
    print("=" * 45)
    print()
    print("🏥 HOSPITAL ENVIRONMENT:")
    print("   • Gamepad/Joystick input")
    print("   • DAQ pulse generation for EEG")
    print("   • Hardware screening tests")
    print("   • Fullscreen mode (1920x1080)")
    print("   • Extended sequences (2 sequences, 15 images each)")
    print("   • Research-grade data collection")
    print()
    print("🔬 LAB ENVIRONMENT:")
    print("   • Keyboard input only")
    print("   • No pulse generation")
    print("   • No hardware screening")
    print("   • Windowed mode (1024x768)")
    print("   • Shorter sequences (3 sequences, 10 images each)")
    print("   • Development and testing friendly")
    print()

def select_environment():
    """Interactive environment selection"""
    display_environment_info()
    
    while True:
        print("Select environment:")
        print("1. Hospital (Full hardware)")
        print("2. Lab (Basic setup)")
        print("3. Custom configuration")
        print("0. Exit")
        print()
        
        choice = input("Enter choice (0-3): ").strip()
        
        if choice == '0':
            print("Exiting...")
            return None
        elif choice == '1':
            return 'hospital'
        elif choice == '2':
            return 'lab'
        elif choice == '3':
            return 'custom'
        else:
            print("Invalid choice. Please select 0-3.")
            print()

def check_environment_requirements(environment):
    """Check if environment requirements are met"""
    print(f"Checking {environment} environment requirements...")
    
    if environment == 'hospital':
        # Check for gamepad
        try:
            from rsvp_hardware import GamepadController
            gamepad = GamepadController()
            if gamepad.initialize():
                print(f"✅ Gamepad detected: {gamepad.gamepad_name}")
                gamepad.cleanup()
            else:
                print("⚠️  No gamepad detected - Hospital environment may not work properly")
                response = input("Continue anyway? (y/n): ").lower()
                if response != 'y':
                    return False
        except ImportError:
            print("❌ Gamepad support not available (pygame missing)")
            return False
        
        # Check for DAQ
        try:
            from rsvp_hardware import PulseGenerator
            pulse_gen = PulseGenerator()
            if pulse_gen.initialize():
                print("✅ DAQ device detected")
                pulse_gen.cleanup()
            else:
                print("⚠️  No DAQ device detected - EEG pulses will not work")
                response = input("Continue anyway? (y/n): ").lower()
                if response != 'y':
                    return False
        except ImportError:
            print("⚠️  DAQ support not available (nidaqmx missing)")
            response = input("Continue without pulses? (y/n): ").lower()
            if response != 'y':
                return False
    
    elif environment == 'lab':
        print("✅ Lab environment - keyboard and monitor only")
    
    return True

def run_with_environment(environment):
    """Run the experiment with specified environment"""
    
    # Check requirements
    if not check_environment_requirements(environment):
        print("Environment requirements not met.")
        return False
    
    # Load appropriate config
    config_files = {
        'hospital': 'rsvp_config_hospital.json',
        'lab': 'rsvp_config_lab.json',
        'custom': 'rsvp_config.json'
    }
    
    config_file = config_files.get(environment, 'rsvp_config.json')
    
    if not os.path.exists(config_file):
        print(f"Configuration file {config_file} not found!")
        print("Please ensure the configuration files are present.")
        return False
    
    try:
        print(f"\nStarting RSVP experiment in {environment.upper()} mode...")
        print("=" * 50)
        
        # Create and run experiment with environment pre-configured
        experiment = RSVPExperiment(config_file)
        
        # Run experiment with environment parameter (patient-friendly)
        success = experiment.run_experiment(environment=environment)
        
        if success:
            print(f"\n🎉 Experiment completed successfully in {environment.upper()} mode!")
            print("Data has been saved to the 'experiment_data' folder.")
        else:
            print(f"\nExperiment ended early in {environment.upper()} mode.")
        
        return success
        
    except KeyboardInterrupt:
        print(f"\nExperiment interrupted by user in {environment.upper()} mode.")
        return False
    except Exception as e:
        print(f"\nError running experiment in {environment.upper()} mode: {e}")
        return False

def main():
    """Main launcher function"""
    print("RSVP Experiment Launcher")
    print("=" * 30)
    print()
    
    # Check basic requirements
    if not os.path.exists("RSVP_HClinic/000rsvpscr_pic"):
        print("❌ Error: Images directory not found!")
        print("Please ensure the RSVP_HClinic folder is in the same directory as this script.")
        input("Press Enter to exit...")
        return
    
    # Environment selection
    environment = select_environment()
    if not environment:
        return
    
    # Run experiment
    success = run_with_environment(environment)
    
    # Final message
    if success:
        print("\nThank you for using the RSVP experiment!")
    else:
        print("\nExperiment session ended.")
    
    input("\nPress Enter to exit...")

def quick_hospital():
    """Quick launcher for hospital environment"""
    print("Quick Hospital Environment Launch")
    print("=" * 35)
    return run_with_environment('hospital')

def quick_lab():
    """Quick launcher for lab environment"""
    print("Quick Lab Environment Launch")
    print("=" * 30)
    return run_with_environment('lab')

if __name__ == "__main__":
    # Check for command line arguments for quick launch
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == 'hospital' or arg == 'h':
            quick_hospital()
        elif arg == 'lab' or arg == 'l':
            quick_lab()
        else:
            print(f"Unknown argument: {arg}")
            print("Usage: python launch_rsvp.py [hospital|lab]")
    else:
        main()
