import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

os.environ['WA_SHOPPING'] = 'http://localhost:7770'
os.environ['WA_SHOPPING_ADMIN'] = 'http://localhost:7780'
os.environ['WA_REDDIT'] = 'http://localhost:9999'
os.environ['WA_GITLAB'] = 'http://localhost:8023'
os.environ['WA_MAP'] = 'http://localhost:3000'
os.environ['WA_WIKIPEDIA'] = 'http://localhost:8888'
os.environ['WA_HOMEPAGE'] = 'http://localhost:4399'

task_ids = [27, 30, 603, 604, 616, 618, 714, 718, 733]

def run_task(tid):
    cmd = [
        'python', 'agent/run_webarena.py',
        '--task', 'reddit',
        '--task_ids', str(tid),
        '--exp', 'reddit_fix_test',
        '--model_name', 'gpt-5',
        '--headless', 'true'
        # NO --rerun flag for concurrent execution
    ]
    print(f"\n{'='*60}")
    print(f"Starting Reddit task {tid}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, env=os.environ)
    
    print(f"\n{'='*60}")
    print(f"Task {tid} finished with return code: {result.returncode}")
    print(f"{'='*60}\n")
    
    return tid, result.returncode

print("Running 9 Reddit tasks with 3 concurrent workers...")
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(run_task, tid) for tid in task_ids]
    for future in as_completed(futures):
        task_id, returncode = future.result()

print("\nAll Reddit tasks completed!")
