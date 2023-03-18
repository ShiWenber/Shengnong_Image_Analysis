import cv2
import os
from time import time

def merge_image_to_video(fold_path: str, img_size: tuple = (640, 480), fps: int = 20, fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), save_path: str = "output.mp4"):
    """合成图片为视频

    Args:
        fold_path (str): 图片文件夹的路径
        img_size (tuple, optional): 图片的尺寸，需要fold_path下的图片统一尺寸, cv2.VideoWriter的参数. Defaults to (640, 480).
        fps (int, optional): 帧率, cv2.VideoWriter的参数 . Defaults to 20.
        fourcc (cv2.VideoWriter_fourcc, optional): cv2.VideoWriter的参数. Defaults to cv2.VideoWriter_fourcc('m', 'p', '4', 'v').
        save_path (str, optional): 视频保存的路径，cv2.VideoWriter的参数. Defaults to "output.mp4".
    """
    start_time = time()
    video = cv2.VideoWriter(save_path, fourcc, fps, img_size)

    file_ls = []
    for f1 in os.listdir(fold_path):
        file = os.path.join(fold_path, f1)
        file_ls.append(file)
    file_ls.sort()
    img_ls = map(cv2.imread, file_ls)

    print("merge_image_to_video_io: ", time() - start_time)
    for i in img_ls:
        video.write(i)

    video.release()
    print("merge_image_to_video: ", time() - start_time)



if __name__ == '__main__':
    # 多进程加速
    from multiprocessing import Pool
    # 当机位为6时，最多六条并行，继续增加Pool池也不会提速
    pool = Pool(6)
    folder_names = map(lambda x:r"C:\Users\shiwenbo\OneDrive\images\gather\src" + str(x), range(6))
    print(folder_names)
    start_time = time()
    idx: int = 0
    for i in folder_names:
        pool.apply_async(merge_image_to_video, args=(i, (640, 480), 20, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), "src" + str(idx) + ".mp4"))
        # merge_image_to_video(i, (640, 480), 20, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), "src" + str(idx) + ".mp4")
        idx += 1
    pool.close()
    pool.join()
    print("time: ", time() - start_time)

