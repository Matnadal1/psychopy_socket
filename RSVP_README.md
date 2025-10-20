# RSVP Experiment - Python Translation

This is a complete Python/PsychoPy translation of the original MATLAB/Psychtoolbox RSVP (Rapid Serial Visual Presentation) experiment.

## Current Implementation

The Python version focuses on **face recognition** tasks where:
- Participants view rapid sequences of face images
- Participants respond when they recognize faces
- Responses are collected via keyboard or gamepad
- DAQ integration for EEG synchronization (optional)
- Hardware screening tests (optional)

## Python Translation Features

### ✅ Fully Implemented
- **Image Loading**: Automatic loading of all images from the pictures directory
- **RSVP Presentation**: Rapid serial visual presentation with configurable ISI
- **Face Recognition Task**: Simplified experiment focusing on person recognition
- **Response Collection**: Keyboard/gamepad responses with precise timing
- **DAQ Integration**: MCC USB-1208FS-Plus support for EEG synchronization
- **Gamepad Support**: Full gamepad/joystick integration
- **Multi-language Support**: English, Spanish, and French instructions
- **Data Recording**: Comprehensive CSV and JSON data output
- **Configurable Parameters**: JSON-based configuration system
- **Participant Info**: GUI dialog for participant demographics
- **Hardware Screening**: Optional screening tests for hardware validation

### 🔧 Key Differences from Original MATLAB Version
- **Simplified Task**: Removed colored lines, focuses on face recognition
- **Enhanced Hardware**: Full DAQ and gamepad integration
- **Modern Architecture**: Cleaner code structure with better error handling
- **Enhanced Data**: More structured data output with better analysis capabilities

## File Structure

```
├── rsvp_experiment.py         # Main experiment class
├── rsvp_hardware.py          # Hardware integration module (gamepad, DAQ)
├── launch_rsvp.py            # Environment launcher
├── rsvp_config_hospital.json # Hospital environment config (full hardware)
├── rsvp_config_lab.json      # Lab environment config (basic setup)
├── rsvp_config.json          # Default/custom config
├── CONFIG_README.md          # Configuration documentation
├── MCC_DAQ_SETUP.md         # DAQ setup guide
├── RSVP_README.md            # This documentation
├── experiment_data/          # Output directory (created automatically)
└── RSVP_HClinic/            # Original MATLAB experiment folder
    └── 000rsvpscr_pic/      # Face images directory
```

## Usage

### Quick Start
```powershell
# Launch with environment selection
python launch_rsvp.py

# Quick launch options
python launch_rsvp.py hospital  # Hospital environment (full hardware)
python launch_rsvp.py lab      # Lab environment (basic setup)
```

### Advanced Usage
```python
from rsvp_experiment import RSVPExperiment

# Create experiment with custom config
experiment = RSVPExperiment('custom_config.json')

# Run the experiment with pre-configured environment
experiment.run_experiment(environment='hospital')  # or 'lab'
```

## Configuration

The experiment uses three configuration files for different environments:

### Hospital Environment (`rsvp_config_hospital.json`)
- Full hardware setup with gamepad and DAQ
- Extended sequences (2 sequences × 15 images)
- Hardware screening enabled

### Lab Environment (`rsvp_config_lab.json`)
- Basic setup with keyboard only
- Shorter sequences (3 sequences × 10 images)
- No hardware dependencies

### Custom Configuration (`rsvp_config.json`)
- Template for custom configurations
- Balanced settings between Hospital and Lab

Key parameters:
```json
{
  "withpulses": true,              // Enable DAQ pulse generation
  "device_response": "gamepad",    // "gamepad" or "keyboard"
  "language": "english",           // english/spanish/french
  "window_resolution": [1920, 1080], // Display resolution
  "fullscreen": true,              // Fullscreen mode
  "isi": [1.0],                   // Inter-stimulus interval in seconds
  "seq_length": 15,               // Images per sequence
  "n_sequences": 2,               // Number of sequences
  "enable_screening": true        // Hardware screening tests
}
```

## Data Output

### CSV Files (`*_responses.csv`)
- `sequence_number`: Which sequence (1, 2, 3...)
- `image_position`: Position in sequence (0-based index)
- `reaction_time`: Response time in seconds (from ISI start)
- `correct`: Always true (legacy field, not meaningful in current version)
- `timestamp`: Exact time of response

### JSON Files (`*_complete.json`)
Complete experiment data including:
- Participant information
- Configuration settings
- Trial structure
- All responses
- Summary statistics

## Key Classes and Methods

### RSVPExperiment Class
- `__init__(config_file)`: Initialize with optional config
- `run_experiment()`: Run the complete experiment
- `load_images()`: Load face images from directory
- `generate_trial_structure()`: Create sequences and color changes
- `run_sequence(sequence_info)`: Present a single RSVP sequence
- `save_data(participant_info)`: Save all experimental data

### Configuration Methods
- `load_config(file)`: Load settings from JSON
- `save_config(file)`: Save current settings to JSON
- `get_participant_info()`: GUI dialog for participant data

## Experiment Flow

1. **Participant Info**: Collect demographics via GUI dialog
2. **Instructions**: Display task instructions in selected language
3. **Image Loading**: Load all face images and create textures
4. **Trial Generation**: Create randomized sequences
5. **Sequence Presentation**: 
   - Present rapid image sequence
   - Collect responses during ISI periods
   - Send DAQ pulses for EEG synchronization (if enabled)
6. **Data Saving**: Save responses and experiment data
7. **Completion**: Show summary statistics

## Technical Details

### Timing
- Uses PsychoPy's precise timing system
- Frame-based presentation for consistency
- Response timing with sub-millisecond precision
- Reaction time measured from ISI start to response

### Hardware Integration
- **Gamepad Support**: Full joystick/gamepad integration with edge-triggered detection
- **DAQ Integration**: MCC USB-1208FS-Plus support for EEG synchronization
- **Pulse Generation**: Digital pulses for stimulus and response events
- **Hardware Screening**: Optional tests for hardware validation

### Response Detection
- Spacebar/gamepad buttons for responses
- Escape key to quit experiment
- Edge-triggered detection prevents multiple responses per press
- Responses recorded during ISI periods between images

## Validation Against Original

The Python version maintains the core experimental logic:
- ✅ Same image presentation timing
- ✅ Same DAQ pulse generation and timing
- ✅ Same gamepad response handling (edge-triggered)
- ✅ Similar randomization procedures
- ✅ Equivalent data collection
- ✅ Multi-language support
- ✅ Hardware integration (gamepad, DAQ)

## Requirements

### Core Dependencies
```
psychopy>=2023.1.0
pandas>=1.5.0
numpy>=1.20.0
```

### Optional Hardware Dependencies
```
pygame>=2.0.0          # For gamepad support
mcculw>=1.0.0          # For MCC DAQ support
```

## Hardware Setup

### Gamepad/Joystick
- Any pygame-compatible gamepad/joystick
- Buttons 0 and 1 are used for responses
- Automatically detected and configured

### DAQ Device (MCC USB-1208FS-Plus)
- See `MCC_DAQ_SETUP.md` for detailed setup instructions
- Used for EEG synchronization pulses
- Optional but recommended for research applications

## Troubleshooting

### Common Issues
1. **Images not loading**: Check `pictures_path` in config
2. **Window not opening**: Try setting `fullscreen: false`
3. **Gamepad not detected**: Check pygame installation and device connection
4. **DAQ not working**: See `MCC_DAQ_SETUP.md` for setup instructions
5. **Poor timing**: Ensure no other programs are running
6. **Data not saving**: Check write permissions in experiment directory

### Performance Tips
- Close other applications during experiment
- Use SSD storage for better image loading
- Consider fullscreen mode for better timing
- Test on target hardware before data collection
- Use Hospital environment for research-grade data collection

This translation preserves the essential experimental paradigm while modernizing the codebase and improving data handling capabilities.
