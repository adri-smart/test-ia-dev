import { test, expect } from '@playwright/test';
import { QueryPage } from '../pages/query.page';

test.describe('Query Functionality', () => {
  let queryPage: QueryPage;

  test.beforeEach(async ({ page }) => {
    queryPage = new QueryPage(page);
    await page.goto('/');
  });

  test('KAN-469: should process a basic query and receive a response', async ({ page }) => {
    await queryPage.submitQuery('muéstrame las ventas totales del último trimestre');
    
    // Wait for the response to be visible
    await expect(queryPage.responseArea).toBeVisible({ timeout: 15000 });
    
    const responseText = await queryPage.getResponseText();
    expect(responseText).not.toBe('');
    // A simple check to see if the response is somewhat relevant
    expect(responseText.toLowerCase()).toContain('ventas');
  });

  test('KAN-478: should handle an unrecognized query gracefully', async ({ page }) => {
    await queryPage.submitQuery('gibberish query that makes no sense');
    
    await expect(queryPage.responseArea).toBeVisible({ timeout: 10000 });
    
    const responseText = await queryPage.getResponseText();
    // Expect a fallback message based on KAN-478
    expect(responseText.toLowerCase()).toContain('no entendí');
  });
});
