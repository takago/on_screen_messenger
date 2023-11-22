#! python3 -u

import deepl
import os

translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))

while True:
    try:
        text = input()
    except EOFError:
        break
    result = translator.translate_text(text, source_lang='JA', target_lang='EN-US')
    print(result.text+'\n')
