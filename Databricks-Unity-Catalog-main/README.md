# 🧠 **Databricks Unity Catalog & Delta Lake Data Governance Project**

This project demonstrates the implementation of **Unity Catalog** in **Azure Databricks**, focusing on managing data governance, access control, and data organization through **catalogs, schemas, tables, and volumes**.

The notebook walks through real-time scenarios covering **managed and external data storage**, **Delta tables**, **views**, and **volumes** using **Azure Data Lake Storage (ADLS Gen2)**.

It provides a hands-on understanding of how Databricks handles **data lineage, retention, and recovery** (DROP/UNDROP), and integrates with **external cloud storage**.

---

### 🧩 Key Scenarios Implemented

| Scenario       | Type                                               | Description                                                      |
| -------------- | -------------------------------------------------- | ---------------------------------------------------------------- |
| **Scenario 1** | Managed Catalog → Managed Schema → Managed Table   | Demonstrates fully managed data within Databricks.               |
| **Scenario 2** | External Catalog → Managed Schema → Managed Table  | Catalog stored externally; Databricks manages schema and tables. |
| **Scenario 3** | External Catalog → External Schema → Managed Table | Complete control of storage locations via external definitions.  |
| **Scenario 4** | External Table                                     | Demonstrates linking external data to Databricks tables.         |

---

### ⚙️ Technologies & Tools

* **Azure Databricks**
* **Unity Catalog**
* **Delta Lake**
* **Azure Data Lake Storage Gen2 (ADLS)**
* **PySpark / Spark SQL**
* **Databricks Utilities (dbutils.fs)**
* **Delta File System (DFS) Integration**

---

### 🔍 Features Implemented

#### 🗂️ Managed Catalog, Schema, and Table

```sql
CREATE CATALOG man_cata;
CREATE SCHEMA man_cata.man_schema;
CREATE TABLE man_cata.man_schema.man_table (id INT, name STRING) USING DELTA;
```

* Data managed entirely within Databricks-managed storage.
* Metadata tracked automatically in the **Unity Catalog metastore**.

---

#### 🗄️ External Catalog (ADLS-Backed)

```sql
CREATE CATALOG ext_cata
MANAGED LOCATION 'abfss://mycontainer@storagemoderdb.dfs.core.windows.net/external_catalog';
```

* Uses **Azure Data Lake Storage** as an external managed location.
* Enables data sharing and governance beyond Databricks’ internal environment.

---

#### 🧱 External Schema & Table

```sql
CREATE SCHEMA ext_cata.ext_schema
MANAGED LOCATION 'abfss://mycontainer@storagemoderdb.dfs.core.windows.net/ext_schema';
```

* Schema stored externally.
* Demonstrates flexible hybrid storage management.

---

#### 📊 External Table with Location

```sql
CREATE TABLE man_cata.man_schema.ext_table
USING DELTA
LOCATION 'abfss://mycontainer@storagemoderdb.dfs.core.windows.net/ext_table/man_table3';
```

* Reads directly from ADLS Delta path.
* Supports **time travel**, **ACID transactions**, and **schema evolution**.

---

#### 🗑️ DROP & UNDROP Table

```sql
DROP TABLE man_cata.man_schema.man_table;
UNDROP TABLE man_cata.man_schema.man_table;
```

* Demonstrates Databricks’ **table recovery (Time Travel)** capabilities.

---

#### 🔎 Querying External Data

```sql
SELECT * FROM delta.`abfss://mycontainer@storagemoderdb.dfs.core.windows.net/ext_table/man_table3`
WHERE id = 1;
```

---

#### 👁️ Views in Databricks

**Permanent View:**

```sql
CREATE VIEW man_cata.man_schema.view1 AS
SELECT * FROM delta.`abfss://mycontainer@storagemoderdb.dfs.core.windows.net/ext_table/man_table3` WHERE id = 1;
```

**Temporary View:**

```sql
CREATE OR REPLACE TEMP VIEW temp_view AS
SELECT * FROM delta.`abfss://mycontainer@storagemoderdb.dfs.core.windows.net/ext_table/man_table3` WHERE id = 1;
```

---

#### 💾 Volumes (External Data Directory)

```sql
CREATE EXTERNAL VOLUME man_cata.man_schema.extvolume
LOCATION 'abfss://mycontainer@storagemoderdb.dfs.core.windows.net/volumes';
```

**Copying Files to Volume:**

```python
dbutils.fs.cp(
  'abfss://mycontainer@storagemoderdb.dfs.core.windows.net/source/Sales',
  'abfss://mycontainer@storagemoderdb.dfs.core.windows.net/volumes/Sales'
)
```

**Querying Data in Volume:**

```sql
SELECT * FROM csv.`/Volumes/man_cata/man_schema/extvolume/Sales`
```

---

### 🧠 Learning Outcomes

✅ Understand the differences between **managed** and **external** catalogs, schemas, and tables.
✅ Work with **Azure Data Lake integration** using ABFSS paths.
✅ Perform **data recovery** (UNDROP) using Delta Time Travel.
✅ Manage **permissions and governance** via Unity Catalog.
✅ Create **views and volumes** for reusable, modular data access.

---

### 🔐 Best Practices Followed

* Used **Delta Lake for ACID compliance**.
* Implemented **external storage segregation** for scalability.
* Followed **Unity Catalog hierarchy** (Catalog → Schema → Table).
* Cleaned up resources post-demo using `DROP` statements.

---

### 💼 Real-World Use Case

A **data platform team** in a large enterprise can use this architecture to:

* Manage **data across multiple environments (dev/staging/prod)**
* Centralize governance using **Unity Catalog**
* Enable secure data sharing across departments using **external catalogs**
* Recover accidentally dropped tables using **UNDROP functionality**

---

### 🧑‍💻 Author

**Pooja**
\
*Data Engineer (Machine Learning) | Cloud & DevOps Enthusiast*
\
📍 Project: *Databricks Unity Catalog & Delta Lake Data Governance*
