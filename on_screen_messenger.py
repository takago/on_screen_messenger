# 鷹合研(2023,11/23)
#
# 簡単なテスト
# echo "Hello" | nc -u localhost 10000 -q 0
# fortune | nc -u localhost 10000 -q0

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
import sys
import queue
import threading
import socket

# メッセージキュー
q = queue.Queue()

def net_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 10000))
    while True:
        (recv_text, adr) = s.recvfrom(65535)
        q.put( recv_text.decode('utf-8') ) # キューに追加する

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # アイコンを作成
        self.myicon=dict()

        self.myicon['show']=QPixmap( 32, 32 )
        painter=QPainter(self.myicon['show'])
        painter.eraseRect(0, 0, 32, 32)
        painter.setPen(Qt.black)
        painter.setFont( QFont("IPAGothic") )
        painter.drawText( QPoint(16, 16), "あ" )
        painter.end()
         
        self.myicon['hide']=QPixmap( 32, 32 )
        painter=QPainter(self.myicon['hide'])
        painter.eraseRect(0, 0, 32, 32)
        painter.end()

        self.setWindowIcon(QIcon(self.myicon['show']))
        self.setGeometry(0, 0, screen_size.width(), screen_size.height()//3)

        win_flags = Qt.FramelessWindowHint        # フレームなし．
        win_flags |= Qt.WindowStaysOnTopHint      # 常に最前面になる（他が全画面表示しても大丈夫）
        win_flags |= Qt.WindowTransparentForInput # 下側のアプリを操作できる(その代わり，テキスト入力やボタンが押せなくなる)
                                                  # 文字列などを画面上にオーバレイ表示させるのに使えそう
        win_flags |= Qt.Tool                      # 「パネル」にアプリケーションアイコンを表示しない

        self.setWindowFlags(win_flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        frame = QFrame(parent=self)
        frame.setStyleSheet("QFrame {background: rgba(0,0,0,0%)}")

        box=QHBoxLayout()
        self.edit = QTextEdit()
        self.edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # スクロールバーを表示しない
        self.edit.setCursorWidth(0) # カーソルを消す
        self.edit.setText('\n\n(o_o)/\n')
        self.edit.setStyleSheet("background: rgba(0,0,0,0%); color: rgba(255,0,0,60%); font-size: 48pt; border-radius: 0px; border: 2px solid rgba(255,0,0,0%);")
        box.addWidget(self.edit)
        frame.setLayout(box)
        self.setCentralWidget(frame)

        # タイマー（文字を動かす）
        self.timer0 = QTimer()
        self.timer0.setSingleShot(False)  # 連続 or 1ショットか
        self.timer0.setInterval(10)
        self.timer0.timeout.connect(self.scroll_message)
        self.timer0.start()

        # タイマー（受信テキストの追加）
        self.timer1 = QTimer()
        self.timer1.setSingleShot(False)  # 連続 or 1ショットか
        self.timer1.setInterval(100)
        self.timer1.timeout.connect(self.append_message)
        self.timer1.start()

        # システムトレイの設置
        self.tray = QSystemTrayIcon(QIcon(self.myicon['show']))
        m = QMenu() # システムトレイで表示させたいメニュー
        self.tray.setContextMenu(m)
        self.tray.show()
        self.tray.setToolTip('On Screen Messenger')
        self.SHOW=True
        self.tray.activated.connect(self.onActivated)       # クリックされたら

        # タスクトレイ（バッファのクリア）
        myact0 = QAction('Clear Buffer', m)
        m.addAction(myact0)
        myact0.triggered.connect(self.clear_buffer)

        # タスクトレイ（一時停止）
        myact1 = QAction('Pause', m, checkable=True)
        myact1.setChecked(False)              # 選択状態にしておく
        m.addAction(myact1)
        myact1.triggered.connect(self.pause_scroll)

        # タスクトレイ（ダイアログ）
        myact2 = QAction('Information', m)
        m.addAction(myact2)
        myact2.triggered.connect(self.showdialog)
        app.setQuitOnLastWindowClosed(False) # ダイアログを閉じてもメインプログラムは止めない

    def showdialog(self):
        mymsg = QMessageBox()
        mymsg.setIcon(QMessageBox.Information)
        mymsg.setText("On-Screen-Messenger\nCopyright 2023 TAKAGO LAB.")
        mymsg.setWindowTitle("About this application")
        mymsg.exec()

    def onActivated(self, reason):
        self.SHOW = not self.SHOW
        if self.SHOW: # チェックされたら
            w.show() # メインウィンドウを表示する
            self.tray.setIcon(QIcon(self.myicon['show']))
        else:
            w.hide() # メインウィンドウを表示しない（タスクトレイのみになる）
            self.tray.setIcon(QIcon(self.myicon['hide']))

    def append_message(self): # キューから取り出して，表示テキストに追加する
        if not q.empty():
            n = self.edit.verticalScrollBar().value() # 現在のスクロールバー値を退避
            self.edit.setText( self.edit.toPlainText()+q.get() ) # テキストを付け足す
            self.edit.verticalScrollBar().setValue(n) # 退避してあったスクロールバー値を復元

    def scroll_message(self):
        n = self.edit.verticalScrollBar().value()
        if n < self.edit.verticalScrollBar().maximum():
            self.edit.verticalScrollBar().setValue( n+1 ) # 少し進める

    def clear_buffer(self, action):
        self.edit.setText('')

    def pause_scroll(self, action):
        if action: # チェックされたら
            self.timer0.stop()
        else:
            self.timer0.start()

if __name__ == '__main__':

    threading.Thread(target=net_thread,daemon=True).start()

    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    screen_size = screen.size()
    print('Size: %d x %d' % (screen_size.width(), screen_size.height()))

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())