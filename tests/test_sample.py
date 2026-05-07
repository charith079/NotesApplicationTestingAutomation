def test_open_browser(driver):
    driver.get("https://practice.expandtesting.com/notes/app")
    assert "Notes" in driver.title