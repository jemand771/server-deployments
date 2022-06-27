import os
import pathlib


def main():
    os.system("kubectl config use-context 771-new")
    for ext in ("json", "yaml"):
        for file in pathlib.Path("..").glob(f"**/*.{ext}s"):
            new_file = file.parent / file.name[:-1]
            if new_file.is_file():
                continue
            print(f"sealing {file} -> {new_file}")
            os.system(f"D:/software/kubeseal/kubeseal -o {ext} <{file} >{new_file}")
            os.system(f"git add {new_file} >nul 2>&1")


if __name__ == '__main__':
    main()
