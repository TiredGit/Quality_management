import { test, expect } from '@chromatic-com/playwright';

test('Главная страница', async ({ page }) => {
  await page.goto('/');

  await expect(page.locator('h1')).toHaveText(
    'Лучшая стрижка в центре города'
  );

  await expect(page.locator('.hero__bg')).toBeVisible();
});