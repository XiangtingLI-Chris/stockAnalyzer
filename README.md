# stockAnalyzer

A multi-stage Python stock analysis project for the China A-share market.  
This project combines announcement scraping, text-based sentiment analysis, multi-year price screening, monthly pattern mining, and simplified reason tagging to identify potentially recurring bullish signals.

## Background

This project was originally built as a practical internal-style side project during my internship.  
Because the development environment at that time was isolated from GitHub, the code history was not managed online during development.  
This repository is a later organized and public upload of the project for portfolio and learning purposes.

## Project Goal

The goal of this project is to explore a structured workflow for stock signal discovery in the China A-share market:

1. Collect stock-related announcements
2. Extract and analyze article content
3. Identify potentially positive announcements
4. Combine announcement results with historical stock price data
5. Screen for stocks with strong percentage-change events
6. Mine repeated monthly upward patterns across multiple years
7. Add simplified reason labels for easier interpretation

Rather than serving as a production trading system, this project is better understood as an exploratory data-analysis pipeline.

## Tech Stack

- Python
- Pandas
- AkShare
- Web scraping / content extraction
- Excel / CSV export

## Repository Structure

```text
stockAnalyzer/
├── Project/
│   ├── Stage_01/
│   ├── Stage_02/
│   ├── Stage_03/
│   └── Stage_04/
└── selfLearning/
```

## Workflow Overview

### Stage 01 - Announcement Collection and Sentiment Filtering

This stage focuses on stock announcement analysis.

Main tasks:
- Filter stock announcement links
- Extract article text content
- Analyze article sentiment
- Retrieve target stock information
- Query historical stock price range and current price
- Output announcements judged as positive

Key idea:
- If an announcement is classified as **bullish**, the stock is kept for further attention.

Typical modules:
- `contentScrap.py`
- `articleAnalyse.py`
- `stockDataAnalyse.py`
- `pipeline.py`
- `main.py`

---

### Stage 02 - Multi-Year Daily Price Screening

This stage focuses on large-scale historical price screening across A-share stocks.

Main tasks:
- Fetch stock list
- Build a multi-year date range
- Pull daily historical price data using AkShare
- Filter trading days whose `pct_chg` is above a threshold
- Save batch results to CSV
- Merge batch outputs into a final result table

Typical screening logic:
- Keep rows where percentage change is greater than or equal to a chosen threshold
- Preserve key fields such as:
  - `trade_date`
  - `code`
  - `name`
  - `open`
  - `pct_chg`

Typical modules:
- `akshare_client.py`
- `config.py`
- `pipeline.py`
- `main.py`

---

### Stage 03 - Monthly Pattern Mining

This stage takes Stage 02 output and looks for repeated month-level patterns.

Main tasks:
- Parse dates into year / month / year-month fields
- Count upward-hit frequency for each stock in each month
- Detect stocks that show upward records in the same month across multiple years
- Export the filtered recurring-month results

Example idea:
- If a stock repeatedly appears in the same month across several different years, that month may indicate a recurring seasonal or event-driven pattern worth further investigation.

Typical modules:
- `analysis_monthly.py`
- `io_stage2.py`
- `export.py`
- `config.py`
- `main.py`

---

### Stage 04 - Simplified Reason Tagging

This stage adds a lightweight interpretation layer to the screened results.

Main tasks:
- Read the Stage 03 outputs
- Match or infer simplified “reason” labels
- Produce a more readable final result set for downstream inspection

This stage is not intended to provide rigorous causal inference.  
Its purpose is to improve interpretability and make the output easier to review manually.

Typical modules:
- `analyze_reason.py`
- `pipeline.py`
- `config.py`
- `main.py`

## Output

Depending on the stage, the project produces:
- intermediate CSV files
- Excel result files
- filtered stock hit tables
- monthly recurring-pattern summaries

## How to Run

Because this repository was originally developed stage by stage, each stage has its own entry script.

In general, you can run a stage with:

```text
cd Project/Stage_01
python main.py
```

or

```text
cd Project/Stage_02
python main.py
```

and similarly for `Stage_03` and `Stage_04`.

## Notes

- This project is intended for research, learning, and portfolio demonstration.
- It is not financial advice.
- Some modules and outputs reflect the exploratory nature of the original internship-side implementation.
- The repository may still be improved with:
  - a root-level dependency file
  - a unified configuration interface
  - better logging
  - result screenshots
  - cleaned ignored files such as IDE metadata

## What I Learned

Through this project, I practiced:

- structuring a multi-stage data pipeline
- combining text analysis with market data
- using Pandas for data transformation
- working with AkShare for A-share historical data retrieval
- exporting analysis results for manual review
- organizing a project around iterative analysis stages

## Future Improvements

Possible next steps:
- add a root `requirements.txt`
- add a top-level orchestrator script
- improve sentiment classification quality
- replace heuristic reason tagging with a stronger NLP approach
- add better exception handling and logging
- visualize recurring monthly patterns
- add unit tests and sample datasets

## Disclaimer

This repository is for educational and portfolio purposes only.  
It does not constitute investment advice or a production-grade trading system.
