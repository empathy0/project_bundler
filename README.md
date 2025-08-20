### How to Use

1.  **Save the Script:** Save the code above into a file named `bundle_project.py` in your project's root directory (or anywhere else on your system).

2.  **Open Your Terminal:** Navigate to your project's root directory.
    ```bash
    cd /path/to/your/project
    ```

3.  **Run the Script:**

    *   **Basic Usage (uses defaults):**
        This will scan the current directory (`.`), respect `.gitignore`, and create `project_bundle.md`.
        ```bash
        python bundle_project.py
        ```

    *   **Specify Output File:**
        ```bash
        python bundle_project.py --output my_ai_prompt.md
        ```

    *   **Specify Project Directory:**
        If you saved the script elsewhere, you can point it to your project.
        ```bash
        python /path/to/bundle_project.py --root /path/to/your/project
        ```

    *   **Specify Which File Types to Include:**
        This will *only* include Python and JavaScript files.
        ```bash
        python bundle_project.py --include .py .js
        ```

4.  **Use the Output:** A file named `project_bundle.md` (or your custom name) will be created. You can open this file, copy its entire content, and paste it into your AI chat prompt.

### Example Output (`project_bundle.md`)

The generated file will look something like this:

```markdown
# Project Bundle: my-awesome-app

This file contains a bundle of all relevant code files from the project, formatted for use with an AI.
Each file's content is enclosed in a Markdown code block, with its original path specified.

---

**File:** `src/main.py`

```python
import utils

def main():
    """The main entry point of the application."""
    print("Hello, World!")
    utils.helper_function()

if __name__ == "__main__":
    main()
```

---

**File:** `src/utils.py`

```python
def helper_function():
    """A simple helper function."""
    print("This is the helper function speaking.")
```

---

**File:** `README.md`

```markdown
# My Awesome App

This is a sample project to demonstrate the bundler script.
```

```

This structured format is highly effective for giving an AI the full context of your project's codebase.