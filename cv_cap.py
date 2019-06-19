"""
接続されたカメラ画像を表示し、queueを受け取るとqueueの名前の画像を保存する
"""

# OpenCV のインポート
import cv2
import sys
import time

# cv_capのみのテスト用のモジュール
from multiprocessing import Manager

class VideoClass:
    def __init__(self, queue, end_flag):
        super(VideoClass, self).__init__()
        self.q = queue
        self.end_flag = end_flag
        self.cap_video()

    def cap_video(self):
        # VideoCaptureのインスタンスを作成する。
        cap = cv2.VideoCapture(0)

        while True:
            # VideoCaptureから1フレーム読み込む
            ret, frame = cap.read()

            if not self.q.empty():
                cv2.imwrite('photo/{}.jpg'.format(self.q.get()), frame)

            # 加工なし画像を表示する
            cv2.imshow('Raw Frame', frame)

            if not self.end_flag.empty():
                print(self.end_flag.get())
                break

            # キー入力を1ms待って、k が27（ESC）だったらBreakする
            k = cv2.waitKey(1)
            if k == 27:
                break

        # キャプチャをリリースして、ウィンドウをすべて閉じる
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()


if __name__ == "__main__":
    q = Manager().Queue()
    end_flag = Manager().Queue()
    q.put("aa")
    end_flag.put("ee")
    VideoClass(q, end_flag).cap_video()
