# on_screen_messenger
This tool displays messages on the desktop.
   ![](https://github.com/takago/on_screen_messenger/blob/main/screenshots/screenshot03.png)
   
Qtを使ってスクリーン上にメッセージを自動スクロール表示するツールを作りました．例によってLinuxで作りましたが，多分Windowsでも動くと思います．
どのような感じで動くかは動作は以下のビデオを参考にしてください． https://youtu.be/0LAD8-ASEgw

長所？：
 - 透過的になっているので，デスクトップの操作は従来どおり可能．
 - 最前面に表示（何かをフルスクリーン表示していてもその上に描画される）.
 - UDPでテキストを投げ込むだけで，簡単に表示

利用例：
 - 緊急地震速報といった重要な情報を表示する．
 - マイクで拾った音を文字起こし（必要に応じて翻訳）して表示する(↓ OpenAIのwhisperや，DeepL-APIを使ってみた例)．
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshots/screenshot00.png)
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshots/screenshot01.png)
 - PCで鳴っている音声を文字起こし（↓のように出力デバイスのmonitorを選べば簡単）
   - ![](https://github.com/takago/on_screen_messenger/blob/main/screenshots/screenshot02.png)

----
## 実行方法（書くのが面倒なのでかなりテキトウです）
### 準備
```
conda create -n wp000 -c conda-forge python=3.9 ipython cudatoolkit-dev cudatoolkit cudnn numba numpy pytorch-gpu tqdm more-itertools tiktoken=0.3.1 ffmpeg-python=0.2.0

pip install whisper-mic deepl
（minicondaなどでPython実行環境を作っておくことを推奨）
```
whisper-mic.pyを修正（一つはバグ対応，もう一つは言語設定）
```diff
--- whisper_mic.py.org	2023-11-23 22:08:17.192311969 +0900
+++ whisper_mic.py	2023-11-23 22:11:30.226769425 +0900
@@ -14,7 +14,7 @@
 
 
 class WhisperMic:
-    def __init__(self,model="base",device=("cuda" if torch.cuda.is_available() else "cpu"),english=False,verbose=False,energy=300,pause=2,dynamic_energy=False,save_file=False, model_root="~/.cache/whisper",mic_index=None):
+    def __init__(self,model="base",device=("cuda" if torch.cuda.is_available() else "cpu"),english=False,verbose=False,energy=300,pause=2,dynamic_energy=False,save_file=False, model_root=os.path.expanduser("~/.cache/whisper"),mic_index=None):
         self.logger = get_logger("whisper_mic", "info")
         self.energy = energy
         self.pause = pause
@@ -132,7 +132,7 @@
         if self.english:
             result = self.audio_model.transcribe(audio_data,language='english')
         else:
-            result = self.audio_model.transcribe(audio_data)
+            result = self.audio_model.transcribe(audio_data,language='japanese')
 
         predicted_text = result["text"]
         if not self.verbose:
```
### 起動（本体）

```
sudo apt-get install python3-qtpy
git clone https://github.com/takago/on_screen_messenger.git
cd on_screen_messenger
python ./on_screen_messenger.py &
（システムトレイ上に常駐する）
```
   ![](https://github.com/takago/on_screen_messenger/blob/main/screenshots/screenshot04.png)
   
### 動作テスト（UDP:10000ポートに書き込むプログラムなら何でも良い）
```
fortune | nc -u localhost 10000 -q0
cowsay Hello | nc -u localhost 10000 -q0

~/miniconda3/envs/wp000/bin/python demo.py --audio
(喋った日本語が，スクリーンに表示される)

~/miniconda3/envs/wp000/bin/python demo.py --translate=en2jp --key='XXXXXXXXXXXXXXXXXXX'
(タイプした英語が日本語になって，スクリーンに表示される. keyはDEEPL-APIのキーを指定すること)

~/miniconda3/envs/wp000/bin/python ./demo.py --audio --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．）

~/miniconda3/envs/wp000/bin/python ./demo.py --audio --translate=jp2en --key='XXXXXXXXXXXXXXXXXXX'
（喋った日本語が英語になって，スクリーンに表示される．）
```

----
## メモ
whisper-micを使って音声入力するときはヘッドセットを使うとよいかも
