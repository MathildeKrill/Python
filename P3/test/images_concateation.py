import codecs
import re, sys
import numpy, cv2, os
import urllib.request

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
IMWRITE_JPEG_QUALITY = 95
DEFAULT_WIDTH_WHITE_PC = .02
DEFAULT_SHRINK_SIZE = 1200

def is_in_user_folder(filename):
    return filename.startswith(os.path.expanduser('~/'))

def add_url_if_necessary(filename, url_path):
    if is_in_user_folder(filename):
        return filename
    if filename.startswith('http'):
        return filename
    return url_path + filename
 
def filename_to_image(filename):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    if is_in_user_folder(filename):
        image = cv2.imread(filename)
    else:
        url = filename
        request = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(request).read()
        image = numpy.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR) 
    # return the image
    return image

def image_crop_square(img, new_size):
    height, width, _ = img.shape
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
    return new_images 

def create_image(height, width):
    new_image = numpy.zeros((int(height), int(width), 3), numpy.uint8)
    return new_image

def save_image(filename, image):
    #cv2.imshow('img-windows', image)
    #cv2.waitKey(0)
    filename_path = os.path.expanduser('~/Desktop/' + filename + '.jpg')
    cv2.imwrite(filename_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), IMWRITE_JPEG_QUALITY])        

def concatenate_images(images, horizontally_not_vertically, same_images_size, width_white_pc = DEFAULT_WIDTH_WHITE_PC):   
    new_images = size_same(images,     height_not_width=horizontally_not_vertically, crop_not_scale=False)
    if same_images_size:
        new_images = size_same(new_images, height_not_width=(not horizontally_not_vertically), crop_not_scale=True)
    if horizontally_not_vertically:
        dim_same_size = 0
    else:
        dim_same_size = 1
    same_size = new_images[0].shape[dim_same_size]
    qty_images = len(new_images)
    sum_images_diff_sizes=0
    for image in new_images:
        sum_images_diff_sizes += image.shape[1 - dim_same_size]
    if horizontally_not_vertically:   
        width_white = int(sum_images_diff_sizes / (1. - width_white_pc * (qty_images - 1)) * width_white_pc)
    else:
        width_white = int(same_size * width_white_pc)
    total_new_size = width_white * (qty_images - 1) + sum_images_diff_sizes
    
    if horizontally_not_vertically:
        big_image = create_image(same_size, total_new_size)
    else:
        big_image = create_image(total_new_size, same_size)        
    big_image.fill(255)
    
    counter=0
    for image in new_images:
        add_size = image.shape[1 - dim_same_size]
        if horizontally_not_vertically:
            big_image[:, counter : (counter + add_size)] = image
        else:
            big_image[counter : (counter + add_size), :] = image
        counter += add_size + width_white
    return big_image

def shrink(image, max_width = -1, max_height = -1):
    height, width, _ = image.shape
    resize_factor = 1
    if width > max_width and max_width > 0:
        resize_factor = width / max_width
    if max_height > 0:
        if resize_factor < (height / max_height):
            resize_factor = (height / max_height)
    if resize_factor < (1 - 1e-6):
        return image
    print (image.shape)      
    new_image = cv2.resize(image, None, fx = 1./resize_factor, fy = 1./resize_factor)
    print (new_image.shape)      
    return new_image

def crop_concatenate_resize(urls, filename, cropped_size, final_width):
    cropped_images = [image_crop_square(img = filename_to_image(url), new_size = cropped_size) for url in urls]      
    big_image = concatenate_images(cropped_images, horizontally_not_vertically = True, same_images_size = True, width_white_pc = 0)  
    small = shrink(image = big_image, max_width = final_width)    
    save_image(filename, small)      

def make_image_grid(filenames, result_filename, default_url, shrink_size = DEFAULT_SHRINK_SIZE):
    filenames_with_path = [[add_url_if_necessary(fn, default_url) for fn in fns] for fns in all_fns]
    images = [[filename_to_image(fn) for fn in fns] for fns in filenames_with_path]
    big_images = [concatenate_images(images_row, 
                                     horizontally_not_vertically = True, 
                                     same_images_size = True) for images_row in images]
    big_image_2 = concatenate_images(big_images, 
                                     horizontally_not_vertically = False, 
                                     same_images_size = False)
    final_image = shrink(big_image_2, DEFAULT_SHRINK_SIZE)
    save_image(filename = result_filename, image = final_image) 

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
    
    # all_fns = [['AN00149889_001_l.jpg', 'AN00150545_001_l.jpg', 'AN00150544_001_l.jpg'],
    #            ['AN00472211_001_l.jpg', 'AN00472213_001_l.jpg'],
    #            ['KK_6025_01.jpg', 'KK_6754_01.jpg', 'KK_6753_01.jpg', 'KK_6020_13168.jpg']]
    # cover_filename = 'headlessHorsemen'
    all_fns = [ [os.path.expanduser('~/Desktop/Screenshot 2020-04-20 at 21.51.48.png')], 
                ['7818_Kelly-Tan-iPhone-Photos-9_w1120.jpg']]
    cover_filename = 'motivation'

    make_image_grid(filenames = all_fns, 
                    result_filename = 'horsemen_' + cover_filename + '_cover', 
                    default_url = 'http://www.yu51a5.org/wp-content/uploads/horsemen/')

    # ids = [18207157] 18202573, 18201481]# , 18204280, 18201471, 18236941, 18236949, 18230064, 18219808, 18236701, 18201473, 18204280, 18204280,
    # 18232830, 18220883, 18250418, 18236701, 18201363, 18201547, 18201832, 18201843, 18206785, 18202573, 18231792]
    # for id in ids:
    #     url_beginning = 'https://ikmk.smb.museum/image/' + str(id) + '/'
    #     urls = [url_beginning + 'vs_exp.jpg', url_beginning + 'rs_exp.jpg']
    #     double_image_big = concatenate_images([filename_to_image(a_url) for a_url in urls], 
    #                                           horizontally_not_vertically = True, 
    #                                           same_images_size = False)
    #     double_image = shrink(double_image_big, max_width=1024)
    #     save_image(filename = 'ikmk_coin_' + str(id), image = double_image)
    #     print('insert_into_images("horsemen/ikmk_coin_{:n}.jpg", \n\
    #                         "ikmk", \n\
    #                         "{:n}", \n\
    #                         " showing  on horseback on reverse, <br/>minted in  under , Roman Republic Empire");'.format(id, id));

#     file_path = os.path.expanduser('~/Downloads/Officers Expense Claim Form/Sheet1.html')                      
#     my_encoding = 'utf-8'
#     with codecs.open(file_path, encoding = my_encoding) as file_opened:
#         file_contents = file_opened.read()
#                
#     n=1             
#     for match in re.finditer(pattern = 'img src=\'(.*?)[\'\;]', string = file_contents): #/\<img src=/
#         a_url = match.group(1)
#         print(a_url)
#           
#         try:
#             an_image = url_to_image(a_url)
#             print('ok')
#         except:
#             print('---NOT OK')
#         if n<10:
#             str_n = '0' + str(n)
#         else:
#             str_n = str(n)
#         save_image(filename = 'mensa_expenses_' + str_n, image = an_image)
#         n=n + 1

