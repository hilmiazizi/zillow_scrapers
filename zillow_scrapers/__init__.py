from playwright.sync_api import sync_playwright

# Auto-install Playwright browsers when the package is installed
def install_playwright():
    import subprocess
    subprocess.run(["playwright", "install"], check=True)


if __name__ == "__main__":
    install_playwright()