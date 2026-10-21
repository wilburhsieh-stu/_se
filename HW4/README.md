# Git 協作流程與操作說明

本文件說明如何從母專案 `se-test-examples/git-examples` 進行 Fork、建立分支、發起 Pull Request 並完成合併的完整流程。

## 採用之 Git 工作流程 (Git Workflow)

本次操作採用的是開源社群與跨團隊協作中最常見的 **Forking Workflow (分叉工作流)**，並結合了 **GitHub Flow (功能分支工作流)** 的核心概念。

* **Forking Workflow**：開發者沒有母專案的直接推播 (Push) 權限，因此先將母專案 Fork 到自己的帳號下（子專案），在本地修改後推送到子專案，再透過 Pull Request 請求母專案管理者合併。
* **GitHub Flow**：無論是修復 Bug 還是開發新功能，都會從 `main` 切換出一個具描述性的分支（如 `developGitBranch`），開發完成後發起 PR，經過審查與討論後再 Merge 回 `main`。

---

## 完整操作步驟

### 1. Fork (複製/分叉專案)
**目標：** 創造子專案 `ccckmit/git-examples`
這是一個純 GitHub 平台上的操作，無法單用 Git 指令完成。

1. 登入 GitHub，前往母專案網址：`https://github.com/se-test-examples/git-examples`
2. 點擊頁面右上角的 **「Fork」** 按鈕。
3. 選擇你的帳號 (`ccckmit`) 作為目標，點擊「Create fork」。
4. 系統會自動建立子專案：`https://github.com/ccckmit/git-examples`。

### 2. 分支 (Branching)
**目標：** 將專案拉到本地端，並建立 `developGitBranch` 分支進行開發。

打開終端機 (Terminal / Git Bash)，依序輸入以下指令：

```bash
# 1. 將子專案 Clone 到本地端
git clone https://github.com/ccckmit/git-examples.git

# 2. 進入專案資料夾
cd git-examples

# 3. 建立並自動切換到新的分支 developGitBranch
git checkout -b developGitBranch

# 4. (在此處進行程式碼的新增或修改)

# 5. 將變更加入暫存區並提交 (Commit)
git add .
git commit -m "Add new feature in developGitBranch"

# 6. 將本地的新分支推送到個人的遠端子專案 (Origin)
git push origin developGitBranch
```

### 3. Pull Request (合併請求)
**目標：** 請求將子專案的變更或分支，合併回母專案。
這也是一個 GitHub 平台上的操作。

1. 前往你的子專案頁面：`https://github.com/ccckmit/git-examples`
2. GitHub 通常會偵測到你剛剛推送了新分支，並顯示一個綠色的 **「Compare & pull request」** 按鈕，點擊它。
   *(如果沒看到，請點擊「Pull requests」頁籤 -> 「New pull request」)*
3. 確保比較的目標設定正確：
   * **Base repository**: `se-test-examples/git-examples` (母專案)
   * **Base**: `main` (或是母專案的 `developGitBranch`)
   * **Head repository**: `ccckmit/git-examples` (子專案)
   * **Compare**: `developGitBranch` (你剛剛推播的分支)
4. 填寫 PR 的標題與描述，說明這次的修改內容，最後點擊 **「Create pull request」**。

### 4. 合併 (Merge)
**目標：** 將 `developGitBranch` 的程式碼正式併入母專案的 `main` 分支。

**方法 A：透過 GitHub 網頁介面 (推薦)**
母專案的管理者（或擁有寫入權限的人）前往母專案的 Pull Requests 頁面，檢查程式碼無誤後，點擊綠色的 **「Merge pull request」**，然後點擊「Confirm merge」。

**方法 B：透過 Git 指令 (本機操作)**
如果你自己就是母專案的管理者，也可以在本地端進行合併：

```bash
# 1. 切回主分支 main
git checkout main

# 2. 確保本地的 main 是最新版本 (若是從遠端拉取)
git pull origin main

# 3. 將 developGitBranch 分支合併進來
git merge developGitBranch

# 4. 推送合併後的 main 分支到遠端母專案
git push origin main
