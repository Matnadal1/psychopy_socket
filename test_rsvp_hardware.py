#!/usr/bin/env python3
"""
RSVP Hardware Test Suite
========================

Standalone test script for RSVP hardware components.
This script allows you to test gamepad, pulse generation, and screening functionality
independently of the main experiment.
"""

import sys
import os
from psychopy import visual, core, event
from rsvp_hardware import (
    GamepadController, 
    PulseGenerator, 
    ScreeningTools,
    test_gamepad_standalone,
    test_pulses_standalone
)

def test_gamepad_interactive():
    """Interactive gamepad test with visual feedback"""
    print("Interactive Gamepad Test")
    print("=" * 30)
    
    # Initialize gamepad
    gamepad = GamepadController()
    if not gamepad.initialize():
        print("Failed to initialize gamepad")
        return False
    
    # Create simple window for visual feedback
    try:
        window = visual.Window([800, 600], color='gray', units='pix')
        
        # Create visual elements
        title = visual.TextStim(
            window, 
            text=f"Gamepad Test: {gamepad.gamepad_name}",
            pos=(0, 250),
            height=30,
            color='white'
        )
        
        button_text = visual.TextStim(
            window,
            text="Press gamepad buttons\nPress 'q' on keyboard to exit",
            pos=(0, 0),
            height=25,
            color='white'
        )
        
        status_text = visual.TextStim(
            window,
            text="",
            pos=(0, -150),
            height=20,
            color='yellow'
        )
        
        # Test loop
        print("Visual gamepad test started. Press 'q' to exit.")
        
        while True:
            # Check keyboard for exit
            keys = event.getKeys()
            if 'q' in keys or 'escape' in keys:
                break
            
            # Check gamepad buttons
            button_states = gamepad.get_all_buttons()
            pressed_buttons = [i for i, state in enumerate(button_states) if state]
            
            if pressed_buttons:
                status_text.text = f"Buttons pressed: {pressed_buttons}"
                status_text.color = 'green'
            else:
                status_text.text = "No buttons pressed"
                status_text.color = 'yellow'
            
            # Draw everything
            title.draw()
            button_text.draw()
            status_text.draw()
            window.flip()
            
            core.wait(0.01)
        
        window.close()
        gamepad.cleanup()
        print("Interactive gamepad test completed")
        return True
        
    except Exception as e:
        print(f"Error in interactive gamepad test: {e}")
        gamepad.cleanup()
        return False

def test_pulse_interactive():
    """Interactive pulse test with visual feedback"""
    print("Interactive Pulse Test")
    print("=" * 25)
    
    # Initialize pulse generator
    pulse_gen = PulseGenerator()
    if not pulse_gen.initialize():
        print("Failed to initialize pulse generator")
        return False
    
    try:
        window = visual.Window([800, 600], color='gray', units='pix')
        
        # Create visual elements
        title = visual.TextStim(
            window,
            text="Pulse Generator Test",
            pos=(0, 250),
            height=30,
            color='white'
        )
        
        instructions = visual.TextStim(
            window,
            text="Press number keys (1-9) to send pulses\nPress 's' for signature pulse\nPress 'q' to exit",
            pos=(0, 100),
            height=20,
            color='white'
        )
        
        status_text = visual.TextStim(
            window,
            text="Ready to send pulses",
            pos=(0, -50),
            height=25,
            color='yellow'
        )
        
        pulse_display = visual.Rect(
            window,
            width=100,
            height=100,
            pos=(0, -150),
            fillColor='red'
        )
        pulse_display.opacity = 0
        
        print("Interactive pulse test started. Press number keys to send pulses.")
        
        while True:
            keys = event.getKeys()
            
            if 'q' in keys or 'escape' in keys:
                break
            
            pulse_sent = False
            pulse_value = 0
            
            # Check for number key presses
            for i in range(1, 10):
                if str(i) in keys:
                    pulse_value = i
                    pulse_gen.send_pulse(pulse_value)
                    pulse_sent = True
                    break
            
            # Check for signature pulse
            if 's' in keys:
                pulse_gen.send_signature_pulses()
                status_text.text = "Signature pulses sent!"
                pulse_display.opacity = 1
                pulse_sent = True
            
            if pulse_sent and pulse_value > 0:
                status_text.text = f"Pulse sent: {pulse_value}"
                pulse_display.opacity = 1
            elif not pulse_sent:
                status_text.text = "Ready to send pulses"
                pulse_display.opacity = max(0, pulse_display.opacity - 0.05)
            
            # Draw everything
            title.draw()
            instructions.draw()
            status_text.draw()
            pulse_display.draw()
            window.flip()
            
            core.wait(0.01)
        
        window.close()
        pulse_gen.cleanup()
        print("Interactive pulse test completed")
        return True
        
    except Exception as e:
        print(f"Error in interactive pulse test: {e}")
        pulse_gen.cleanup()
        return False

def test_screening_suite():
    """Test the complete screening suite"""
    print("Screening Suite Test")
    print("=" * 20)
    
    try:
        window = visual.Window([1024, 768], color='gray', units='pix')
        
        # Initialize hardware
        gamepad = GamepadController()
        gamepad.initialize()
        
        pulse_gen = PulseGenerator()
        pulse_gen.initialize()
        
        # Create screening tools
        screening = ScreeningTools(window)
        screening.set_hardware(gamepad, pulse_gen)
        
        # Run screening battery
        screening.run_screening_battery()
        
        # Cleanup
        window.close()
        if gamepad.connected:
            gamepad.cleanup()
        if pulse_gen.available:
            pulse_gen.cleanup()
        
        print("Screening suite completed")
        return True
        
    except Exception as e:
        print(f"Error in screening suite: {e}")
        return False

def main():
    """Main test interface"""
    print("RSVP Hardware Test Suite")
    print("=" * 30)
    print()
    print("Available tests:")
    print("1. Simple Gamepad Test")
    print("2. Interactive Gamepad Test")
    print("3. Simple Pulse Test")
    print("4. Interactive Pulse Test")
    print("5. Screening Suite Test")
    print("6. Run All Tests")
    print("0. Exit")
    print()
    
    while True:
        try:
            choice = input("Select test (0-6): ").strip()
            
            if choice == '0':
                print("Exiting...")
                break
            elif choice == '1':
                test_gamepad_standalone()
            elif choice == '2':
                test_gamepad_interactive()
            elif choice == '3':
                test_pulses_standalone()
            elif choice == '4':
                test_pulse_interactive()
            elif choice == '5':
                test_screening_suite()
            elif choice == '6':
                print("Running all tests...")
                test_gamepad_standalone()
                test_gamepad_interactive()
                test_pulses_standalone()
                test_pulse_interactive()
                test_screening_suite()
                print("All tests completed!")
            else:
                print("Invalid choice. Please select 0-6.")
            
            print()
            
        except KeyboardInterrupt:
            print("\nTest interrupted by user")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
