#!/bin/bash
# Quick stats for network_fix_test results

echo "=== QUICK STATS ==="
total=$(find results/webarena/*/network_fix_test -name "summary_info.json" | wc -l)
echo "Total tasks: $total"

echo -e "\nStep distribution:"
find results/webarena/*/network_fix_test -name "summary_info.json" -exec grep -h '"n_steps"' {} \; | grep -o '[0-9]\+' | sort -n | uniq -c

echo -e "\nSuccess count:"
find results/webarena/*/network_fix_test -name "summary_info.json" -exec grep -h '"cum_reward"' {} \; | grep -v ': 0' | wc -l
