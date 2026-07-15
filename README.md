# 簡報瑞士刀

跨平台的系統匣簡報輔助工具。程式不會開啟主視窗，所有設定都在系統匣圖示的右鍵選單中完成。

## 功能

- 聚光燈游標：以不攔截點擊的半透明圓圈跟隨游標，可調整顏色、透明度與 48–320 px 圓圈大小。
- 按鍵顯示：在游標所在螢幕中央下方顯示單鍵或組合鍵，不會攔截原本的鍵盤輸入。
- 自動保存：記住兩項功能的啟用狀態與外觀設定。
- 多螢幕與高 DPI：使用 Qt 邏輯像素定位與繪製。

## 開發與執行

需要 [uv](https://docs.astral.sh/uv/)；Python 3.12 及相依套件會由 uv 管理。

```powershell
uv sync
uv run prtools
```

品質檢查：

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

## 打包

`pysidedeploy.spec` 使用 Qt 官方 `pyside6-deploy`。請在要發行的作業系統上原生執行：

```powershell
uv sync
uv run pyside6-deploy -c pysidedeploy.spec --force
```

輸出位於 `dist/`。Windows、macOS 與 Linux 必須各自在對應平台建置，不支援交叉編譯。

## 平台注意事項

- Windows：不需要額外權限。
- macOS：首次啟用按鍵顯示時，請依系統提示授予「輸入監控」或「輔助使用」權限。拒絕後按鍵顯示會保持關閉。
- Linux：完整支援目標為 X11，桌面環境必須提供 StatusNotifierItem 或 XEmbed 系統匣。GNOME 可能需要 AppIndicator 類型的擴充套件。
- Wayland：受全域輸入與覆蓋層協定限制，按鍵顯示和點擊穿透不保證可用；程式會在選單中顯示警告。

按鍵內容只用於即時畫面顯示，不會寫入設定、檔案或日誌。
