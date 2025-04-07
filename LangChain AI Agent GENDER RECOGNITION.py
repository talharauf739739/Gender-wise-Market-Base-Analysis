from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
import os

# Set your OpenAI Key
os.environ["OPENAI_API_KEY"] = "your-openai-key"

# 1. Few-shot-like gender identification by name
def identify_gender(text: str) -> str:
    # Simple rule-based for example (Talha = male, Ayesha = female)
    male_names = ["Talha", "Asad", "Ahmed", "Ali"]
    female_names = ["Ayesha", "Zainab", "Fatima", "Sara"]

    name = text.strip().split(" ")[0]
    if name in male_names:
        return f"{name} is likely MALE."
    elif name in female_names:
        return f"{name} is likely FEMALE."
    else:
        return f"Gender for {name} is unclear, please consult ML model or API."

gender_tool = Tool(
    name="GenderIdentifier",
    func=identify_gender,
    description="Identifies gender based on first name using pattern matching."
)

# 2. Agent setup
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

agent = initialize_agent(
    tools=[gender_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 3. Run
prompt = "Find out the gender of the person named Ayesha Khan"
response = agent.run(prompt)
print(response)
