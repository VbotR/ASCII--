import cv2
import os
import time
import sys
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image, width=80):
    """
    Преобразует изображение в ASCII-графику.
    """
    try:
        if image is None or image.size == 0:
            raise ValueError("Кадр пустой или имеет некорректный размер.")
        height, orig_width = image.shape[:2]
        if orig_width == 0 or height == 0:
            raise ValueError("Некорректный размер кадра: ширина или высота равна 0.")
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        aspect_ratio = height / orig_width
        new_height = int(aspect_ratio * width * 0.55)
        image = cv2.resize(image, (width, new_height))
        ascii_str = "".join([ASCII_CHARS[pixel // 25] for pixel in image.flatten()])
        ascii_img = "\n".join([ascii_str[i:i+width] for i in range(0, len(ascii_str), width)])
        return ascii_img
    except Exception as e:
        print(f"Ошибка при преобразовании кадра в ASCII: {e}")
        return ""

def play_ascii_animation_from_file(file_path, delay=0.1, loop=True):
    """
    Воспроизводит сохранённое ASCII-видео из файла.
    """
    try:
        with open(file_path, "r") as f:
            data = f.read().split("\n===FRAME===\n")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return

    try:
        while True:  # Цикличное воспроизведение
            for frame in data:
                os.system("cls" if os.name == "nt" else "clear")
                print(frame)
                time.sleep(delay)
            if not loop:
                break
    except KeyboardInterrupt:
        print("\nАнимация остановлена пользователем.")

def video_to_ascii(video_path, output_folder="ascii_frames", width=80, fps=10):
    """
    Преобразует видео в серию ASCII-кадров.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Не удалось открыть видео: {video_path}")
    
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    if frame_rate <= 0:
        frame_rate = fps
    frame_interval = max(1, frame_rate // fps)

    frame_count = 0
    ascii_frame_count = 0

    all_frames = []  

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame is not None:
            print(f"Обработка кадра {frame_count}: Размеры кадра {frame.shape}")
        else:
            print(f"Пропущен кадр {frame_count}: Пустой или повреждённый кадр.")
            frame_count += 1
            continue

        if frame_count % frame_interval == 0:
            try:
                ascii_art = image_to_ascii(frame, width=width)
                if ascii_art:
                    all_frames.append(ascii_art)
                    ascii_frame_count += 1
            except Exception as e:
                print(f"Ошибка при обработке кадра {frame_count}: {e}")
        frame_count += 1

    cap.release()
    return all_frames

def main_menu():
    while True:
        print("\nASCII-аниматор")
        print("1. Преобразовать видео в ASCII")
        print("2. Воспроизвести сохранённое ASCII-видео")
        print("3. Посмотреть демо-видео")
        print("4. Выйти")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            video_path = input("Введите путь к вашему видео: ").strip()
            output_folder = "ascii_frames"
            try:
                print("Обработка видео...")
                all_frames = video_to_ascii(video_path, output_folder)
                save_option = input("Сохранить результат в файл для воспроизведения? (y/n): ").strip().lower()
                if save_option == 'y':
                    with open("ascii_video.txt", "w") as f:
                        f.write("\n===FRAME===\n".join(all_frames))
                    print("Результат сохранён в ascii_video.txt.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
            finally:
                if os.path.exists(output_folder):
                    for file in os.listdir(output_folder):
                        os.remove(os.path.join(output_folder, file))
                    os.rmdir(output_folder)
        elif choice == "2":
            file_path = input("Введите путь к файлу с ASCII-видео: ").strip()
            play_ascii_animation_from_file(file_path, loop=True)  # Цикличное воспроизведение
        elif choice == "3":
            demo_file = "ascii_demo_video.txt"
            if os.path.exists(demo_file):
                print("Воспроизведение демо-видео...")
                play_ascii_animation_from_file(demo_file, loop=True)  # Цикличное воспроизведение демо
            else:
                print(f"Демо-видео {demo_file} не найдено.")
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
