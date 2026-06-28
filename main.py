import argparse
import hashlib
import os
import shutil
from collections import defaultdict
from pathlib import Path

folder_path = Path()
folder_delete = Path('C:\\Users\\адм\\Desktop\\sensory_profile_app\\test_data\\for del')
file_names = []
hash_files = {}
# for file_name in os.listdir(folder_path):
#     if os.path.isfile(os.path.join(folder_path, file_name)):
#         file_names.append(file_name)
parser = argparse.ArgumentParser(description='Утилита, перемещает дубликаты файлов '\
        'в отдельную папку и удаляет по запросу пользователя')
parser.add_argument("--path", required=True,
                        help='Путь к папке на проверку дубликатов')
parser.add_argument('--action',
                        choices=['dry-run', 'del', 'move'],
                        default='dry-run')

args = parser.parse_args()
    
def main():
    
    init_action(args.path)
    #init_path()

    

    # # validate_hash(all_files, hash_files)
    # move_duplicates_in_folder()
    # delete_duplicate(folder_delete)


def generate_hash(file):
    #print(f"Генерация хэша для файла: {file}")
    h = hashlib.sha256()
    with open(file, "rb") as f:
        while chunk := f.read(65536):   # 64 КБ за раз
            h.update(chunk)
    digest = h.hexdigest()
    #print("Хэш заверен")
    #print()

    return digest

def checkfiles(folder):
    folder = Path(folder)
    global hash_files
# Используем defaultdict для хранения хэшей и связанных файлов
    hash_files = defaultdict(list)
    for file_path in folder.rglob('*'):
        if '.venv' in file_path.parts or 'venv' in file_path.parts :
            continue  # Пропускаем папку .venv или venv

        if file_path.is_file():  # Проверяем, что это файл, а не папка
            #print('\n' .join(file_names))
            file_names.append(file_path)
            hashed = generate_hash(file_path)  # Генерируем хэш для файла
            hash_files[hashed].append(file_path)  # Добавляем файл в словарь по его хэшу

    return file_names

def validate_hash(file_name, hash_files):
    try:

        for file_hash, files in hash_files.items():
            if len(files) > 1:
                print(f"Найдены дубликаты для хэша {file_hash}:")
                for file in files:
                    file_names.append(file)
                    print(f" - {file}")

    except Exception as e:
        print(f"Произошла ошибка при проверке хэшей: {e}")

    print()
    
def init_action(folder_path):
    try:
        if not os.path.exists(folder_path):
            print(f"Папка {folder_path} не существует.")
            return
        checkfiles(folder_path)
        
        if args.action == 'dry-run':
            file_hash = find_duplicates(hash_files)
            
        elif args.action == 'move':
            dupl = find_duplicates(hash_files)
            move_duplicates_in_folder(dupl)
        elif args.action == 'del':
            dupl = find_duplicates(hash_files)
            folder = move_duplicates_in_folder(dupl)
            delete_duplicate(folder)
    except Exception as e:
        print(f"Произошла ошибка при выполнении действия: {e}")

def find_duplicates(hash_files):
    duplicates = []
    for file_hash, files in hash_files.items():
        if len(files) > 1:
            print(f"Найдены дубликаты для хэша {file_hash}:")
            sum_size = sum(file.stat().st_size for file in files)
            sum_mb = sum_size / (1024 * 1024)  # Конвертируем в мегабайты

            
            duplicates.append((file_hash, files, sum_size))
            for file in files:
                print(f" - {file}")
            print(f"Общий размер дубликатов: {sum_mb:.2f} МБ")
    return duplicates

def move_duplicates_in_folder(duplicates):
    new_name = ''
    i = 1
    
    print('------------------------------')
    print('Содержимое папки для удаления')
    print('------------------------------')
    dupl = find_duplicates(hash_files)
        

    for file_hash, files in dupl:
        print('------------------------------')
        print("перемещен в папку 'for del'")
        newest_file = max(files, key = lambda f: f.stat().st_mtime)



        # Оставляем первый файл, остальные удаляем
        for file in files:
            try:
                if file != newest_file:
                    os.makedirs(folder_delete, exist_ok=True)
                    dest = folder_delete / file.name
                    source_path = file
                    if dest.exists():
                        new_name = f"{file.stem}_{i}{file.suffix}"
                        dest = folder_delete / new_name
                        i += 1
                    else:
                        i = 1
                    shutil.move(source_path, dest)

                    print(f"Файл {file}")
                    #print(f"Удален дубликат: {file}")
            except Exception as e:
                print(f"Не удалось переместить файл {file}: {e}")
        print('------------------------------')
    return folder_delete


def delete_duplicate(folder):
    while True:

        if folder.exists() and os.listdir(folder):
            for item in os.listdir(folder):
                print(item)
        else:
            print()
            print('Папка пустая или ее несуществует!')
            return False
        answ = input("Дубликаты были перемещены в папку 'for del'."\
                     "Удалить дубликаты? y/n: ")
        try:
            if answ == 'y':

                try:
                    for file_path in folder.rglob('*'):
                        if file_path.is_file():
                            file_path.unlink()
                    print("Удаление завершено!")
                    return False
                except Exception as e:
                        print("Произошла ошибка при удалении: ", e)
                        return False
            elif answ == 'n':
                return False
            else:
                print("Введите правильное значение!")
                continue
        except Exception as e:
            print("Ошибка при удалении:", e)
            return True
#print("Файлы внутри папки:")
#print('\n' .join(file_names))
#print()





main()
