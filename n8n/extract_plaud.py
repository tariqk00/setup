import json

# Load the exported workflows
with open('debug_n8n/current_workflows.json', 'r') as f:
    workflows = json.load(f)

# Find "Plaud Email to Drive"
target_workflow = next((w for w in workflows if w['name'] == "Plaud Email to Drive"), None)

if target_workflow:
    # Save to the official path
    with open('setup/n8n/plaud_workflow.json', 'w') as f:
        json.dump(target_workflow, f, indent=4)
    print("✅ Successfully extracted 'Plaud Email to Drive' to setup/n8n/plaud_workflow.json")
else:
    print("❌ Could not find workflow named 'Plaud Email to Drive'")
    # Print available names for debugging
    names = [w['name'] for w in workflows]
    print(f"Available workflows: {names}")
