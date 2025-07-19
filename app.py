import requests
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, FIRST_MESSAGE, ACCOUNT_LOOKUP_TOOL_PROMPT, RENTAL_START_AND_END_TOOL_PROMPT, GET_EXTENDED_COST_TOOL_PROMPT

load_dotenv()
HEADERS = {"Authorization": f"Bearer {os.environ['VAPI_API_KEY']}"}

class VapiAgent:
    def __init__(self):
        self.URL = "https://api.vapi.ai"

    # Step 1: Upload the files to the VAPI as knowledge base
    def upload_files(self, file_path):
        """
        Upload a file to the VAPI API for the AI agent to look up the data from.
        Args:
            file_path: The path to the file to upload
        Returns:
            The file ids of the uploaded files
        """
        
        url = f"{self.URL}/file"
        
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, headers=HEADERS, files=files)
            return response.json()
    
    # Step 2: Create the AI agent
    def create_agent(self):
        """
        Create an AI agent with the given name, first message, model, and voice.
        Args:
            name: The name of the agent
            first_message: The first message the agent will send
            model: The model to use for the agent
            voice: The voice to use for the agent
        Returns:
            The id of the created agent
        """

        url = f"{self.URL}/assistant"
        HEADERS["Content-Type"] = "application/json"
        data = {
            "name": "Elizabeth",
            "firstMessage": FIRST_MESSAGE,
            "model": {
                "provider": "openai",
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    }
                ]
            },
            "voice": {
                "provider": "vapi",
                "voiceId": "Kylie"
            }
        }

        response = requests.post(url, headers=HEADERS, json=data)
        assistant = response.json()
        return assistant['id']
    

    # Step 3: Add the custom tools to the agent
    def create_tool(self, name, description, knowledge_bases):
        url = f"{self.URL}/tool"
        HEADERS["Content-Type"] = "application/json"
        
        data = {
            "type": "query",
            "function": {
                "name": name,
                "description": description
            },
            "knowledgeBases": knowledge_bases
        }
        
        response = requests.post(url, headers=HEADERS, json=data)
        return response.json()
    

    def create_tools(self, renters_info_file_id, rental_schedule_file_id):
        """
        Create the tools for the agent.
        Args:
            renters_info_file_id: The id of the renters info file
            rental_schedule_file_id: The id of the rental schedule file
        Returns:
            The ids of the created tools
        """
        tool_ids = []

        # A: Create the account lookup tool
        account_lookup_tool = self.create_tool(
        "account_lookup",
        ACCOUNT_LOOKUP_TOOL_PROMPT,
        [{"provider": "google", "name": "renters_info", "description": "Use this to retrieve account information", "fileIds": [renters_info_file_id]}]
    )

        #B: Create the get rental start and end tool
        get_rental_start_and_end_tool = self.create_tool(
        "get_rental_start_and_end",
        RENTAL_START_AND_END_TOOL_PROMPT,
        [
            {"provider": "google", "name": "renters_info info", "description": "Use this to retrieve account information", "fileIds": [renters_info_file_id]},
            {"provider": "google", "name": "rental_schedule", "description": "Use this to retrieve transactions", "fileIds": [rental_schedule_file_id]}
        ]
    )
        #C: Create the get extended cost tool
        get_extended_cost_tool = self.create_tool(
        "get_extended_cost", 
        GET_EXTENDED_COST_TOOL_PROMPT,
        [
            {"provider": "google", "name": "renters_info info", "description": "Use this to retrieve account information", "fileIds": [renters_info_file_id]},
            {"provider": "google", "name": "rental_schedule", "description": "Use this to retrieve transactions", "fileIds": [rental_schedule_file_id]}
        ]
    )
        tool_ids = [account_lookup_tool['id'], get_rental_start_and_end_tool['id'], get_extended_cost_tool['id']]
        return tool_ids
    

    # Step 4: add the tools to the agent
    def update_assistant_with_tools(self, assistant_id, tool_ids):
        url = f"{self.URL}/assistant/{assistant_id}"
        HEADERS["Content-Type"] = "application/json"
        
        data = {
            "model": {
                "toolIds": tool_ids
            }
        }
        
        response = requests.patch(url, headers=HEADERS, json=data)
        return response.json()
    

agent = VapiAgent()

# Step 1: Upload the files to the VAPI API as knowledge base
try:
    renters_info_file_id = agent.upload_files("renters_info.csv")['id']
    rental_schedule_file_id = agent.upload_files("rental_schedule.csv")['id']
    print("--------------------------------")
    print("Step 1: Files successfully uploaded")
    print(f"renters_info_file_id: {renters_info_file_id}")
    print(f"rental_schedule_file_id: {rental_schedule_file_id}")
    print("--------------------------------")
except Exception as e:
    print(f"Error uploading files: {e}")
    exit(1)

# Step 2: create the agent
try:
    assistant_id = agent.create_agent()
    print("--------------------------------")
    print("Step 2: Agent created")
    print(f"assistant_id: {assistant_id}")
    print("--------------------------------")
except Exception as e:
    print(f"Error creating agent: {e}")
    exit(1)

# Step 3: create tools and get the tool ids
try:
    tool_ids = agent.create_tools(renters_info_file_id, rental_schedule_file_id)
    print("--------------------------------")
    print("Step 3: Tools created")
    print(f"tool_ids: {tool_ids}")
    print("--------------------------------")
except Exception as e:
    print(f"Error creating tools: {e}")
    exit(1)