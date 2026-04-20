# **🚀 EC2 CPU Alerting with AWS CloudWatch & SNS**

## **📌 Overview**

This project demonstrates how to monitor **EC2 CPU utilization** using **AWS CloudWatch**, trigger alarms when CPU usage crosses a threshold, and send real-time alerts through **Amazon SNS**.
A Python script is used to intentionally spike CPU usage on the EC2 instance to validate alerting behavior.

---

## **🧱 Architecture**

* 🖥️ **EC2 Instance (Ubuntu t2.micro)** — runs a Python script that simulates CPU spikes
* 📊 **AWS CloudWatch Metrics** — tracks real-time CPU utilization
* 🚨 **CloudWatch Alarm** — triggers when CPU crosses threshold (e.g., 50%)
* 📬 **Amazon SNS** — sends email alerts to subscribed users

---

## **🛠️ Steps to Reproduce**

### **1️⃣ Launch EC2 Instance**

* Choose **Ubuntu t2.micro**
* Enable **public IP**
* Attach your **key pair**
* SSH into instance:

```
ssh -i key.pem ubuntu@<public-ip>
```

---

### **2️⃣ Create the CPU Spike Script**

Create file:

```
nano CPU_spike.py
```

Run:

```
python3 CPU_spike.py
```

---

### **3️⃣ Monitor CPU Usage in CloudWatch**

* Go to **CloudWatch → Metrics → EC2**
* Select **CPUUtilization**
* Switch between **Maximum** and **Average**
* Observe spike after running the script 📈

---

### **4️⃣ Create a CloudWatch Alarm**

* Go to **CloudWatch → Alarms → Create alarm**
* Choose **EC2 → Per-Instance Metrics**
* Select **CPUUtilization**
* Statistic: **Maximum**
* Threshold: **50%** ⚠️

---

### **5️⃣ Configure SNS Notification**

* Create an **SNS Topic**
* Add your **email**
* Set custom message:

  > “⚠️ CPU Utilization crossed 50% — please take action.”

Confirm subscription via email 📩

---

### **6️⃣ Test the Alarm**

* Run CPU spike script again
* Alarm enters **ALARM** state 🚨
* Receive SNS email notification

---

## **🎯 Use Cases**

* Server performance monitoring
* Auto-scaling automation
* Production alerting systems
* Cost optimization through usage insights

---

## **🧰 Tech Stack**

* **AWS EC2**
* **AWS CloudWatch**
* **Amazon SNS**
* **Python**

---