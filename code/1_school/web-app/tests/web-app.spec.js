import { test, expect } from '@playwright/test';
import { pathToFileURL } from 'url';

// Test credentials
const TEST_USERNAME = `testuser_${Date.now()}`;
const TEST_EMAIL = `testuser_${Date.now()}@example.com`;
const TEST_PASSWORD = 'testpassword';

// Helper function to wait for the server to be ready
async function waitForServerReady(url, retries = 90, delay = 2000) { // Increased retries and delay
    console.log(`\nWaiting for server at ${url} to be ready...`);
    for (let i = 0; i < retries; i++) {
        process.stdout.write(`  Attempt ${i + 1}/${retries}... `); // Log attempt
        try {
            const response = await fetch(url);
            if (response.status < 500) {
                console.log(`Server is ready after ${i + 1} attempts.`);
                return true;
            }
        } catch (error) {
            // Connection refused, server not up yet, etc.
        }
        await new Promise(resolve => setTimeout(resolve, delay));
    }
    console.error("Server did not become ready within the allotted time.");
    return false;
}

test.describe('Web App Minimal Demonstration', () => {
  test.beforeAll(async () => {
    test.setTimeout(180000); // Set a longer timeout for beforeAll hook (3 minutes)
    const baseURL = test.use?.baseURL || 'http://127.0.0.1:5000'; // Get baseURL from Playwright config
    if (!await waitForServerReady(baseURL)) {
        console.error("Exiting tests as the web server is not responsive.");
        process.exit(1);
    }
  });

  test('should demonstrate core web app functionalities', async ({ page }) => {

    // 0. Register a new user
    console.log(`\n0. Registering a new user: ${TEST_USERNAME}`);
    await page.goto('/register');
    await page.waitForLoadState('domcontentloaded');

    await page.fill('input[name="username"]', TEST_USERNAME);
    await page.fill('input[name="email"]', TEST_EMAIL);
    await page.fill('input[name="password"]', TEST_PASSWORD);
    await page.locator('button[type="submit"]').click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000); // Wait for potential redirect/flash

    const registrationSuccess = await page.locator('.flash-success').isVisible();
    if (registrationSuccess) {
        console.log(`   Registration successful for ${TEST_USERNAME}.`);
    } else {
        const errorText = await page.locator('.flash-danger').innerText().catch(() => '');
        console.warn(`   Registration might have failed: ${errorText || 'Unknown error'}. Attempting to log in.`);
    }
    
    // 1. Log in to the Flask app
    console.log(`\n1. Logging in as ${TEST_USERNAME}...`);
    await page.goto('/login');
    await page.waitForLoadState('domcontentloaded');

    await page.fill('input[name="username"]', TEST_USERNAME);
    await page.fill('input[name="password"]', TEST_PASSWORD);
    await page.locator('button[type="submit"]').click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000); // Wait for dashboard load

    await expect(page.locator('h2')).toContainText(`Welcome to your Dashboard, ${TEST_USERNAME}!`);
    console.log(`   Successfully logged in as ${TEST_USERNAME}.`);
    await page.waitForTimeout(2000);

    // 2. Navigate to Words page (Generated HTML page)
    console.log("\n2. Navigating to Words page to demonstrate HTML generation.");
    await page.goto('/words');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(2000);
    console.log("   Words page loaded.");

    // 3. Include pictures and/or CSS (Implicit, check for stylesheet or image presence)
    console.log("\n3. Verifying static assets (CSS, images).");
    const cssLinkElement = page.locator('link[rel="stylesheet"][href*="/static/css/style.css"]');
    await expect(cssLinkElement).toHaveAttribute('href', /static\/css\/style\.css/); // Check href attribute
    const cssHref = await cssLinkElement.getAttribute('href');
    console.log(`   CSS link href: ${cssHref}`);
    
    // Verify CSS is actually applied by checking a CSS property on an element
    await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(244, 244, 244)'); // Corresponds to #f4f4f4
    console.log(`   CSS stylesheet loaded and applied successfully.`);
    await page.waitForTimeout(1000); // Small pause for visual confirmation in headed mode
    
    // Check for placeholder image if used
    const imageLoaded = await page.locator('img[src*="/static/img/placeholder.png"]').isVisible();
    console.log(`   Placeholder image loaded (if used directly): ${imageLoaded}`);
    await page.waitForTimeout(2000);

    // 4. Accept input from the user & Perform error checking on the input
    console.log("\n4. Demonstrating user input and error checking on Add Word form.");
    await page.goto('/words'); // Ensure we are on the words page with the form
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    console.log("   Attempting to add word with missing 'New Language Word' (expected error)...");
    await page.locator('input[name="english_translation"]').fill('Error Test');
    await page.locator('button:has-text("Add Word")').click();
    await page.waitForTimeout(1000);
    const errorFlashMessage = page.locator('.flash-danger');
    await expect(errorFlashMessage).toBeVisible();
    await expect(errorFlashMessage).toContainText('New language word is required.');
    console.log(`   Error message received: "${await errorFlashMessage.innerText()}"`);
    await page.waitForTimeout(2000);

    // 5. Modify content of HTML generated by the app based on user input (add a word)
    console.log("\n5. Successfully adding a new word to modify content dynamically.");
    const NEW_WORD = 'PlaywrightTestWord';
    const ENGLISH_TRANS = 'Playwright Test Translation';

    await page.locator('input[name="new_language_word"]').fill(NEW_WORD);
    await page.locator('input[name="english_translation"]').fill(ENGLISH_TRANS);
    await page.locator('button:has-text("Add Word")').click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    const successFlashMessage = page.locator('.flash-success');
    await expect(successFlashMessage).toBeVisible();
    await expect(successFlashMessage).toContainText(`Word "${NEW_WORD}" added successfully!`);
    
    // Verify word is in the table
    const wordInTable = page.locator('table tbody tr', { hasText: NEW_WORD });
    await expect(wordInTable).toBeVisible();
    console.log(`   Successfully added "${NEW_WORD}" and it appeared in the table.`);
    await page.waitForTimeout(2000);

    // --- Demonstrate Data Permanence Across Sessions ---
    console.log("\n6. Demonstrating data permanence across sessions: Logging out and back in.");
    await page.goto('/logout');
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('h2', { hasText: 'Log In' })).toBeVisible();
    console.log(`   Logged out. Now logging back in...`);

    await page.goto('/login');
    await page.fill('input[name="username"]', TEST_USERNAME);
    await page.fill('input[name="password"]', TEST_PASSWORD);
    await page.locator('button[type="submit"]').click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // Verify word is still present after re-login
    console.log(`   Verifying "${NEW_WORD}" is still present after re-login.`);
    await page.goto('/words'); // Navigate back to words page if not already there
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('table tbody tr', { hasText: NEW_WORD })).toBeVisible();
    console.log(`   "${NEW_WORD}" is confirmed to be present after re-login.`);
    await page.waitForTimeout(2000);

    // 7. Stretch Goal: Integrate a database into your web app (implicit via CRUD)
    console.log("\n7. (Stretch Goal: Database Integration) Demonstrating persistent storage.");
    console.log("   The successful addition of words and their display confirms interaction with the SQLite database.");
    console.log("   Now, deleting the test word to clean up...");
    
    // Find the row for the newly added word and click its delete button
    const deleteButton = page.locator('tr', { hasText: NEW_WORD }).locator('button.delete-btn');
    await deleteButton.click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    const deleteSuccessFlashMessage = page.locator('.flash-success');
    await expect(deleteSuccessFlashMessage).toBeVisible();
    await expect(deleteSuccessFlashMessage).toContainText('Word deleted successfully!');
    
    await expect(page.locator(`text=${NEW_WORD}`)).not.toBeVisible();
    console.log(`   Successfully deleted "${NEW_WORD}".`);
    await page.waitForTimeout(2000);

    // 7. Log out
    console.log("\n7. Logging out.");
    await page.goto('/logout');
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('h2', { hasText: 'Log In' })).toBeVisible();
    console.log(`   Logged out successfully.`);

    console.log("\n✅ Web App Minimal Demonstration complete.");
  });
});
