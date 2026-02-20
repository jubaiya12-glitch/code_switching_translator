from src.code_switch_handler import CodeSwitchHandler


if __name__ == "__main__":
    handler = CodeSwitchHandler(target_language='en')

    while True:
        text = input("\nEnter text (type exit to quit): ")

        if text.lower() == "exit":
            break

        result = handler.process_text(text)
        print("\nFinal Output:", result["translated"])
