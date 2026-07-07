from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
    max_tokens=500
)

messages = []

print("Welcome!! To exit press 0")
print("Choose AI personality: Angry, Happy, Sad, Rude")

behaviour = input("Type your AI behaviour: ")

messages.append(
    SystemMessage(content=f"You are a {behaviour} AI. Respond accordingly.")
)

while True:
    prompt = input("Human: ")
    if prompt == '0':
        break

    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages)
    text = response.content

    print("Bot:", text)

    messages.append(AIMessage(content=text))