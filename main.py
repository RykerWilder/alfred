import os
import logging
import time
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from modules.wrapper import get_tools

# importing modules
from modules.network import Network
from modules.time import Time


#instances
net = Network()
clock = Time()


load_dotenv()

def load_system_prompt():
    with open('./system_prompt.txt', 'r') as f:
        return f.read().strip()


MIC_INDEX = None
TRIGGER_WORD = "alfred"
CONVERSATION_TIMEOUT = 20


logging.basicConfig(level=logging.DEBUG)


recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)


# Initialize LLM
llm = ChatOllama(model=os.getenv("OLLAMA_MODEL"), reasoning=False)


# Tools
tools = get_tools(net, clock)

# Tool-calling prompt
system_prompt = load_system_prompt()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


# TTS setup
def speak_text(text: str):
    try:
        engine = pyttsx3.init()
        for voice in engine.getProperty("voices"):
            if "jamie" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"TTS failed: {e}")


# Main interaction loop
def write():
    conversation_mode = False
    last_interaction_time = None

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    if not conversation_mode:
                        logging.info("Listening for wake word...")
                        audio = recognizer.listen(source, timeout=10)
                        transcript = recognizer.recognize_google(audio)
                        logging.info(f"Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"Triggered by: {transcript}")
                            speak_text("How can i help you sir?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")

                    else:
                        logging.info("Listening for next command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio)
                        logging.info(f"Command: {command}")

                        if os.getenv("STANDBY_KEYWORD").lower() in command.lower():
                            logging.info(f"Exit keyword detected. Exiting conversation mode.")
                            speak_text("Going to standby, sir.")
                            conversation_mode = False
                            continue 

                        logging.info("Sending command to agent...")
                        response = executor.invoke({"input": command})
                        content = response["output"]
                        logging.info(f"Agent responded: {content}")

                        print("Alfred:", content)
                        speak_text(content)
                        last_interaction_time = time.time()

                except sr.WaitTimeoutError:
                    logging.warning("Timeout waiting for audio.")
                    if (
                        conversation_mode
                        and time.time() - last_interaction_time > CONVERSATION_TIMEOUT
                    ):
                        logging.info(
                            "No input in conversation mode. Returning to wake word mode."
                        )
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("Could not understand audio.")
                except Exception as e:
                    logging.error(f"Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"Critical error in main loop: {e}")


if __name__ == "__main__":
    write()