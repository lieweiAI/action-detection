from xml.dom.minidom import parse
from PIL import Image
import os

# xml_dir = r"E:yolov3\data\path\outputs"
# xml_dir = r"G:\img_label\train_xml"
# xml_dir = r"G:\yolov5-master\data\augmentation\outputs"
xml_dir = r"E:\imgs_and_labels\labels"
xml_file_list = os.listdir(xml_dir)


def parse_2_txt():
    for file_path in xml_file_list:
        xml_path = os.path.join(xml_dir, file_path)
        dom = parse(xml_path)
        root = dom.documentElement
        img_name = root.getElementsByTagName("path")[0].childNodes[0].data
        label_name = os.path.split(img_name)[-1].split(".")[0]

        img_size = root.getElementsByTagName("size")[0]
        img_w = int(img_size.getElementsByTagName("width")[0].childNodes[0].data)
        img_h = int(img_size.getElementsByTagName("height")[0].childNodes[0].data)
        # img_c = img_size.getElementsByTagName("depth")[0].childNodes[0].data
        # objects = root.getElementsByTagName("object")
        item = root.getElementsByTagName("item")
        with open(rf"E:\imgs_and_labels\txt_labels/{label_name}.txt", "w") as f:
            for box in item:
                cls_name = box.getElementsByTagName("name")[0].childNodes[0].data
                # a = box.getElementsByTagName("xmin")[0].childNodes[0].data

                x1 = float(box.getElementsByTagName("xmin")[0].childNodes[0].data)
                y1 = float(box.getElementsByTagName("ymin")[0].childNodes[0].data)
                x2 = float(box.getElementsByTagName("xmax")[0].childNodes[0].data)
                y2 = float(box.getElementsByTagName("ymax")[0].childNodes[0].data)

                if min(x1, x2) > img_w or min(y1, y2)>img_h:
                    print(f"bbs out of range: x1:{x1},y1:{y1},x2:{x2},y2:{y2}")
                    print(xml_path)
                    continue

                if max(x1, x2) < 0 or max(y1, y2) < 0:
                    print(f"bbs out of range: x1:{x1},y1:{y1},x2:{x2},y2:{y2}")
                    print(xml_path)
                    continue

                def maxmin(x, y):
                    if x > y:
                        return y
                    elif x < 0:
                        return 0
                    else:
                        return x

                x1, y1, x2, y2 = map(maxmin, [x1,y1,x2,y2],[img_w, img_h, img_w, img_h])

                w, h = (x2 - x1) / img_w, (y2 - y1) / img_h
                cx, cy = (w / 2 + x1) / img_w, (h / 2 + y1) / img_h

                if not len(list(filter(lambda x: (0 <= x <= 1), [w, h, cx, cy]))) == 4:
                    print(file_path)
                    raise ValueError(f"cx:{cx}, cy:{cy}, w:{w}, h:{h}")

                if cls_name == "smoke":
                    class_num = 0
                elif cls_name == "call":
                    class_num = 1
                elif cls_name == "drink":
                    class_num = 2
                else:
                    raise ValueError("class name error!")
                f.writelines(f"{' '.join(list(map(str, [class_num, cx, cy, w, h])))}\n")

        # print(len(objects))


def check_cls_name():
    for file_path in xml_file_list:
        xml_path = os.path.join(xml_dir, file_path)
        dom = parse(xml_path)
        root = dom.documentElement
        item = root.getElementsByTagName("item")
        for box in item:
            cls_name = box.getElementsByTagName("name")[0].childNodes[0].data
            if cls_name == "smoker":
                print(xml_path)


if __name__ == '__main__':
    # check_cls_name()
    parse_2_txt()
