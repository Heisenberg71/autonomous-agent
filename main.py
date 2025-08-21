import sys
from agent.agent import process_user_query

def print_correct_usage():
    user_instructions = "Usage: python main.py <your question here>"
    print(user_instructions)
    sys.exit(1)

def generate_result():
    user_query = " ".join(sys.argv[1:])
    generated_result = process_user_query(user_query)
    print(generated_result)

def main():
    if len(sys.argv) < 2:
        print_correct_usage()
    generate_result()
    

if __name__ == "__main__":
    main()
