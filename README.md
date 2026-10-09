[README.md](https://github.com/user-attachments/files/33268482/README.md)
# NLP Log Triage

Organize application logs into technical categories and produce a summary by category and severity.

## Tools

Python, pandas, regular expressions

## Workflow

1. Normalize message case and whitespace.
2. Categorize messages using ordered keyword rules.
3. Extract explicit ERROR, WARN and INFO severity labels.
4. Preserve unmatched messages as uncategorized.
5. Export classified logs, summary counts and example evaluation metrics.

## Data and method

Uses fictional application logs and rule-based text processing. When multiple rules match, the first category is selected.

## Run locally

```bash
python -m pip install -r requirements.txt
python main.py
```

For the package versions used to verify the project, install `requirements-tested.txt` instead.

## Run in Google Colab

Upload `project.ipynb` to Google Colab and select **Run all**.

## Files

- `main.py`: executable Python script.
- `project.ipynb`: notebook with the same workflow and example outputs.
- `requirements.txt`: required Python packages.
- `requirements-tested.txt`: package versions used for verification.
- `outputs/`: generated data, reports and results.

## About

This is a learning project prepared with AI assistance.
