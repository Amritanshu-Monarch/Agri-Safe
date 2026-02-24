"""
Dataset Preparation Script
───────────────────────────
Downloads PlantVillage dataset and splits into train/val sets.
Run this BEFORE train_model.py

Usage:
    python prepare_dataset.py
"""

import os
import shutil
import random
from pathlib import Path

DATASET_SOURCE = "dataset/raw"       # Put your PlantVillage images here
DATASET_OUTPUT = "dataset"
TRAIN_SPLIT    = 0.85                # 85% train, 15% validation
SEED           = 42

def split_dataset():
    raw_path = Path(DATASET_SOURCE)
    if not raw_path.exists():
        print("""
❌ Raw dataset folder not found!

Please download the PlantVillage dataset:
  Option A (Kaggle): 
    https://www.kaggle.com/datasets/emmarex/plantdisease
    Extract to: dataset/raw/

  Option B (Direct download via Python):
    pip install kaggle
    kaggle datasets download -d emmarex/plantdisease
    unzip plantdisease.zip -d dataset/raw/

  Expected structure:
    dataset/raw/
      Potato___Late_blight/   ← folder per class
        image1.jpg
        image2.jpg
        ...
      Tomato___healthy/
        ...
        """)
        return

    classes = [d for d in raw_path.iterdir() if d.is_dir()]
    print(f"Found {len(classes)} classes in dataset")

    total_images = 0
    for cls in classes:
        images = list(cls.glob("*.jpg")) + list(cls.glob("*.JPG")) + \
                 list(cls.glob("*.png")) + list(cls.glob("*.jpeg"))

        if not images:
            continue

        random.seed(SEED)
        random.shuffle(images)
        split_idx = int(len(images) * TRAIN_SPLIT)
        train_imgs = images[:split_idx]
        val_imgs   = images[split_idx:]

        # Create train/val directories
        train_dir = Path(DATASET_OUTPUT) / "train" / cls.name
        val_dir   = Path(DATASET_OUTPUT) / "val"   / cls.name
        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True,   exist_ok=True)

        for img in train_imgs:
            shutil.copy2(img, train_dir / img.name)
        for img in val_imgs:
            shutil.copy2(img, val_dir / img.name)

        total_images += len(images)
        print(f"  ✅ {cls.name}: {len(train_imgs)} train, {len(val_imgs)} val")

    print(f"\n🎉 Dataset ready! {total_images} images split into train/val")
    print(f"   Run: python train_model.py")

if __name__ == "__main__":
    split_dataset()
