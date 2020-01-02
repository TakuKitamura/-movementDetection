import cv2
import time
import os
import base64
import json

save_dir = "./img/"


if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

def main():
    cam = cv2.VideoCapture(0)
    img1 = img2 = img3 = get_image(cam)
    th = 1000
    max_image_number = 10
    while True:
        if cv2.waitKey(1) == 13: break
        diff = check_image(img1, img2, img3)
        cnt = cv2.countNonZero(diff)
        print(cnt, th)
        if cnt > th:
            print("検出")
            cv2.imshow('PUSH ENTER KEY', img3)
            img_file_path = save_dir + str(time.time()) + ".jpg"
            cv2.imwrite(img_file_path, img3)
            img_list = os.listdir(save_dir)
            img_list.sort()
            # print(img_list)
            # print("aaa", img_list)
            if len(img_list) > max_image_number:
                # print("before", img_list)
                for i in range(0, len(img_list)):
                    os.remove(save_dir + img_list[i])
                    # print('path', save_dir + img_list[i])
                    img_list.pop(0)
                    # print("before222", img_list)
                    if len(img_list) == max_image_number:
                        break
                # print("after", img_list)
            imgs_data = {}
            # print("bbb", img_list)
            img_list.sort(reverse=True)
            for v in img_list:
                with open(save_dir + v, mode='rb') as f:
                    imgs_data[v] = base64.b64encode(f.read()).decode("utf-8")
            # print(imgs_data)

            with open("imgs.json", "w") as f:
                json.dump(imgs_data, f)
            # time.sleep(1)
        else:
            cv2.imshow('PUSH ENTER KEY', diff)
        img1, img2, img3 = (img2, img3, get_image(cam))
    cam.release()
    cv2.destroyAllWindows()

def check_image(img1, img2, img3):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    gray3 = cv2.cvtColor(img3, cv2.COLOR_RGB2GRAY)

    diff1 = cv2.absdiff(gray1, gray2)
    diff2 = cv2.absdiff(gray2, gray3)

    diff_and = cv2.bitwise_and(diff1, diff2)

    _, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)

    diff = cv2.medianBlur(diff_wb, 5)

    return diff

def get_image(cam):
    img = cam.read()[1]
    # img = cv2.resize(img, (600, 400))
    return img
main()