import os
from PIL import Image
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBoxesOnImage


ia.seed(1)

GREEN = [0, 255, 0]
ORANGE = [255, 140, 0]
RED = [255, 0, 0]

# Pad image with a 1px white and (BY-1)px black border
def _pad(image, by):
    image_border1 = ia.augmenters.size.pad(image, top=1, right=1, bottom=1, left=1,
                           mode="constant", cval=255)
    image_border2 = ia.augmenters.size.pad(image_border1, top=by-1, right=by-1,
                           bottom=by-1, left=by-1,
                           mode="constant", cval=0)
    return image_border2

# Draw BBs on an image
# and before doing that, extend the image plane by BORDER pixels.
# Mark BBs inside the image plane with green color, those partially inside
# with orange and those fully outside with red.
def draw_bbs(image, bbs, border):
    image_border = _pad(image, border)
    for bb in bbs.bounding_boxes:
        if bb.is_fully_within_image(image.shape):
            color = GREEN
        elif bb.is_partly_within_image(image.shape):
            color = ORANGE
        else:
            color = RED
        image_border = bb.shift(x=border, y=border)\
                         .draw_on_image(image_border, size=2, color=color)

    return image_border

def get_inner_bbs(image_path, dst_img_dir, array_info, p_numbers):
    '''
    :param image_path: src img path
    :param dst_img_dir: img save path
    :param coor_array: label coor array
    :param p_numbers: Numbers of images to enhance
    :return: [(bbs_array, img_info),
            (bbs_array, img_info)]
    '''




    try:
        assert array_info.shape[1] == 5
        coor_array = array_info[:, :-1]
        cls_array = array_info[:, -1]

        image = Image.open(image_path)
        image = np.array(image)
        img_name = os.path.split(image_path)[-1].split(".")[0]
        bbs = BoundingBoxesOnImage.from_xyxy_array(coor_array, shape=image.shape)
    except Exception as e:
        print(f"err:{e}")
        print(array_info.shape)
        print(image_path)
        return None

    # # Draw the original picture
    # image_before = draw_bbs(image, bbs, 100)
    # ia.imshow(image_before)

    # Image augmentation sequence
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),
        iaa.Crop(percent=(0, 0.1)),
        iaa.Sometimes(
            0.5,
            iaa.GaussianBlur(sigma=(0, 0.5))
        ),
        # Strengthen or weaken the contrast in each image.
        iaa.LinearContrast((0.75, 1.5)),
        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
        # change illumination
        iaa.Multiply((0.3, 1.2), per_channel=0.2),
        # affine transformation
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-5, 5),
            shear=(-8, 8)
        )
    ], random_order=True)  # apply augmenters in random order

    res_list = []
    # gen img and coor
    try:
        for epoch in range(p_numbers):
            image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
            # bbs_aug = bbs_aug.remove_out_of_image().clip_out_of_image()

            # # draw aug img and label
            image_after = bbs_aug.draw_on_image(image_aug, size=2, color=[0, 0, 255])
            ia.imshow(image_after)

            # save img
            h, w, c = image_aug.shape

            img_aug_name = rf'{dst_img_dir}/{img_name}_{epoch}.jpg'
            im = Image.fromarray(image_aug)

            im.save(img_aug_name)


            bbs_array = bbs_aug.to_xyxy_array()
            result_array = np.column_stack((bbs_array, cls_array))
            res_list.append([result_array, (img_aug_name, h, w, c)])
    except Exception as e:
        print(e)
        print(img_aug_name)
        return None
    # return coor and img info
    return res_list





if __name__ == '__main__':
    bbs = np.array([[25, 75, 25, 75], [100, 150, 25, 75], [175, 225, 25, 75]])
    get_inner_bbs(r"/inference/output/smoke81.jpg", r"/data/augmentation", bbs, 3)