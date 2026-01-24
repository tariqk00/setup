import json
import copy

INPUT_FILE = "setup/n8n/plaud_workflow_v5.json" # Using v5/v6 base
OUTPUT_FILE = "setup/n8n/plaud_workflow_v7.json"

def create_debug_workflow():
    with open(INPUT_FILE, 'r') as f:
        workflow = json.load(f)

    # Update Name
    workflow['name'] = "Plaud to Drive Inbox V7 (Debug)"
    if 'versionId' in workflow:
        del workflow['versionId'] # Let n8n generate or we can gen one

    # Add a Debug Log Node
    # This node will upload a text file summarizing what the trigger found
    debug_node = {
        "parameters": {
            "content": "='Subject: ' + $json.subject + '\\nDate: ' + $json.date + '\\nHas Binary: ' + (Object.keys($binary || {}).length > 0 ? 'Yes' : 'No') + '\\nBinary Keys: ' + Object.keys($binary || {}).join(', ')",
            "name": "='debug_log_' + new Date().getTime() + '.txt'",
            "parentId": "16N14A_m847eSortz8hxbfhrk0YyvtouD"
        },
        "id": "debug_node_999",
        "name": "Upload Debug Log",
        "type": "n8n-nodes-base.googleDrive",
        "typeVersion": 2,
        "position": [
             680,
             100 
        ],
        "credentials": {
            "googleDriveOAuth2Api": {
                "id": "G8O3ahUTehXWQ76O", 
                "name": "Google Drive account"
            }
        }
    }

    workflow['nodes'].append(debug_node)

    # Connect Trigger -> Debug Node
    # Check if 'Gmail Trigger' exists in connections
    if 'Gmail Trigger' in workflow['connections']:
        workflow['connections']['Gmail Trigger']['main'][0].append({
            "node": "Upload Debug Log",
            "type": "main",
            "index": 0
        })
    else:
        print("Error: Gmail Trigger not found in connections")

    # Fix the Split Attachments Code to be safer
    # If no binary, we can't really do anything, but let's make sure it doesn't crash
    # The existing code is fine, it just returns empty array if no binary.
    
    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(workflow, f, indent=4)
    
    print(f"✅ Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    create_debug_workflow()
