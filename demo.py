# 鷹合研(2023,11/23)

import os
import argparse
import sys

PYTHON=sys.executable # 現在実行しているPythonのパスを取得する

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--translate', choices=['jp2en', 'en2jp', 'none'], default='none', help='翻訳する')
parser.add_argument('-k', '--key', default='XXXXXXXXXXX', help='DEEPL-APIのキー')
parser.add_argument('-a', '--audio', action='store_true', help='オーディオデバイスから入力する')
parser.add_argument('-p', '--port', default=10000, help='on_screen_messengerのUDPポート番号')
args = parser.parse_args()

cmd ='nc -u localhost %d -q0' % args.port

if args.translate=='jp2en':
    os.environ['DEEPL_API_KEY'] = args.key
    cmd = ' | '.join( [PYTHON+' -u sub/deepl_jp2en.py', cmd])
elif args.translate=='en2jp':
    os.environ['DEEPL_API_KEY'] = args.key
    cmd = ' | '.join( [PYTHON+' -u sub/deepl_en2jp.py', cmd])

if args.audio == True:
    cmd = ' | '.join( [PYTHON+' -u sub/whisper_mic_jp.py' ,cmd] )

print('-'*len(cmd))
print(cmd)
print('-'*len(cmd))
os.system(cmd)