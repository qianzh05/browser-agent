import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

os.environ['SHOPPING'] = 'http://localhost:7770'
os.environ['SHOPPING_ADMIN'] = 'http://localhost:7780/admin'
os.environ['REDDIT'] = 'http://localhost:9999'
os.environ['GITLAB'] = 'http://localhost:8023'
os.environ['MAP'] = 'http://localhost:3000'
os.environ['WIKIPEDIA'] = 'http://localhost:8888'
os.environ['HOMEPAGE'] = 'http://localhost:4399'

tasks_by_domain = {
    'shopping': [25, 142, 159, 163, 225, 228, 238, 270, 281, 284, 352, 432, 517, 574, 654, 692, 126],
    'shopping_admin': [6, 94, 95, 114, 203, 344, 348, 459, 777, 781],
    'reddit': [27, 30, 603, 604, 616, 618, 714, 718, 733],
    'gitlab': [104, 389, 665, 754],
    'map': [32, 89, 99, 220, 223, 250, 367, 758, 311, 467]
}

experiment_name = "sonnet46_concurrent"

def run_task(domain, tid):
    cmd = [
        'python', 'agent/run_webarena.py',
        '--task', domain,
        '--task_ids', str(tid),
        '--exp', experiment_name,
        '--model_name', 'anthropic.claude-sonnet-4-6',
        '--headless', 'true',
        '--tips', 'true',
        '--use_screenshot', 'true',
        '--use_som', 'true'
    ]
    result = subprocess.run(cmd, env=os.environ)
    return domain, tid, result.returncode

def run_domain(domain, tids):
    for tid in tids:
        _, _, rc = run_task(domain, tid)
        print(f">>> {domain}.{tid} done (rc={rc}) <<<")

total = sum(len(v) for v in tasks_by_domain.values())
print(f"Running {total} tasks with container-wise parallelism...\n")

with ThreadPoolExecutor(max_workers=len(tasks_by_domain)) as executor:
    futures = {executor.submit(run_domain, domain, tids): domain
               for domain, tids in tasks_by_domain.items()}
    for future in as_completed(futures):
        print(f">>> Domain {futures[future]} fully completed <<<")

print("\nALL TASKS COMPLETED!")
