
from config import *
from moviepy.editor import VideoFileClip


# 长代码连接 https://blog.csdn.net/longjuanfengzc/article/details/103006691
#获取视频的播放时长 # pip install moviepy /可以传网络资源
def gitVideoTime(videoUrl):
    try:
        clip = VideoFileClip(videoUrl)
        time = clip.duration
        return int(time)
    except:
        return 0




