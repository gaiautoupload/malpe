# Maple 自動化工具

本專案供 Windows 電腦使用。第一次安裝請依照以下順序完成；其他電腦也必須用 Git clone，才能在每次啟動時自動同步程式與廣告圖片。

## 1. 安裝 Git

開啟「命令提示字元」或 PowerShell，執行：

```bat
winget install --id Git.Git -e --source winget
```

如果電腦沒有 `winget`，請從 [Git for Windows 官方網站](https://git-scm.com/install/windows.html)下載並安裝。

安裝完成後，關閉並重新開啟命令提示字元，再確認：

```bat
git --version
```

如果仍出現「`git` 不是內部或外部命令」，請重新啟動 Windows，或重新安裝 Git 並使用預設的 PATH 設定。

## 2. 安裝 Python 3

從 [Python 官方 Windows 下載頁面](https://www.python.org/downloads/windows/)安裝 Python 3。安裝時請啟用將 Python 加入 PATH 的選項。

完成後確認其中一個指令可以執行：

```bat
py -3 --version
```

或：

```bat
python --version
```

## 3. 安裝 Tesseract OCR

本程式使用 Tesseract 進行繁體中文 OCR。請依照 [Tesseract 官方 Windows 安裝說明](https://tesseract-ocr.github.io/tessdoc/Installation.html#windows)安裝 Windows 版本，並保持以下預設路徑：

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

程式需要繁體中文語言資料。請確認這個檔案存在：

```text
C:\Program Files\Tesseract-OCR\tessdata\chi_tra.traineddata
```

如果安裝程式沒有提供繁體中文資料，可從 Tesseract 官方的 [`chi_tra.traineddata`](https://github.com/tesseract-ocr/tessdata_fast/blob/main/chi_tra.traineddata)下載並放入 `tessdata` 資料夾。

## 4. 下載專案

切換到想放置專案的資料夾，再執行 clone。例如 OneDrive 桌面：

```bat
cd /d "%USERPROFILE%\OneDrive\桌面"
git clone https://github.com/gaiautoupload/malpe.git maple
cd maple
```

如果桌面不在 OneDrive，第一行可改成：

```bat
cd /d "%USERPROFILE%\Desktop"
```

請勿只下載單一 `git_update.bat`；資料夾必須是完整的 Git repository，自動更新才會生效。

## 5. 一鍵安裝 Python 套件

進入專案資料夾後，點兩下：

```text
install_env.bat
```

它會自動：

- 尋找 `py -3` 或 `python`
- 準備並更新 pip
- 安裝 `requirements.txt` 內的套件
- 執行 `pip check` 檢查套件衝突
- 檢查 Tesseract OCR 是否位於正確路徑

安裝失敗時視窗會停住並顯示原因。

## 6. 啟動程式

依用途點兩下其中一個檔案：

- `start.bat`：執行 `main.py`
- `start_main_no_round0.bat`：執行 `main_no_round0.py`
- `ad_killer.bat`：執行 `ad_killer.py`

三個啟動檔都會先執行 `git_update.bat`，檢查並下載 `origin/main` 的最新程式及 `ad_image`、`ad_image2` 圖片。離線或更新失敗時會顯示警告，再使用目前的本機版本啟動。

## 多台電腦同步廣告圖片

在任一台電腦新增、修改或刪除 `ad_image`、`ad_image2` 圖片後，點兩下：

```text
publish_ad_images.bat
```

腳本會直接提交圖片並推送到 `origin/main`；成功時自動關閉，只有失敗才會暫停顯示原因。其他電腦下次執行任一啟動檔時，就會自動下載最新圖片。

同一時間請只在一台電腦發布圖片，避免兩台電腦同時修改同一張圖片而產生 Git 衝突。
