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
    print(filename)
    if is_in_user_folder(filename):
        image = cv2.imread(filename)
    else:
        url = filename
        request = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(request).read()
        image = numpy.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR) 
    # return the image
    print(image.shape)
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
    new_image = cv2.resize(image, None, fx = 1./resize_factor, fy = 1./resize_factor)      
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

    """     all_fns = [['AN00149889_001_l.jpg', 'AN00150545_001_l.jpg', 'AN00150544_001_l.jpg'],
               ['AN00472211_001_l.jpg', 'AN00472213_001_l.jpg'],
               ['KK_6025_01.jpg', 'KK_6754_01.jpg', 'KK_6753_01.jpg', 'KK_6020_13168.jpg']]
    cover_filename = 'headlessHorsemen'
    all_fns = [ [os.path.expanduser('~/Desktop/Screenshot 2020-04-20 at 21.51.48.png')], 
                ['7818_Kelly-Tan-iPhone-Photos-9_w1120.jpg']]
    cover_filename = 'motivation' 
    all_fns = [ ['Alexander_the_Great_mosaic.jpg', 'image04123.jpg'], 
                ['Battle_of_the_Milvian_Bridge_by_Giulio_Romano_1520-24.jpg'], 
                ['tapisserie_de_bayeux_1.png'],
                ['Lomonosov_Poltava_1762_1764.jpg', 'Louis_XVI_roi_citoyen.png']]
    cover_filename = 'pivotal'

    all_fns = [ ['20493560.jpeg', 'AN00134115_001_l.jpg', 'DP857126.jpg'], 
                ['henri_iv_roi_de_france_bd.jpg', '850px-Velazquez_-_Principe_Baltasar_Carlos_Museo_del_Prado_1634-35.jpg', 'August_der_Starke.jpg'],
                ['bonhams.jpeg', '841px-Sir_Joshua_Reynolds_-_Sir_Jeffrey_Amherst_-_Google_Art_Project.jpg', 'Francisco_de_Goya_-_Retrato_ecuestre_de_Fernando_VII_-_Google_Art_Project.jpg']]
    cover_filename = 'symbol' 

    all_fns = [ ['AN00038779_001_l.jpg','257182-1330624364.jpg','Budapest_Rearing_Horse.png'], 
                ['UN_GoodDefeats-Evil_StGeorge.jpg', 'Bronze_equestrian_statue_of_Don_Juan_de_Onate_Salazar_by_John_Sherrill_Houser_El_Paso_International_Aitport_2006.jpg'], 
                ['5c895100b81a771347b3655a007fa6fa.jpg', 'Macedonia_Square_Skopje_NMK.jpg'],
                ['shivajimemorialconcepte.jpg'],
                ['AN00297125_001_l-1.jpg', 'Leopold_V_Archduke_of_Austria_-_Innsbruck.jpg','1024px-Jackson_Statue_in_DC.jpg']]
    cover_filename = 'technology' 

    all_fns = [['AN00431083_001_l-1.jpg','AlexanderSarcophaguslionhunt.jpg'],
               ['Bellerophon_Autun.jpg','sasson_75.jpg','holy_rider.png'],
               ['96-004222.jpg','St_Dmitrij_03.jpg','Santiago_a_caballo.jpg','Yuhanna-Mercurius.jpg'],
               ['863px-Carlos_V_en_Muehlberg_by_Titian_from_Prado_in_Google_Earth.jpg','Goltzius_MarcusCurtius_Christies.png','goldenhorseman.jpg', '866px-Jacques_Louis_David_-_Bonaparte_franchissant_le_Grand_Saint-Bernard_20_mai_1800_-_Google_Art_Project.jpg'],
               ['bronze-horseman.jpg','1024px-Jackson_Statue_in_DC.jpg','Rani-Jhansi-Statue-installed1.jpg']
               ]
    cover_filename = 'genealogy'
    
    all_fns = [['04-007446.jpg','WOA_IMAGE_const.jpg','143a7046fb3354a9333dea57a8b82377.jpg'],
               ['Pierre_Mignard_-_Ludwig_XVI._zu_Pferde_-_hi_res_1200dpi.jpg','2006BB2180_jpg_l.jpg','864px-Buffi_-_Equestrian_portrait_of_Marie_Jeanne_of_Savoy-Nemours_-_Palazzo_Madama.jpg'],
               ['Frederik_Hendrik_and_Maurits_as_generals_by_Thomas_Willeboirts_Bosschaert.jpg', 'John_Churchill_1st_Duke_of_Marlborough_by_Sir_Godfrey_Kneller_Bt_2.jpg','Johann_Gottfried_Tannauer_03.jpg'],
               ]
    cover_filename = 'victory'

    all_fns = [['44668089.jpeg',os.path.expanduser('~/Downloads/tsipori-palestine-ca-4th.jpg')],
               ['Aleksandrovo_kurgan.jpg'],
               ['King_John_hunting_-_Statutes_of_England_14th_C_f.116_-_BL_Cotton_MS_Claudius_D_II.jpg', 'Gaston_Phoebus_2.jpg'],
               ['Hunt_in_the_forest_by_paolo_uccello.jpg']
               ]
    cover_filename = 'hunting'

    all_fns = [['499182.jpg','776px-Count-Duke_of_Olivares.jpg','850px-Rubens_-_San_Jorge_y_el_Dragon_Museo_del_Prado_1605.jpg'],
               ['Santiago_Matamoro_Cordoba_Spain.jpeg','7P5M2591.jpg','83K97084.jpg'],
               ['Gonzales_Coques_-_An_equestrian_portrait_of_an_elegant_gentleman_and_lady_in_a_wooded_landscape.jpg','1275px-Peter_Paul_Rubens_110.jpg','La_Bataille_dIssus_-_Jan_Brueghel.jpeg'],
               ['Louis_XIII_Richelieu_devant_La_Rochelle.jpg','Madame_La_Comtesse_de_Saint_Geran.jpg','866px-Jacques_Louis_David_-_Bonaparte_franchissant_le_Grand_Saint-Bernard_20_mai_1800_-_Google_Art_Project.jpg'],
               ['August_der_Starke.jpg','augustus-iii.jpg','fig.-3-archduke-maximilian-ii-emanuel-of-baveria-by-roger-schabol-signed-and-dated-1707-after-a-design-by-desjardin-1.jpg'],
               ['Leopold_V_Archduke_of_Austria_-_Innsbruck.jpg','KK_968_12844.jpg','KK_4663_57604.jpg'],
               ['167167-1297701516.jpg','James_Scott.jpg','673px-Britain_Needs_You_at_Once_-_WWI_recruitment_poster_-_Parliamentary_Recruiting_Committee_Poster_No._108.jpg'],
               ['Equestrian_portrait_of_Alexis_of_Russia_17_c_GIM.jpg','Allegory_of_the_Victory_at_Poltava._Apotheosis_of_Peter_I.jpg','0_113499_f752414e_orig.jpg']
               ]
    cover_filename = 'part3'
    all_fns = [[,,],
               [,,],
               [,,],
               [,,],
               [,,],
               [,,],
               [,,],
               [,,],
               ]
    cover_filename = ''
    """
    
    all_fns = [['aabar-harema.jpg','AN00032649_001_l.jpg','AN00313723_001_l.jpg'],
               ['AN00431083_001_l-1.jpg','20131205_Istanbul_106.jpg','Tetradrachm_Evagoras_II_368-346BC.jpg'],
               ['Pittore_di_amphiaraos_gruppo_pontico_oinochoe_etrusca_con_cavalieri_al_galoppo_dalla_177_della_necr._dellosteria_540-510_ac_ca.jpg','de86d6162f2358da8191a446f9fe1ea8.jpg','d8c292099ae2528c989114fb3acece55.jpg'],
               ['00-008264.jpg','MANF1999_99_101_SEQ_001_P.jpg','SC47844.jpg'],
               ['article-2676413-1F4CE2CB00000578-295_634x430.jpg','44668089.jpeg','AN00274931_001_l.jpg'],
               ['EstelaFunerariaConCombateNoroesteDeAtenasSigloIVAC.jpg','gods_jul08_5.jpg__600x0_q85_upscale.jpg','The-Merrin-Gallery-Terracotta-Rider-Canosan-Hellenistic-Periodca-323-BC.jpeg'],
               ['WOA_IMAGE_comb.jpg','Cavaler_Trac_Stara_Zagora_IMG_8671_02.jpg','4082479429_f57aed4e0a_o.jpg'],
               ['22.jpg','Stele_funeraire_du_soldat_Comnisca_sept_2013_01.jpg','fcc6a2fc50c8d4ce4ece0357a745caea.jpg'],
               ['Meleagrus-Hunt.jpg','tenma-01.jpg','603px-British_Airborne_Units.svg_.png'],
               ['06xx_Jagdschale_m._sasanidischem_Grosskoenig_Iran_7._Jht._anagoria.jpg','279383001.jpg','spp290_horse_rider_statuette.png'],
               ['86-005013.jpg','Barb372-100.png','medal.png'],
               ['Chanter_Angelos_Akotandos_-_St_George_on_Horseback_Slaying_the_Dragon_-_Google_Art_Project.jpg','Wooden_S.George_15th_c._Rostov_Kremlin_by_shakko_02.jpg','Saint_Demetrius_bulgarian_icon.jpg'],
               ['st-george-xi-cent-svaneti-museum.jpg','813px-St_George_Georgia_15th_c.jpg','Tbilisi_StGeorge.jpg'],
               ['Susenyos_Wellcome_L0031387_cropped.jpg','Yuhanna-Mercurius.jpg','The_death_of_Absalom6.jpg'],
               ['B_Valladolid_93.jpg','Second_Horseman_Battistero_di_Padova.jpg','John_Hamilton_Mortimer_-_Death_on_a_Pale_Horse_-_Google_Art_Project.jpg'],
               ]
    cover_filename = 'part1'
    
    make_image_grid(filenames = all_fns, 
                    result_filename = 'horsemen_' + cover_filename + '_cover', 
                    default_url = 'http://www.yu51a5.org/wp-content/uploads/horsemen/')
