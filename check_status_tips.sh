#!/bin/bash
echo "======================================"
echo " EVALUATION STATUS REPORT"
echo "======================================"
echo ""
echo "=== COMPLETED TASKS BY DOMAIN ==="
total_success=0
total_partial=0
total_failed=0
total_completed=0
for domain in shopping shopping_admin gitlab reddit map; do
    completed=0; success=0; partial=0
    echo ""
    echo "$domain:"
    for task_dir in $(ls -d results/webarena/$domain/with_tips/webarena.* 2>/dev/null | sort -t. -k2 -n); do
        if [ -f "$task_dir/summary_info.json" ]; then
            completed=$((completed + 1))
            task_id=$(basename $task_dir | sed 's/webarena\.//')
            n_steps=$(grep '"n_steps"' $task_dir/summary_info.json | grep -oP '\d+')
            reward=$(grep '"cum_reward"' $task_dir/summary_info.json | grep -oP '[\d\.]+' | head -1)
            if (( $(echo "$reward == 1.0" | bc -l) )); then
                status="✓ SUCCESS"; success=$((success + 1))
            elif (( $(echo "$reward > 0.0" | bc -l) )); then
                status="~ PARTIAL"; partial=$((partial + 1))
            else
                status="✗ FAILED"
            fi
            printf "  Task %-4s: %2d steps - %s (reward: %s)\n" "$task_id" "$n_steps" "$status" "$reward"
        fi
    done
    [ $completed -gt 0 ] && echo "  Subtotal: $success success, $partial partial, $((completed-success-partial)) failed / $completed"
    total_success=$((total_success + success))
    total_partial=$((total_partial + partial))
    total_completed=$((total_completed + completed))
done
total_failed=$((total_completed - total_success - total_partial))
echo ""
echo "=== CURRENTLY RUNNING ==="
found=0
for task_dir in results/webarena/*/with_tips/webarena.*; do
    if [ -d "$task_dir" ] && [ ! -f "$task_dir/summary_info.json" ]; then
        task_id=$(basename $task_dir)
        domain=$(echo $task_dir | cut -d'/' -f3)
        step_count=$(ls $task_dir/steps_info_*.json 2>/dev/null | wc -l)
        printf "  %-20s [%-15s] %d steps so far\n" "$task_id" "$domain" "$step_count"
        found=1
    fi
done
[ $found -eq 0 ] && echo "  None"
echo ""
echo "=== OVERALL SUMMARY ==="
echo "Total completed: $total_completed/50"
echo "  ✓ Successful: $total_success"
echo "  ~ Partial:    $total_partial"
echo "  ✗ Failed:     $total_failed"
echo "  ⏳ Remaining: $((50 - total_completed))"
echo ""
echo "Success rate: $(echo "scale=1; $total_success * 100 / $total_completed" | bc 2>/dev/null || echo "N/A")%"
echo "Partial rate: $(echo "scale=1; $total_partial * 100 / $total_completed" | bc 2>/dev/null || echo "N/A")%"
