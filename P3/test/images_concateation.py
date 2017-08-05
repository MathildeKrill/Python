import numpy as np
import cv2, os
import urllib.request

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
IMWRITE_JPEG_QUALITY = 95
 
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    request = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(request).read()
    image = np.asarray(bytearray(resp), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    # return the image
    return image

def image_crop_square(img, new_size):
    height, width, _ = img.shape
    y = int((height - new_size) / 2)
    x = int((width - new_size) / 2)
    crop_img = img[y : new_size + y, x : new_size + x]
    return crop_img

def concatenate_images(cropped_images):
    start_x = [0] + [0 for _ in cropped_images]
    
    total_height, start_x[1], _ = cropped_images[0].shape
    
    for i in range(1, len(cropped_images)):
        height, width, _ = cropped_images[i].shape
        start_x[i+1] = start_x[i] + width
        if total_height > height:
            total_height = height
    
    big_image = np.zeros((total_height, start_x[-1], 3), np.uint8)
    
    for i in range(len(cropped_images)):
        big_image[:, start_x[i] : (start_x[i+1])] = cropped_images[i][0:total_height, :]
        
    return big_image

def crop_concatenate_resize(urls, filename, cropped_size, final_width):
    cropped_images = [image_crop_square(img = url_to_image(url), new_size = cropped_size) for url in urls]      
    big_image = concatenate_images(cropped_images)  
    
    _, width, _ = big_image.shape          
    resize_factor = final_width / width
    small = cv2.resize(big_image, (0,0), fx = resize_factor, fy = resize_factor)
         
    cv2.imwrite(os.path.expanduser('~/Desktop/' + filename + '.jpg'), small, [int(cv2.IMWRITE_JPEG_QUALITY), IMWRITE_JPEG_QUALITY])        
        # cv2.imshow('img-windows',small)
        # cv2.waitKey(0)

if __name__ == '__main__':
    mfas = [# [950, "http://mfas3.s3.amazonaws.com/objects/SC246818.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246819.jpg", "stater-of-taras-tarentum-with-horse-and-rider-struck-under-philokles-955"], 
            [950, "http://mfas3.s3.amazonaws.com/objects/SC246826.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246827.jpg", "stater-of-taras-tarentum-with-horse-and-rider-struck-under-aristokles-960"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246810.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246811.jpg", "stater-of-taras-tarentum-with-horse-and-rider-951"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246382.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246383.jpg", "stater-of-taras-tarentum-with-rider-vaulting-from-horse-942"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246384.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246385.jpg", "stater-of-taras-tarentum-with-rider-vaulting-from-horse-943"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246802.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246803.jpg", "stater-of-taras-tarentum-with-warrior-on-horseback-crowned-by-victory-struck-under-kallikrates-885"], 
            # [850, "http://mfas3.s3.amazonaws.com/objects/SC255772.jpg", "http://mfas3.s3.amazonaws.com/objects/SC255773.jpg", "stater-of-kelenderis-with-youth-riding-horse-2761"], 
            # [850, "http://mfas3.s3.amazonaws.com/objects/SC251597.jpg", "http://mfas3.s3.amazonaws.com/objects/SC251598.jpg", "drachm-of-aspendos-with-horseman-hurling-spear-3297"], 
            # [800, "http://mfas3.s3.amazonaws.com/objects/SC253370.jpg", "http://mfas3.s3.amazonaws.com/objects/SC253371.jpg", "stater-of-kyzikos-with-horse-and-rider-above-tunny-fish-3299"], 
            [950, "http://mfas3.s3.amazonaws.com/objects/SC246411.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246410.jpg", "nommos-of-taras-tarentum-with-horse-and-rider-2945"], 
            # [950, "", "", ""], 
            ]

    for mfa in mfas:
        crop_concatenate_resize(urls = mfa[1:-1], filename = mfa[-1], cropped_size = mfa[0], final_width = 1024)
 

