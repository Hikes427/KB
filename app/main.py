from llm import ask_llm
def main():
 print("AI Solutions Architect Assistant")
 print("Type 'exit' to quit\n")
 while True:
  question = input("Architect > ")
  if question.lower() == "exit":
     break
  answer = ask_llm(question)
  print("\nAnswer:\n")
  print(answer)
  print()
if __name__ == "__main__":
 main()