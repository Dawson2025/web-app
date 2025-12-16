import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Test credentials
const TEST_USERNAME = `testuser_${Date.now()}`; // Unique username for each run
const TEST_EMAIL = `testuser_${Date.now()}@example.com`;
const TEST_PASSWORD = 'testpassword';

const BASE_URL = 'http://127.0.0.1:5000'; // Flask app runs on port 5000

async function waitForServerReady(url, retries = 60, delay = 2000) {
    console.log(`\nWaiting for server at ${url} to be ready...`);
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url);
            // Consider any successful HTTP response (not connection refused, not server error) as ready
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

async function run() {
    console.log("🚀 Starting Web App Minimal Demonstration...");
    console.log("This script will demonstrate the 5 core requirements and database integration stretch goal.");

    // Ensure server is ready
    if (!await waitForServerReady(BASE_URL)) {
        console.error("Exiting demonstration as the web server is not responsive.");
        process.exit(1);
    }

    let browser;
    try {
        browser = await chromium.launch({ headless: false, slowMo: 500, args: ['--start-maximized'] });
        const context = await browser.newContext();
        const page = await context.newPage();

        // 0. Register a new user
        console.log(`\n0. Registering a new user: ${TEST_USERNAME}`);
        await page.goto(`${BASE_URL}/register`);
        await page.waitForLoadState('domcontentloaded');

        await page.fill('input[name="username"]', TEST_USERNAME);
        await page.fill('input[name="email"]', TEST_EMAIL);
        await page.fill('input[name="password"]', TEST_PASSWORD);
        await page.locator('button[type="submit"]').click();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(1000); // Wait for potential redirect/flash

        let registrationSuccess = await page.locator('.flash-success').isVisible();
        if (registrationSuccess) {
            console.log(`   Registration successful for ${TEST_USERNAME}.`);
        } else {
            const errorText = await page.locator('.flash-danger').innerText().catch(() => '');
            console.error(`   Registration failed: ${errorText || 'Unknown error'}`);
            // Attempt to login if already registered (e.g., from previous run cleanup failure)
            console.log("   Attempting to log in, assuming user might already exist.");
        }
        
        // 1. Log in to the Flask app
        console.log(`\n1. Logging in as ${TEST_USERNAME}...`);
        await page.goto(`${BASE_URL}/login`);
        await page.waitForLoadState('domcontentloaded');

        await page.fill('input[name="username"]', TEST_USERNAME);
        await page.fill('input[name="password"]', TEST_PASSWORD);
        await page.locator('button[type="submit"]').click();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000); // Wait for dashboard load

        let loggedInUser = await page.locator('h2').innerText();
        if (loggedInUser.includes(TEST_USERNAME)) {
            console.log(`   Successfully logged in as ${TEST_USERNAME}.`);
        } else {
            console.error("   Login failed or dashboard not loaded as expected.");
            process.exit(1);
        }
        await page.waitForTimeout(2000);

        // 2. Navigate to Words page (Generated HTML page)
        console.log("\n2. Navigating to Words page to demonstrate HTML generation.");
        await page.goto(`${BASE_URL}/words`);
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(2000);
        console.log("   Words page loaded.");

        // 3. Include pictures and/or CSS (Implicit, check for stylesheet or image presence)
        console.log("\n3. Verifying static assets (CSS, images).");
        const cssLoaded = await page.locator('link[rel="stylesheet"][href*="/static/css/style.css"]').isVisible();
        console.log(`   CSS stylesheet loaded: ${cssLoaded}`);
        const imageLoaded = await page.locator('img[src*="/static/img/placeholder.png"]').isVisible(); // Check if placeholder is directly in words.html or similar
        // Note: For this minimal app, images might only be present in specific templates if added.
        console.log(`   Placeholder image loaded (if used directly): ${imageLoaded}`);
        await page.waitForTimeout(2000);

        // 4. Accept input from the user & Perform error checking on the input
        console.log("\n4. Demonstrating user input and error checking on Add Word form.");
        await page.goto(`${BASE_URL}/words`); // Ensure we are on the words page with the form
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(1000);

        console.log("   Attempting to add word with missing 'New Language Word' (expected error)...");
        await page.locator('input[name="english_translation"]').fill('Error Test');
        await page.locator('button:has-text("Add Word")').click();
        await page.waitForTimeout(1000);
        let missingWordError = await page.locator('.flash-danger').innerText().catch(() => '');
        if (missingWordError.includes('New language word is required.')) {
            console.log(`   Error message received: "${missingWordError}"`);
        } else {
            console.warn(`   Expected "New language word is required." error, got: "${missingWordError}"`);
        }
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

        let addSuccess = await page.locator('.flash-success').isVisible();
        let wordInTable = await page.locator(`text=${NEW_WORD}`).isVisible();
        if (addSuccess && wordInTable) {
            console.log(`   Successfully added "${NEW_WORD}" and it appeared in the table.`);
        } else {
            console.error("   Failed to add word or verify its presence.");
        }
        await page.waitForTimeout(2000);

        // 6. Stretch Goal: Integrate a database into your web app (implicit via CRUD)
        console.log("\n6. (Stretch Goal: Database Integration) Demonstrating persistent storage.");
        console.log("   The successful addition of words and their display confirms interaction with the SQLite database.");
        console.log("   Now, deleting the test word to clean up...");
        
        // Find the row for the newly added word and click its delete button
        const deleteButton = page.locator('tr', { hasText: NEW_WORD }).locator('button.delete-btn');
        await deleteButton.click();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);

        let deleteSuccess = await page.locator('.flash-success').isVisible();
        let wordGone = !(await page.locator(`text=${NEW_WORD}`).isVisible());
        if (deleteSuccess && wordGone) {
            console.log(`   Successfully deleted "${NEW_WORD}".`);
        } else {
            console.error("   Failed to delete word or verify its removal.");
        }
        await page.waitForTimeout(2000);

        // 7. Log out
        console.log("\n7. Logging out.");
        await page.goto(`${BASE_URL}/logout`);
        await page.waitForLoadState('domcontentloaded');
        let logoutSuccess = await page.locator('h2', { hasText: 'Log In' }).isVisible();
        console.log(`   Logged out successfully: ${logoutSuccess}`);

        console.log("\n✅ Web App Minimal Demonstration complete.");
        console.log("The browser will close in 5 seconds...");
        await page.waitForTimeout(5000);

    } catch (error) {
        console.error("❌ An error occurred during the demonstration:", error);
    } finally {
        if (browser) await browser.close();
    }
}

run();
