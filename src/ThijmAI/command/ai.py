import sys
import os
import logging
from llama_cpp import Llama

class suppress_output:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

logging.basicConfig(level=logging.WARNING)

with suppress_output():
    llm = Llama(model_path="./models_ai/model_tinyllama.gguf")


def chat(prompt):
    with suppress_output():
        response = llm(prompt, max_tokens=110)

    model_answer = response["choices"][0]["text"].strip()
    return model_answer

