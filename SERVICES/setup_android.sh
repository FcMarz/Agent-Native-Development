#!/bin/bash
# setup_android.sh - Configures USB permissions for the connected Sony Android phone.

# Find the Sony device on USB
SONY_DEVICE=$(lsusb | grep -E "0fce:(320d|420d)")

if [ -z "$SONY_DEVICE" ]; then
    echo "❌ Error: Sony Android phone (Vendor: 0fce, Product: 420d/320d) not found on USB."
    echo "Please ensure the phone is connected via USB and USB Debugging is enabled in Developer Options."
    exit 1
fi

# Extract bus and device numbers
BUS=$(echo "$SONY_DEVICE" | awk '{print $2}')
DEV=$(echo "$SONY_DEVICE" | awk '{print $4}' | sed 's/://')
DEV_PATH="/dev/bus/usb/$BUS/$DEV"

echo "📱 Found Sony Android phone at: $DEV_PATH"
echo "Current permissions: $(ls -l $DEV_PATH)"
echo ""
echo "--- ACTION REQUIRED ---"
echo "Linux restricts direct USB write access by default, resulting in 'no permissions' for ADB."
echo "Please execute the following commands in your host terminal to grant access:"
echo ""
echo "1️⃣  Apply a temporary fix for this session:"
echo "    sudo chmod 666 $DEV_PATH"
echo ""
echo "2️⃣  Apply a permanent udev rule (recommended):"
echo "    echo 'SUBSYSTEM==\"usb\", ATTR{idVendor}==\"0fce\", ATTR{idProduct}==\"420d\", MODE=\"0666\"' | sudo tee /etc/udev/rules.d/51-android-sony.rules"
echo "    sudo udevadm control --reload-rules && sudo udevadm trigger"
echo ""
echo "3️⃣  Restart your ADB server to apply changes:"
echo "    ./SERVICES/platform-tools/adb kill-server"
echo "    ./SERVICES/platform-tools/adb devices"
echo ""
echo "Once completed, you should see your device listed as 'device' instead of 'no permissions'."
