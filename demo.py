#! python3

# 使い方
# ./demo.py --mic --translate=jp2en


#-----------------------------------
#
# 環境に合わせて設定
#
#-----------------------------------
DEEPL_API_KEY = 'ee9db349-09d7-551b-2971-bf9a4030a2fd:fx'
PYTHON = '/home/takago/miniconda3/envs/wp000/bin/python'
UDP_PORT = 10000

#------------------------------------
#
# ここから触らない
#
#-----------------------------------
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--translate', choices=['jp2en', 'en2jp', 'none'], default='none', help='翻訳する')
parser.add_argument('-m', '--mic', action='store_true', help='マイクから入力する')
args = parser.parse_args()

cmd ='nc -u localhost %d -q0' % UDP_PORT

if args.translate=='jp2en':
    os.environ['DEEPL_API_KEY'] = DEEPL_API_KEY
    cmd = ' | '.join( [PYTHON+' -u deepl_jp2en.py', cmd])
elif args.translate=='en2jp':
    os.environ['DEEPL_API_KEY'] = DEEPL_API_KEY
    cmd = ' | '.join( [PYTHON+' -u deepl_en2jp.py', cmd])

if args.mic == True:
    cmd = ' | '.join( [PYTHON+' -u whisper_mic_jp.py' ,cmd] )

print(cmd)
os.system(cmd)