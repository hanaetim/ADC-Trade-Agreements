/**
 * Smoke test: Login flow
 * Verifies basic authentication through the login form
 */

import { test, expect } from './_pipeline_guard';

test.describe('Login Flow', () => {
  test('should login successfully with seed credentials', async ({ page }) => {
    // Navigate to the application root
    await page.goto('/');

    // Should redirect to login page when not authenticated
    await expect(page).toHaveURL('/login');

    // Verify login page elements
    await expect(page.getByRole('heading', { name: /International Agreements & Origin/i })).toBeVisible();
    await expect(page.getByRole('textbox', { name: /email/i })).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();

    // Fill in login form with seed credentials
    await page.getByRole('textbox', { name: /email/i }).fill('intake@example.com');
    await page.getByLabel(/password/i).fill('Intake-pass-1');

    // Submit the form
    await page.getByRole('button', { name: /sign in/i }).click();

    // Should redirect to cases page after successful login
    await expect(page).toHaveURL('/cases');

    // Verify authenticated user is displayed in the app bar
    const appBar = page.getByRole('banner');
    await expect(appBar.getByText('intake@example.com')).toBeVisible();
    await expect(appBar.getByText('intake_exception_handler')).toBeVisible();

    // Verify navigation is available
    await expect(page.getByRole('navigation', { name: /Primary/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /Cases/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /New case/i })).toBeVisible();
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await page.goto('/login');

    // Fill in invalid credentials
    await page.getByRole('textbox', { name: /email/i }).fill('invalid@example.com');
    await page.getByLabel(/password/i).fill('WrongPassword!');

    // Submit the form
    await page.getByRole('button', { name: /sign in/i }).click();

    // Should show error message
    await expect(page.getByText(/sign in failed/i)).toBeVisible();

    // Should still be on login page
    await expect(page).toHaveURL('/login');
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.getByRole('textbox', { name: /email/i }).fill('intake@example.com');
    await page.getByLabel(/password/i).fill('Intake-pass-1');
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page).toHaveURL('/cases');

    // Click logout
    await page.getByRole('button', { name: /sign out/i }).click();

    // Should redirect to login
    await expect(page).toHaveURL('/login');
  });
});
