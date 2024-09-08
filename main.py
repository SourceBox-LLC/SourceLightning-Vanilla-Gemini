import google.generativeai as genai
from dotenv import load_dotenv
import os

# Function to save the API key to a .env file
def save_api_key_to_env(api_key, key_name):
    if os.path.exists(".env"):
        os.remove(".env")  # Remove existing .env file if it exists
    with open(".env", "w") as env_file:
        env_file.write(f"{key_name}={api_key}\n")
    print(".env file created with the API key.")

def get_gemini_api_key():
    # Check if API key is present in environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Prompt the user to enter the API key if not found
        manual_api_key = input("Enter your Gemini API key: ")
        save_api_key_to_env(manual_api_key, "GEMINI_API_KEY")
        # Reload the environment with the new API key
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
    return api_key

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = get_gemini_api_key()

# Configure the Gemini client with API key from .env
try:
    genai.configure(api_key=api_key)
    print("Gemini client configured successfully.")
except Exception as e:
    raise RuntimeError(f"Failed to configure Gemini API: {e}")

# List to store conversation history
conversation_history = []

def gemini_response(user_input):
    print("Generating response...\n")
    """
    Generate a response from Gemini based on user input and conversation history.
    """
    try:
        # Add the user's input to the conversation history
        if not user_input.strip():
            raise ValueError("User input cannot be empty.")

        conversation_history.append({"role": "user", "content": user_input})

        # Concatenate the entire conversation history into a single string
        conversation_string = ""
        for message in conversation_history:
            conversation_string += f"{message['role']}: {message['content']}\n"

        if not conversation_string.strip():
            raise ValueError("Conversation history cannot be empty.")

        # Generate the content using the Gemini API
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini model: {e}")

        try:
            response = model.generate_content(conversation_string)
        except Exception as e:
            raise RuntimeError(f"Failed to generate content with Gemini API: {e}")

        # Extract the assistant's reply
        assistant_reply = response.text
        if not assistant_reply:
            raise ValueError("Empty response from Gemini API.")

        # Add the assistant's reply to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except ValueError as ve:
        return f"Error: {ve}"
    except RuntimeError as re:
        return f"Error: {re}"
    except Exception as e:
        return f"Unexpected error occurred: {e}"

def run_chatbot():
    print("\nWelcome to the Gemini Command Line Chatbot!\n")
    print("Type 'exit' to end the conversation.\n")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            # Generate a response and print it
            response = gemini_response(user_input)
            print(f"Gemini: {response}\n")

        except KeyboardInterrupt:
            print("\nChatbot session terminated.")
            break

if __name__ == "__main__":
    run_chatbot()
