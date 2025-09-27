import os
import re

# Корневая папка с ресурсами (поменяй если нужно)
RESOURCE_DIR = "Resources"

# Регулярка для поиска строк, похожих на пути
PATH_PATTERN = re.compile(r'["\']?([A-Za-z0-9_\-/\\]+\.(yml|png|rsi|ogg|wav))["\']?')

def check_path(path, file, line_num):
    errors = []
    if "\\" in path:
        errors.append("использует обратный слэш \\ вместо /")
    if not path.startswith("/"):
        errors.append("не начинается с /")
    if ".." in path:
        errors.append("содержит .. (некорректный путь)")
    if errors:
        print(f"[!] Проблема в {file}:{line_num} → {path} ({'; '.join(errors)})")

for root, _, files in os.walk(RESOURCE_DIR):
    for fname in files:
        if fname.endswith(".yml"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                for num, line in enumerate(f, start=1):
                    match = PATH_PATTERN.search(line)
                    if match:
                        check_path(match.group(1), fpath, num)

print("Проверка завершена ✅")
