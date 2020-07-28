import os
import shutil

img_dir = r"G:\drive\images\val2017"
xml_dir = r"E:\imgs_and_labels\labels"

txt_dir = r"G:\drive\labels\train2017"
dst_txt_dir = r"G:\drive\labels\val2017"



def rm_img():
    for img_path in os.listdir(img_dir):
        if img_path.endswith(".jpg"):
            txt_path = f"{xml_dir}/{os.path.split(img_path)[-1].split('.')[0]}.xml"     # .xml文件,必要时替换为.txt
            if not os.path.exists(txt_path):
                print(txt_path)
                os.remove(f"{img_dir}/{img_path}")


def rm_xml():
    for txt_path in os.listdir(xml_dir):
        if txt_path.endswith(".xml"):
            img_path = f"{img_dir}/{os.path.split(txt_path)[-1].split('.')[0]}.jpg"
            if not os.path.exists(img_path):
                print(img_path)
                os.remove(f"{xml_dir}/{txt_path}")


def mv_txt():
    for img_path in os.listdir(img_dir):
        try:
            txt_name = img_path.split(".")[0]
            shutil.move(f"{txt_dir}/{txt_name}.txt", f"{dst_txt_dir}/{txt_name}.txt")
        except Exception as e:
            print(f"err: {e}")
            print(img_path)
if __name__ == '__main__':
    mv_txt()
    # rm_img()