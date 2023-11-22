# on_screen_messenger
This tool displays messages on the desktop.

Qt/whisper-mic/deepl-apiを使ってスクリーン上にメッセージを表示するツールを作成した．

![](https://github.com/takago/on_screen_messenger/blob/main/screenshot00.png)
![](https://github.com/takago/on_screen_messenger/blob/main/screenshot01.png)
https://youtu.be/0LAD8-ASEgw

----
## 実行方法
```
git clone https://github.com/takago/on_screen_messenger.git
cd on_screen_messenger

./on_screen_messenger.git &
（システムトレイ上に常駐する）

~/miniconda3/envs/wp000/bin/pythondemo.py --mic
(喋った日本語が，スクリーンに表示される)

~/miniconda3/envs/wp000/bin/pythondemo.py --translate=en2jp --key='XXXXXXXXXXXXXXXXXXX'
(タイプした英語が日本語になって，スクリーンに表示される)

~/miniconda3/envs/wp000/bin/python ./demo.py --mic --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．Python は whisper-micやdeeplが使えるパスを指定すること！）

~/miniconda3/envs/wp000/bin/python ./demo.py --mic --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．Python は whisper-micやdeeplが使えるパスを指定すること！）


```
