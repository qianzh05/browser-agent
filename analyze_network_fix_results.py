#!/usr/bin/env python3
"""
Analyze network_fix_test results to identify failure patterns
"""
import json
from pathlib import Path
from collections import Counter, defaultdict

def main():
    results_dir = Path('results/webarena')
    results = list(results_dir.glob('*/network_fix_test/*/summary_info.json'))
    
    print("="*70)
    print("DETAILED FAILURE ANALYSIS - network_fix_test")
    print("="*70 + "\n")
    
    # Categorize tasks by step count
    zero_step = []
    one_step = []
    multi_step_fail = []
    success = []
    
    for r in results:
        data = json.load(open(r))
        task_id = r.parts[-2]
        category = r.parts[-3]
        steps = data['n_steps']
        reward = data['cum_reward']
        err_msg = data.get('err_msg')
        
        task_info = {
            'task_id': task_id,
            'category': category,
            'steps': steps,
            'reward': reward,
            'err_msg': err_msg,
            'path': r.parent
        }
        
        if steps == 0:
            zero_step.append(task_info)
        elif steps == 1:
            one_step.append(task_info)
        elif reward == 0:
            multi_step_fail.append(task_info)
        else:
            success.append(task_info)
    
    # 1. Zero-step failures (initialization errors)
    print(f"🔴 ZERO-STEP FAILURES ({len(zero_step)} tasks)")
    print("-"*70)
    if zero_step:
        print("These tasks failed during initialization:\n")
        for task in zero_step[:10]:
            err = task['err_msg'] if task['err_msg'] else 'No error message'
            print(f"  {task['category']}/{task['task_id']}")
            print(f"    Error: {err[:100]}")
        if len(zero_step) > 10:
            print(f"\n  ... and {len(zero_step)-10} more")
    print()
    
    # 2. One-step failures (potential network errors)
    print(f"⚠️  ONE-STEP FAILURES ({len(one_step)} tasks)")
    print("-"*70)
    if one_step:
        print("Checking for network errors in trajectory files...\n")
        network_errors = []
        agent_errors = []
        
        for task in one_step:
            trajectory_file = task['path'] / 'trajectory.json'
            if trajectory_file.exists():
                with open(trajectory_file) as f:
                    content = f.read()
                    if 'unauthorized' in content.lower() or 'not allowed' in content:
                        network_errors.append(task)
                    else:
                        agent_errors.append(task)
        
        print(f"  Network/Permission errors: {len(network_errors)}")
        for task in network_errors[:5]:
            print(f"    {task['category']}/{task['task_id']}")
        
        print(f"\n  Agent reasoning errors: {len(agent_errors)}")
        for task in agent_errors[:5]:
            print(f"    {task['category']}/{task['task_id']}")
    print()
    
    # 3. Multi-step failures (agent reasoning issues)
    print(f"🔄 MULTI-STEP FAILURES ({len(multi_step_fail)} tasks)")
    print("-"*70)
    if multi_step_fail:
        print("Tasks that ran multiple steps but failed:\n")
        for task in sorted(multi_step_fail, key=lambda x: x['steps'], reverse=True)[:10]:
            print(f"  {task['category']}/{task['task_id']}: {task['steps']} steps")
    print()
    
    # 4. Successes
    print(f"✅ SUCCESSES ({len(success)} tasks)")
    print("-"*70)
    if success:
        for task in success:
            print(f"  {task['category']}/{task['task_id']}: {task['steps']} steps, reward={task['reward']}")
    print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total tasks: {len(results)}")
    print(f"  Zero-step failures: {len(zero_step)} ({len(zero_step)/len(results)*100:.1f}%)")
    print(f"  One-step failures: {len(one_step)} ({len(one_step)/len(results)*100:.1f}%)")
    print(f"  Multi-step failures: {len(multi_step_fail)} ({len(multi_step_fail)/len(results)*100:.1f}%)")
    print(f"  Successes: {len(success)} ({len(success)/len(results)*100:.1f}%)")
    
    if one_step:
        print(f"\n⚠️  Need to investigate {len(one_step)} one-step failures")
        print(f"    Run: grep -r 'unauthorized\\|not allowed' results/webarena/*/network_fix_test/*/trajectory.json")

if __name__ == '__main__':
    main()
