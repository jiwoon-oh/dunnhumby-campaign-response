# Data

The analysis uses the dunnhumby *The Complete Journey* dataset: household-level grocery transactions of about 2,500 frequent shoppers over two years, with household demographics and direct-marketing (campaign) history for some households.

The CSV files are not in this repository (they are git-ignored). Download them and place them in this folder.

| Item | Value |
|---|---|
| Source | dunnhumby, [Source Files](https://www.dunnhumby.com/source-files/) page, entry "The Complete Journey" (the page links a download; it lists no file names, so the names below are the ones the notebooks read) |
| Files | `transaction_data.csv`, `campaign_table.csv`, `campaign_desc.csv` (also `hh_demographic.csv`, `product.csv`, `coupon.csv`, `coupon_redempt.csv`, `causal_data.csv`, which only the overview notebook reads) |
| Location | `data/` (the notebooks read `DATA_DIR / "<file>.csv"`, where `DATA_DIR` comes from `config.py`) |
| Size | `transaction_data.csv` is about 135 MB (2,595,732 rows) |

Household-level files that the notebooks write (for example `campaign_households.csv`) go to `outputs/intermediate/` and are git-ignored.

Why the files are not here: the dunnhumby page shows no redistribution terms, so I do not redistribute the data, and the main table is large. Please check dunnhumby's terms on that page before reuse.
