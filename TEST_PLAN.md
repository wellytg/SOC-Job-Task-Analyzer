# Local Test Plan: SOC-Job-Task-Analyzer

Follow these steps to verify that the project is correctly set up and the analysis pipeline is functional.

## **Prerequisites**
- Python 3.10+ installed.
- VS Code installed with the **Python Extension** (by Microsoft).

---

## **Step 1: Environment Setup**
1.  Open VS Code in the project root: `C:\Core_Workspace\02_Projects\SOC-Job-Task-Analyzer`.
2.  Open the integrated terminal (`Ctrl + ` `).
3.  Create a fresh virtual environment:
    ```powershell
    python -m venv venv
    ```
4.  Activate the environment:
    ```powershell
    .\venv\Scripts\activate
    ```
5.  Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```

---

## **Step 2: Verify Rule-Based Classification**
We will test if the `data_analyzer.py` can process a sample file using your `rules.json`.

1.  **Prepare Test Data**: 
    Ensure you have at least one `.csv` file in `data/processed/`. (e.g., `soc_jobs_flattened_20251029_192918.csv`).
2.  **Run the Script**:
    ```powershell
    python src/data_analyzer.py data/processed/soc_jobs_flattened_20251029_192918.csv configs/rules.json
    ```
3.  **Expected Output**:
    - The terminal should show "Loading and consolidating...", "De-duplicating...", and "Classifying titles...".
    - A summary JSON report and two new CSV files (SOC Tier 1 and Unclassified) should appear in `data/processed/`.

---

## **Step 3: Verify Scraper Setup (Optional)**
1.  Open `src/soc_scrapper_API.py`.
2.  Check if you have your API keys configured (e.g., in a `.env` file or directly in the script for local testing).
3.  Run the script:
    ```powershell
    python src/soc_scrapper_API.py
    ```
4.  **Expected Output**: A new `.json` file should be generated in `data/raw/`.

---

## **Step 4: VS Code Integration Tips**
- **Select Interpreter**: Press `Ctrl + Shift + P`, type "Python: Select Interpreter", and choose the one in your `./venv/`.
- **Debugging**: Open `src/data_analyzer.py`, set a breakpoint (click the red dot next to line numbers), and press `F5` to debug the execution.
- **Git**: Use the "Source Control" tab (`Ctrl + Shift + G`) to see changes and sync with GitHub.
