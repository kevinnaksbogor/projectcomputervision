import cv2
import pickle
import numpy as np  # Pastikan numpy diimpor

# Load daftar posisi parkir dari file
try:
    with open('ParkirPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []

dragging = False
drag_corner = -1
drag_index = -1
drag_offset = (0, 0)  # Offset untuk memindahkan seluruh kotak

# Fungsi untuk mendeteksi klik mouse
def mouseClick(events, x, y, flags, params):
    global dragging, drag_corner, drag_index, drag_offset

    if events == cv2.EVENT_LBUTTONDOWN:  # Klik kiri
        for i, corners in enumerate(posList):
            for j, (cx, cy) in enumerate(corners):
                if abs(cx - x) < 10 and abs(cy - y) < 10:  # Deteksi sudut yang diklik
                    dragging = True
                    drag_index = i
                    drag_corner = j
                    break
            if dragging:
                break
            # Jika klik di dalam area kotak
            if cv2.pointPolygonTest(np.array(corners, np.int32), (x, y), False) >= 0:
                dragging = True
                drag_index = i
                drag_corner = -1  # Tidak ada sudut spesifik, memindahkan kotak
                drag_offset = (x, y)
                break
        else:
            # Tambahkan kotak baru
            new_box = [(x, y), (x + 110, y), (x + 110, y + 42), (x, y + 42)]
            posList.append(new_box)

    elif events == cv2.EVENT_MOUSEMOVE:  # Gerakkan kotak atau sudut
        if dragging and drag_index != -1:
            if drag_corner != -1:  # Gerakkan sudut spesifik
                posList[drag_index][drag_corner] = (x, y)
            else:  # Pindahkan seluruh kotak
                dx = x - drag_offset[0]
                dy = y - drag_offset[1]
                posList[drag_index] = [(cx + dx, cy + dy) for cx, cy in posList[drag_index]]
                drag_offset = (x, y)

    elif events == cv2.EVENT_LBUTTONUP:  # Lepaskan klik kiri
        dragging = False
        drag_corner = -1
        drag_index = -1

    elif events == cv2.EVENT_RBUTTONDOWN:  # Klik kanan untuk menghapus kotak
        for i, corners in enumerate(posList):
            if cv2.pointPolygonTest(np.array(corners, np.int32), (x, y), False) >= 0:
                posList.pop(i)
                break

    # Simpan daftar posisi parkir ke file
    with open('ParkirPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    image_path = 'p1.jpeg'
    img_original = cv2.imread(image_path)
    img = cv2.resize(img_original, (1080, 720))

    # Gambar kotak parkir
    for corners in posList:
        points = np.array(corners, np.int32)
        cv2.polylines(img, [points], isClosed=True, color=(255, 0, 255), thickness=2)
        for (x, y) in corners:
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)
