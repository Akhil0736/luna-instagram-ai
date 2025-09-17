import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Python path includes: {sys.path[:3]}")

# Test the import
try:
    from agents.conversation.conversation_agent import ConversationAgent
    print("✅ ConversationAgent imported successfully!")
    agent = ConversationAgent()
    print("✅ ConversationAgent instantiated successfully!")
except Exception as e:
    print(f"❌ Import error: {e}")
    
    # Check if agents directory exists
    agents_path = os.path.join(project_root, 'agents')
    conv_path = os.path.join(agents_path, 'conversation', 'conversation_agent.py')
    print(f"Agents directory exists: {os.path.exists(agents_path)}")
    print(f"ConversationAgent file exists: {os.path.exists(conv_path)}")
