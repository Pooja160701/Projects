## 📁 **Project Name:** GitHub-Collaborator-Access-Checker

---

### 🧠 **Project Overview**

In many organizations, developers or DevOps engineers frequently need to verify **who has access** to specific GitHub repositories.
However, users without **admin rights** or **access to the Settings → Collaborators** tab cannot view this information directly.

This project automates that task using the **GitHub REST API**, allowing you to list all users with **read access (pull permission)** to a given repository — without logging into GitHub.

You’ll use:

* **GitHub API** for data access
* **curl** for making HTTP requests
* **jq** for JSON parsing
* **Shell scripting** for automation

---

### ⚙️ **Technologies Used**

* 🐚 **Bash (Shell Scripting)**
* 🌐 **GitHub API**
* 🧰 **curl** (HTTP client)
* 🔍 **jq** (JSON processor)
* ☁️ **EC2 instance** (Ubuntu environment for deployment and testing)

---

### 📁 **Project Structure**

```
GitHub-Collaborator-Access-Checker/
│
├── list-users.sh          # Main script file
└── README.md              # Documentation
```

---

### 🔑 **Environment Setup (Pre-requisites)**

#### 1️⃣ Generate a Personal Access Token (PAT)

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (Classic)**
2. Click **Generate new token (classic)**
3. Select the following scopes:

   * ✅ `repo` (Full control of private repositories)
   * ✅ `read:org`
4. Copy and securely store your token.

---

#### 2️⃣ Export Environment Variables

```bash
export username="your_github_username"
export token="ghp_your_generated_token"
```

---

#### 3️⃣ Install jq

```bash
sudo apt update
sudo apt install jq -y
```

---

#### 4️⃣ Make Script Executable

```bash
chmod +x list-users.sh
```

---

#### 5️⃣ Run the Script

```bash
./list-users.sh <repo_owner> <repo_name>
```

---

### 🧾 **Example Output (`sample_output.txt`)**

```
Listing users with read access to devops-by-examples/python...

Users with read access to devops-by-examples/python:
pooja-devops
teammate1
teammate2
```

---

### 🧠 **Explanation of Key Components**

| Section                           | Description                                                                            |
| --------------------------------- | -------------------------------------------------------------------------------------- |
| **helper()**                      | Validates the number of command-line arguments and prints usage instructions.          |
| **github_api_get()**              | Uses `curl` to make authenticated API requests to GitHub.                              |
| **list_users_with_read_access()** | Filters collaborator data to show only users with `pull` (read) permission using `jq`. |
| **Environment Variables**         | Keeps credentials secure and avoids hardcoding tokens in the script.                   |

---

### 🧩 **Real-World Use Case**

* DevOps teams can automate repository access audits.
* Managers can schedule this script to run daily or weekly via `cron` to monitor access changes.
* Useful for compliance or access review processes in CI/CD pipelines.

---

### 🕒 **Optional Automation with Cron**

To schedule the script daily at 8 PM:

```bash
crontab -e
```

Then add:

```bash
0 20 * * * /full/path/to/GitHub-Collaborator-Access-Checker/list-users.sh octocat Hello-World >> collaborator_report.txt
```

---

### 🔐 **Security Note**

⚠️ **Never commit your GitHub token or credentials** to public repositories.

To prevent accidental exposure:

1. Add this to `.gitignore`:

   ```bash
   echo "collaborator_report.txt" >> .gitignore
   echo "list-users.sh" >> .gitignore
   ```

   *(only if you keep real credentials or outputs inside)*

2. Use **environment variables or AWS Secrets Manager** to store tokens safely.

---

### 🧱 **Future Enhancements**

* Send collaborator list via **email or Slack webhook**
* Integrate with **GitHub Actions** for scheduled reporting
* Add **filters for permission types (admin, write, read)**

---

### 👩‍💻 **Author**

**Pooja**
\
DevOps & Cloud Enthusiast ☁️
\
📍 Project: *GitHub API Integration using Shell Script*