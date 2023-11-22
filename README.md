# on_screen_messenger
This tool displays messages on the desktop.

Qtを使ってスクリーン上にメッセージを表示するツールを開発しました．例によってLinuxで作りましたが，多分Windowsでも動くと思います．
どのような感じで動くかは動作は以下のビデオを参考にしてください． https://youtu.be/0LAD8-ASEgw

長所？：
 - 透過的になっているので，デスクトップの操作は従来どおり可能．
 - 最前面に表示（何かをフルスクリーン表示していてもその上に描画される）.
 - UDPでテキストを投げ込むだけで，簡単に表示

利用例：
 - 緊急地震速報といった重要な情報を表示する．
 - Zoom音声や，マイクで拾った音を文字起こし（必要に応じて翻訳）して表示する(OpenAIのwhisperや，DeepL-APIを使うと簡単です)．
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshot00.png)
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshot01.png)


----
## 実行方法（書くのが面倒なのでかなりテキトウです）
```
git clone https://github.com/takago/on_screen_messenger.git
cd on_screen_messenger
```

```
./on_screen_messenger.git &
（システムトレイ上に常駐する）
```

```
~/miniconda3/envs/wp000/bin/pythondemo.py --mic
(喋った日本語が，スクリーンに表示される)

~/miniconda3/envs/wp000/bin/pythondemo.py --translate=en2jp --key='XXXXXXXXXXXXXXXXXXX'
(タイプした英語が日本語になって，スクリーンに表示される)

~/miniconda3/envs/wp000/bin/python ./demo.py --mic --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．Python は whisper-micやdeeplが使えるパスを指定すること！）

~/miniconda3/envs/wp000/bin/python ./demo.py --mic --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．Python は whisper-micやdeeplが使えるパスを指定すること！）
```

----
## メモ
whisper-micを使って音声入力するときはヘッドセットを使うとよいかも
