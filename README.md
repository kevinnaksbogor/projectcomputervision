# Library yang digunakan

OpenCV | pip install opencv-python

cvzone | pip install cvzone

NumPy | pip install numpy

PyExcel | pip install openpyxl

# Cara Penggunaan

1. Run program PemilihParkir.py dan atur kotak sesuai dengan kotak parkir
2. Run program main.py untuk melihat hasil

Informasi lainnya:
1. Jika ingin mengganti gambar, ubah nama pada `image_path` pada main.py sesuai dengan nama file gambar (dengan format ekstensinya)
2. Untuk mengganti threshold, ubah nilai pada file main.py pada bagian Status slot parkir bagian `if count < x:` sesuai yang diinginkan. Threshold tersebut merupakan nilai piksel yang dideteksi. Jika lebih kecil maka slot parkir dianggap kosong, jika lebih besar dianggap terisi
3. PixelThresh.py digunakan untuk melihat jumlah pixel untuk mendapatkan angka threshold
4. File `ParkirPos` berisi koordinat dari kotak - kotak yang telah di atur. Untuk membuat file ParkirPos yang baru untuk menggunakan gambar lain, ubah nama `ParkirPos` pada PemilihParkir.py dan main.py menjadi nama lain, contoh ParkirPos1
5. File `StatusParkirUPI.xlsx` berisi data status parkir apakah Terisi atau Kosong berdasarkan dari kotak yang telah diatur
