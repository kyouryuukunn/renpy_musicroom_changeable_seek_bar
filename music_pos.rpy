# MusicRoomで再生位置を表示、変更出来るようになります。
# Ren'Pyv6.99.9以上で動作します。

#使用法
# music_pos.rpyをgameフォルダに置きMusicRoom クラス替わりにMusicRoom2クラスを使用
# してミュージックルームを作成します。
# mp = MusicRoom2(fadeout=1.0)

#MusicRoomスクリーンでtimerメンバ関数をタイマーに設定します。
#timer 1.0 repeat True action mp.timer

#スクリーンにバーを表示します。
#bar adjustment mp.music_adj
#スクリーンに再生位置をテキストで表示します。
#add mp.music_pos(size=10, italic=True)

#MusicRoomクラスのplayとPlay, __MusicRoomPlayを上書きしています。
#今後これらの関数が変更されると正常に動作しなくなるでしょう

#2022/6/26 Ren'Py 8.0.0で動作確認
#2020/3/22 動作確認
#2017/8/8 v6.99.12 で動作確認

#本家で同機能を実装するには
#MusicRoom以外で使用するなら現在のプレイリスト、ループ, フェード設定の所得機能が必要
#get_durationはプレフィックスのあるファイルの再生時に機能しないため、手動定義が必要
init -100 python:

    def remove_play_prefix(filename):
        if filename is None:
            return None
        m = re.match(r'<(.*)>(.*)', filename)
        if not m:
            return filename
        return m.group(2)

    @renpy.pure
    class __MusicRoomPlay(Action, FieldEquality):
        """
        The action returned by MusicRoom.Play when called with a file.
        """

        identity_fields = [ "mr" ]
        equality_fields = [ "filename" ]


        def __init__(self, mr, filename):
            self.mr = mr
            self.filename = filename
            self.selected = self.get_selected()

        def __call__(self):
 
            renpy.restart_interaction()

            ##changed#####
            # if renpy.music.get_playing(self.mr.channel) == self.filename:
            filename = renpy.music.get_playing(self.mr.channel)
            filename = remove_play_prefix(filename)
            if filename == self.filename:
            ##changed#####
                if renpy.music.get_pause(self.mr.channel):
                    renpy.music.set_pause(False, self.mr.channel)
                    return

            self.mr.play(self.filename, 0)

        def get_sensitive(self):
            return self.mr.is_unlocked(self.filename)

        def get_selected(self):
            ##changed#####
            # return renpy.music.get_playing(self.mr.channel) == self.filename
            filename = renpy.music.get_playing(self.mr.channel)
            filename = remove_play_prefix(filename)
            return filename == self.filename
            ##changed#####

        def periodic(self, st):
            if self.selected != self.get_selected():
                self.selected = self.get_selected()
                renpy.restart_interaction()

            self.mr.periodic(st)

            return .1

    class MusicRoom2(MusicRoom):
        def __init__(self, *args, **kwargs):
            super(MusicRoom2, self).__init__(*args, **kwargs)
            self.music_text = "00:00/00:00"
            self.music_adj = ui.adjustment(value=0., range=1., changed=self.changed, adjustable=True)
            self.manual_change = True

        def timer(self):
            fn = renpy.music.get_playing(self.channel)
            fn = remove_play_prefix(fn)
            length = renpy.music.get_duration(self.channel)
            pos = renpy.music.get_pos(self.channel)
            self.manual_change = False
            if length == 0 or pos < 0 or pos > length:
                self.music_adj.change(0)
                pos = 0
            else:
                self.music_adj.change(float(pos) / float(length))
            self.manual_change = True

            self.music_text = "%02d:%02d/%02d:%02d" % ( pos / 60, pos % 60, length / 60, length % 60)

        def music_pos(self, *args, **kwargs):
            return DynamicDisplayable(self.dynamic_text, **kwargs)
        def dynamic_text(self, st, at, **kwargs):
            return Text(self.music_text, **kwargs), .1
        def changed(self, changed):
            fn = renpy.music.get_playing(self.channel)
            fn = remove_play_prefix(fn)
            length = renpy.music.get_duration(self.channel)
            if length > 0 and self.manual_change:
                #to があるとget_durationで再生時時間が所得できない
                fn = "<from "+str(changed*length)+" loop 0>"+fn
                self.Play(fn)()

        def Play(self, filename=None):

            if filename is None:
                return self.play

########changed##########
            # if filename not in self.filenames:
            m = re.match(r'<(.*)>(.*)', filename)
            if filename not in self.filenames and not m and m.group(2) not in self.filenames:
########changed##########
                raise Exception("{0!r} is not a filename registered with this music room.".format(filename))

            return __MusicRoomPlay(self, filename)
        

        def play(self, filename=None, offset=0, queue=False):

            playlist = self.unlocked_playlist(filename)

            if not playlist:
                return

            if filename is None:
                filename = renpy.music.get_playing(channel=self.channel)
                filename = remove_play_prefix(filename)

            try:
########changed##########
                # idx = playlist.index(filename)
                m = re.match(r'<(.*)>(.*)', filename) if filename is not None else None
                if not m:
                    idx = playlist.index(filename)
                else:
                    idx = playlist.index(m.group(2))
########changed##########
            except ValueError:
                idx = 0

            idx = (idx + offset) % len(playlist)

            if self.single_track:
                playlist = [ playlist[idx] ]
            elif self.loop:
                playlist = playlist[idx:] + playlist[:idx]
            else:
                playlist = playlist[idx:]

########added##########
            if m:
                playlist[playlist.index(m.group(2))] = filename
########added##########

            renpy.store.test = playlist
            if queue:
                renpy.music.queue(playlist, channel=self.channel, loop=self.loop)
            else:
                renpy.music.play(playlist, channel=self.channel, fadeout=self.fadeout, fadein=self.fadein, loop=self.loop)
