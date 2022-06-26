# MusicRoomで再生位置を表示出来るようにします。表示するだけで変更は出来ません。
#使用法
#MusicRoom クラスのインスタンスを引数に、MusicPosクラスのインスタンスを作成します。
#mp = MusicPos(mr)
#作成したインスタンスのmusic_time属性にlengthメンバ関数を使用して曲の長さを登録します。
#length(分, 秒)で指定します。
#mp.music_time['bgm/track1.ogg'] = mp.length(3, 14)
#MusicRoomスクリーンでtimerメンバ関数をタイマーに設定します。
#timer 1.0 repeat True action mp.timer

#スクリーンにバーを表示します。
#bar adjustment mp.music_adj
#スクリーンに再生位置を表示します。
#add mp.music_pos(size=10, italic=True)


init -100 python:
    class MusicPos():
        def __init__(self, mr):
            self.mr = mr
            self.music_time = {}
            self.music_text = "00:00/00:00"
            self.music_adj = ui.adjustment(value=0, range=1)

        def timer(self):
            length = self.music_time.get(renpy.music.get_playing(self.mr.channel), 0)
            pos = renpy.audio.audio.get_channel(self.mr.channel).get_pos()
            if length == 0 or pos < 0:
                self.music_adj.change(0)
                pos = 0
            else:
                self.music_adj.change(float(pos) / float(length))

            self.music_text = "%02d:%02d/%02d:%02d" % ( pos / 60000, (pos % 60000) / 1000, length / 60000, (length % 60000) / 1000)

        def length(self, min, sec):
            return (min * 60 + sec) * 1000

        def music_pos(self, *args, **kwargs):
            return DynamicDisplayable(self.dynamic_text, **kwargs)
        def dynamic_text(self, st, at, **kwargs):
            return Text(self.music_text, **kwargs), .1
