const { test, expect } = require('@playwright/test');

// 3. 端到端測試 (End-to-End Tests)
test.describe('Dashboard E2E Tests', () => {
  
  test('應能成功載入首頁並顯示正確標題', async ({ page }) => {
    // 導航到應用程式根目錄 (需確保前端正在運行)
    await page.goto('/');

    // 驗證標題是否存在
    await expect(page).toHaveTitle(/Dashboard/);
  });

  test('應能點擊按鈕並觸發 UI 變更', async ({ page }) => {
    await page.goto('/');

    // 尋找按鈕並點擊 (無頭瀏覽器模擬真實使用者操作)
    const button = page.getByRole('button', { name: /開始測試/i });
    if (await button.isVisible()) {
      await button.click();
      // 驗證畫面上出現了測試結果的元素
      await expect(page.locator('.test-results')).toBeVisible();
    }
  });
});
