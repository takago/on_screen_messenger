# on_screen_messenger
This tool displays messages on the desktop.


----
## インストール
```
git clone https://github.com/takago/on_screen_messenger.git
cd on_screen_messenger

# インストールと自動起動の登録
vi demo.py 
 DEEPL_API_KEYパスを編集
 PYTHONパスを編集(whisper-micやdeeplが使えるPythonにする)

on_screen_messenger.git &
 ./demo.py --mic --translate=jp2en  （←喋った日本語が英語になって，スクリーンに表示される）
```
