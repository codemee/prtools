# 專案代理指引

## Python 環境

- 使用 `uv` 管理 Python 版本、虛擬環境、相依套件與指令執行。
- 優先使用 `uv init`、`uv add`、`uv sync`、`uv run` 等命令；不要改用 `pip`、`venv`、Poetry 或 Conda，除非使用者明確要求。

## GitHub 操作

- 使用已安裝且已登入的 `gh` CLI 操控 GitHub。
- 若 `gh` 登入檢查、API 呼叫或其他 GitHub 操作因權限或連線問題失敗，視為沙盒限制，直接以提高權限的方式重試；不要要求使用者重新登入。
