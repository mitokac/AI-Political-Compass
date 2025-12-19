import json
from llama_cpp import Llama, LlamaGrammar
from pathlib import Path

def sentence_input():
    print("Input sentence:")
    #sentence = input()
    
    sentence = "People should be allowed to opt out of state systems (schooling, pensions) and choose privately."
    return sentence


def grading(sentence):
    model_name = "Qwen3-4B-Q8_0.gguf"
    #model_name = "Llama-3.2-1B-Instruct-Q8_0.gguf"
    model_path = "/home/mito/LLMs/" + model_name

    def load_system_prompt() -> str:
        return Path("system_prompt.txt").read_text(encoding="utf-8").strip()




    g = r"""
    root  ::= "{" ws "\"horizontal\"" ws ":" ws horizontal ws "," ws "\"vertical\"" ws ":" ws vertical ws "}"
    horizontal ::= "100" | [1-9] [0-9] | [0-9]
    vertical ::= "100" | [1-9] [0-9] | [0-9]
    ws    ::= [ \t\n\r]*
    """
    g = LlamaGrammar.from_string(g)

    #example of grammar:
    #{"horizontal": 63, "vertical": 12}


    llm = Llama(
            model_path = model_path,
            verbose=False
          # n_gpu_layers=-1, # Uncomment to use GPU acceleration
          # seed=1337, # Uncomment to set a specific seed
          # n_ctx=2048, # Uncomment to increase the context window


    )

    system_prompt = load_system_prompt()

    resp = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": sentence},
        ],
        temperature=0.0,
        max_tokens=32,
        grammar=g,
    )
    txt = resp["choices"][0]["message"]["content"]
    punkt = json.loads(txt)
    return punkt


def main():
    sentence = sentence_input()
    score = grading(sentence)



    print(score["horizontal"], score["vertical"])

if __name__ == '__main__':
    main()
