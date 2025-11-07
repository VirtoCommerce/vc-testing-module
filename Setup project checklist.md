# VirtoCommerce E2E Testing - Project Setup Checklist

## ✅ Prerequisites

- [ ] **Python 3.7+** installed
  - Check version: `python --version`
  
- [ ] **pip** (Python package manager) installed
  - Check version: `pip --version`
  
- [ ] **Git** installed
  - Check version: `git --version`
  
- [ ] **IDE installed** (Cursor AI recommended, or PyCharm)

- [ ] **GitHub access** to VirtoCommerce/vc-testing-module repository

---

## 📥 Step 1: Clone the Repository

- [ ] Open terminal/command prompt

- [ ] Clone the repository:
  ```bash
  git clone https://github.com/VirtoCommerce/vc-testing-module
  ```

- [ ] Navigate to project directory:
  ```bash
  cd vc-testing-module
  ```

- [ ] Verify you're in the correct directory:
  ```bash
  ls  # Should see requirements.txt, tests_graphql/, tests_e2e/, etc.
  ```

---

## 🐍 Step 2: Create Virtual Environment

- [ ] Create virtual environment:
  ```bash
  python -m venv .venv
  ```

- [ ] Activate virtual environment:
  
  **On macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```
  
  **On Windows:**
  ```bash
  .venv\Scripts\activate
  ```

- [ ] Verify activation (you should see `(.venv)` in your terminal prompt)

---

## 📦 Step 3: Install Python Dependencies

- [ ] Upgrade pip:
  ```bash
  python -m pip install --upgrade pip
  ```

- [ ] Install project dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Wait for installation to complete (this may take a few minutes)

- [ ] Verify installation (no errors should appear)

---

## 🔧 Step 4: Install Pre-commit Hooks

⚠️ **Important: This step must be done manually!**

- [ ] Install pre-commit hooks:
  ```bash
  pre-commit install
  ```

- [ ] Verify installation:
  ```bash
  pre-commit --version
  ```

- [ ] You should see a message: "pre-commit installed at .git/hooks/pre-commit"

---

## 🎭 Step 5: Install Playwright Browsers

- [ ] Install Playwright browsers:
  ```bash
  playwright install
  ```

- [ ] Wait for browser downloads to complete (this downloads Chromium, Firefox, and WebKit)

- [ ] Verify Playwright installation:
  ```bash
  python -c "import playwright; print(playwright.__version__)"
  ```

- [ ] Should print Playwright version number without errors

---

## 🔐 Step 6: Configure Environment Variables

- [ ] Create `.env` file in the project root:
  ```bash
  touch .env  # On macOS/Linux
  type nul > .env  # On Windows
  ```

- [ ] Open `.env` file in your editor

- [ ] Replace values:
  ```
  FRONTEND_BASE_URL=your_frontend_base_url
  BACKEND_BASE_URL=your_backend_base_url
   
  STORE_ID=dataset_store_id
 
  ADMIN_USERNAME=your_admin_name
  ADMIN_PASSWORD=your_admin_password
  USERS_PASSWORD=dataset_user_password
  ```

- [ ] Replace values with actual data (get from team)

- [ ] Save the file

- [ ] **Important:** Verify `.env` is in `.gitignore` (should already be there)

---

## 🗄️ Step 7: Seed Test Data (Optional)

- [ ] Run dataset seeder:
  ```bash
  python -m dataset.dataset_seeder
  ```

- [ ] Wait for completion

- [ ] Check for any error messages

---

## 🧪 Step 8: Verify Installation - Run Tests

### Test GraphQL Tests

- [ ] Run GraphQL test suite:
  ```bash
  pytest -v -s tests_graphql/tests/
  ```

- [ ] Verify tests execute (some may fail if environment is not fully configured)

### Test E2E Tests

- [ ] Run E2E tests in headless mode:
  ```bash
  pytest tests_e2e/tests/ -v -s
  ```

- [ ] Run E2E tests with visible browser:
  ```bash
  pytest tests_e2e/tests/ -v -s --show-browser
  ```

- [ ] Browser should open and tests should run

---

## 🎯 Step 9: Test Custom Options

- [ ] Test checkout mode options:
  ```bash
  pytest tests_e2e/tests/ --checkout-mode single-page --show-browser
  pytest tests_e2e/tests/ --checkout-mode multi-step --show-browser
  ```

- [ ] Test product quantity control options:
  ```bash
  pytest tests_e2e/tests/ --product-quantity-control stepper --show-browser
  pytest tests_e2e/tests/ --product-quantity-control button --show-browser
  ```

- [ ] All options should work without errors

---

## 📝 Step 10: IDE Configuration

### For Cursor AI / VS Code:

- [ ] Open project in Cursor AI:
  ```bash
  cursor .  # If cursor command is available
  ```

- [ ] Select Python interpreter:
  - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
  - Type "Python: Select Interpreter"
  - Choose the `.venv` interpreter

- [ ] Install recommended extensions:
  - Python
  - Pylance
  - Playwright Test for VSCode

### For PyCharm:

- [ ] Open project in PyCharm

- [ ] Configure Python interpreter:
  - Go to Settings → Project → Python Interpreter
  - Select the `.venv/bin/python` interpreter

- [ ] Mark directories:
  - Right-click on test directories
  - Mark as "Test Sources Root"

---

## ✨ Step 11: Final Verification

- [ ] **Virtual environment activated** (check terminal prompt)

- [ ] **Pre-commit hooks working:**
  ```bash
  pre-commit run --all-files
  ```

- [ ] **All tests can be discovered:**
  ```bash
  pytest --collect-only
  ```

- [ ] **Environment variables loaded:**
  ```bash
  python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('TOKEN:', 'SET' if os.getenv('TOKEN') else 'NOT SET')"
  ```

- [ ] **Can run specific test:**
  ```bash
  pytest tests_graphql/tests/ -k "test" --collect-only
  ```

---

## 🚀 Success!

If all checkboxes are complete, your environment is ready! 

### Next Steps:

- [ ] Review the project structure
- [ ] Read through existing tests
- [ ] Try modifying a simple test
- [ ] Run your first test successfully
- [ ] Attend team onboarding session

---

## 🆘 Troubleshooting

### Common Issues:

**Virtual environment not activating:**
- Make sure you're in the project directory
- Try creating venv again: `python -m venv .venv --clear`

**Playwright browsers not installing:**
- Run with sudo/admin if needed: `sudo playwright install`
- Or: `playwright install --with-deps`

**Tests failing:**
- Check if `.env` file has correct token
- Verify network connection to test environment
- Check if test environment is running

**Pre-commit hooks not working:**
- Reinstall: `pre-commit uninstall && pre-commit install`
- Update: `pre-commit autoupdate`

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

## 📞 Need Help?

- Check project README: https://github.com/VirtoCommerce/vc-testing-module
- Contact team lead
- Ask in team chat channel 
- Review Playwright docs: https://playwright.dev/python/
- Python https://www.python.org/downloads/

