# 技術設計

本文說明簡報瑞士刀的跨平台後端、macOS 原生整合及相關安全邊界。

## 元件與資料流

`AppController` 負責讀寫設定並協調系統匣、聚光燈、鍵盤監看與提示覆蓋層。系統匣面板關閉後才啟動鍵盤後端，避免在 macOS 原生選單追蹤迴圈內初始化事件監看器。鍵盤後端只送出格式化前的按下／放開事件；`KeyChordTracker` 去除重複事件並維護目前按鍵集合，`KeystrokeOverlay` 顯示最後一次完整組合，在所有按鍵放開後延遲淡出。

## macOS 聚光燈與覆蓋層

macOS 沒有支援背景程式跨應用程式替換系統游標的公開 API，因此聚光燈使用透明 Qt 工具視窗跟隨 `QCursor`。Cocoa 原生視窗另套用以下限制：

- `NSFloatingWindowLevel`：高於一般應用程式，低於選單列與彈出選單。
- `NSWindowStyleMaskNonactivatingPanel` 與 `WA_ShowWithoutActivating`：顯示時不成為 key window。
- `hidesOnDeactivate = false`：切換應用程式後仍維持顯示。
- 關閉陰影、邊框及不透明背景，並忽略所有滑鼠事件。
- 加入所有 Space，且可顯示於全螢幕輔助空間。

系統匣面板展開前會同步一次游標位置，避免原生選單追蹤期間 Qt 計時器暫停而留下舊位置。

## macOS 鍵盤監看

macOS 使用 Core Graphics `CGEventTapCreate`，位置為 `kCGHIDEventTap`／`kCGHeadInsertEventTap`，選項固定為 `kCGEventTapOptionListenOnly`。選擇 HID 前端是為了在 Carbon 全域快捷鍵或其他快捷鍵工具處理事件前取得副本；listen-only 保證 callback 的回傳值不能用來阻止事件繼續傳遞。

事件 tap 在專用 Core Foundation run loop 執行。callback 不操作 Qt widget 或 Qt timer，只透過 Qt signal 將資料排回主執行緒。監看範圍限於 `keyDown`、`keyUp` 與 `flagsChanged`：

- 修飾鍵狀態從事件 flags 重建，避免遺失或重複事件造成黏鍵。
- 左右修飾鍵合併為 Command、Shift、Option、Control 的顯示狀態。
- `keycode 255` 是系統狀態事件，會直接忽略。
- Caps Lock 以一次性按鍵顯示，不會因鎖定狀態永久留在組合中。
- ANSI 字母、數字、方向鍵與常用標點使用實體 keycode 映射，不記錄輸入文字。

此後端需要 macOS「輸入監控」權限。程式只在記憶體中維護當前按鍵狀態，不保存、記錄或傳送按鍵內容。

## 其他平台

- Windows 聚光燈替換真正的系統游標，並由獨立 watchdog 在異常終止後復原；鍵盤監看使用 `pynput`。
- Linux 聚光燈使用透明覆蓋層，鍵盤監看使用 `pynput`。X11 支援較完整；Wayland 受全域輸入與點擊穿透協定限制。

## 驗證

提交前執行：

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

macOS 手動驗證應涵蓋游標進入選單列、展開系統匣面板、切換焦點、中英文輸入、一般字母與標點、修飾組合鍵，以及已被其他快捷鍵工具註冊的組合。
