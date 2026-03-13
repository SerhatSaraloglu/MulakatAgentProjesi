from lmstudio_client import generate_response

def main():
    system_prompt = "You are a professional HR interviewer."
    user_prompt = "Ask one interview question for a sales consultant candidate."

    result = generate_response(system_prompt, user_prompt)
    print("\nModel output:")
    print(result)

if __name__ == "__main__":
    main()