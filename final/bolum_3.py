import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import label2rgb
from scipy.ndimage import binary_closing, binary_fill_holes
from skimage.morphology import remove_small_objects, disk

# 1. Görüntüyü oku ve RGB form
# atına çevir
görüntü = cv2.imread("taneli_30.jpg")
görüntü_rgb = cv2.cvtColor(görüntü, cv2.COLOR_BGR2RGB)
plt.figure(), plt.imshow(görüntü_rgb), plt.title("1. Orijinal Görüntü"), plt.axis("off")

# 2. HSV renk uzayına dönüştür
hsv = cv2.cvtColor(görüntü, cv2.COLOR_BGR2HSV)
h = hsv[:, :, 0] / 180.0 
s = hsv[:, :, 1] / 255.0 
v = hsv[:, :, 2] / 255.0  

# 3. Turuncu renk için eşikleme
renk_maske = (h > 0.03) & (h < 0.10)
doygunluk_maske = s > 0.4
parlaklık_maske = v < 0.95
maske = renk_maske & doygunluk_maske & parlaklık_maske

# 4. Morfolojik işlemlerle temizleme
maske = remove_small_objects(maske, min_size=30)
maske = binary_closing(maske, structure=disk(3))
maske = binary_fill_holes(maske)

plt.figure(), plt.imshow(maske, cmap='gray'), plt.title("2. Maske Sonucu"), plt.axis("off")

# 5. Bağlı bileşenleri etiketle
etiketli = label(maske)
tane_sayısı = etiketli.max()
özellikler = regionprops(etiketli)

# 6. Tane sayısını yazdır
print(f"Tespit edilen tane sayısı: {tane_sayısı}")

# 7. Görselleştirme
renkli_etiket = label2rgb(etiketli, image=görüntü_rgb, bg_label=0)
plt.figure(), plt.imshow(renkli_etiket), plt.title("3. Etiketlenmiş Taneler"), plt.axis("off")

for i, özellik in enumerate(özellikler):
    y, x = özellik.centroid
    plt.text(x, y, str(i+1), color='red', fontsize=12)

plt.tight_layout()
plt.show()
