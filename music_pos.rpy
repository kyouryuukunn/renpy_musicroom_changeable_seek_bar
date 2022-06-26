# MusicRoomで再生位置を表示、変更出来るようになります。
# Ren'Pyv6.99.9以上で動作します。

#使用法
# music_pos.rpyをgameフォルダに置きMusicRoom クラス替わりにMusicRoom2クラスを使用
# してミュージックルームを作成します。
# mp = MusicRoom2(fadeout=1.0)

#作成したインスタンスのmusic_time属性にlengthメンバ関数を使用して曲の長さを登録します。
#mp.music_time['bgm/track1.ogg'] = mp.length(3, 14) #3分14秒

#MusicRoomスクリーンでtimerメンバ関数をタイマーに設定します。
#timer 1.0 repeat True action mp.timer

#スクリーンにバーを表示します。
#bar adjustment mp.music_adj
#スクリーンに再生位置をテキストで表示します。
#add mp.music_pos(size=10, italic=True)

#MusicRoomクラスのplayとPlay, __MusicRoomPlay, renpy.audio.music.get_playingを上書きしています。
#今後これらの関数が変更されると正常に動作しなくなるでしょう

#2020/3/22 動作確認
#2017/8/8 v6.99.12 で動作確認

init 100 python:
########changed##########
    def get_playing(channel="music", with_prefix=False):
########changed##########
        """
        :doc: audio

        If the given channel is playing, returns the playing file name.
        Otherwise, returns None.

        `with_prefix`
        return file name with partial prefix
        """

        try:
########changed##########
            c = renpy.audio.audio.get_channel(channel)
            filename = c.get_playing()
            if with_prefix:
                return filename
            if filename is None:
                return None
            m = re.match(r'<(.*)>(.*)', filename)
            if not m:
                return filename
            return m.group(2)
########changed##########
        except:
            if renpy.config.debug_sound:
                raise

            return None
    renpy.audio.music.get_playing = get_playing

init -100 python:
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
            self.mr.play(self.filename, 0)

        def get_sensitive(self):
            return self.mr.is_unlocked(self.filename)

        def get_selected(self):
            return renpy.music.get_playing(self.mr.channel) == self.filename

        def periodic(self, st):
            if self.selected != self.get_selected():
                self.selected = self.get_selected()
                renpy.restart_interaction()

            self.mr.periodic(st)

            return .1

    class MusicRoom2(MusicRoom):
        def __init__(self, *args, **kwargs):
            super(MusicRoom2, self).__init__(*args, **kwargs)
            self.music_time = {}
            self.music_text = "00:00/00:00"
            self.music_adj = ui.adjustment(value=0., range=1., changed=self.changed, adjustable=True)
            self.manual_change = True

        def timer(self):
            fn = renpy.music.get_playing(self.channel, with_prefix=True)
            length = self.music_time.get(renpy.music.get_playing(self.channel), 0)
            pos = renpy.music.get_pos(self.channel)
            self.manual_change = False
            if length == 0 or pos < 0 or pos > length:
                self.music_adj.change(0)
                pos = 0
            else:
                self.music_adj.change(float(pos) / float(length))
            self.manual_change = True

            self.music_text = "%02d:%02d/%02d:%02d" % ( pos / 60, pos % 60, length / 60, length % 60)

        def length(self, min, sec):
            return min * 60 + sec

        def music_pos(self, *args, **kwargs):
            return DynamicDisplayable(self.dynamic_text, **kwargs)
        def dynamic_text(self, st, at, **kwargs):
            return Text(self.music_text, **kwargs), .1
        def changed(self, changed):
            fn = renpy.music.get_playing(self.channel)
            length = self.music_time.get(fn, 0)
            if length > 0 and self.manual_change:
                fn = "<from "+str(changed*length)+" to "+str(length)+" loop 0>"+fn
                self.Play(fn)()

        def Play(self, filename=None):

            if filename is None:
                return self.play

########changed##########
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

########changed##########
            try:
                m = re.match(r'<(.*)>(.*)', filename) if filename is not None else None
                if not m:
                    idx = playlist.index(filename)
                else:
                    idx = playlist.index(m.group(2))
            except ValueError:
                idx = 0
########changed##########

            idx = (idx + offset) % len(playlist)

            if self.single_track:
                playlist = [ playlist[idx] ]
            elif self.loop:
                playlist = playlist[idx:] + playlist[:idx]
            else:
                playlist = playlist[idx:]

########changed##########
            if m:
                playlist[playlist.index(m.group(2))] = filename
########changed##########

            if queue:
                renpy.music.queue(playlist, channel=self.channel, loop=self.loop)
            else:
                renpy.music.play(playlist, channel=self.channel, fadeout=self.fadeout, fadein=self.fadein, loop=self.loop)
