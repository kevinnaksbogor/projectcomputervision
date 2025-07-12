import cv2
import pickle
import cvzone
import numpy as np

# Load gambar
image_path = 'p1.jpeg'
img_original = cv2.imread(image_path)
if img_original is None:
    raise FileNotFoundError(f"Gambar '{image_path}' tidak ditemukan.")

img = cv2.resize(img_original, (1080, 720))

# Load posisi parkir
try:
    with open('ParkirPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError("File 'ParkirPos' tidak ditemukan. Jalankan PemilihParkir.py terlebih dahulu untuk menentukan posisi parkir.")
except EOFError:
    posList = []  # Jika file kosong, gunakan daftar kosong

# Preprocessing gambar
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 25, 16)
imgMedian = cv2.medianBlur(imgThreshold, 5)
kernel = np.ones((3, 3), np.int8)
imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

# Fungsi untuk memeriksa slot parkir dan menampilkan jumlah piksel non-zero
def checkSlot(imgPro):
    for corners in posList:
        # Konversi sudut menjadi array NumPy untuk operasi lebih mudah
        points = np.array(corners, np.int32)

        # Dapatkan area crop berdasarkan koordinat minimum dan maksimum
        x_min = min(pt[0] for pt in corners)
        y_min = min(pt[1] for pt in corners)
        x_max = max(pt[0] for pt in corners)
        y_max = max(pt[1] for pt in corners)
        imgCrop = imgPro[y_min:y_max, x_min:x_max]

        # Hitung jumlah piksel non-zero
        count = cv2.countNonZero(imgCrop)

        # Tentukan warna berdasarkan jumlah piksel
        color = (0, 255, 0) #if count < 500 else (0, 0, 255)

        # Gambar kotak dan jumlah piksel pada gambar utama
        cv2.polylines(img, [points], isClosed=True, color=color, thickness=2)
        cv2.putText(img, str(count), (x_min + 25, y_min + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


# Panggil fungsi untuk memeriksa slot parkir
checkSlot(imgDilate)

# Tampilkan hasil
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", img)
#cv2.imshow("ImageBlur", imgBlur)
#cv2.imshow("ImageThres", imgThreshold)
#cv2.imshow("ImageDilate", imgDilate)
cv2.waitKey(0)
cv2.destroyAllWindows()
