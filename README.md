# on_screen_messenger
This tool displays messages on the desktop.

![](https://youtu.be/0LAD8-ASEgw)

----
## インストール
```
git clone https://github.com/takago/on_screen_messenger.git
cd on_screen_messenger

# 設定と，起動

vi demo.py 
  (1) DEEPL_API_KEYパスを編集
  (2) PYTHONパスを編集(whisper-micやdeeplが使えるPythonにする)

on_screen_messenger.git &
./demo.py --mic --translate=jp2en  （←喋った日本語が英語になって，スクリーンに表示される）
./demo.py --translate=jp2en (←タイプした日本語が英語になって，スクリーンに表示される)
```
