import numpy, cv2, os
import urllib.request

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
IMWRITE_JPEG_QUALITY = 95
 
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    request = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(request).read()
    image = numpy.asarray(bytearray(resp), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    # return the image
    return image

def image_crop_square(img, new_size):
    height, width, _ = img.shape
    print(str(height) + '; ' + str(width))
    if new_size > height:
        new_size = height
    if new_size > width:
        new_size = width
    y = int((height - new_size) / 2)
    x = int((width - new_size) / 2)
    crop_img = img[y : new_size + y, x : new_size + x]
    return crop_img

def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return int(float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1)))
    return int(float(num[:-1])) 

def size_same(images, height_not_width, crop_not_scale=False):
    if height_not_width:
        shape_dim = 0
    else:
        shape_dim = 1
    min_size = min([image.shape[shape_dim] for image in images])
    if crop_not_scale:
        offsets = [int((image.shape[shape_dim] - min_size) / 2) for image in images] 
        if height_not_width:
            new_images = [image[offset : offset + min_size, :] for offset, image in zip(offsets, images)]
        else: 
            new_images = [image[:, offset : offset + min_size] for offset, image in zip(offsets, images)]
    else:
        scale_factors = [min_size/image.shape[shape_dim] for image in images]
        new_images = [cv2.resize(image, dsize=None, fx=scale_factor, fy=scale_factor) for (scale_factor, image) in zip(scale_factors, images)] 
    for image in new_images:
        print(image.shape)       
    return new_images 

def create_image(height, width):
    new_image = numpy.zeros((int(height), int(width), 3), numpy.uint8)
    return new_image

def save_image(filename, image):
    #cv2.imshow('img-windows', image)
    #cv2.waitKey(0)
    filename_path = os.path.expanduser('~/Desktop/' + filename + '.jpg')
    print(filename_path)
    cv2.imwrite(filename_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), IMWRITE_JPEG_QUALITY])        

def concatenate_images(images, horizontally_not_vertically, same_images_size, width_white_pc = .05):   
    new_images = size_same(images,     height_not_width=horizontally_not_vertically, crop_not_scale=False)
    if same_images_size:
        new_images = size_same(new_images, height_not_width=(not horizontally_not_vertically), crop_not_scale=True)
    if horizontally_not_vertically:
        dim_same_size = 0
    else:
        dim_same_size = 1
    same_size = new_images[0].shape[dim_same_size]
    print(same_size)
    qty_images = len(new_images)
    sum_images_diff_sizes=0
    for image in new_images:
        sum_images_diff_sizes += image.shape[1 - dim_same_size]
    if horizontally_not_vertically:   
        width_white = int(sum_images_diff_sizes / (1. - width_white_pc * (qty_images - 1)) * width_white_pc)
    else:
        width_white = int(same_size * width_white_pc)
    print(width_white)    
    total_new_size = width_white * (qty_images - 1) + sum_images_diff_sizes
    print(total_new_size)    
    
    if horizontally_not_vertically:
        big_image = create_image(same_size, total_new_size)
    else:
        big_image = create_image(total_new_size, same_size)        
    big_image.fill(255)
    print(big_image.shape)    
    
    counter=0
    for image in new_images:
        add_size = image.shape[1 - dim_same_size]
        print(counter, (counter + add_size))
        print(image.shape)
        if horizontally_not_vertically:
            big_image[:, counter : (counter + add_size)] = image
        else:
            big_image[counter : (counter + add_size), :] = image
        counter += add_size + width_white
    cv2.imshow('img-windows', big_image)    
    cv2.waitKey(0)
    return big_image

def crop_concatenate_resize(urls, filename, cropped_size, final_width):
    cropped_images = [image_crop_square(img = url_to_image(url), new_size = cropped_size) for url in urls]      
    big_image = concatenate_images(cropped_images, horizontally_not_vertically = True, same_images_size = True, width_white_pc = 0)  
    
    _, width, _ = big_image.shape          
    resize_factor = final_width / width
    small = cv2.resize(big_image, (0,0), fx = resize_factor, fy = resize_factor)
    
    save_image(filename, small)       

if __name__ == '__main__':
    mfas = [# [950, "http://mfas3.s3.amazonaws.com/objects/SC246818.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246819.jpg", "stater-of-taras-tarentum-with-horse-and-rider-struck-under-philokles-955"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246826.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246827.jpg", "stater-of-taras-tarentum-with-horse-and-rider-struck-under-aristokles-960"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246810.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246811.jpg", "stater-of-taras-tarentum-with-horse-and-rider-951"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246382.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246383.jpg", "stater-of-taras-tarentum-with-rider-vaulting-from-horse-942"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246384.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246385.jpg", "stater-of-taras-tarentum-with-rider-vaulting-from-horse-943"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246802.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246803.jpg", "stater-of-taras-tarentum-with-warrior-on-horseback-crowned-by-victory-struck-under-kallikrates-885"], 
            # [850, "http://mfas3.s3.amazonaws.com/objects/SC255772.jpg", "http://mfas3.s3.amazonaws.com/objects/SC255773.jpg", "stater-of-kelenderis-with-youth-riding-horse-2761"], 
            # [850, "http://mfas3.s3.amazonaws.com/objects/SC251597.jpg", "http://mfas3.s3.amazonaws.com/objects/SC251598.jpg", "drachm-of-aspendos-with-horseman-hurling-spear-3297"], 
            # [800, "http://mfas3.s3.amazonaws.com/objects/SC253370.jpg", "http://mfas3.s3.amazonaws.com/objects/SC253371.jpg", "stater-of-kyzikos-with-horse-and-rider-above-tunny-fish-3299"], 
            # [950, "http://mfas3.s3.amazonaws.com/objects/SC246411.jpg", "http://mfas3.s3.amazonaws.com/objects/SC246410.jpg", "nommos-of-taras-tarentum-with-horse-and-rider-2945"], 
            # [850, "http://mfas3.s3.amazonaws.com/objects/SC250984.jpg", "http://mfas3.s3.amazonaws.com/objects/SC250985.jpg", "stater-of-pherai-with-head-of-hekate-struck-under-alexander-4050"], 
            # [650, "http://ikmk.smb.museum/mk-edit/images/n32/32837/vs_org.jpg", "http://ikmk.smb.museum/mk-edit/images/n32/32837/rs_org.jpg", "ikmk-18231388"], 
            # [650, "http://ikmk.smb.museum/mk-edit/images/n0/593/vs_org.jpg", "http://ikmk.smb.museum/mk-edit/images/n0/593/rs_org.jpg", "ikmk-18200577"], 
            # [650, "http://ikmk.smb.museum/mk-edit/images/n0/589/vs_org.jpg", "http://ikmk.smb.museum/mk-edit/images/n0/589/rs_org.jpg", "ikmk-18200575"], 
            # [650, "http://ikmk.smb.museum/mk-edit/images/n52/52943/vs_org.jpg", "http://ikmk.smb.museum/mk-edit/images/n52/52943/rs_org.jpg", "ikmk-18250633"], 
            # [650, "http://ikmk.smb.museum/mk-edit/images/n15/15012/vs_org.jpg", "http://ikmk.smb.museum/mk-edit/images/n15/15012/rs_org.jpg", "ikmk-18214934"], 
            # [850, "http://mfas3.s3.amazonaws.com/objects/SC251695.jpg", "http://mfas3.s3.amazonaws.com/objects/SC251696.jpg", "trihemidrachm-of-corinth-with-bellerophon-riding-pegasos-1451"], 
            # [850, "http://mfas3.s3.amazonaws.com/objects/SC269208.jpg", "http://mfas3.s3.amazonaws.com/objects/SC269209.jpg", "coin-of-thyatira-with-bust-of-severus-alexander-struck-under-mar-pollianus-264438"], 
            # [1200, "http://mfas3.s3.amazonaws.com/objects/SC266375.jpg", "http://mfas3.s3.amazonaws.com/objects/SC266376.jpg", "coin-of-corinth-with-head-of-aphrodite-struck-under-q-caecilius-niger-and-c-heius-pamphilus-259879"], 
            # [800, "http://mfas3.s3.amazonaws.com/objects/SC251274.jpg", "http://mfas3.s3.amazonaws.com/objects/SC251275.jpg", "drachm-of-kibyra-with-head-of-youth-3507"], 
            # [650, "", "", "ikmk-"], 
            # [950, "", "", ""], 
            
            ]

    # for mfa in mfas:
    #    crop_concatenate_resize(urls = mfa[1:-1], filename = mfa[-1], cropped_size = mfa[0], final_width = 1024)
    
    images = [url_to_image('http://www.yu51a5.com/wp-content/uploads/horsemen/' + fn) for fn in ['AN00149889_001_l.jpg',
                                                                                   'AN00150545_001_l.jpg',
                                                                                   'AN00150544_001_l.jpg']]
    concatenate_images(images, horizontally_not_vertically = False, same_images_size = True, width_white_pc = .05)
 

