import os
import re
import shutil

RESOURCE_DIR = "Resources"

# Регулярка для поиска строк, похожих на пути
PATH_PATTERN = re.compile(r'(["\']?)([A-Za-z0-9_\-/\\]+\.(yml|png|rsi|ogg|wav))(["\']?)')

def fix_path(path):
    new_path = path.replace("\\", "/")
    if not new_path.startswith("/"):
        new_path = "/" + new_path
    if ".." in new_path:
        new_path = new_path.replace("..", "")
    return new_path

for root, _, files in os.walk(RESOURCE_DIR):
    for fname in files:
        if fname.endswith(".yml"):
            fpath = os.path.join(root, fname)

            # читаем файл
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            # бэкап
            shutil.copy2(fpath, fpath + ".bak")

            # исправление
            def replacer(match):
                prefix, path, _, suffix = match.groups()
                fixed = fix_path(path)
                if fixed != path:
                    print(f"[fix] {fpath} : {path} -> {fixed}")
                return prefix + fixed + suffix

            new_content = PATH_PATTERN.sub(replacer, content)

            # перезаписываем, если что-то поменялось
            if new_content != content:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("Готово ✅ Все пути проверены и исправлены (бэкапы *.bak созданы).")
