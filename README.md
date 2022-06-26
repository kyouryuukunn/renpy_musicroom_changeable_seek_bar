Add ren'Py the seek bar and current position text "XX:XX/XX:XX" for Music Room.

How to Use
1. create the MusicPos instance with MusicRoom instance
mr = MusicRoom(...)
mp = MusicPos(mr)
2. call lenght to regist the length of music files.
mp.music_time['bgm/track1.ogg'] = mp.length(3, 14) # (min, sec)
3. add musicroom screen mp.timer.
timer 1.0 repeat True action mp.timer
4. show bar and text in music room screen.

bar adjustment mp.music_adj
add mp.music_pos(size=10, italic=True)


使用法
MusicRoom クラスのインスタンスを引数に、MusicPosクラスのインスタンスを作成します。
mp = MusicPos(mr)
作成したインスタンスのmusic_time属性にlengthメンバ関数を使用して曲の長さを登録します。
length(分, 秒)で指定します。
mp.music_time['bgm/track1.ogg'] = mp.length(3, 14)
MusicRoomスクリーンでtimerメンバ関数をタイマーに設定します。
timer 1.0 repeat True action mp.timer

スクリーンにバーを表示します。
bar adjustment mp.music_adj
スクリーンに再生位置を表示します。
add mp.music_pos(size=10, italic=True)

![Demo](https://dl.dropboxusercontent.com/s/cyfizgl2pvk8w9x/musicroom2.png)
