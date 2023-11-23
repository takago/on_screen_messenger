import deepl
import os

translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))

n=0
while True:
    try:
        text = input()
    except EOFError:
        break
    result = translator.translate_text(text, source_lang='EN', target_lang='JA')
    n=n+1
    print('[%d] %s' % (n,text))
    print('[%d] %s' % (n,result.text))

