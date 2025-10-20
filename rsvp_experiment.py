"""
RSVP (Rapid Serial Visual Presentation) Experiment - Python Translation
========================================================================

Translated from MATLAB/Psychtoolbox to Python/PsychoPy

This experiment presents rapid sequences of face images with colored lines above and below.
Participants detect color changes in the lines during image presentation.

Original MATLAB code: rsvpscr_KCL_mac_PTB3.m
Translation by: AI Assistant

Key features:
- Rapid image sequences at customizable ISI (Inter-Stimulus Interval)
- Color change detection task on horizontal lines
- Precise timing control
- Gamepad and keyboard response options
- Comprehensive data logging
"""

from psychopy import visual, core, event, data, gui, clock, monitors
import pandas as pd
import numpy as np
import json
import os
import random
import glob
from datetime import datetime
from pathlib import Path
import time
import threading
from rsvp_hardware import create_hardware_manager, cleanup_hardware, ScreeningTools

class RSVPExperiment:
    """Main RSVP Experiment class"""
    
    def __init__(self, config_file=None):
        """Initialize the RSVP experiment"""
        
        # Default configuration
        self.config = {
            'withpulses': False,  # DAQ pulse generation
            'language': 'english',  # 'english', 'spanish', 'french'
            'device_response': 'keyboard',  # 'keyboard' or 'gamepad'
            'pictures_path': 'RSVP_HClinic/000rsvpscr_pic',
            'window_resolution': [1024, 768],
            'fullscreen': False,
            'isi': [1.0],  # Inter-stimulus interval in seconds
            'seq_length': 10,  # Number of images per sequence
            'n_sequences': 1,  # Number of sequences
            'max_wait_response': 10.0,  # Maximum wait time for response
            'min_blank_duration': 1.25,
            'max_rand_blank': 0.5,
            'daq_device': 'Dev1',  # DAQ device name
            'daq_port': 'port0',   # DAQ port name
            'enable_screening': False  # Enable screening tests
        }
        
        # Load custom config if provided
        if config_file and os.path.exists(config_file):
            print(f"Loading configuration from: {config_file}")
            self.load_config(config_file)
            print(f"Configuration loaded successfully")
            print(f"  - Sequences: {self.config.get('n_sequences', 'default')}")
            print(f"  - Sequence length: {self.config.get('seq_length', 'default')}")
            print(f"  - Device: {self.config.get('device_response', 'default')}")
            print(f"  - Pulses: {self.config.get('withpulses', 'default')}")
        
        # Initialize experiment variables
        self.window = None
        self.images = []
        self.image_textures = []
        self.image_names = []
        self.times = []
        self.responses = []
        self.trial_data = []
        
        # Timing control variables (matching MATLAB)
        self.ifi = None  # Inter-frame interval
        self.slack = None  # Slack time (1/3 of IFI)
        self.wait_reset = 0.04  # Must be shorter than shortest ISI
        self.value_reset = 0
        self.tprev = None  # Previous time
        
        # Hardware components
        self.hardware = None
        self.gamepad = None
        self.pulse_gen = None
        self.screening = None
        
        # Color definitions
        self.colors = {
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'white': [255, 255, 255],
            'black': [0, 0, 0],
            'gray': [128, 128, 128]
        }
        
        # Messages in different languages
        self.messages = {
            'ready_begin': {
                'english': 'Ready to begin?',
                'spanish': 'Listo para empezar?',
                'french': 'Etes-vous pret pour commencer?'
            },
            'ready_continue': {
                'english': 'Ready to continue?',
                'spanish': 'Listo para continuar?',
                'french': 'Etes-vous pret pour continuer?'
            },
            'instructions': {
                'english': '''RSVP Color Change Detection

You will see sequences of face images with colored lines above and below.

Your task:
- Watch for COLOR CHANGES in the horizontal lines
- Press SPACEBAR as quickly as possible when you detect a color change
- Try to respond to every color change you see

The experiment will begin shortly.
Press SPACEBAR to start.''',
                'spanish': '''Detección de Cambios de Color RSVP

Verás secuencias de imágenes de caras con líneas de colores arriba y abajo.

Tu tarea:
- Observa los CAMBIOS DE COLOR en las líneas horizontales
- Presiona BARRA ESPACIADORA lo más rápido posible cuando detectes un cambio de color
- Trata de responder a cada cambio de color que veas

El experimento comenzará pronto.
Presiona BARRA ESPACIADORA para empezar.''',
                'french': '''Détection de Changements de Couleur RSVP

Vous verrez des séquences d'images de visages avec des lignes colorées en haut et en bas.

Votre tâche:
- Surveillez les CHANGEMENTS DE COULEUR dans les lignes horizontales
- Appuyez sur BARRE D'ESPACE le plus rapidement possible quand vous détectez un changement de couleur
- Essayez de répondre à chaque changement de couleur que vous voyez

L'expérience va commencer bientôt.
Appuyez sur BARRE D'ESPACE pour commencer.'''
            }
        }
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                custom_config = json.load(f)
            self.config.update(custom_config)
            print(f"Configuration loaded from {config_file}")
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self, config_file):
        """Save current configuration to JSON file"""
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Configuration saved to {config_file}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_participant_info(self, environment=None):
        """Collect participant information"""
        participant_info = {
            'Participant ID': '',
            'Age': '',
            'Gender': ['Male', 'Female', 'Other', 'Prefer not to say'],
            'Session Number': 1,
            'Handedness': ['Right', 'Left', 'Ambidextrous'],
            'Language': ['english', 'spanish', 'french']
        }
        
        dlg = gui.DlgFromDict(
            dictionary=participant_info,
            title='RSVP Experiment - Participant Information',
            order=['Participant ID', 'Age', 'Gender', 'Session Number', 'Handedness', 'Language']
        )
        
        if dlg.OK:
            self.config['language'] = participant_info['Language'].lower()
            
            # Add environment to participant info for logging (but don't reconfigure)
            if environment:
                participant_info['Environment'] = environment
            
            return participant_info
        else:
            return None
    
    def configure_environment(self, environment):
        """Configure experiment settings based on environment"""
        print(f"Configuring for {environment} environment...")
        
        if environment.lower() == 'hospital':
            # Hospital environment: Full hardware setup
            self.config.update({
                'device_response': 'gamepad',
                'withpulses': True,
                'enable_screening': True,
                'fullscreen': True,  # Hospital likely has dedicated monitor
                'window_resolution': [1920, 1080],  # Higher resolution for hospital
                'n_sequences': 5,  # More sequences for research
                'seq_length': 15   # Longer sequences
            })
            print("  ✅ Gamepad input enabled")
            print("  ✅ DAQ pulse generation enabled")
            print("  ✅ Hardware screening enabled")
            print("  ✅ Fullscreen mode enabled")
            
        elif environment.lower() == 'lab':
            # Lab environment: Basic setup, keyboard only
            self.config.update({
                'device_response': 'keyboard',
                'withpulses': False,
                'enable_screening': False,
                'fullscreen': False,  # Windowed for easier development/testing
                'window_resolution': [1024, 768],  # Standard resolution
                'n_sequences': 3,  # Fewer sequences for testing
                'seq_length': 10   # Standard length
            })
            print("  ✅ Keyboard input enabled")
            print("  ✅ Windowed mode for easy testing")
            print("  ✅ Basic configuration")
        
        print(f"Environment configuration complete: {environment}")
    
    def setup_window(self):
        """Create and configure the experiment window"""
        self.window = visual.Window(
            size=self.config['window_resolution'],
            color='gray',
            units='pix',
            fullscr=self.config['fullscreen'],
            screen=0
        )
        
        # Get window properties
        self.window_rect = self.window.size
        self.x_center = self.window_rect[0] / 2
        self.y_center = self.window_rect[1] / 2
        
        # Calculate timing parameters (matching MATLAB)
        self.ifi = self.window.monitorFramePeriod
        self.slack = self.ifi / 3.0  # Slack time (1/3 of IFI)
        
        print(f"Window created: {self.window_rect}")
        print(f"Frame rate: {1/self.ifi:.1f} Hz")
        print(f"Inter-frame interval: {self.ifi*1000:.2f} ms")
        print(f"Slack time: {self.slack*1000:.2f} ms")
        
        # Initialize hardware
        self.hardware = create_hardware_manager(self.config)
        self.gamepad = self.hardware.get('gamepad')
        self.pulse_gen = self.hardware.get('pulse_gen')
        
        # Initialize screening tools
        self.screening = ScreeningTools(self.window)
        self.screening.set_hardware(self.gamepad, self.pulse_gen)
        
        return True
    
    def load_images(self):
        """Load all images from the pictures directory"""
        pictures_path = self.config['pictures_path']
        
        if not os.path.exists(pictures_path):
            raise FileNotFoundError(f"Pictures directory not found: {pictures_path}")
        
        # Find all image files
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(pictures_path, ext)))
            image_files.extend(glob.glob(os.path.join(pictures_path, ext.upper())))
        
        if not image_files:
            raise FileNotFoundError(f"No image files found in {pictures_path}")
        
        print(f"Found {len(image_files)} images")
        
        # Load images and create textures
        self.image_names = []
        self.image_textures = []
        
        for img_file in image_files:
            try:
                # Create image stimulus
                img_stim = visual.ImageStim(
                    win=self.window,
                    image=img_file,
                    units='pix'
                )
                
                self.image_textures.append(img_stim)
                self.image_names.append(os.path.basename(img_file))
                
            except Exception as e:
                print(f"Error loading image {img_file}: {e}")
        
        print(f"Successfully loaded {len(self.image_textures)} images")
        
        # Save image names for reference
        self.save_image_names()
        
        return len(self.image_textures) > 0
    
    def save_image_names(self):
        """Save the list of image names used"""
        output_dir = "experiment_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/ImageNames_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            for name in self.image_names:
                f.write(f"{name}\n")
        
        print(f"Image names saved to {filename}")
    
    def generate_trial_structure(self):
        """Generate the trial structure and color changes"""
        n_images = len(self.image_textures)
        isi_values = self.config['isi']
        seq_length = self.config['seq_length']
        n_sequences = self.config['n_sequences']
        
        if n_images < seq_length:
            raise ValueError(f"Not enough images ({n_images}) for sequence length ({seq_length})")
        
        # Generate image order for each sequence
        self.trial_structure = []
        
        for seq_idx in range(n_sequences):
            # Randomly select images for this sequence
            selected_images = random.sample(range(n_images), seq_length)
            
            # Select ISI for this sequence
            isi = random.choice(isi_values)
            
            sequence_info = {
                'sequence_number': seq_idx + 1,
                'image_indices': selected_images,
                'isi': isi
            }
            
            self.trial_structure.append(sequence_info)
        
        print(f"Generated {len(self.trial_structure)} sequences")
    
    
    def check_for_response(self):
        """Check for response from keyboard or gamepad (edge-triggered like MATLAB)"""
        response = None
        
        # Check keyboard
        keys = event.getKeys()
        if 'escape' in keys:
            return 'escape'
        if 'space' in keys:
            return 'space'
        
        # Check gamepad if available (edge-triggered like MATLAB)
        if self.gamepad and self.gamepad.connected:
            # Check button 0 and 1 (similar to MATLAB version)
            button_0_pressed = self.gamepad.get_button_state(0)
            button_1_pressed = self.gamepad.get_button_state(1)
            
            # Only trigger on button press if not already pressed (edge-triggered)
            if (button_0_pressed and not getattr(self, '_button_0_was_pressed', False)) or \
               (button_1_pressed and not getattr(self, '_button_1_was_pressed', False)):
                
                # Debug: print which button was pressed
                if button_0_pressed and not getattr(self, '_button_0_was_pressed', False):
                    print(f"Button 0 (X) pressed")
                if button_1_pressed and not getattr(self, '_button_1_was_pressed', False):
                    print(f"Button 1 (A) pressed")
                
                # Update button state tracking
                self._button_0_was_pressed = button_0_pressed
                self._button_1_was_pressed = button_1_pressed
                
                return 'space'  # Treat gamepad buttons as space
            
            # Update button state tracking
            self._button_0_was_pressed = button_0_pressed
            self._button_1_was_pressed = button_1_pressed
        
        return None
    
    def wait_for_continue_response(self):
        """Wait for continue response (space/gamepad or escape)"""
        while True:
            response = self.check_for_response()
            if response == 'escape':
                return False
            if response == 'space':
                return True
            core.wait(0.001)
    
    def show_instructions(self):
        """Display experiment instructions"""
        lang = self.config['language']
        instructions_text = self.messages['instructions'][lang]
        
        # Add device-specific instructions
        if self.config['device_response'] == 'gamepad' and self.gamepad and self.gamepad.connected:
            instructions_text += f"\n\nGamepad detected: {self.gamepad.gamepad_name}\nPress any gamepad button to respond."
        
        instructions = visual.TextStim(
            win=self.window,
            text=instructions_text,
            pos=(0, 0),
            height=25,
            color='white',
            wrapWidth=800
        )
        
        while True:
            instructions.draw()
            self.window.flip()
            
            response = self.check_for_response()
            if response == 'escape':
                return False
            if response == 'space':
                return True
            
            core.wait(0.016)
    
    def show_message(self, message_key):
        """Display a message and wait for response"""
        lang = self.config['language']
        message_text = self.messages[message_key][lang]
        
        message = visual.TextStim(
            win=self.window,
            text=message_text,
            pos=(0, 0),
            height=30,
            color='white'
        )
        
        while True:
            message.draw()
            self.window.flip()
            
            response = self.check_for_response()
            if response == 'escape':
                return False
            if response == 'space':
                return True
            
            core.wait(0.016)
    
    
    def run_sequence(self, sequence_info):
        """Run a single RSVP sequence (simplified - images only)"""
        seq_num = sequence_info['sequence_number']
        image_indices = sequence_info['image_indices']
        isi = sequence_info['isi']
        
        print(f"Running sequence {seq_num} with {len(image_indices)} images, ISI={isi}s")
        
        # Initialize response tracking
        sequence_responses = []
        k = 0  # Time index counter (matching MATLAB)
        
        # Initialize button state tracking for edge-triggered detection
        self._button_0_was_pressed = False
        self._button_1_was_pressed = False
        
        # Random timing parameters (matching MATLAB)
        min_blank = self.config['min_blank_duration']
        max_rand_blank = self.config['max_rand_blank']
        
        randTime_blank = min_blank + max_rand_blank * random.random()
        
        # Initialize timing
        self.times = []
        sequence_clock = core.Clock()  # Use PsychoPy clock for timing
        
        # Initial blank screen
        self.window.clearBuffer()
        times_k = self.window.flip()
        self.times.append(times_k)
        k += 1
        
        # Send initial blank pulse
        if self.pulse_gen and self.pulse_gen.available:
            self.pulse_gen.send_pulse(self.pulse_gen.pulse_codes['blank_on'])
            time.sleep(self.wait_reset)
            self.pulse_gen.send_pulse(self.pulse_gen.pulse_codes['value_reset'])
        
        self.tprev = times_k
        k += 1
        
        # Present image sequence
        for img_idx, image_index in enumerate(image_indices):
            # Draw image only
            self.window.clearBuffer()
            self.image_textures[image_index].draw()
            
            # Calculate flip time (matching MATLAB timing)
            if img_idx == 0:
                flip_time = self.tprev + randTime_blank - self.slack
            else:
                flip_time = self.tprev + isi - self.slack
            
            times_k = self.window.flip(flip_time)
            self.times.append(times_k)
            
            # Send image onset pulse
            if self.pulse_gen and self.pulse_gen.available:
                if img_idx == 0:
                    pulse_value = self.pulse_gen.pulse_codes['pic_onoff_2'][0]
                else:
                    pulse_value = self.pulse_gen.pulse_codes['pic_onoff_1'][0] if img_idx % 2 == 0 else self.pulse_gen.pulse_codes['pic_onoff_2'][0]
                
                self.pulse_gen.send_pulse(pulse_value)
                time.sleep(self.wait_reset)
                self.pulse_gen.send_pulse(self.pulse_gen.pulse_codes['value_reset'])
            
            self.tprev = times_k
            k += 1
            
            # Wait for ISI time and check for responses
            isi_start_time = sequence_clock.getTime()
            while (sequence_clock.getTime() - isi_start_time) < isi:
                response = self.check_for_response()
                if response == 'space':
                    rt = sequence_clock.getTime() - isi_start_time
                    self.record_response(seq_num, img_idx, rt, True)
                    sequence_responses.append({
                        'sequence': seq_num,
                        'image_position': img_idx + 1,
                        'reaction_time': rt,
                        'correct': True
                    })
                    
                    # Send response pulse
                    if self.pulse_gen and self.pulse_gen.available:
                        self.pulse_gen.send_pulse(self.pulse_gen.pulse_codes['resp_offset'])
                        time.sleep(self.wait_reset)
                        self.pulse_gen.send_pulse(self.pulse_gen.pulse_codes['value_reset'])
                    
                    print(f"Response recorded: Button press at image {img_idx + 1}, RT={rt:.3f}s")
                    
                elif response == 'escape':
                    return False
                
                core.wait(0.001)
        
        # Final blank screen
        self.window.clearBuffer()
        times_k = self.window.flip(self.tprev + isi - self.slack)
        self.times.append(times_k)
        
        # Send final blank pulse
        if self.pulse_gen and self.pulse_gen.available:
            self.pulse_gen.send_pulse(self.pulse_gen.pulse_codes['blank_on'])
            time.sleep(self.wait_reset)
            self.pulse_gen.send_pulse(self.pulse_gen.pulse_codes['value_reset'])
        
        self.tprev = times_k
        k += 1
        
        # Wait for final blank duration
        final_wait_time = randTime_blank
        if final_wait_time > 0:
            core.wait(final_wait_time)
        
        print(f"Sequence {seq_num} completed. Responses: {len(sequence_responses)}")
        return True
    
    
    def record_response(self, sequence, image_position, reaction_time, correct):
        """Record a participant response"""
        response_data = {
            'sequence_number': sequence,
            'image_position': image_position,
            'reaction_time': reaction_time,
            'correct': correct,
            'timestamp': datetime.now().isoformat()
        }
        
        self.responses.append(response_data)
        self.times.append(core.getTime())
    
    def save_data(self, participant_info):
        """Save all experimental data"""
        output_dir = "experiment_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        participant_id = participant_info.get('Participant ID', 'unknown')
        session = participant_info.get('Session Number', 1)
        
        filename_base = f"{output_dir}/RSVP_{participant_id}_session_{session}_{timestamp}"
        
        # Save responses as CSV
        if self.responses:
            df = pd.DataFrame(self.responses)
            csv_filename = f"{filename_base}_responses.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Responses saved to {csv_filename}")
        
        # Save complete experiment data as JSON
        experiment_data = {
            'participant_info': participant_info,
            'config': self.config,
            'trial_structure': self.trial_structure,
            'responses': self.responses,
            'times': self.times,
            'image_names': self.image_names,
            'start_time': datetime.now().isoformat(),
            'summary': self.calculate_summary()
        }
        
        json_filename = f"{filename_base}_complete.json"
        with open(json_filename, 'w') as f:
            json.dump(experiment_data, f, indent=2)
        
        print(f"Complete data saved to {json_filename}")
        
        return True
    
    def calculate_summary(self):
        """Calculate summary statistics"""
        if not self.responses:
            return {}
        
        df = pd.DataFrame(self.responses)
        
        summary = {
            'total_responses': len(df),
            'correct_responses': sum(df['correct']),
            'accuracy': sum(df['correct']) / len(df) * 100,
            'mean_reaction_time': df['reaction_time'].mean(),
            'median_reaction_time': df['reaction_time'].median(),
            'std_reaction_time': df['reaction_time'].std()
        }
        
        return summary
    
    def run_experiment(self, environment=None):
        """Run the complete RSVP experiment"""
        try:
            print("Starting RSVP Experiment")
            print("=" * 50)
            
            # Get participant information
            participant_info = self.get_participant_info(environment)
            if not participant_info:
                print("Experiment cancelled - no participant info")
                return False
            
            # Setup experiment
            print("Setting up experiment...")
            self.setup_window()
            self.load_images()
            self.generate_trial_structure()
            
            # Run screening if enabled
            if self.config.get('enable_screening', False):
                print("Running screening battery...")
                self.screening.run_screening_battery()
            
            # Show instructions
            if not self.show_instructions():
                print("Experiment cancelled during instructions")
                return False
            
            # Send experiment signature pulses at start (matching MATLAB)
            if self.pulse_gen and self.pulse_gen.available:
                print("Sending experiment signature pulses...")
                self.pulse_gen.send_signature_pulses()
            
            # Run sequences
            for sequence_info in self.trial_structure:
                # Show ready message
                if not self.show_message('ready_continue'):
                    print("Experiment cancelled by user")
                    break
                
                # Run sequence
                if not self.run_sequence(sequence_info):
                    print("Experiment cancelled during sequence")
                    break
            
            # Save data
            print("Saving experimental data...")
            self.save_data(participant_info)
            
            # Show completion message
            summary = self.calculate_summary()
            completion_text = f"""Experiment Complete!

Responses: {summary.get('total_responses', 0)}
Accuracy: {summary.get('accuracy', 0):.1f}%
Mean RT: {summary.get('mean_reaction_time', 0):.3f}s

Thank you for participating!
Press any key to exit."""
            
            completion = visual.TextStim(
                win=self.window,
                text=completion_text,
                pos=(0, 0),
                height=25,
                color='white',
                wrapWidth=600
            )
            
            while True:
                keys = event.getKeys()
                if keys:
                    break
                
                completion.draw()
                self.window.flip()
                core.wait(0.016)
            
            return True
            
        except Exception as e:
            print(f"Error during experiment: {e}")
            return False
        
        finally:
            # Cleanup hardware
            if self.hardware:
                cleanup_hardware(self.hardware)
            
            # Cleanup window
            if self.window:
                self.window.close()
            core.quit()

def main():
    """Main function to run the RSVP experiment"""
    # Create and run experiment
    experiment = RSVPExperiment()
    
    # Optionally save default config
    experiment.save_config('rsvp_config.json')
    
    # Run the experiment
    success = experiment.run_experiment()
    
    if success:
        print("Experiment completed successfully!")
    else:
        print("Experiment ended early or with errors.")

if __name__ == "__main__":
    main()
