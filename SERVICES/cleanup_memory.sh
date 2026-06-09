#!/usr/bin/env bash
# Resource and Memory Management Utility for Agent-Native Development Laboratory
# This script displays memory stats, identifies dangling/runaway processes, and cleans memory caches.

echo "============================================================"
echo "📊 SYSTEM RESOURCE DIAGNOSTIC"
echo "============================================================"
date
echo ""

# 1. Show current memory and swap status
echo "--- Memory & Swap Usage ---"
free -h
echo ""

# 2. Show disk space
echo "--- Disk Space Usage ---"
df -h /
echo ""

# 3. Check for high-memory processes
echo "--- Top 10 Memory Consuming Processes ---"
ps aux --sort=-%mem | head -n 11
echo ""

# 4. Check for dangling Python or Node execution threads from simulations
echo "--- Active Simulation / Research Processes ---"
SIM_PROCS=$(pgrep -f -a "run_debate|run_02_evaluator|run_03_critic_loop|input_server")
if [ -z "$SIM_PROCS" ]; then
    echo "No active background simulation/evaluator processes found."
else
    echo "$SIM_PROCS"
    echo ""
    echo "💡 To terminate all background simulation threads, run:"
    echo "   pkill -f 'run_debate|run_02_evaluator|run_03_critic_loop'"
fi
echo ""

# 5. Reclaim memory caches if running as root
echo "--- Memory Reclaim Options ---"
if [ "$EUID" -ne 0 ]; then
    echo "ℹ️  Run this script with sudo/root permissions to drop system memory caches:"
    echo "   sudo $0 --clean"
else
    if [ "$1" = "--clean" ]; then
        echo "🧹 Dropping PageCache, dentries, and inodes..."
        sync
        echo 3 > /proc/sys/vm/drop_caches
        echo "✅ System memory caches cleared successfully."
        echo ""
        free -h
    else
        echo "💡 Sudo detected. Run with '--clean' flag to drop system memory caches."
    fi
fi
echo "============================================================"
