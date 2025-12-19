import json, os
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

def ui():

    try:

        size = os.get_terminal_size()
        size_correction = round(size.columns/2)

        width = size.columns - size_correction
        height = round(width/2.4)
        if height % 2 == 0:
            height += 1

        right_text = {
            0: "AI Political Compass grader",
            1: "by mitokac",
            # 4: f"Wynik poziomy: {score['horizontal']}",
            # 5: f"Wynik pionowy: {score['vertical']}"
        }

        print("┌" + "─" * width + "┐")

        # Rysowanie środka
        for i in range(height):


            row = "│" + " " * (round(width/2)-1) + ":" + " " *  (round(width/2)-1) + "│"

            if i == round(height/2):
                row = "│" + "-" * width + "│"


            # Sprawdzamy, czy dla tej linii (i) mamy przypisany tekst
            # Jeśli tak, dodajemy numer i treść. Jeśli nie, zostawiamy puste.
            if i in right_text:
                text_side = f"{right_text[i]}"
            else:
                text_side = ""

            print(f"{row}   {text_side}")

        print("└" + "─" * width + "┘")


    except OSError:
        print("Use this in a terminal you stupid fuck")




def main():
    # sentence = sentence_input()
    # score = grading(sentence)
    ui()


    # print(score["horizontal"], score["vertical"])

if __name__ == '__main__':
    main()
