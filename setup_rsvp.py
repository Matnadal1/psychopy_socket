#!/usr/bin/env python3
"""
RSVP Experiment Setup Script
============================

This script helps set up the RSVP experiment environment and test hardware components.
"""

import sys
import os
import subprocess

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        print("Note: nidaqmx is optional and only needed for DAQ pulse generation")
        return False

def check_directories():
    """Check if required directories exist"""
    print("Checking directories...")
    
    required_dirs = [
        "RSVP_HClinic/000rsvpscr_pic",
        "experiment_data"
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"{dir_path} - Found")
        else:
            print(f"{dir_path} - Missing")
            if dir_path == "experiment_data":
                os.makedirs(dir_path)
                print(f"   Created {dir_path}")
            else:
                all_good = False
    
    return all_good

def test_hardware():
    """Test hardware components"""
    print("Testing hardware components...")
    
    try:
        from rsvp_hardware import GamepadController, PulseGenerator
        
        # Test gamepad
        print("Testing gamepad...")
        gamepad = GamepadController()
        if gamepad.initialize():
            print(f"✅ Gamepad found: {gamepad.gamepad_name}")
            gamepad.cleanup()
        else:
            print("⚠️  No gamepad detected (optional)")
        
        # Test DAQ
        print("Testing DAQ...")
        pulse_gen = PulseGenerator()
        if pulse_gen.initialize():
            print("✅ DAQ device found")
            pulse_gen.cleanup()
        else:
            print("⚠️  No DAQ device found (optional)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Hardware test error: {e}")
        return False

def create_config_templates():
    """Create configuration templates for different environments"""
    print("Creating environment configuration templates...")
    
    import json
    
    # Hospital environment config
    hospital_config = {
        "withpulses": True,
        "language": "english",
        "device_response": "gamepad",
        "pictures_path": "RSVP_HClinic/000rsvpscr_pic",
        "window_resolution": [1920, 1080],
        "fullscreen": True,
        "isi": [1.0],
        "seq_length": 15,
        "n_sequences": 5,
        "max_wait_response": 10.0,
        "min_blank_duration": 1.25,
        "max_rand_blank": 0.5,
        "min_lines_duration": 0.5,
        "max_rand_lines": 0.2,
        "line_thickness": 5,
        "line_offset": 5,
        "daq_device": "Dev1",
        "daq_port": "port0",
        "enable_screening": True
    }
    
    # Lab environment config
    lab_config = {
        "withpulses": False,
        "language": "english",
        "device_response": "keyboard",
        "pictures_path": "RSVP_HClinic/000rsvpscr_pic",
        "window_resolution": [1024, 768],
        "fullscreen": False,
        "isi": [1.0],
        "seq_length": 10,
        "n_sequences": 3,
        "max_wait_response": 10.0,
        "min_blank_duration": 1.25,
        "max_rand_blank": 0.5,
        "min_lines_duration": 0.5,
        "max_rand_lines": 0.2,
        "line_thickness": 5,
        "line_offset": 5,
        "daq_device": "Dev1",
        "daq_port": "port0",
        "enable_screening": False
    }
    
    # Default/custom config (balanced)
    default_config = {
        "withpulses": False,
        "language": "english",
        "device_response": "keyboard",
        "pictures_path": "RSVP_HClinic/000rsvpscr_pic",
        "window_resolution": [1024, 768],
        "fullscreen": False,
        "isi": [1.0],
        "seq_length": 10,
        "n_sequences": 3,
        "max_wait_response": 10.0,
        "min_blank_duration": 1.25,
        "max_rand_blank": 0.5,
        "min_lines_duration": 0.5,
        "max_rand_lines": 0.2,
        "line_thickness": 5,
        "line_offset": 5,
        "daq_device": "Dev1",
        "daq_port": "port0",
        "enable_screening": False
    }
    
    # Save configurations
    with open("rsvp_config_hospital.json", "w") as f:
        json.dump(hospital_config, f, indent=2)
    print("✅ Created rsvp_config_hospital.json (Full hardware)")
    
    with open("rsvp_config_lab.json", "w") as f:
        json.dump(lab_config, f, indent=2)
    print("✅ Created rsvp_config_lab.json (Basic setup)")
    
    with open("rsvp_config.json", "w") as f:
        json.dump(default_config, f, indent=2)
    print("✅ Created rsvp_config.json (Default/Custom)")

def main():
    """Main setup function"""
    print("RSVP Experiment Setup")
    print("=" * 25)
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        return False
    
    print(f"Python {sys.version}")
    print()
    
    # Install requirements
    if not install_requirements():
        print("Some packages failed to install. You may need to install them manually.")
    print()
    
    # Check directories
    if not check_directories():
        print("Missing required directories. Please ensure RSVP_HClinic folder is present.")
        return False
    print()
    
    # Test hardware
    test_hardware()
    print()
    
    # Create config templates
    create_config_templates()
    print()
    
    print("Setup Summary:")
    print("=" * 15)
    print("✅ Basic setup completed!")
    print("📁 Environment configurations created:")
    print("   • rsvp_config_hospital.json (Full hardware)")
    print("   • rsvp_config_lab.json (Basic setup)")
    print("   • rsvp_config.json (Custom template)")
    print("🎮 Hardware components tested")
    print()
    print("Next steps:")
    print("1. Run 'python test_rsvp_hardware.py' to test hardware")
    print("2. Run 'python launch_rsvp.py' to select environment and start")
    print("3. Quick launch options:")
    print("   - 'python launch_rsvp.py hospital' for Hospital environment")
    print("   - 'python launch_rsvp.py lab' for Lab environment")
    print("4. Edit config files to customize the experiment")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nSetup error: {e}")
        sys.exit(1)
