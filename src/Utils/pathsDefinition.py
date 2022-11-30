from pathlib import Path
import os


projectPath = Path(os.path.dirname(__file__)).parent.parent
srcPath = projectPath / "src"
figPath = srcPath / "fig"


if __name__ == "__main__":
    print(projectPath)
    print(projectPath / "hello" / "hi")
