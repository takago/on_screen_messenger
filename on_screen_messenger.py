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
        painter.setPen(QColor("#000000"))
        # painter.setFont( QFont("IPAGothic") )
        painter.drawText( QPoint(16, 16), "あ" )
        painter.end()

        self.myicon['hide']=QPixmap( 32, 32 )
        painter=QPainter(self.myicon['hide'])
        painter.eraseRect(0, 0, 32, 32)
        painter.setPen(QColor("#AAAAAA"))
        # painter.setFont( QFont("IPAGothic") )
        painter.drawText( QPoint(16, 16), "あ" )
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
        box.addWidget(self.edit)
        frame.setLayout(box)
        self.setCentralWidget(frame)
        self.SCROLL = True

        # 色
        self.col=dict()
        self.col['fg']='rgba(255,0,0,60%)' # テキストのカラー
        self.col['bg']='rgba(0,0,0,0%)'    # 背景色のカラー
        self.font=dict()
        self.font['family']='Ubuntu Mono'
        self.font['size']=48

        # スタイルを反映
        self.update_mystyle()

        # 影を付ける
        if True:
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(32)
            effect.setColor(QColor("#000000"))
            effect.setOffset(5,5)
            self.edit.setGraphicsEffect(effect)

        # タイマー
        self.timer0 = QTimer()
        self.timer0.setSingleShot(False)  # 連続 or 1ショットか
        self.timer0.setInterval(10)
        self.timer0.timeout.connect(self.append_message)
        self.timer0.start()

        #-----------------------------------------------------
        # システムトレイの設置

        self.tray = QSystemTrayIcon(QIcon(self.myicon['show']))
        m = QMenu() # システムトレイで表示させたいメニュー（コンテクストメニュー）
        self.tray.setContextMenu(m)
        self.tray.show()
        self.tray.setToolTip('On Screen Messenger')
        self.SHOW=True
        self.tray.activated.connect(self.onActivated)       # クリックされたら

        # メニュー項目（バッファのクリア）
        myact0 = QAction('Clear Buffer', m)
        m.addAction(myact0)
        myact0.triggered.connect(self.clear_buffer)

        # メニュー項目（一時停止）
        myact1 = QAction('Pause', m, checkable=True)
        myact1.setChecked(False)              # 選択状態にしておく
        m.addAction(myact1)
        myact1.triggered.connect(self.pause_scroll)

        # メニュー項目（背景の透明度を調整するスライダ）
        myact2 = QAction('trasnparency', m)
        m.addAction(myact2)
        myact2.triggered.connect(self.showslider)

        # メニュー項目（文字色を選択するスライダ）
        myact3 = QAction('font-color', m)
        m.addAction(myact3)
        myact3.triggered.connect(self.showcolsel)

        # メニュー項目（フォント選択ダイアログ）
        myact4 = QAction('font', m)
        m.addAction(myact4)
        myact4.triggered.connect(self.showfontsel)


        # セパレータ
        m.addSeparator()

        # メニュー項目（ダイアログ）
        myact5 = QAction('Information', m)
        m.addAction(myact5)
        myact5.triggered.connect(self.showdialog)
        app.setQuitOnLastWindowClosed(False) # ダイアログを閉じてもメインプログラムは止めない

        # セパレータ
        m.addSeparator()

        # タスクトレイ
        myact6 = QAction('Quit', m)
        m.addAction(myact6)
        myact6.triggered.connect(sys.exit)

        #-----------------------------------------------------

        # スライダー
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setValue(0)
        self.slider.setRange(0,30)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(10)
        self.slider.valueChanged.connect(self.slider_changed)
        self.slider.setWindowIcon(QIcon(self.myicon['show']))
        self.slider.setWindowTitle('Trasnparency Setting')

        #-----------------------------------------------------

        # メッセージボックス
        self.mymsg = QMessageBox()
        self.mymsg.setIcon(QMessageBox.Information)
        self.mymsg.setText("On-Screen-Messenger\nCopyright 2023 TAKAGO LAB.")
        self.mymsg.setWindowTitle("About this application")
        self.mymsg.setWindowIcon(QIcon(self.myicon['show']))

    # スタイルシート
    def update_mystyle(self):
        txt='background: '+self.col['bg']+';' # 背景色
        txt+='color: '+self.col['fg']+';'     # 文字色
        txt+='font-family: '+self.font['family']+';' # フォント
        txt+='font-size: '+str(self.font['size'])+'pt;' # フォントサイズ
        txt+='border-radius: 0px;'
        txt+='border: 0px solid rgba(255,0,0,0%);'
        # print(txt)
        self.edit.setStyleSheet(txt)

    def showcolsel(self,action):
        color = QColorDialog.getColor()
        if color.isValid():
            #print(color.name())
            #print(color.rgba())
            r,g,b=color.red(), color.green(), color.blue()
            self.col['fg']='rgba(%d,%d,%d,60%%)' % (r,g,b)
            self.update_mystyle()

    def showfontsel(self,action):

        current_font = QFont( self.font['family'], pointSize=self.font['size'] )
        font, ok=QFontDialog.getFont(current_font)
        if ok: # フォントが選択されたら
            self.font['family']=font.family()
            self.font['size']=font.pointSize()
            # print(self.font['family'],self.font['size'])
            self.update_mystyle()
            m=self.edit.verticalScrollBar().maximum()
            self.edit.verticalScrollBar().setValue( m ) 


    def slider_changed(self,value):
        self.col['bg']='rgba(0,0,0,%d%%)' % value
        self.update_mystyle()

    def showslider(self, action):
        self.slider.show()  # スライダーを表示

    def showdialog(self):
        self.mymsg.show()

    def onActivated(self, reason):
        self.SHOW = not self.SHOW
        if self.SHOW: # チェックされたら
            w.show() # メインウィンドウを表示する
            self.tray.setIcon(QIcon(self.myicon['show']))
        else:
            w.hide() # メインウィンドウを表示しない（タスクトレイのみになる）
            self.tray.setIcon(QIcon(self.myicon['hide']))

    def append_message(self): # キューから取り出して，表示テキストに追加する
        n = self.edit.verticalScrollBar().value() # 現在のスクロールバー値を退避
        if not q.empty():
            self.edit.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor) # カーソルを末尾に
            self.edit.insertPlainText( q.get() ) # テキストを付け足す
            self.edit.verticalScrollBar().setValue(n) # 退避してあったスクロールバー値を復元
        if self.SCROLL:
            if n < self.edit.verticalScrollBar().maximum():
                self.edit.verticalScrollBar().setValue( n+1 ) # 少し進める

    def clear_buffer(self, action):
        self.edit.setText('')

    def pause_scroll(self, action):
        if action: # チェックされたら
            self.SCROLL = False
        else:
            self.SCROLL = True

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
