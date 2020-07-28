# coding=utf-8

import os
import cv2




def video2frame(video_src_path, frame_save_path, interval):
    """
    将视频按固定间隔读取写入图片
    :param video_src_path: 视频存放路径
    :param frame_save_path:　保存路径
    :param interval:　保存帧间隔
    :return:　帧图片
    """
    videos = os.listdir(video_src_path)
    for video in videos:
        if not video.endswith(".mp4"):
            videos.remove(video)

    for each_video in videos:
        each_video_name = each_video[:-4]
        video_save_name = each_video.split(".")[0]
        each_video_full_path = os.path.join(video_src_path, each_video)

        cap = cv2.VideoCapture(each_video_full_path)
        frame_index = 0
        frame_count = 0
        if cap.isOpened():
            success = True
        else:
            success = False
            print("读取失败!")

        while (success):
            success, frame = cap.read()
            print("ok")
            if frame_index % interval == 0:
                cv2.imwrite("‪E://1.jpg", frame)
                frame_count += 1

            frame_index += 1

    cap.release()


if __name__ == '__main__':
    videos_src_path = r"E:\videos"
    frames_save_path = r"‪E:\images"
    time_interval = 50
    video2frame(videos_src_path, frames_save_path,  time_interval)

