# MCC USB-1208FS-Plus DAQ Setup Guide
=====================================

This guide explains how to set up the MCC USB-1208FS-Plus DAQ device for use with the RSVP experiment.

## Prerequisites

1. **Hardware**: MCC USB-1208FS-Plus DAQ device
2. **Operating System**: Windows 10/11 (recommended)
3. **Python**: Python 3.7 or higher

## Installation Steps

### 1. Install MCC Universal Library Drivers

1. Download the Universal Library from the official MCC website:
   - Go to: https://www.mccdaq.com/software-drivers
   - Download "Universal Library for Windows"
   - Install the drivers following the installation wizard

2. Install and configure InstaCal:
   - Download InstaCal from: https://www.mccdaq.com/downloads/instacal.aspx
   - Install and run InstaCal
   - Connect your USB-1208FS-Plus device
   - In InstaCal, the device should appear and be assigned board number 0
   - Save the configuration

3. Verify installation:
   - Check Device Manager to ensure the device is recognized
   - No yellow warning symbols should appear
   - InstaCal should show the device as "Available"

### 2. Install Python Library

Install the mcculw Python library:

```powershell
pip install mcculw
```

### 3. Test the Installation

The DAQ functionality is automatically tested when you run the experiment. The launcher will check for DAQ availability and report any issues.

## Configuration

The RSVP experiment will automatically detect and use the MCC USB-1208FS-Plus device. No additional configuration is required.

### Pulse Codes

The following pulse codes are used for EEG synchronization:

- `data_signature_on`: 85
- `data_signature_off`: 84
- `pic_onoff_1`: [1, 5, 17]
- `pic_onoff_2`: [3, 9, 33]
- `blank_on`: 69
- `trial_on`: 113
- `resp_offset`: 81
- `value_reset`: 0

## Troubleshooting

### Common Issues

1. **"mcculw not available" error**:
   - Ensure mcculw is installed: `pip install mcculw`
   - Check that the Universal Library drivers are installed

2. **"No MCC devices found" error**:
   - Verify the USB-1208FS-Plus is connected
   - Check Device Manager for device recognition
   - Try a different USB port
   - Restart the computer after driver installation

3. **"Error initializing MCC DAQ" error**:
   - Ensure only one MCC device is connected
   - Check that no other software is using the device
   - Verify the device is not in use by InstaCal
   - Make sure the device is configured in InstaCal with board number 0

### Device Manager Check

In Windows Device Manager, you should see:
- **Measurement Computing Devices** category
- **USB-1208FS-Plus** device listed without warnings

### InstaCal Configuration

If you have InstaCal installed:
1. Open InstaCal
2. Verify the USB-1208FS-Plus appears in the device list
3. The device should show as "Available" (not "In Use")

## Technical Details

### Digital Output Configuration

The device is configured to use:
- **Port**: FIRSTPORTA (8-bit digital output)
- **Board Number**: Automatically detected (usually 0)
- **Pulse Duration**: 40ms (configurable via `wait_reset`)

### Compatibility

This implementation is compatible with:
- MCC USB-1208FS-Plus
- Other MCC devices with similar digital output capabilities

## Support

For technical support:
1. Check the MCC Universal Library documentation
2. Visit the MCC support website
3. Contact your system administrator

## Notes

- The device must be connected before running the experiment
- Only one MCC device should be connected at a time
- The device is automatically detected and configured
- All pulse codes are compatible with the original MATLAB implementation
