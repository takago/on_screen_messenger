import deepl

translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))

while True:
    try:
        text = input()
    except EOFError:
        break
    result = translator.translate_text(text, source_lang='EN', target_lang='JA')
    print(result.text+'\n')