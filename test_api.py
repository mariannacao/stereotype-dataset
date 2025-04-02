import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

def load_env():
    current_dir = Path(__file__).parent.absolute()
    env_path = current_dir / '.env'
    print(f"Looking for .env at: {env_path}")
    
    if not env_path.exists():
        print(f"ERROR: No .env file found at {env_path}")
        return False
        
    load_dotenv(env_path)
    return True

def test_openrouter():
    print("Testing OpenRouter configuration...")
    
    if not load_env():
        return
    
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY is not set in .env file")
        return
    
    print("\nEnvironment Variables:")
    print(f"OPENROUTER_API_KEY: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        print("\nInitializing OpenRouter client...")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "TestApp"  
            }
        )
        
        print("\nSending API request...")
        messages = [{"role": "user", "content": "Say hello!"}]
        model = "deepseek/deepseek-chat-v3-0324:free" 
        print(f"Messages: {messages}")
        print(f"Model: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        
        print("\nRaw API Response:")
        print(response)
        print("\nFormatted Response:")
        print(response.choices[0].message.content)
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nDetailed Error Information:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())

def test_openai():
    print("Testing OpenAI configuration...")
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = "gpt-3.5-turbo" 
    
    print(f"API Key present: {bool(api_key)} (starts with: {api_key[:4]}...)")
    print(f"Model: {model}")
    
    try:
        client = OpenAI(
            api_key=api_key
        )
        
        print("\nTesting API call...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say hello!"}
            ],
            temperature=0.7
        )
        
        print("\nAPI Response:")
        print(response.choices[0].message.content)
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    print("=== Testing OpenRouter API ===")
    test_openrouter() 