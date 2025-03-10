# Setup Guide for Visual Tests
 
## Prerequisites
0. Install Cursor AI (recommended IDE)
1. Clone/download project and open with Cursor AI (or PyCharm)
 
## Python Setup
1. Create virtual environment (in project directory):
   ```bash
   python3 -m venv .venv
   ```
 
2. Activate virtual environment:
   ```bash
   # On Mac/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```
 
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
 
## Environment Setup
4. Create `.env` file in project root with:
   ```
   BASE_URL=https://vcst-qa-storefront.govirto.com
   USER_EMAIL=auto@visual.com
   PASSWORD=Password1!
   BACK_URL=https://vcst-qa.govirto.com
   API_KEY=ab9c17c3-fba0-45dc-b2cc-7bd07d4096e2
   SELENIUM_REMOTE_URL=http://localhost:4444
   ```
 
## Docker Setup
5. Install Docker Desktop from https://www.docker.com/products/docker-desktop/
 
6. Run Selenium Grid container:
   ```bash
   docker run --rm -d -p 4444:4444 -p 5900:5900 --shm-size="2g" \
   -e SE_NODE_GRID_URL="http://localhost:4444" \
   --platform linux/amd64 \
   selenium/standalone-chrome
   ```
 
## Remote Desktop Viewer Setup
7. Install a VNC viewer (required for test observation):
   - Recommended: RealVNC Viewer
     - Windows: https://www.realvnc.com/en/connect/download/viewer/
     - Mac: Screen Sharing Utility (built-in)
   - Alternative options:
     - TightVNC
     - UltraVNC
     - Any VNC client of your choice
 
8. Connect to running tests:
   - Open your VNC viewer
   - Connect to: `localhost:5900`
   - Password: `secret`
 
## Running Your First Test
9. Run the login test:
   ```bash
   # Make sure you're in the project directory and virtual environment is activated
   pytest tests_visual/tests/test_login_visual.py
   ```
   You should see:
   - Test execution in your VNC viewer
   - Test results in your terminal

## Code Formatting

This project uses Black for automatic code formatting.

### Usage

When committing code, the formatting workflow is:

1. Try to commit:
```bash
git commit -m "your message"
```

2. Black will automatically:
   - Check all Python files
   - Fix formatting issues
   - Show which files were modified
   - Fail the commit if any files were changed

3. If Black made changes:
   - Review the changes (choose any):
     - Check Black's output in terminal
     - Use `git diff` to see detailed changes (press 'q' to exit)
     - Open modified files in your editor
   - Stage the reformatted files: `git add .`
   - Commit again with the same message

This ensures all code follows consistent formatting standards.