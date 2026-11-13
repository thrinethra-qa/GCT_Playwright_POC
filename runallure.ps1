
# GCT Playwright POC - Allure Report Runner

# Step 1: Run Behave tests and generate Allure results.
Write-Host "`nRunning GCT Behave tests..." -ForegroundColor Cyan

behave features/gct_tests.feature `
    --tags="not @intentional_failure" `
    -f allure_behave.formatter:AllureFormatter `
    -o allure-results `
    --no-capture

# Stop if the test execution command fails.
if ($LASTEXITCODE -ne 0) {
    Write-Host "Behave execution returned a failure." -ForegroundColor Red
}

# Step 2: Preserve history from the previous report.
if (Test-Path "allure-report\history") {
    Copy-Item "allure-report\history" `
        "allure-results\history" -Recurse -Force

    Write-Host "Previous Allure history copied." -ForegroundColor Green
}

# Step 3: Generate the updated Allure report.
Write-Host "`nGenerating Allure report..." -ForegroundColor Cyan

allure generate allure-results --clean -o allure-report

# Step 4: Open the report.
if ($LASTEXITCODE -eq 0) {
    Write-Host "Allure report generated successfully!" -ForegroundColor Green
    allure open allure-report
}
else {
    Write-Host "Allure report generation failed." -ForegroundColor Red
}
