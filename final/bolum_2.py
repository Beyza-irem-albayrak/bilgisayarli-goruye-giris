import cv2
import numpy as np
import os
from glob import glob

# AYARLAR
num_questions = 20
choices = ['A', 'B', 'C', 'D', 'E']
bubble_radius = 10
bubble_spacing = 41
start_x = 98
start_y = 197
line_spacing = 50


# Balon Pozisyonları
def get_bubble_positions():
    positions = []
    for i in range(num_questions):
        y = start_y + i * line_spacing
        row = []
        for j in range(len(choices)):
            x = start_x + j * bubble_spacing
            row.append((x, y))
        positions.append(row)
    return positions

bubble_positions = get_bubble_positions()

# Cevap Anahtarını Oku
def read_answer_key(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"HATA: Cevap anahtarı {image_path} okunamadı!")
        return None
    answer_key = []
    for i, row in enumerate(bubble_positions):
        correct_choice = None
        for j, (x, y) in enumerate(row):
            roi = img[y-bubble_radius:y+bubble_radius, x-bubble_radius:x+bubble_radius]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            fill_ratio = cv2.countNonZero(thresh) / (thresh.shape[0] * thresh.shape[1])
            if fill_ratio > 0.45:
                correct_choice = choices[j]
        answer_key.append(correct_choice)
    return answer_key

# Öğrenci Formunu Değerlendir
def process_student_form(image_path, answer_key):
    img = cv2.imread(image_path)
    if img is None:
        print(f"HATA: {image_path} okunamadı!")
        return None
    filename = os.path.basename(image_path)
    student_id = filename.split('_')[1].split('.')[0]
    student_id = str(100000 + int(student_id))

    student_answers = []
    for i, row in enumerate(bubble_positions):
        chosen = None
        max_fill = 0
        for j, (x, y) in enumerate(row):
            roi = img[y-bubble_radius:y+bubble_radius, x-bubble_radius:x+bubble_radius]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            fill_ratio = cv2.countNonZero(thresh) / (thresh.shape[0] * thresh.shape[1])
            if fill_ratio > max_fill and fill_ratio > 0.4:
                max_fill = fill_ratio
                chosen = choices[j]
        student_answers.append(chosen)

    correct = 0
    wrong = 0
    blank = 0
    for student_ans, correct_ans in zip(student_answers, answer_key):
        if student_ans is None:
            blank += 1
        elif student_ans == correct_ans:
            correct += 1
        else:
            wrong += 1

    return student_id, correct, wrong, blank

# === ANA PROGRAM ===
if __name__ == "__main__":
    cevap_yolu = "cevap_0000.png"  # Cevap anahtarı dosya adı
    form_yolu = "form_*.png"       # Öğrenci formları kalıbı

    answer_key = read_answer_key(cevap_yolu)
    if not answer_key:
        exit()

    print("📄 Cevap Anahtarı:", answer_key)

    form_dosyalar = sorted(glob(form_yolu))
    if not form_dosyalar:
        print("Hiç öğrenci formu bulunamadı!")
        exit()

    for path in form_dosyalar:
        result = process_student_form(path, answer_key)
        if result:
            student_id, correct, wrong, blank = result
            print(f"Öğrenci {student_id} → ✅ Doğru: {correct}, ❌ Yanlış: {wrong}, ⭕ Boş: {blank}")
