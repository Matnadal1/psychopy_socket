# RSVP Experiment - Python Translation

This is a complete Python/PsychoPy translation of the original MATLAB/Psychtoolbox RSVP (Rapid Serial Visual Presentation) experiment.

## Original Experiment

The original experiment (`rsvpscr_KCL_mac_PTB3.m`) is a color change detection task where:
- Participants view rapid sequences of face images
- Colored horizontal lines appear above and below the images
- Participants must detect when the line colors change
- Responses are collected via keyboard or gamepad

## Python Translation Features

### ✅ Fully Implemented
- **Image Loading**: Automatic loading of all images from the pictures directory
- **RSVP Presentation**: Rapid serial visual presentation with configurable ISI
- **Color Change Detection**: Random color changes in horizontal lines during sequences
- **Response Collection**: Keyboard responses with precise timing
- **Multi-language Support**: English, Spanish, and French instructions
- **Data Recording**: Comprehensive CSV and JSON data output
- **Configurable Parameters**: JSON-based configuration system
- **Participant Info**: GUI dialog for participant demographics

### 🔧 Key Differences from MATLAB Version
- **No DAQ Integration**: Python version doesn't include hardware pulse triggers
- **Simplified Input**: Currently keyboard-only (gamepad can be added)
- **Enhanced Data**: More structured data output with better analysis capabilities
- **Modern GUI**: Uses PsychoPy's built-in GUI components

## File Structure

```
├── rsvp_experiment.py         # Main experiment class
├── rsvp_hardware.py          # Hardware integration module  
├── launch_rsvp.py            # Environment launcher
├── test_rsvp_hardware.py     # Hardware testing suite
├── setup_rsvp.py             # Setup and configuration script
├── rsvp_config_hospital.json # Hospital environment config
├── rsvp_config_lab.json      # Lab environment config
├── rsvp_config.json          # Default/custom config
├── launch_hospital.bat       # Windows Hospital launcher
├── launch_lab.bat            # Windows Lab launcher
├── CONFIG_README.md          # Configuration documentation
├── RSVP_README.md            # This documentation
├── experiment_data/          # Output directory (created automatically)
└── RSVP_HClinic/            # Original MATLAB experiment folder
    └── 000rsvpscr_pic/      # Face images directory
```

## Usage

### Quick Start
```powershell
# Setup (run once)
python setup_rsvp.py

# Launch with environment selection
python launch_rsvp.py

# Quick launch options
python launch_rsvp.py hospital  # Hospital environment
python launch_rsvp.py lab       # Lab environment

# Windows batch files
launch_hospital.bat              # Double-click for Hospital
launch_lab.bat                   # Double-click for Lab
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

Edit `rsvp_config.json` to customize the experiment:

```json
{
  "language": "english",           // english/spanish/french
  "pictures_path": "RSVP_HClinic/000rsvpscr_pic",
  "window_resolution": [1024, 768],
  "fullscreen": false,
  "isi": [1.0],                   // Inter-stimulus interval in seconds
  "seq_length": 10,               // Images per sequence
  "n_sequences": 3,               // Number of sequences
  "line_thickness": 5,            // Thickness of colored lines
  "line_offset": 5                // Distance from image edges
}
```

## Data Output

### CSV Files (`*_responses.csv`)
- `sequence_number`: Which sequence (1, 2, 3...)
- `image_position`: Position in sequence (1-10)
- `reaction_time`: Response time in seconds
- `correct`: Whether response was to a color change
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
4. **Trial Generation**: Create randomized sequences with color changes
5. **Sequence Presentation**: 
   - Show "Ready to continue?" message
   - Present rapid image sequence with colored lines
   - Detect color changes at random times
   - Collect spacebar responses
6. **Data Saving**: Save responses and experiment data
7. **Completion**: Show summary statistics

## Technical Details

### Timing
- Uses PsychoPy's precise timing system
- Frame-based presentation for consistency
- Response timing with sub-millisecond precision

### Color Changes
- Random number of changes per sequence (1-5 typically)
- Changes occur at random times within ISI
- Colors alternate between red and green
- Independent top and bottom line colors

### Response Detection
- Spacebar for color change responses
- Escape key to quit experiment
- Responses within 1 second of color change marked as "correct"

## Validation Against Original

The Python version maintains the core experimental logic:
- ✅ Same image presentation timing
- ✅ Same color change detection task
- ✅ Similar randomization procedures
- ✅ Equivalent data collection
- ✅ Multi-language support

## Requirements

```
psychopy>=2023.1.0
pandas>=1.5.0
numpy>=1.20.0
```

## Future Enhancements

Potential additions to match original functionality:
- [ ] Gamepad support using PsychoPy's joystick module
- [ ] DAQ integration for EEG/physiological recordings
- [ ] Advanced trial balancing algorithms
- [ ] Real-time performance feedback
- [ ] Eye-tracking integration

## Troubleshooting

### Common Issues
1. **Images not loading**: Check `pictures_path` in config
2. **Window not opening**: Try setting `fullscreen: false`
3. **Poor timing**: Ensure no other programs are running
4. **Data not saving**: Check write permissions in experiment directory

### Performance Tips
- Close other applications during experiment
- Use SSD storage for better image loading
- Consider fullscreen mode for better timing
- Test on target hardware before data collection

This translation preserves the essential experimental paradigm while modernizing the codebase and improving data handling capabilities.
