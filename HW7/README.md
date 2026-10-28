# Full-Stack Test Dashboard Project

這個專案包含三種層級的測試：
1. **單元測試 (Rust)**: 位於 `backend-rust/`
2. **系統測試 (Node.js API)**: 位於 `api-node/`
3. **E2E 測試 (Playwright)**: 位於 `e2e-tests/`

## 啟動與測試指令

### 1. Rust 單元測試
cd backend-rust
cargo test

### 2. Node.js 系統測試
cd api-node
npm install
npm test

### 3. Playwright E2E 測試
cd e2e-tests
npm install
npx playwright install
npx playwright test
