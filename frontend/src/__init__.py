import pathlib
import sys

ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
SRC_DIR = ROOT_DIR / "src"

sys.path.append(str(SRC_DIR))

if __name__ == "__main__":
    print(SRC_DIR)