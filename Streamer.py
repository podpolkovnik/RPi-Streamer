import json
import subprocess as sp
import time
import json
from watchdog2 import FileModifiedObserver


class RawCmd:
    def __init__(self, raw_cmd, split=' '):
        self.raw_cmd = raw_cmd.split(split)


class Streamer:
    def __init__(self, dash_rule):
        self.dash_rule = dash_rule
        self.command = {}
        self.direct = None
        self.processes = []

    def param_set(self, param, val=None):
        cmd_param = self.dash_rule(param)
        if cmd_param in self.command:
            self.command[cmd_param] = val
        else:
            self.command.update({cmd_param: val})
        return self

    def get_cmd(self):
        out_cmd = []
        for key, val in self.command.items():
            if isinstance(key, RawCmd):
                out_cmd.extend(key.raw_cmd)
            else:
                out_cmd.append(key)
            if val is not None:
                if isinstance(val, Streamer):
                    out_cmd.extend(val.get_cmd())
                else:
                    out_cmd.append(str(val))
        return out_cmd

    def get_raw_cmd(self):
        raw_cmd = ''
        cmd = self.get_cmd()
        for val in cmd:
            raw_cmd += val + ' '
        return raw_cmd

    def raw_command(self, raw_cmd):
        self.command.update({RawCmd(raw_cmd): None})

    def read_from_conf(self, conf):
        with open(conf, 'r') as read_file:
            data = json.load(read_file)
            for key in data.keys():
                if data[key]['enable'] == True:
                    arg = data[key]['arg']
                    print(key, arg)
                    self.param_set(key, arg)
        return self

    def direct_to(self, streamer):
        self.direct = streamer
        return self

    def run_command(self):
        p1 = sp.Popen(self.get_cmd(), stdin=sp.PIPE, stdout=sp.PIPE)
        if self.direct is not None:
            p2 = sp.Popen(self.direct.get_cmd(), stdin=p1.stdout, stdout=sp.PIPE)
        self.processes.append(p1)
        self.processes.append(p2)

    def stop_command(self):
        for process in self.processes:
            process.terminate()

    def restart_command(self):
        self.stop_command()
        self.run_command()


class FFMpeg(Streamer):
    def __init__(self):
        super().__init__(lambda param: '-' + param)
        self.command = {'ffmpeg': None, }


class LibcameraVid(Streamer):
    def __init__(self):
        super().__init__(lambda param: '--' + param if len(param) > 1 else '-' + param)
        self.command = {'libcamera-vid': None, }


config = {}

with open("twin_patch.json", "r") as twin_patch:
    config = json.load(twin_patch)


f = FFMpeg()

# f.param_set('i', '-')\
#     .param_set('f', 'lavfi')\
#     .param_set('i', 'anullsrc')\
#     .param_set('acodec', 'libmp3lame')\
#     .param_set('ar', 44100)\
#     .param_set('deinterlace')\
#     .param_set('vcodec', 'libx264')\
#     .param_set('pix_fmt', 'yuv420p')\
#     .param_set('s', '1920x1080')\
#     .param_set('preset', 'ultrafast')\
#     .param_set('tune', 'fastdecode')\
#     .param_set('r', '30')\
#     .param_set('g', 120)\
#     .param_set('b:v', '6000k')\
#     .param_set('f flv', 'rtmp://a.rtmp.youtube.com/live2/qs42-amm2-yfxz-x6vk-3v8w')

f.raw_command('-i - -f lavfi -i anullsrc -acodec libmp3lame -ar 44100 -deinterlace -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -tune fastdecode -g 120 -b:v 6000k -threads:6 -qscale:3 -b:a:712000 -buffsize:512k -f flv rtmp://a.rtmp.youtube.com/live2/qs42-amm2-yfxz-x6vk-3v8w')
l = LibcameraVid()
l.read_from_conf('/home/pi/camera_conf.json')\
    .direct_to(f)\
    .run_command()


def file_modified_handler():
    global l
    print('CONF MODIFIED')
    l.read_from_conf('/home/pi/camera_conf.json')
    l.restart_command()


observer = FileModifiedObserver('/home/pi/', 'camera_conf.json', file_modified_handler)
observer.start()

while True:
    pass

