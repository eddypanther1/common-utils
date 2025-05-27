#helper_test.py
from helper_functions import print_llm_response, get_llm_response

jp_words = ["難読漢字","言葉","文章","発音","難しい文法"]
en_words = []

for word in jp_words:
    prompt = f"Translate the following Japanese word {word} into English. Max 2 words (1 word preferred). Don't explain."
    english_word = get_llm_response(prompt)   
    print(f"{word}: {english_word}")
