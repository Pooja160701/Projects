# 🏗️ **Netflix Azure Data Engineering Project — End-to-End ETL Pipeline using Databricks Auto Loader and Delta Live Tables**

### 🎬 Project Overview

This project demonstrates a **real-time data engineering pipeline on Azure** using **Databricks**, **Delta Lake**, and **Azure Data Lake Storage (ADLS Gen2)**.

The pipeline ingests, processes, and transforms Netflix dataset files through **Bronze–Silver–Gold architecture**, leveraging **Auto Loader** for incremental ingestion and **Delta Live Tables (DLT)** for quality enforcement and pipeline orchestration.

It showcases how modern data platforms handle **incremental data loading, schema evolution, transformation, and validation** efficiently and reliably.

---

### 🧩 **Architecture Layers**

| Layer            | Technology                         | Description                                                                       |
| ---------------- | ---------------------------------- | --------------------------------------------------------------------------------- |
| **Raw (Source)** | CSV files in ADLS Gen2             | Unprocessed Netflix datasets.                                                     |
| **Bronze**       | Databricks Auto Loader (Streaming) | Incrementally ingests raw CSV data into Delta format.                             |
| **Silver**       | Spark SQL & PySpark                | Cleans, transforms, and enriches data for analytics.                              |
| **Gold**         | Delta Live Tables (DLT)            | Applies business logic, data quality rules, and generates analytics-ready tables. |

---

### ⚙️ **Technologies Used**

* **Azure Databricks**
* **Azure Data Lake Storage Gen2 (ADLS)**
* **PySpark / Spark SQL**
* **Delta Lake & Delta Live Tables (DLT)**
* **Auto Loader (cloudFiles)**
* **Databricks Jobs & Widgets**
* **Python & Structured Streaming**

---

### 📁 **Project Structure**

```
Netflix_Azure_Data_Engineering_Project/
│
├── 1_Autoloader.dbc                 # Incremental ingestion from Raw → Bronze using Auto Loader
├── 2_Silver.dbc                     # Silver layer transformations
├── 3_lookupNotebook.dbc             # Lookup arrays for metadata
├── 4_Silver.dbc                     # Feature engineering and aggregation
├── 5_lookupNotebook.dbc             # Parameter passing for jobs
├── 6_falsenotebook.dbc              # Task value handling between jobs
├── 7_DLT_Notebook.dbc               # Gold layer pipeline using DLT
├── RawData/                         # Source Netflix CSV files
│    ├── netflix_titles.csv
│    ├── netflix_cast.csv
│    ├── netflix_countries.csv
│    ├── netflix_directors.csv
│    ├── netflix_category.csv
└── README.md                        # Documentation
```

---

### 🚀 **Pipeline Workflow**

#### 🥉 **1️⃣ Bronze Layer (Incremental Ingestion)**

**Notebook:** `1_Autoloader.dbc`

* Uses **Databricks Auto Loader** to continuously ingest CSV files from ADLS Gen2 raw container.
* Schema tracking via **checkpoint** for new files.

```python
df = spark.readStream.format("cloudFiles")\
  .option("cloudFiles.format", "csv")\
  .option("cloudFiles.schemaLocation", checkpoint_location)\
  .load("abfss://raw@netflixprojectdlansh.dfs.core.windows.net")

df.writeStream.option("checkpointLocation", checkpoint_location)\
  .trigger(processingTime='10 seconds')\
  .start("abfss://bronze@netflixprojectdlansh.dfs.core.windows.net/netflix_titles")
```

✅ *Result:* Raw Netflix data stored as Delta tables in **Bronze** layer.

---

#### 🥈 **2️⃣ Silver Layer (Data Transformation)**

**Notebook:** `2_Silver.dbc` & `4_Silver.dbc`

* Reads Bronze data, cleans nulls, casts data types, and derives new columns (`Shorttitle`, `type_flag`, etc.).
* Uses **window functions** for duration ranking.
* Stores transformed data in **Silver container** as Delta tables.

---

#### 🧩 **3️⃣ Lookup Tables**

**Notebook:** `3_lookupNotebook.dbc`

* Defines lookup arrays for `directors`, `cast`, `countries`, and `category` datasets.
* Uses Databricks job utilities to dynamically pass values to downstream tasks.

---

#### 🪙 **4️⃣ Gold Layer (Delta Live Tables)**

**Notebook:** `7_DLT_Notebook.dbc`

* Implements **Delta Live Tables (DLT)** for real-time transformation and validation.
* Uses **expectations (data quality rules)** such as `show_id IS NOT NULL`.
* Creates live streaming tables like `gold_netflixdirectors`, `gold_netflixcountries`, `gold_netflixtitles`.

```python
@dlt.table
@dlt.expect_all_or_drop({"rule1": "show_id is NOT NULL"})
def gold_netflixtitles():
    df = spark.readStream.table("LIVE.gold_trns_netflixtitles")
    return df
```

✅ *Result:* Gold Delta tables ready for analytics and reporting.

---

### 🧠 **Key Features**

* 🔁 **Incremental streaming ingestion** using Auto Loader.
* 🧹 **Data cleaning and standardization** with PySpark transformations.
* 🧱 **Delta Lake ACID compliance** for reliable table operations.
* ✅ **DLT-based data quality validation** ensuring clean production datasets.
* 🔧 **Dynamic parameter passing** across notebooks using Databricks widgets and job utilities.
* 📈 **Multi-layer data architecture (Bronze → Silver → Gold)** aligning with the Medallion Architecture pattern.

---

### 💾 **Sample Data Sources**

* `netflix_titles.csv`
* `netflix_cast.csv`
* `netflix_directors.csv`
* `netflix_countries.csv`
* `netflix_category.csv`

---

### 🧰 **How to Run**

1. Upload `.dbc` notebooks to Databricks workspace.
2. Connect Databricks to **Azure Data Lake Storage Gen2** via **Service Principal or Key Vault**.
3. Update storage paths for:

   * Raw data → `abfss://raw@...`
   * Bronze → `abfss://bronze@...`
   * Silver → `abfss://silver@...`
4. Execute notebooks in order:

   * `1_Autoloader.dbc`
   * `2_Silver.dbc`
   * `4_Silver.dbc`
   * `7_DLT_Notebook.dbc`

---

### 📊 **Visualization & Insights**

Example visualization using:

```python
df_vis = df.groupBy("type").agg(count("*").alias("total_count"))
display(df_vis)
```

Produces insights on total **Movies vs TV Shows** on Netflix.

---

### 🧾 **Learning Outcomes**

✅ Design and implement **end-to-end ETL pipelines** using Databricks & ADLS.
✅ Understand the **Medallion Architecture (Bronze, Silver, Gold)** pattern.
✅ Use **Auto Loader for streaming ingestion** and **DLT for validation**.
✅ Leverage **PySpark transformations and window functions** for analytics.
✅ Apply **data quality rules and governance** in DLT pipelines.

---

### 👩‍💻 **Author**

**Pooja**
\
*Data Engineer | Cloud & DevOps Enthusiast*
\
📍 Project: *Netflix Azure Data Engineering Pipeline using Auto Loader & Delta Live Tables*