# ProMediaConverter

A simple Windows desktop tool I built to convert and resize images and videos without losing quality.

## What it does

**Images**
- Converts between PNG, JPG, WEBP, BMP, TIFF, and ICO.
- Resizes to custom pixel dimensions (Width x Height) or keeps the original size.
- Automatically fills a white background when converting transparent PNGs to JPG or BMP so they don't turn black.

**Videos**
- Converts between MP4, MKV, AVI, MOV, and WEBM.
- Uses FFmpeg stream copy when changing formats without resizing, so it finishes in seconds with zero quality loss.
- Supports 1080p, 720p, 480p, or custom resolutions.

## Download & Setup

1. Go to the [Latest Release](https://github.com/iMJsvc/ProMediaConverter) page and download `ProMediaConverter.exe`.
2. Double-click the file to run it. You don't need Python installed.

**Note for videos:** Make sure FFmpeg is installed on your PC if you want to convert or resize videos. You can install it quickly via Command Prompt:

```bash
winget install ffmpeg
```

## Running from source

If you want to run or modify the Python script directly:

```bash
pip install customtkinter Pillow
python app.py
```
