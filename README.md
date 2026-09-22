# ⛑️ Employee Management API — AI-Integrated🤖 CI/CD Pipeline 

An end-to-end DevOps portfolio project demonstrating **CI/CD automation, Docker, Amazon ECR, Amazon EKS, Kubernetes, Prometheus, Grafana, SonarQube, and Anthropic Claude AI integration**.

---

## 📌 Project Overview

This project contains a **Spring Boot Employee Management REST API** with an automated CI/CD pipeline.

A simple `git push` triggers:

```text
GitHub
   ↓
Jenkins
   ↓
Maven Build & Test
   ↓
SonarQube Quality Gate
   ↓
Docker Build
   ↓
Amazon ECR
   ↓
Amazon EKS
   ↓
Monitoring Verification
   ↓
AI Release Notes

```
The application itself is the vehicle; the main project focus is the DevOps automation around the application.

## 🏗️ Architecture

```
Developer
    │
    │ git push
    ▼
 GitHub
    │
    │ Webhook
    ▼
 Jenkins
    │
    ├── Build & Test
    ├── JaCoCo
    ├── SonarQube
    ├── Quality Gate
    ├── Docker Build & Push
    ├── Deploy to EKS
    ├── Verify Monitoring
    └── AI Release Notes
              │
              ▼
         Amazon EKS
         ┌───────────────┐
         │ Employee API  │
         │ 2 Pods        │
         └───────┬───────┘
                 │
                 │ /actuator/prometheus
                 ▼
          ServiceMonitor
                 │
                 ▼
            Prometheus
                 │
                 ▼
             Grafana

AI FAILURE FLOW

Jenkins Failure
      ↓
Jenkins Log
      ↓
analyze_failure.py
      ↓
Claude API
      ↓
Root Cause / Exact Fix / Prevention
      ↓
ai_failure_summary.md
```
## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Java 17 | Application |
| Spring Boot | REST API |
| Maven | Build & dependency management |
| JaCoCo | Test coverage |
| SonarQube | Code quality |
| Jenkins | CI/CD |
| Docker | Containerization |
| Amazon ECR | Docker registry |
| Amazon EKS | Kubernetes platform |
| Kubernetes | Deployment & scaling |
| HPA | Auto scaling |
| Helm | Kubernetes package management |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |
| GitHub | Source control |
| Anthropic Claude | AI-assisted automation |


## 🔄 CI/CD Pipeline
The Jenkins pipeline contains 8 stages:
```
1. Checkout
2. Build & Unit Test
3. SonarQube Analysis
4. Quality Gate
5. Docker Build & Push
6. Deploy to EKS
7. Verify Monitoring
8. AI: Generate Release Notes
```
## Pipeline Flow

```
Git Push
   ↓
Jenkins
   ↓
Maven Build + Test
   ↓
SonarQube
   ↓
Quality Gate
   ↓
Docker
   ↓
Amazon ECR
   ↓
Amazon EKS
```
# ☸️ Kubernetes Deployment

The application is deployed to **Amazon EKS** with:

- **2 replicas**
  - Provides high availability
- **Kubernetes `LoadBalancer` Service**
  - Exposes the application externally
- **Readiness Probe**
  - Ensures traffic is sent only to ready pods
- **Liveness Probe**
  - Restarts unhealthy containers
- **Horizontal Pod Autoscaler (HPA)**
  - Scales pods based on CPU utilization
- **CPU requests and limits**
  - Defines container resource requirements

## HPA Configuration

```
Minimum replicas: 2
Maximum replicas: 6
CPU target: 70%
```
## 📊 Monitoring — Prometheus + Grafana

Spring Boot Actuator exposes:

```
/actuator/prometheus
```

Prometheus discovers the application through a Kubernetes ServiceMonitor.

```
Employee API
     ↓
/actuator/prometheus
     ↓
ServiceMonitor
     ↓
Prometheus
     ↓
Grafana
```
### 📊 Monitoring Components

- **Prometheus** – Metrics collection and monitoring
- **Grafana** – Metrics visualization and dashboards
- **Alertmanager** – Alert management and notifications
- **Node Exporter** – Host/node-level system metrics
- **kube-state-metrics** – Kubernetes object and resource metrics

## Grafana Dashboards


```
12900 → Spring Boot metrics
15661 → Kubernetes cluster metrics
4701  → JVM metrics
```

# 🤖 AI Integration

This project contains two AI workflows.

**1. AI Build Failure Diagnosis**

When Jenkins fails:

```
Jenkins Build Failure
        ↓
Jenkins Console Log
        ↓
analyze_failure.py
        ↓
Claude API
        ↓
AI Diagnosis
```
The generated report contains:

```
Root Cause
Exact Fix
Prevention
```

## 2. AI Release Notes

After a successful pipeline:

```
Git Commits
    ↓
Claude API
    ↓
RELEASE_NOTES.md
    ↓
Jenkins Artifact
```

## 🧪 Failure Test
The AI failure workflow was tested using a controlled Java build failure.

```
Temporary Code Error
        ↓
Jenkins Build & Unit Test ❌
        ↓
Failure Handler
        ↓
AI Failure Analyzer
        ↓
Claude
        ↓
ai_failure_summary.md
        ↓
Code Restored
        ↓
Jenkins Build ✅
```
This demonstrates that the AI functionality is integrated into the Jenkins failure workflow.

# 📂 Project Structure

```
employee-management-api/
│
├── Jenkinsfile
├── Dockerfile
├── pom.xml
├── sonar-project.properties
├── README.md
│
├── src/
│   ├── main/
│   └── test/
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
│
└── ai-assistant/
    ├── analyze_failure.py
    ├── generate_release_notes.py
    └── requirements.txt
```
# 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/employees` | Get all employees |
| GET | `/api/employees/{id}` | Get employee |
| POST | `/api/employees` | Create employee |
| PUT | `/api/employees/{id}` | Update employee |
| DELETE | `/api/employees/{id}` | Delete employee |

***Actuator***
```
/actuator/health
/actuator/prometheus
/actuator/metrics
```

# 🔐 Security

Secrets are not stored in source code.

The project uses Jenkins Credentials for sensitive values such as:

```
GitHub credentials
Anthropic API key
SonarQube credentials
```

#  📸 Project Screenshots

## EC2 Instance Launched

<img width="1664" height="814" alt="ec2 instance launched-2" src="https://github.com/user-attachments/assets/4672b8b9-b599-4280-a093-957ff41b1bc0" />

## Jenkins Installed

<img width="1353" height="978" alt="jenkins installed-3" src="https://github.com/user-attachments/assets/99b92b2e-479c-4c9f-85a2-7af22db268fb" />

## Pipeline Success

<img width="1898" height="989" alt="jenkins pipeline-5" src="https://github.com/user-attachments/assets/2462d7ff-8967-407f-93a5-89e9064ffd33" />

## Sonarqube Scanner Passed

<img width="1482" height="990" alt="sonarqube success-7" src="https://github.com/user-attachments/assets/01fdb355-2e99-4e3c-b27a-b989585f79d0" />

## AWS ECR Created

<img width="1722" height="960" alt="aws ecr image-8" src="https://github.com/user-attachments/assets/b4f39a2b-aadb-4698-8dec-5634570a8839" />

##  K8s Pods Status

<img width="970" height="655" alt="k8s cmds-9" src="https://github.com/user-attachments/assets/c6e0c41e-d9ef-497e-842e-b876b2b211b3" />

## Live API Status

<img width="1806" height="470" alt="live api status-10" src="https://github.com/user-attachments/assets/226132da-25d2-4a67-82b8-1ac5e8820c7e" />

## Release Note - 1 

<img width="1461" height="643" alt="OUTPUT release note-11" src="https://github.com/user-attachments/assets/90c418dc-2469-484d-bcda-295277a9ae01" />

## Failed Pipeline (Code issue)

<img width="1919" height="947" alt="intentianlly failed the pipeline-12" src="https://github.com/user-attachments/assets/2c44657e-cac0-45b3-96da-e72f1cb55af6" />

## Pipeline Rectified:

<img width="1919" height="998" alt="success pipeline-13" src="https://github.com/user-attachments/assets/49cf6cd1-0c9d-482a-8a6f-a4de69bac0bd" />

## Final Jenkins Logs

<img width="1079" height="778" alt="success jenkins log-14" src="https://github.com/user-attachments/assets/5a23dac9-79e2-4485-96d9-dbbcc19d48c6" />

## Prometheus Status - UP

<img width="1914" height="981" alt="prometheus-15" src="https://github.com/user-attachments/assets/abf98907-36bd-4f93-81ae-f887bea57308" />

## Grafana Dashboard:

<img width="1913" height="688" alt="grafana overview-16" src="https://github.com/user-attachments/assets/73a6dd9a-ec0c-437b-adea-fee77c14fdb5" />

## K8s Dashboard:

<img width="1919" height="993" alt="k8s dashboard-17" src="https://github.com/user-attachments/assets/92514c27-1e24-4bc2-a77d-c31477eeef3a" />

## Springboot Dashboard:

<img width="1918" height="993" alt="springboot dashboard-18" src="https://github.com/user-attachments/assets/8ca68593-f4b5-4ad6-8e14-9fdae80579cb" />


## Final Release Notes:

<img width="1907" height="665" alt="final release note" src="https://github.com/user-attachments/assets/72439ba5-d7c1-45d5-b985-121d5c25d559" />


# 🔗 Links

## GitHub: YOUR_GITHUB_REPOSITORY

## Portfolio: YOUR_PORTFOLIO_URL

## LinkedIn: YOUR_LINKEDIN_URL

 
# 👨‍💻 Author

<h2>Sundar S</h2>

DevOps Engineer | AWS | Jenkins | Docker | Kubernetes | Terraform | Ansible | Prometheus | Grafana





