import json

INPUT_FILE = "setup/n8n/plaud_workflow.json"
OUTPUT_FILE = "setup/n8n/plaud_workflow_v5.json"

def fix_workflow():
    with open(INPUT_FILE, 'r') as f:
        workflow = json.load(f)

    nodes = workflow['nodes']
    connections = workflow['connections']

    # 1. Fix Email Body (Fallback to text)
    for node in nodes:
        if node['name'] == 'Upload Email Body':
            # Use 'text' if 'textAsHtml' is missing
            node['parameters']['content'] = '={{ $json.textAsHtml || $json.text }}'
            # Ensure filename is safe
            node['parameters']['name'] = '={{ $json.date }} {{ $json.subject.replace(/[^a-zA-Z0-9 ]/g, "") }}.html'

    # 2. Fix Attachments (Split binary keys)
    # We need to insert a Code node to split "attachment_0", "attachment_1" into separate items.
    
    # Define new node
    split_node = {
        "parameters": {
            "jsCode": """
const results = [];
for (const item of items) {
  if (item.binary) {
    for (const key of Object.keys(item.binary)) {
      results.push({
        json: {
          ...item.json,
          original_binary_key: key
        },
        binary: {
          data: item.binary[key]
        }
      });
    }
  }
}
return results;
"""
        },
        "id": "split_attachments_node",
        "name": "Split Attachments",
        "type": "n8n-nodes-base.code",
        "typeVersion": 1,
        "position": [
            680, 
            500 
        ]
    }
    
    nodes.append(split_node)

    # 3. Update "Upload Attachments" to receive from Split Node
    for node in nodes:
        if node['name'] == 'Upload Attachments':
            # It now receives normalized "data" from the split node
            node['parameters']['fileSelector'] = 'data' 
            # Update name to ensure uniqueness
            node['parameters']['name'] = '={{ $json.date }} {{ $json.subject.replace(/[^a-zA-Z0-9 ]/g, "") }} - {{ $binary.data.fileName }}'
            # Adjust position to be after split
            node['position'] = [900, 500]

    # 4. Rewire Connections
    # Configuration -> Utils(Split) -> Upload Attachments
    
    # Remove old connection: Configuration -> Upload Attachments
    if 'Configuration' in connections and 'main' in connections['Configuration']:
        main_outputs = connections['Configuration']['main'][0]
        # Filter out the one pointing to Upload Attachments
        connections['Configuration']['main'][0] = [
            link for link in main_outputs if link['node'] != 'Upload Attachments'
        ]
        
        # Add connection: Configuration -> Split Attachments
        connections['Configuration']['main'][0].append({
            "node": "Split Attachments",
            "type": "main",
            "index": 0
        })

    # Add connection: Split Attachments -> Upload Attachments
    connections['Split Attachments'] = {
        "main": [
            [
                {
                    "node": "Upload Attachments",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }
    
    # 5. Connect Upload Attachments -> Archive Email (Merging back)
    # Existing connection usually handles this, but let's check
    # The existing JSON had "Upload Attachments" -> "Archive Email". 
    # That is preserved in 'Upload Attachments' outgoing connections key if it exists.
    # We just need to make sure we didn't break the 'node name' reference (we didn't).

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(workflow, f, indent=4)
    
    print(f"✅ Fixed workflow saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    fix_workflow()
