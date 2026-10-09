from __future__ import annotations

import shutil
from pathlib import Path


def package_bundle() -> Path:
    project_root = Path(__file__).resolve().parents[1]
    dist_dir = project_root / "dist"
    dist_dir.mkdir(exist_ok=True)

    archive_name = "rag_workshop_classroom_bundle.zip"
    archive_path = dist_dir / archive_name
    if archive_path.exists():
        archive_path.unlink()

    files_to_include = [
        "app.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        "core",
        "ui",
        "data/demo",
        "scripts",
        "tests",
    ]

    root_items = [project_root / name for name in files_to_include]
    temp_dir = dist_dir / "bundle_temp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    for item in root_items:
        destination = temp_dir / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)

    shutil.make_archive(str(dist_dir / "rag_workshop_classroom_bundle"), "zip", temp_dir)
    shutil.rmtree(temp_dir)
    print(f"Created bundle: {archive_path}")
    return archive_path


if __name__ == "__main__":
    package_bundle()
