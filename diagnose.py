import json
import os
import glob

# Define the path and specific tasks we saw
base_dir = os.path.expanduser('~/browser-agent/results/webarena/shopping/concurrent_50/')
task_ids = ['webarena.126', 'webarena.145', 'webarena.166', 'webarena.228', 'webarena.331']

for task_id in task_ids:
    print(f"\n=== ANALYSIS: {task_id} ===")
    path = os.path.join(base_dir, task_id)
    
    # 1. Check the Summary (Did it crash? Did it think it won?)
    summary_path = os.path.join(path, "summary_info.json")
    if os.path.exists(summary_path):
        try:
            with open(summary_path) as f:
                data = json.load(f)
                print(f"Final State: {data.get('state')}") # 'stopped', 'failed', etc.
                if data.get('error'):
                    print(f"CRITICAL ERROR: {data.get('error')}")
        except:
            print("Error reading summary.")
    else:
        print("No summary_info.json found (Task likely crashed hard).")

    # 2. Check the Last Recorded Step
    step_files = glob.glob(os.path.join(path, "steps_info_*.json"))
    if step_files:
        # Find the highest numbered step
        latest_step = max(step_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        with open(latest_step) as f:
            step_data = json.load(f)
            step_num = step_data.get('step')
            action = step_data.get('action', 'No action')
            obs = step_data.get('obs', {})
            error = obs.get('last_action_error')
            
            print(f"Stopped at Step: {step_num}")
            print(f"Last Action: {action}")
            if error:
                print(f"ACTION ERROR: {error}")
            else:
                print("No specific action error recorded.")
    else:
        print("No step files found.")
