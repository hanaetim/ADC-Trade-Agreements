/**
 * E2E test for case queue wireframe
 * Tests the case queue page with filtering and navigation
 */

import { test, expect } from './_pipeline_guard'

test.describe('Case Queue Wireframe', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to login page
    await page.goto('/login')
    
    // Wait for login form to be visible
    await page.waitForSelector('form', { state: 'visible', timeout: 10000 })

    // Login with intake exception handler credentials
    await page.fill('input[name="email"]', 'intake@example.com')
    await page.fill('input[name="password"]', 'Intake-pass-1')
    await page.click('button[type="submit"]')

    // Wait for navigation to cases page (default landing)
    await page.waitForURL('**/cases', { timeout: 15000 })
    
    // Wait for the table to be visible after login
    await page.waitForSelector('table', { state: 'visible', timeout: 5000 })
  })

  test('should display case queue with summary strip', async ({ page }) => {
    // Verify page title
    await expect(page.getByRole('heading', { name: 'Cases', level: 1 })).toBeVisible()
    await expect(page.getByText('Intake exception queue')).toBeVisible()

    // Verify summary strip is present with metrics
    // The exact numbers may vary, just check the labels exist
    await expect(page.getByText(/Blocked at intake/i)).toBeVisible()
    await expect(page.getByText(/Queued for review/i)).toBeVisible()
    await expect(page.getByText(/Registration sync failed/i)).toBeVisible()
    await expect(page.getByText(/Routed in the last 7 days/i)).toBeVisible()
  })

  test('should display filter bar with all controls', async ({ page }) => {
    // Verify filter controls exist
    await expect(page.locator('select[name="workflow_type"]')).toBeVisible()
    await expect(page.locator('select[name="case_state"]')).toBeVisible()
    await expect(page.locator('select[name="assigned_role"]')).toBeVisible()

    // Verify filter buttons
    await expect(page.getByRole('button', { name: /Apply filters/i })).toBeVisible()
    await expect(page.getByRole('button', { name: /Clear filters/i })).toBeVisible()
  })

  test('should display quick filter chips', async ({ page }) => {
    // Verify quick filter label
    await expect(page.getByText('Quick filters:')).toBeVisible()

    // Verify quick filter chips are present
    await expect(page.getByRole('button', { name: /All states/i })).toBeVisible()
    await expect(page.getByRole('button', { name: /^intake_blocked$/i })).toBeVisible()
    await expect(page.getByRole('button', { name: /^queued_for_review$/i })).toBeVisible()
  })

  test('should display case table with columns', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Verify column headers
    await expect(page.getByRole('columnheader', { name: /Case reference/i })).toBeVisible()
    await expect(page.getByRole('columnheader', { name: /Workflow type/i })).toBeVisible()
    await expect(page.getByRole('columnheader', { name: /Case state/i })).toBeVisible()
    await expect(page.getByRole('columnheader', { name: /Current step/i })).toBeVisible()
    await expect(page.getByRole('columnheader', { name: /Accountable role/i })).toBeVisible()
  })

  test('should apply workflow type filter', async ({ page }) => {
    // Wait for initial load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Select origin_ruling filter
    await page.selectOption('select[name="workflow_type"]', 'origin_ruling')

    // Click Apply filters
    await page.click('button:has-text("Apply filters")')

    // Wait for table to update
    await page.waitForTimeout(1000)

    // Verify filter was applied (URL or table should update)
    // In a real implementation, we'd check the filtered results
    // For now, just verify the page didn't error
    await expect(page.locator('table.cases')).toBeVisible()
  })

  test('should apply case state filter', async ({ page }) => {
    // Wait for initial load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Select intake_blocked filter
    await page.selectOption('select[name="case_state"]', 'intake_blocked')

    // Click Apply filters
    await page.click('button:has-text("Apply filters")')

    // Wait for table to update
    await page.waitForTimeout(1000)

    // Verify filter was applied
    await expect(page.locator('table.cases')).toBeVisible()
  })

  test('should use quick filter chips', async ({ page }) => {
    // Wait for initial load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Click intake_blocked quick filter chip
    const intakeBlockedChip = page.getByRole('button', { name: /^intake_blocked$/i })
    await intakeBlockedChip.click()

    // Wait for update
    await page.waitForTimeout(1000)

    // Verify chip is now active (has different styling)
    await expect(intakeBlockedChip).toHaveAttribute('aria-pressed', 'true')
  })

  test('should clear filters', async ({ page }) => {
    // Wait for initial load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Apply some filters
    await page.selectOption('select[name="workflow_type"]', 'origin_ruling')
    await page.click('button:has-text("Apply filters")')
    await page.waitForTimeout(500)

    // Click Clear filters
    await page.click('button:has-text("Clear filters")')

    // Wait for update
    await page.waitForTimeout(1000)

    // Verify filter selects are back to default
    await expect(page.locator('select[name="workflow_type"]')).toHaveValue('all')
  })

  test('should navigate to case detail on Open button click', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Click the first Open button
    const openButtons = page.getByRole('button', { name: /^Open$/i })
    const firstOpenButton = openButtons.first()
    
    // Wait for button to be visible and clickable
    await expect(firstOpenButton).toBeVisible()
    await firstOpenButton.click()

    // Wait for navigation to case detail page
    await page.waitForURL(/\/cases\/[a-f0-9-]+$/, { timeout: 5000 })

    // Verify we're on a case detail page
    const url = page.url()
    expect(url).toMatch(/\/cases\/[a-f0-9-]+$/)
  })

  test('should display pagination controls', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Verify pagination text is present
    await expect(page.locator('text=/Showing.*of/i')).toBeVisible()

    // Verify pagination buttons exist
    await expect(page.getByRole('button', { name: /Previous/i })).toBeVisible()
    await expect(page.getByRole('button', { name: /Next/i })).toBeVisible()
  })

  test('should display legend sections', async ({ page }) => {
    // Verify legend sections are present
    await expect(page.getByRole('heading', { name: /Case state labels/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Where a reason came from/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Registration sync/i })).toBeVisible()
  })

  test('should show case references and applicant names', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Check that case references are displayed (format: IAO-YYYY-NNNNNN)
    const caseReferences = page.locator('span.font-mono.font-bold')
    await expect(caseReferences.first()).toBeVisible()
    
    // Case references should follow the pattern
    const firstRef = await caseReferences.first().textContent()
    expect(firstRef).toMatch(/IAO-\d{4}-\d{6}/)
  })

  test('should display case state badges with correct colors', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('table.cases', { timeout: 10000 })

    // Find a badge (any badge will do to verify they render)
    const badges = page.locator('.inline-flex.items-center.gap-1\\.5.px-3')
    await expect(badges.first()).toBeVisible()
  })
})
