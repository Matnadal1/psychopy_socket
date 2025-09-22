# RSVP Experiment Configuration Files

This document explains the configuration system for the RSVP experiment.

## Configuration Files

### Environment-Specific Configurations

#### `rsvp_config_hospital.json` - Hospital Environment
**Purpose**: Full hardware setup for clinical/research use
- ✅ Gamepad input enabled
- ✅ DAQ pulse generation enabled  
- ✅ Hardware screening enabled
- ✅ Fullscreen mode (1920x1080)
- ✅ Extended sequences (5 sequences × 15 images)

```json
{
  "withpulses": true,
  "device_response": "gamepad",
  "fullscreen": true,
  "window_resolution": [1920, 1080],
  "seq_length": 15,
  "n_sequences": 5,
  "enable_screening": true
}
```

#### `rsvp_config_lab.json` - Lab Environment  
**Purpose**: Basic setup for development and testing
- ✅ Keyboard input only
- ❌ No hardware dependencies
- ✅ Windowed mode (1024x768)
- ✅ Shorter sequences (3 sequences × 10 images)

```json
{
  "withpulses": false,
  "device_response": "keyboard", 
  "fullscreen": false,
  "window_resolution": [1024, 768],
  "seq_length": 10,
  "n_sequences": 3,
  "enable_screening": false
}
```

#### `rsvp_config.json` - Default/Custom Configuration
**Purpose**: Template for custom configurations
- Balanced settings between Hospital and Lab
- Can be manually edited for specific needs
- Used when "Custom" environment is selected

## Configuration Parameters

| Parameter | Description | Hospital | Lab | Default |
|-----------|-------------|----------|-----|---------|
| `withpulses` | Enable DAQ pulse generation | `true` | `false` | `false` |
| `language` | Interface language | `"english"` | `"english"` | `"english"` |
| `device_response` | Input device | `"gamepad"` | `"keyboard"` | `"keyboard"` |
| `pictures_path` | Path to face images | Same for all environments |
| `window_resolution` | Display resolution | `[1920, 1080]` | `[1024, 768]` | `[1024, 768]` |
| `fullscreen` | Fullscreen mode | `true` | `false` | `false` |
| `isi` | Inter-stimulus interval (seconds) | `[1.0]` | `[1.0]` | `[1.0]` |
| `seq_length` | Images per sequence | `15` | `10` | `10` |
| `n_sequences` | Number of sequences | `5` | `3` | `3` |
| `max_wait_response` | Response timeout (seconds) | `10.0` | `10.0` | `10.0` |
| `min_blank_duration` | Minimum blank time | `1.25` | `1.25` | `1.25` |
| `max_rand_blank` | Random blank variation | `0.5` | `0.5` | `0.5` |
| `line_thickness` | Line width (pixels) | `5` | `5` | `5` |
| `line_offset` | Line distance from image | `5` | `5` | `5` |
| `daq_device` | DAQ device name | `"Dev1"` | `"Dev1"` | `"Dev1"` |
| `daq_port` | DAQ port name | `"port0"` | `"port0"` | `"port0"` |
| `enable_screening` | Hardware testing | `true` | `false` | `false` |

## Usage

### Automatic Environment Selection
When you run the experiment, select the environment in the participant dialog:
- **Hospital**: Loads `rsvp_config_hospital.json`
- **Lab**: Loads `rsvp_config_lab.json`

### Manual Configuration
1. Edit the appropriate JSON file
2. Modify parameters as needed
3. Save the file
4. Run the experiment

### Custom Configuration
1. Copy `rsvp_config.json` to a new file
2. Modify the settings
3. Use the custom launcher: `python rsvp_experiment.py your_config.json`

## Hardware Requirements

### Hospital Environment
- **Required**: Gamepad/joystick (pygame compatible)
- **Optional**: National Instruments DAQ device (nidaqmx)
- **Display**: Capable of 1920x1080 fullscreen

### Lab Environment  
- **Required**: Standard keyboard
- **Display**: Any monitor (windowed mode)

## Troubleshooting

### Configuration Not Loading
- Check JSON syntax (use online JSON validator)
- Ensure file paths are correct
- Verify file permissions

### Hardware Issues
- Run `python test_rsvp_hardware.py` to diagnose
- Check device drivers (gamepad, DAQ)
- Verify pygame and nidaqmx installation

### Display Problems
- Adjust `window_resolution` to match your monitor
- Set `fullscreen: false` for testing
- Check graphics drivers

## Environment Comparison

| Aspect | Hospital | Lab |
|--------|----------|-----|
| **Purpose** | Clinical research | Development/testing |
| **Hardware** | Full setup | Minimal |
| **Complexity** | High | Low |
| **Setup Time** | Longer | Quick |
| **Data Quality** | Research-grade | Testing quality |
| **Troubleshooting** | More complex | Simple |

## File Management

- ✅ Keep: `rsvp_config_hospital.json`, `rsvp_config_lab.json`, `rsvp_config.json`
- ❌ Removed: `rsvp_config_basic.json`, `rsvp_config_advanced.json` (deprecated)

## Quick Reference

```bash
# Setup
python setup_rsvp.py

# Hospital environment
python launch_rsvp.py hospital

# Lab environment  
python launch_rsvp.py lab

# Interactive selection
python launch_rsvp.py

# Test hardware
python test_rsvp_hardware.py
```
