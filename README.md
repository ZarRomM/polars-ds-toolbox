# Polars Data Science Toolbox

**A community-driven collection of utility extensions for Polars DataFrames designed to streamline Exploratory Data Analysis (EDA) and data cleaning workflows.**

This project extends the native functionality of Polars by adding methods that many Data Scientists miss from other libraries (like Pandas), allowing for faster insights and cleaner code.

---

## 🚀 Key Features

This toolbox uses "monkey patching" to attach new methods directly to your Polars DataFrames:

* **`df.info()`**: A complete replica of the Pandas `.info()` method. It provides a concise summary of the DataFrame, including index types, column data types, non-null counts, and memory usage.
* **`df.null_report()`**: Generates a detailed, sorted report of missing values (counts and percentages) to quickly identify data quality issues.
* **`df.clean_names()`**: Automatically standardizes all column names to `snake_case` (lowercase with underscores), removing spaces and special characters for easier coding.

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/ZarRomM/polars-ds-toolbox.git](https://github.com/ZarRomM/polars-ds-toolbox.git)
    cd polars-ds-toolbox
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

Simply import the `toolbox` module at the beginning of your script. The extensions are registered automatically upon import.

```python
import polars as pl
import toolbox  # ⚡ This line activates the extensions!

# Load your data
df = pl.read_csv("dataset.csv")

# 1. Get a quick overview (Pandas style)
df.info()

# 2. Analyze missing values
df.null_report()

# 3. Clean column names for better usability
df = df.clean_names()
