#!/usr/bin/env python3
"""
Workflow Toggle Management Script
Enables/disables workflows across all departments
"""

import json
import os
import sys
from pathlib import Path

# Get the workflows directory (where this script is located)
WORKFLOWS_DIR = Path(__file__).parent.absolute()

def list_workflows():
    """List all available workflows"""
    workflows = []
    for category in ['github-actions', 'system-workflows', 'organizational-workflows']:
        category_path = WORKFLOWS_DIR / category
        if category_path.exists():
            for dept_dir in category_path.iterdir():
                if dept_dir.is_dir():
                    for workflow_file in dept_dir.glob('*.json'):
                        with open(workflow_file, 'r') as f:
                            config = json.load(f)
                            workflows.append({
                                'category': category,
                                'department': dept_dir.name,
                                'file': workflow_file.name,
                                'name': config.get('name', 'Unknown'),
                                'enabled': config.get('enabled', False),
                                'path': str(workflow_file)
                            })
    return workflows

def toggle_workflow(workflow_path, enable):
    """Enable or disable a workflow"""
    with open(workflow_path, 'r') as f:
        config = json.load(f)
    
    config['enabled'] = enable
    
    with open(workflow_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config['name']

def main():
    if len(sys.argv) < 2:
        print("Workflow Management Tool")
        print("=" * 50)
        print("\nUsage:")
        print("  python workflow-manager.py list                    - List all workflows")
        print("  python workflow-manager.py enable <path>           - Enable a workflow")
        print("  python workflow-manager.py disable <path>          - Disable a workflow")
        print("  python workflow-manager.py enable-dept <dept>      - Enable all workflows in department")
        print("  python workflow-manager.py disable-dept <dept>     - Disable all workflows in department")
        print("  python workflow-manager.py status                  - Show workflow status summary")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        workflows = list_workflows()
        print(f"\nFound {len(workflows)} workflows:\n")
        for wf in workflows:
            status = "✓ ENABLED" if wf['enabled'] else "✗ DISABLED"
            print(f"{status} | {wf['category']:25s} | {wf['department']:20s} | {wf['name']}")
    
    elif command == 'status':
        workflows = list_workflows()
        enabled = sum(1 for wf in workflows if wf['enabled'])
        disabled = sum(1 for wf in workflows if not wf['enabled'])
        
        print("\nWorkflow Status Summary")
        print("=" * 50)
        print(f"Total workflows:    {len(workflows)}")
        print(f"Enabled:           {enabled}")
        print(f"Disabled:          {disabled}")
        print()
        
        by_category = {}
        for wf in workflows:
            cat = wf['category']
            if cat not in by_category:
                by_category[cat] = {'enabled': 0, 'disabled': 0}
            if wf['enabled']:
                by_category[cat]['enabled'] += 1
            else:
                by_category[cat]['disabled'] += 1
        
        print("By Category:")
        for cat, stats in by_category.items():
            print(f"  {cat}:")
            print(f"    Enabled:  {stats['enabled']}")
            print(f"    Disabled: {stats['disabled']}")
    
    elif command == 'enable' and len(sys.argv) > 2:
        workflow_path = sys.argv[2]
        name = toggle_workflow(workflow_path, True)
        print(f"✓ Enabled workflow: {name}")
    
    elif command == 'disable' and len(sys.argv) > 2:
        workflow_path = sys.argv[2]
        name = toggle_workflow(workflow_path, False)
        print(f"✗ Disabled workflow: {name}")
    
    elif command == 'enable-dept' and len(sys.argv) > 2:
        department = sys.argv[2]
        workflows = [wf for wf in list_workflows() if wf['department'] == department]
        for wf in workflows:
            toggle_workflow(wf['path'], True)
        print(f"✓ Enabled {len(workflows)} workflows in {department}")
    
    elif command == 'disable-dept' and len(sys.argv) > 2:
        department = sys.argv[2]
        workflows = [wf for wf in list_workflows() if wf['department'] == department]
        for wf in workflows:
            toggle_workflow(wf['path'], False)
        print(f"✗ Disabled {len(workflows)} workflows in {department}")
    
    else:
        print("Invalid command. Use 'list', 'status', 'enable', 'disable', 'enable-dept', or 'disable-dept'")
        sys.exit(1)

if __name__ == '__main__':
    main()
