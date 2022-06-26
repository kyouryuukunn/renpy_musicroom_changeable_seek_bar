Add ren'Py the changeable seek bar and current position text "XX:XX/XX:XX" for Music Room.
MusicRoomに再生位置を表示、変更出来るシークバーと現在時間のテキスト"XX:XX/XX:XX"を表示できるようにします。

![Demo](https://dl.dropboxusercontent.com/s/yimd4lb1f45kxuz/musicroom2.png)

How to Use
1. create the MusicRoom2 instance instead of MusicRoom.
mr = MusicRoom2(...)
2. add musicroom screen mr.timer.
timer 1.0 repeat True action mr.timer
3. show bar and text in music room screen.

bar adjustment mr.music_adj
add mr.music_pos(size=10, italic=True)

This code overwrites __MusicRoomPlay and MusicRoom play and Play.
This won't work if these are changed.


使用法
MusicRoom クラス替わりにMusicRoom2クラスを使用してミュージックルームを作成します。
mr = MusicPos(mr)
MusicRoomスクリーンでtimerメンバ関数をタイマーに設定します。
timer 1.0 repeat True action mr.timer

スクリーンにバーを表示します。
bar adjustment mr.music_adj
スクリーンに再生位置を表示します。
add mr.music_pos(size=10, italic=True)

MusicRoomクラスのplayとPlay, __MusicRoomPlayを上書きしています。
今後これらの関数が変更されると正常に動作しなくなるでしょう

2022/6/25 Ren'Py 8.00で動作確認
2020/3/22 動作確認
2017/8/8 v6.99.12 で動作確認
