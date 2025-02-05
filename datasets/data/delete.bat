@echo off
setlocal enabledelayedexpansion

:: Set folder paths
set "txt_folder=C:\Users\admin\Documents\ocr project\ai\yolo_page_number\data\labels\train"
set "images_folder=C:\Users\admin\Documents\ocr project\ai\yolo_page_number\data\images\train"

:: Loop through all text files in the txt folder
for %%F in (%txt_folder%\*.txt) do (
    for /f "delims=" %%L in (%%F) do (
        set "filename=%%L"
        set "image_path=%images_folder%\!filename!.png"

        if exist "!image_path!" (
            del "!image_path!"
            echo Deleted: !image_path!
        ) else (
            echo File not found: !image_path!
        )
    )
)

echo Process completed.
pause
