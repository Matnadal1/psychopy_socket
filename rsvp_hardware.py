"""
RSVP Hardware Integration Module
================================

This module provides hardware integration for the RSVP experiment including:
- Gamepad/joystick support
- DAQ pulse generation for EEG synchronization
- Hardware testing functions

Dependencies:
- pygame (for gamepad support)
- mcculw (for MCC USB-1208FS-Plus DAQ - optional)
- psychopy
"""

import pygame
import time
import numpy as np
from psychopy import core, event
import warnings

# Optional DAQ support - MCC USB-1208FS-Plus
try:
    from mcculw import ul
    from mcculw.enums import DigitalPortType, DigitalIODirection, InterfaceType
    DAQ_AVAILABLE = True
except ImportError:
    DAQ_AVAILABLE = False
    warnings.warn("mcculw not available. Pulse functionality will be disabled.")

class GamepadController:
    """Gamepad/Joystick controller for RSVP experiment"""
    
    def __init__(self):
        self.gamepad = None
        self.gamepad_name = None
        self.num_buttons = 0
        self.connected = False
        
        # Button mapping (similar to MATLAB PTB)
        self.button_map = {
            'button_1': 0,  # X button (button 1 in MATLAB)
            'button_2': 1,  # A button (button 2 in MATLAB)
            'button_3': 2,  # B button
            'button_4': 3,  # Y button
        }
    
    def initialize(self):
        """Initialize pygame and detect gamepad"""
        try:
            pygame.init()
            pygame.joystick.init()
            
            num_joysticks = pygame.joystick.get_count()
            
            if num_joysticks == 0:
                print("No gamepad detected")
                return False
            
            # Use the first available joystick
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            
            self.gamepad_name = self.gamepad.get_name()
            self.num_buttons = self.gamepad.get_numbuttons()
            self.connected = True
            
            print(f"Gamepad connected: {self.gamepad_name}")
            print(f"Number of buttons: {self.num_buttons}")
            
            return True
            
        except Exception as e:
            print(f"Error initializing gamepad: {e}")
            return False
    
    def get_button_state(self, button_number):
        """Get the current state of a specific button (0-indexed)"""
        if not self.connected:
            return False
        
        try:
            pygame.event.pump()  # Update joystick state
            return self.gamepad.get_button(button_number)
        except Exception as e:
            print(f"Error reading button {button_number}: {e}")
            return False
    
    def get_all_buttons(self):
        """Get the state of all buttons"""
        if not self.connected:
            return []
        
        try:
            pygame.event.pump()
            return [self.gamepad.get_button(i) for i in range(self.num_buttons)]
        except Exception as e:
            print(f"Error reading all buttons: {e}")
            return []
    
    def wait_for_button_press(self, timeout=None):
        """Wait for any button press, return button number or None if timeout"""
        if not self.connected:
            return None
        
        start_time = time.time()
        
        while True:
            pygame.event.pump()
            
            # Check all buttons
            for i in range(self.num_buttons):
                if self.gamepad.get_button(i):
                    return i
            
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                return None
            
            time.sleep(0.001)  # Small delay to prevent excessive CPU usage
    
    def test_gamepad(self):
        """Test gamepad functionality - similar to test_gamepad.m"""
        if not self.connected:
            print("No gamepad connected for testing")
            return False
        
        print(f"Testing gamepad: {self.gamepad_name}")
        print("Press buttons on the gamepad (press 'q' on keyboard to exit)")
        
        # Test loop
        while True:
            # Check keyboard for exit
            keys = event.getKeys()
            if 'q' in keys or 'escape' in keys:
                break
            
            # Check gamepad buttons
            pygame.event.pump()
            button_states = self.get_all_buttons()
            
            # Print button states if any are pressed
            pressed_buttons = [i for i, state in enumerate(button_states) if state]
            if pressed_buttons:
                print(f"Buttons pressed: {pressed_buttons}")
                time.sleep(0.1)  # Debounce
            
            time.sleep(0.01)
        
        print("Gamepad test completed")
        return True
    
    def cleanup(self):
        """Clean up pygame resources"""
        if self.connected and self.gamepad:
            self.gamepad.quit()
        pygame.joystick.quit()
        pygame.quit()
        self.connected = False

class PulseGenerator:
    """DAQ pulse generator for EEG synchronization - MCC USB-1208FS-Plus"""
    
    def __init__(self, device_name=None, port="FIRSTPORTA"):
        self.device_name = device_name
        self.port = port
        self.board_num = 0  # Default board number for MCC devices
        self.available = DAQ_AVAILABLE
        
        # Pulse codes from original MATLAB code (simplified - images only)
        self.pulse_codes = {
            'data_signature_on': 85,
            'data_signature_off': 84,
            'pic_onoff_1': [1, 5, 17],
            'pic_onoff_2': [3, 9, 33],
            'blank_on': 69,
            'trial_on': 113,
            'resp_offset': 81,
            'value_reset': 0
        }
        
        self.wait_reset = 0.04  # Wait time after pulse
    
    def initialize(self):
        """Initialize MCC USB-1208FS-Plus DAQ device"""
        if not self.available:
            print("DAQ not available - pulse generation disabled")
            return False
        
        try:
            # Initialize the Universal Library
            ul.ignore_instacal()
            
            # Get the first available board (USB-1208FS-Plus)
            board_list = ul.get_daq_device_inventory(InterfaceType.USB)
            if not board_list:
                print("No MCC DAQ devices found")
                return False
            
            # Use board number 0 (default for InstaCal configuration)
            # The device should be configured in InstaCal first
            self.board_num = 0
            self.config_first_detected_device(self.board_num)
            # Configure digital port for output (matching MATLAB: DaqDConfigPort(dio,0,0))
            # MATLAB: dio=board, 0=port A, 0=output direction
            ul.d_config_port(self.board_num, DigitalPortType.FIRSTPORTA, DigitalIODirection.OUT)
            
            print(f"MCC DAQ initialized: Board {self.board_num}")
            return True
            
        except Exception as e:
            print(f"Error initializing MCC DAQ: {e}")
            self.available = False
            return False
    
    def send_pulse(self, value):
        """Send a digital pulse with specified value (matching MATLAB exactly)"""
        if not self.available:
            return False
        
        try:
            # Send pulse (matching MATLAB: err=DaqDOut(dio,0,value))
            ul.d_out(self.board_num, DigitalPortType.FIRSTPORTA, value)
            
            # Wait (matching MATLAB: WaitSecs(wait_reset))
            time.sleep(self.wait_reset)
            
            # Reset (matching MATLAB: fff=DaqDOut(dio,0,value_reset))
            ul.d_out(self.board_num, DigitalPortType.FIRSTPORTA, self.pulse_codes['value_reset'])
            
            return True
            
        except Exception as e:
            print(f"Error sending pulse {value}: {e}")
            return False
    
    def send_signature_pulses(self):
        """Send experiment start signature (3 pulses matching MATLAB exactly)"""
        if not self.available:
            return False
        
        try:
            for _ in range(3):
                # Send signature on pulse
                ul.d_out(self.board_num, DigitalPortType.FIRSTPORTA, self.pulse_codes['data_signature_on'])
                time.sleep(0.05)
                
                # Send signature off pulse
                ul.d_out(self.board_num, DigitalPortType.FIRSTPORTA, self.pulse_codes['data_signature_off'])
                time.sleep(0.45)
            
            return True
            
        except Exception as e:
            print(f"Error sending signature pulses: {e}")
            return False
    
    def test_pulses(self):
        """Test pulse generation - similar to test_pulses.m"""
        if not self.available:
            print("DAQ not available for pulse testing")
            return False
        
        test_values = [1, 2, 5, 8, 17, 32, 65, 128, 85, 84, 4, 16, 0]
        
        print("Testing pulse generation...")
        print(f"Sending test values: {test_values}")
        
        for value in test_values:
            print(f"Sending pulse: {value}")
            self.send_pulse(value)
            time.sleep(0.4)
        
        print("Pulse test completed")
        return True
    
    def config_first_detected_device(self, board_num, dev_id_list=None):
        """Adds the first available device to the UL.  If a types_list is specified,
        the first available device in the types list will be add to the UL.

        Parameters
        ----------
        board_num : int
            The board number to assign to the board when configuring the device.

        dev_id_list : list[int], optional
            A list of product IDs used to filter the results. Default is None.
            See UL documentation for device IDs.
        """
        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.ANY)
        if not devices:
            raise Exception('Error: No DAQ devices found')

        print('Found', len(devices), 'DAQ device(s):')
        for device in devices:
            print('  ', device.product_name, ' (', device.unique_id, ') - ',
                  'Device ID = ', device.product_id, sep='')

        device = devices[0]
        if dev_id_list:
            device = next((device for device in devices
                           if device.product_id in dev_id_list), None)
            if not device:
                err_str = 'Error: No DAQ device found in device ID list: '
                err_str += ','.join(str(dev_id) for dev_id in dev_id_list)
                raise Exception(err_str)

        # Add the first DAQ device to the UL with the specified board number
        ul.create_daq_device(board_num, device)
    
    def cleanup(self):
        """Clean up DAQ resources"""
        if self.available:
            try:
                # Reset digital port to 0
                ul.d_out(self.board_num, DigitalPortType.FIRSTPORTA, 0)
            except:
                pass

class ScreeningTools:
    """Screening and calibration tools for the RSVP experiment"""
    
    def __init__(self, window):
        self.window = window
        self.gamepad = None
        self.pulse_gen = None
    
    def set_hardware(self, gamepad, pulse_gen):
        """Set hardware components"""
        self.gamepad = gamepad
        self.pulse_gen = pulse_gen
    
    def test_display(self):
        """Test display functionality"""
        from psychopy import visual
        
        print("Testing display...")
        
        # Test different colors and patterns
        colors = ['red', 'green', 'blue', 'white', 'black']
        
        for color in colors:
            self.window.color = color
            self.window.flip()
            time.sleep(0.5)
        
        # Reset to gray
        self.window.color = 'gray'
        self.window.flip()
        
        print("Display test completed")
    
    def test_timing(self):
        """Test timing precision"""
        from psychopy import visual
        
        print("Testing timing precision...")
        
        # Create a simple stimulus
        stim = visual.Rect(self.window, width=100, height=100, fillColor='white')
        
        # Measure flip timing
        flip_times = []
        n_flips = 60  # Test for 1 second at 60Hz
        
        for i in range(n_flips):
            stim.draw()
            flip_time = self.window.flip()
            flip_times.append(flip_time)
        
        # Calculate timing statistics
        if len(flip_times) > 1:
            intervals = np.diff(flip_times)
            mean_interval = np.mean(intervals)
            std_interval = np.std(intervals)
            
            print(f"Mean flip interval: {mean_interval*1000:.2f} ms")
            print(f"Std flip interval: {std_interval*1000:.2f} ms")
            print(f"Estimated refresh rate: {1/mean_interval:.1f} Hz")
        
        print("Timing test completed")
    
    def run_screening_battery(self):
        """Run complete screening battery"""
        print("Starting RSVP Screening Battery")
        print("=" * 40)
        
        # Test display
        self.test_display()
        
        # Test timing
        self.test_timing()
        
        # Test gamepad if available
        if self.gamepad and self.gamepad.connected:
            self.gamepad.test_gamepad()
        else:
            print("Gamepad not available for testing")
        
        # Test pulses if available
        if self.pulse_gen and self.pulse_gen.available:
            self.pulse_gen.test_pulses()
        else:
            print("Pulse generator not available for testing")
        
        print("Screening battery completed")

def create_hardware_manager(config):
    """Factory function to create hardware manager based on configuration"""
    
    hardware = {
        'gamepad': None,
        'pulse_gen': None,
        'screening': None
    }
    
    # Initialize gamepad if requested
    if config.get('device_response') == 'gamepad':
        gamepad = GamepadController()
        if gamepad.initialize():
            hardware['gamepad'] = gamepad
        else:
            print("Gamepad initialization failed, falling back to keyboard")
    
    # Initialize pulse generator if requested
    if config.get('withpulses', False):
        pulse_gen = PulseGenerator(
            device_name=config.get('daq_device', None),
            port=config.get('daq_port', 'FIRSTPORTA')
        )
        if pulse_gen.initialize():
            hardware['pulse_gen'] = pulse_gen
        else:
            print("Pulse generator initialization failed")
    
    return hardware

def cleanup_hardware(hardware):
    """Clean up all hardware components"""
    if hardware.get('gamepad'):
        hardware['gamepad'].cleanup()
    
    if hardware.get('pulse_gen'):
        hardware['pulse_gen'].cleanup()

# Test functions for standalone testing
def test_gamepad_standalone():
    """Standalone gamepad test"""
    gamepad = GamepadController()
    if gamepad.initialize():
        gamepad.test_gamepad()
        gamepad.cleanup()
    else:
        print("Failed to initialize gamepad")

def test_pulses_standalone():
    """Standalone pulse test"""
    pulse_gen = PulseGenerator()
    if pulse_gen.initialize():
        pulse_gen.test_pulses()
        pulse_gen.cleanup()
    else:
        print("Failed to initialize pulse generator")

if __name__ == "__main__":
    print("RSVP Hardware Test Suite")
    print("=" * 30)
    
    # Test gamepad
    print("\n1. Testing Gamepad...")
    test_gamepad_standalone()
    
    # Test pulses
    print("\n2. Testing Pulses...")
    test_pulses_standalone()
    
    print("\nHardware tests completed")
