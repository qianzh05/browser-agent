#!/bin/bash

echo "======================================"
echo "    EVALUATION STATUS REPORT"
echo "======================================"
echo ""

# Completed tasks by domain
echo "=== COMPLETED TASKS BY DOMAIN ==="
for domain in shopping shopping_admin gitlab reddit map; do
    completed=0
    success=0
    echo ""
    echo "$domain:"
    for task_dir in results/webarena/$domain/env_var_fixed/webarena.*; do
        if [ -f "$task_dir/summary_info.json" ]; then
            completed=$((completed + 1))
            task_id=$(basename $task_dir | sed 's/webarena\.//')
            n_steps=$(grep '"n_steps"' $task_dir/summary_info.json | grep -oP '\d+')
            reward=$(grep '"cum_reward"' $task_dir/summary_info.json | grep -oP '[\d\.]+' | head -1)
            if [ "$reward" = "1.0" ]; then
                status="✓ SUCCESS"
                success=$((success + 1))
            else
                status="✗ FAILED"
            fi
            printf "  Task %-4s: %2d steps - %s\n" "$task_id" "$n_steps" "$status"
        fi
    done
    if [ $completed -gt 0 ]; then
        echo "  Subtotal: $success/$completed successful"
    fi
done

echo ""
echo "=== CURRENTLY RUNNING ==="
running=$(ps aux | grep "run_webarena.py" | grep -v grep | wc -l)
echo "Active processes: $running"
if [ $running -gt 0 ]; then
    echo "Running tasks:"
    ps aux | grep "run_webarena.py" | grep -v grep | awk '{print "  PID " $2 " - " $(NF-3) " task " $(NF-1)}'
fi

echo ""
echo "=== OVERALL SUMMARY ==="
total_completed=$(find results/webarena/*/env_var_fixed/webarena.* -name "summary_info.json" 2>/dev/null | wc -l)
total_success=$(grep -rh '"cum_reward": 1' results/webarena/*/env_var_fixed/*/summary_info.json 2>/dev/null | wc -l)
total_failed=$((total_completed - total_success))
echo "Total completed: $total_completed/50"
echo "  ✓ Successful: $total_success"
echo "  ✗ Failed: $total_failed"
echo "  ⏳ Remaining: $((50 - total_completed))"
echo ""
echo "Success rate: $(echo "scale=1; $total_success * 100 / $total_completed" | bc 2>/dev/null || echo "N/A")%"

