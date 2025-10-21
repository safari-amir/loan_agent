from langchain_community.agent_toolkits import SQLDatabaseToolkit
from agent.db import *
from agent.llm import *

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

for tool in tools:
    print(f"{tool.name}: {tool.description}\n")