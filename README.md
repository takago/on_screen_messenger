# on_screen_messenger
This tool displays messages on the desktop.
   ![](https://github.com/takago/on_screen_messenger/blob/main/screenshot03.png)
   ![](https://github.com/takago/on_screen_messenger/blob/main/screenshot04.png)
   
Qtを使ってスクリーン上にメッセージを自動スクロール表示するツールを開発しました．例によってLinuxで作りましたが，多分Windowsでも動くと思います．
どのような感じで動くかは動作は以下のビデオを参考にしてください． https://youtu.be/0LAD8-ASEgw

長所？：
 - 透過的になっているので，デスクトップの操作は従来どおり可能．
 - 最前面に表示（何かをフルスクリーン表示していてもその上に描画される）.
 - UDPでテキストを投げ込むだけで，簡単に表示

利用例：
 - 緊急地震速報といった重要な情報を表示する．
 - マイクで拾った音を文字起こし（必要に応じて翻訳）して表示する(↓ OpenAIのwhisperや，DeepL-APIを使ってみた例)．
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshot00.png)
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshot01.png)
 - PCで鳴っている音声を文字起こし（↓のように出力デバイスのmonitorを選べば簡単）
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshot02.png)

----
## 実行方法（書くのが面倒なのでかなりテキトウです）
```
git clone https://github.com/takago/on_screen_messenger.git
cd on_screen_messenger
```

```
python ./on_screen_messenger.py &
（システムトレイ上に常駐する）
```

```
fortune | nc -u localhost 10000 -q0
cowsay Hello | nc -u localhost 10000 -q0

~/miniconda3/envs/wp000/bin/python demo.py --mic
(喋った日本語が，スクリーンに表示される)

~/miniconda3/envs/wp000/bin/python demo.py --translate=en2jp --key='XXXXXXXXXXXXXXXXXXX'
(タイプした英語が日本語になって，スクリーンに表示される)

~/miniconda3/envs/wp000/bin/python ./demo.py --mic --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．Python は whisper-micやdeeplが使えるパスを指定すること！）

~/miniconda3/envs/wp000/bin/python ./demo.py --mic --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．Python は whisper-micやdeeplが使えるパスを指定すること！）
```

----
## メモ
whisper-micを使って音声入力するときはヘッドセットを使うとよいかも
