import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter

# 1. Gri tonlamalı (siyah-beyaz) görseli oku
gorsel = cv2.imread("evrak_1.jpg", cv2.IMREAD_GRAYSCALE)
if gorsel is None:
    raise FileNotFoundError("evrak.jpg bulunamadı!")

satir, sutun = gorsel.shape

# 2. Maske oluştur (belge dışını ayıklamak için)

x1, x2 = 136, 1481  # dikey sınırlar (üst-alt)
y1, y2 = 102, 1066   # yatay sınırlar (sol-sağ)

maske = np.zeros((satir, sutun), dtype=np.uint8)
maske[x1:x2, y1:y2] = 1

# 3. Maske uygula (arka planı siyah yap)
maske_uygulanmis = np.zeros_like(gorsel)
maske_uygulanmis[maske == 1] = gorsel[maske == 1]

# 4. Perspektif düzeltme için kaynak ve hedef noktalar
kaynak_noktalar = np.float32([
    [y1, x1],  # Sol üst
    [y2, x1],  # Sağ üst
    [y2, x2],  # Sağ alt
    [y1, x2]   # Sol alt
])

genislik = y2 - y1
yukseklik = x2 - x1

hedef_noktalar = np.float32([
    [0, 0],
    [genislik, 0],
    [genislik, yukseklik],
    [0, yukseklik]
])

# 5. Perspektif düzeltme uygula
donusum_matrisi = cv2.getPerspectiveTransform(kaynak_noktalar, hedef_noktalar)
duzeltilmis = cv2.warpPerspective(maske_uygulanmis, donusum_matrisi, (genislik, yukseklik))

# 6. Kontrastı artır (CLAHE yöntemi)
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
iyilestirilmis = clahe.apply(duzeltilmis)

# 7. Median filtre ile pürüzleri yumuşat
filtrelenmis = median_filter(iyilestirilmis, size=(3, 3))
sonuc = iyilestirilmis.copy()
sonuc[sonuc == 255] = filtrelenmis[sonuc == 255]

# 8. Görselleri göster
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

axs[0].imshow(maske_uygulanmis, cmap='gray')
axs[0].set_title("1. Maske Uygulandı (arka plan siyah)")
axs[0].axis('off')

axs[1].imshow(duzeltilmis, cmap='gray')
axs[1].set_title("2. Perspektif Düzeltildi")
axs[1].axis('off')

axs[2].imshow(sonuc, cmap='gray')
axs[2].set_title("3. Kontrast Artırıldı")
axs[2].axis('off')

plt.tight_layout()
plt.show()

# 9. Son görüntüyü kaydet
cv2.imwrite("output_final.jpg", sonuc)
