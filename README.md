# 🛡️ VeritasAI

### AI-Powered Claim Verification, Evidence Retrieval & Real-Time Social Media Monitoring

> **From social-media claims to evidence-backed verdicts.**

VeritasAI is an evidence-grounded claim verification platform designed to identify factual claims, retrieve relevant evidence, evaluate claim–evidence relationships using Natural Language Inference (NLI), and provide explainable verification results.

Unlike a simple fake-news classifier that returns only `TRUE` or `FALSE`, VeritasAI combines claim detection, entity identification, evidence retrieval, vector search, evidence ranking, evidence filtering, NLI verification, source evaluation, confidence scoring, and AI-generated explanations.

The project also integrates public Mastodon posts and supports real-time hashtag monitoring through Mastodon's WebSocket Streaming API.

---

## 🔗 Project Links

| Resource | Link |
|---|---|
| GitHub Repository | https://github.com/deepika8mandakala/AI_Fact_tool_VeritasAI |
| Hugging Face Gradio Deployment | https://huggingface.co/spaces/deepika-mandakala/Veritas_AI |

---

## 🖼️ Architecture

![VeritasAI Architecture Flow](docs/Veritas_AI_Architecture_Flow.png)

The architecture diagram illustrates the major components of VeritasAI, including the frontend, backend, claim processing pipeline, evidence retrieval, FAISS, DeBERTa NLI verification, explanation generation, and Mastodon monitoring.

---

## 🎯 Project Objective

The objective of VeritasAI is to move beyond simple misinformation classification and build an **evidence-grounded claim verification pipeline**.

Traditional approach:

```text
Social Media Post
        ↓
   Fake / Real
```

VeritasAI follows:

```text
Social Media Post
        ↓
   Claim Detection
        ↓
 Entity Identification
        ↓
 Evidence Retrieval
        ↓
 Evidence Ranking
        ↓
 Evidence Filtering
        ↓
 Natural Language Inference
        ↓
 SUPPORTED / CONTRADICTED / INSUFFICIENT
        ↓
 Confidence + Evidence + Explanation
```

The central design principle is:

> **A claim should be evaluated against retrieved evidence rather than classified in isolation.**

---

## 🚀 Key Features

### 1. Manual Claim Verification

Users can enter a factual claim directly into the application.

**Example:**

```text
The movie Titanic was directed by James Cameron and released in 1997.
```

The system:

1. Processes the claim.
2. Identifies relevant entities.
3. Retrieves relevant evidence.
4. Ranks candidate evidence.
5. Filters irrelevant evidence.
6. Compares the claim with evidence using DeBERTa NLI.
7. Produces a final verdict.
8. Generates an explanation.

Possible results:

```text
🟢 SUPPORTED
🔴 CONTRADICTED
🟡 INSUFFICIENT EVIDENCE
```

### 2. Evidence-Grounded Verification

VeritasAI does not treat the retrieval system as the verifier. FAISS is responsible for retrieving candidate evidence, and the NLI model is responsible for evaluating the relationship between evidence and the claim.

```text
Claim
  ↓
Embedding
  ↓
FAISS Similarity Search
  ↓
Candidate Evidence
  ↓
Reranking
  ↓
Evidence Filtering
  ↓
DeBERTa NLI
  ↓
Final Verdict
```

This separation allows retrieval and verification to perform different responsibilities.

### 3. 🟢 Supported Claims

When the available evidence supports a claim, VeritasAI produces:

```text
🟢 SUPPORTED
```

The result can include: Confidence, Evidence, Source, Retrieval score, Reranking score, Source credibility, Freshness, Quality, Reliability, Bias, and Explanation.

### 4. 🔴 Contradicted Claims

When retrieved evidence conflicts with a claim, VeritasAI can produce:

```text
🔴 CONTRADICTED
```

**Example claim:**

```text
Titanic was directed by Christopher Nolan and released in 2010.
```

**Relevant evidence:**

```text
Titanic was directed by James Cameron and released in 1997.
```

The NLI verification stage can identify the contradiction.

### 5. 🟡 Insufficient Evidence

VeritasAI does not force every claim into a binary true/false decision. If:

- Relevant evidence cannot be retrieved
- Evidence is filtered out
- Available evidence is insufficient
- Model confidence is below the configured threshold

the system returns:

```text
🟡 INSUFFICIENT EVIDENCE
```

This distinction is important:

```text
INSUFFICIENT EVIDENCE ≠ FALSE
```

It means that the available evidence was not sufficient to establish either support or contradiction.

---

## 🌐 Social Media Verification

VeritasAI supports verification of public Mastodon posts. The workflow is:

```text
Mastodon URL
      ↓
Mastodon API
      ↓
Post Extraction
      ↓
Claim Extraction
      ↓
Evidence Retrieval
      ↓
Evidence Ranking
      ↓
Evidence Filtering
      ↓
DeBERTa NLI
      ↓
Verification Result
```

The system can extract factual-looking claims from a Mastodon post and send them through the same evidence-grounded verification pipeline.

---

## ⚡ Real-Time Mastodon Monitoring

VeritasAI supports real-time monitoring of public Mastodon post events using Mastodon's WebSocket Streaming API.

Users can monitor hashtags such as:

```text
#sports  #movies  #science  #technology  #politics
```

**Live architecture:**

```text
Mastodon
    │
    │ WebSocket
    ▼
Hashtag Stream
    │
    ▼
New Post
    │
    ▼
Post Extraction
    │
    ▼
Claim Detection
    │
    ▼
Evidence Retrieval
    │
    ▼
FAISS
    │
    ▼
Wikipedia / Wikidata
    │
    ▼
Evidence Filtering
    │
    ▼
DeBERTa NLI
    │
    ▼
Verification Result
    │
    ▼
Streamlit Dashboard
```

> **Important clarification:** The current live-monitoring feature processes **real-time social-media post events** through Mastodon's WebSocket API. It is **not a video livestream verification system**. Video and audio livestream verification are future extensions.

---

## 🧠 AI / NLP Architecture

VeritasAI uses pretrained Transformer models for claim detection and NLI verification.

**Primary NLI Model:**

```text
MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli
```

The model evaluates:

```text
Evidence + Claim
       ↓
    DeBERTa
       ↓
Entailment / Neutral / Contradiction
       ↓
Supported / Insufficient / Contradicted
```

### 🤖 AI Components

| Component | Technology | Purpose |
|---|---|---|
| Claim Detection | DeBERTa-v3 zero-shot classification | Identifies factual-looking claims |
| Evidence Embeddings | BAAI/bge-small-en-v1.5 | Converts claims/evidence into vectors |
| Vector Retrieval | FAISS | Retrieves semantically similar evidence |
| Verification | DeBERTa-v3 MNLI/FEVER/ANLI | Determines entailment, neutral, or contradiction |
| Explanation | Groq API + `openai/gpt-oss-20b` | Generates human-readable explanations |

The core verification pipeline does not depend on a hosted LLM API. Retrieval, embeddings, and NLI inference are performed by the application's model stack. Groq is used specifically for **explanation generation after the verification pipeline has produced a verdict and selected evidence**.

---

## 🔬 Why DeBERTa?

The core problem is not simply:

> "Is this text fake?"

Instead, the problem is:

> "Does the retrieved evidence support, contradict, or fail to establish this claim?"

This is fundamentally a Natural Language Inference problem. Therefore, an NLI-oriented Transformer is more appropriate than a generic binary fake-news classifier.

The selected checkpoint was fine-tuned using:

- MultiNLI
- FEVER-NLI
- ANLI

This allows VeritasAI to use an existing NLI model instead of training a large Transformer from scratch.

### 📊 DeBERTa Technical Specifications

| Specification | Details |
|---|---|
| Model | `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` |
| Architecture | DeBERTa-v3 Base |
| Parameters | Approximately 183M |
| Transformer Layers | 12 |
| Hidden Size | 768 |
| Attention Heads | 12 |
| Intermediate Size | 3,072 |
| Maximum Sequence Length | 512 tokens |
| Framework | PyTorch |
| NLP Framework | Hugging Face Transformers |
| NLI Training | MultiNLI + FEVER-NLI + ANLI |
| Current Inference | CPU |
| Application Confidence Threshold | 0.60 |

### Confidence Interpretation

A result such as:

```text
97.7% confidence
```

means the verification model assigned approximately 97.7% probability to the selected verification class **for the retrieved evidence**. It should **not** be interpreted as an objectively calibrated 97.7% probability that the claim itself is true.

---

## 🤖 Zero-Shot Claim Detection

VeritasAI also uses the DeBERTa model through a Hugging Face zero-shot classification pipeline:

```python
pipeline(
    "zero-shot-classification",
    model=get_model(),
    tokenizer=get_tokenizer(),
    device=-1
)
```

Zero-shot classification helps the system identify factual-looking content across different domains without requiring a separate supervised classifier for every topic.

**Examples:** sports, movies, science, technology, politics

### Two Roles of the NLP Model

**Role 1 — Claim Detection**

```text
Social Post
    ↓
Text Extraction
    ↓
Claim Detection
```

**Role 2 — Evidence Verification**

```text
Evidence + Claim
       ↓
     DeBERTa
       ↓
Entailment / Neutral / Contradiction
```

These are mapped to:

```text
Entailment    → SUPPORTED
Neutral       → INSUFFICIENT EVIDENCE
Contradiction → CONTRADICTED
```

---

## 🔎 Evidence Retrieval Architecture

VeritasAI uses an evidence-first architecture.

```text
Claim
  ↓
Entity Extraction
  ↓
Query Generation
  ↓
Vector Retrieval
  ↓
FAISS
  ↓
Wikipedia / Wikidata
  ↓
Candidate Evidence
  ↓
Reranking
  ↓
Filtering
  ↓
DeBERTa NLI
  ↓
Final Verdict
```

### FAISS

FAISS is used as the vector similarity search layer. Its responsibility is **retrieval**, not truth determination.

```text
Claim / Query
      ↓
Vector Representation
      ↓
FAISS Similarity Search
      ↓
Candidate Evidence
      ↓
Reranking
      ↓
Filtering
```

The NLI model is responsible for evaluating the relationship between evidence and the claim.

### 📚 Knowledge Sources

The current prototype uses **Wikipedia** and **Wikidata** as knowledge and evidence sources. The retrieval layer obtains candidate evidence from these sources before verification.

### 🧾 Evidence Metadata

Evidence items can contain:

- Document ID, Chunk ID
- Title, Source, URL
- Published date, Chunk text
- Retrieval score, Rerank score, Source score
- Freshness score, Quality score, Quality label
- Reliability, Bias, Category
- Highlight, Verdict, Confidence

---

## 📊 Verification Metrics

The application can expose metrics including:

- Evidence count, Filtered evidence, Confidence
- Evidence agreement, Majority verdict
- Supported count, Contradicted count, Insufficient count
- Source credibility, Freshness, Quality, Reliability, Bias

**Example:**

```text
Evidence Agreement: 100%

Supported: 1
Contradicted: 0
Insufficient: 0
```

---

## 🧠 Explainability

Explainability is a core design principle of VeritasAI.

**Traditional approach:**

```text
POST → FAKE
```

**VeritasAI:**

```text
POST
 ↓
CLAIM
 ↓
EVIDENCE
 ↓
VERDICT
 ↓
CONFIDENCE
 ↓
SOURCE
 ↓
EXPLANATION
```

The system therefore provides an evidence-backed reasoning trail instead of only a classification label.

---

## 🖥️ Frontend Applications

VeritasAI has two frontend/deployment interfaces.

### 1. Streamlit Application

The full project frontend is implemented using Streamlit. The Streamlit application supports:

**Verification**
- Manual claim verification
- Mastodon post verification
- Evidence display, verdict display, confidence, explanation

**Live Monitoring**
- Hashtag monitoring
- Start/stop monitoring
- Live claim detection, live verdicts, live confidence
- Live statistics

**Evidence**
- Evidence cards, source information
- Credibility, freshness, quality, reliability, bias, category
- Evidence highlights, original source links

**Analytics**
- Posts, claims, supported, contradicted, insufficient
- Verification history, live statistics

### 2. Gradio Hugging Face Deployment

A lightweight Gradio interface is provided for public deployment through Hugging Face Spaces.

**Deployment:** https://huggingface.co/spaces/deepika-mandakala/Veritas_AI

The Gradio deployment focuses on the core claim-verification workflow:

```text
User Claim
    ↓
Verification Pipeline
    ↓
Evidence Retrieval
    ↓
DeBERTa NLI
    ↓
Verdict + Confidence
    ↓
Explanation + Evidence
```

The Gradio deployment provides:

- Manual claim verification
- Evidence retrieval
- Verification verdict
- Confidence score
- Reasoning
- Evidence display
- Groq-powered explanation

### Deployment Distinction

The two interfaces serve different purposes:

| Capability | Streamlit | Gradio |
|---|---|---|
| Manual claim verification | ✅ | ✅ |
| Evidence display | ✅ | ✅ |
| Verdict | ✅ | ✅ |
| Confidence | ✅ | ✅ |
| Explanation | ✅ | ✅ |
| Mastodon URL verification | ✅ | Project-dependent |
| Real-time Mastodon monitoring | ✅ | Not currently exposed |
| WebSocket live monitoring | ✅ | Not currently exposed |
| Analytics dashboard | ✅ | Limited |
| Public Hugging Face deployment | Project deployment | ✅ |

The **Streamlit application remains the full-featured project interface**, while the **Gradio application provides the publicly accessible Hugging Face deployment for the core verification workflow**.

---

## ⚙️ FastAPI Backend

The backend is implemented using FastAPI. Responsibilities include:

- Claim verification
- Social-media verification
- Batch verification
- Evidence retrieval
- NLI inference
- Database persistence
- Mastodon integration
- Live monitoring
- Analytics

### API Endpoints

| Purpose | Endpoint |
|---|---|
| Claim Verification | `POST /verification/verify` |
| Social Media Verification | `POST /verification/social/verify` |
| Batch Verification | `POST /verification/verify-batch` |
| Start Live Monitoring | `POST /social/live/start` |
| Stop Live Monitoring | `POST /social/live/stop` |
| Live Monitoring Status | `GET /social/live/status` |
| Live Results | `GET /social/live/results` |
| Analytics Statistics | `GET /analytics/stats` |
| Verification History | `GET /analytics/history` |

---

## 🗄️ Database

The backend uses SQLAlchemy for database interaction. Verification information can be persisted, including Claim, Verdict, Confidence, Explanation, Verification history, and Analytics information.

---

## 📱 Mastodon Integration

Mastodon was selected for the social-media prototype because it provides:

- Public post retrieval
- Developer-friendly APIs
- Hashtag-based streams
- WebSocket streaming
- Programmatic access to post events

### Mastodon URL Verification

```text
Public Mastodon URL
        ↓
Mastodon REST API
        ↓
Post Content
        ↓
HTML/Text Extraction
        ↓
Claim Detection
        ↓
Evidence Retrieval
        ↓
DeBERTa NLI
        ↓
Verdict
```

### WebSocket Monitoring

The live monitoring implementation:

1. Retrieves the Mastodon streaming host.
2. Creates a WebSocket connection.
3. Authenticates using the configured access token.
4. Subscribes to a hashtag stream.
5. Receives update events.
6. Parses the event payload.
7. Extracts the post.
8. Detects claims.
9. Verifies detected claims.
10. Continues processing subsequent posts.
11. Reconnects when the connection is interrupted.

---

## 🔄 WebSocket Reconnection

Real-time connections can be interrupted. The streaming implementation handles reconnection:

```text
WebSocket Connected
       ↓
Receive Posts
       ↓
Connection Lost
       ↓
Wait
       ↓
Reconnect
       ↓
Resume Monitoring
```

This helps prevent temporary WebSocket/network failures from permanently stopping monitoring.

---

## 🏗️ High-Level Architecture

```text
                         ┌─────────────────┐
                         │      USER       │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    STREAMLIT    │
                         │    FRONTEND     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FASTAPI     │
                         │     BACKEND     │
                         └────────┬────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      Claim Verification   Social Verification   Live Monitoring
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │ CLAIM DETECTION │
                         └────────┬────────┘
                                  ▼
                         ┌─────────────────┐
                         │ENTITY EXTRACTION│
                         └────────┬────────┘
                                  ▼
                         ┌──────────────────┐
                         │EVIDENCE RETRIEVAL│
                         └────────┬─────────┘
                                  ▼
                         ┌─────────────────┐
                         │      FAISS      │
                         └────────┬────────┘
                                  ▼
                         ┌──────────────────┐
                         │Wikipedia/Wikidata│
                         └────────┬─────────┘
                                  ▼
                         ┌──────────────────┐
                         │EVIDENCE FILTERING│
                         └────────┬─────────┘
                                  ▼
                         ┌─────────────────┐
                         │   DeBERTa NLI   │
                         └────────┬────────┘
                                  ▼
                 ┌────────────────┼────────────────┐
                 ▼                ▼                ▼
             SUPPORTED       CONTRADICTED     INSUFFICIENT
                 │                │                │
                 └────────────────┼────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │CONFIDENCE +     │
                         │EVIDENCE         │
                         └────────┬────────┘
                                  ▼
                         ┌─────────────────┐
                         │   EXPLANATION   │
                         └────────┬────────┘
                                  ▼
                         ┌─────────────────┐
                         │    FRONTEND     │
                         └─────────────────┘
```

---

## 🔬 Model Selection Journey

The project initially explored a custom ML approach. However, development constraints included:

- Limited laptop specifications
- Limited GPU resources
- Limited VRAM
- Training time
- System memory limitations
- Local model experimentation constraints

Training a large Transformer from scratch was therefore not practical. The project shifted toward a pretrained NLI model. The selection was based on:

```text
Task Suitability
      +
NLI Capability
      +
Fact-Verification Training
      +
Zero-Shot Capability
      +
Local Inference Feasibility
      ↓
DeBERTa-v3
```

This allowed engineering effort to focus on:

- Claim extraction
- Entity identification
- Evidence retrieval
- Vector search
- Evidence ranking
- Evidence filtering
- Source evaluation
- Social-media integration
- Real-time monitoring
- Explainability

---

## 💾 Memory and OOM Optimization

The project encountered memory pressure while loading Transformer models alongside FAISS, FastAPI, Streamlit, and other dependencies. Several optimizations were used.

**Memory-Conscious Model Loading**

```python
AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    low_cpu_mem_usage=True
)
```

**Shared Model Instance**

Instead of loading the model for every request:

```text
First Request
     ↓
Load Model
     ↓
Keep Model in Memory
     ↓
Next Request
     ↓
Reuse Model
```

**CPU Inference**

The current zero-shot pipeline uses CPU inference:

```python
device = -1
```

This reduces dependency on a dedicated GPU for the current implementation.

---

## 🧪 Example Verification

### Supported Claim

```text
The movie Titanic was directed by James Cameron and released in 1997.
```

Expected result:

```text
🟢 SUPPORTED
```

The system retrieves relevant evidence and evaluates the evidence against the claim.

### Contradicted Claim

```text
Titanic was directed by Christopher Nolan and released in 2010.
```

Expected behavior:

```text
🔴 CONTRADICTED
```

depending on the retrieved evidence.

### Insufficient Evidence

An obscure or unsupported claim may produce:

```text
🟡 INSUFFICIENT EVIDENCE
```

For example:

```text
Evidence: 0
Filtered: 0
Confidence: 0.0%
```

This demonstrates that the system does not force every claim into a binary true/false decision.

---

## 🛠️ Engineering Challenges

### 1. ML Model Selection

Large-scale custom model training was difficult because of limited local compute.

**Solution:** Use a pretrained NLI Transformer and focus engineering effort on retrieval, verification, explainability, and social integration.

### 2. DeBERTa Memory Usage

Running PyTorch, Transformer models, FAISS, FastAPI, and Streamlit together created memory pressure.

**Solution:** Memory-conscious loading, shared model instances, CPU inference, environment cleanup, and avoiding repeated model initialization.

### 3. Claim Extraction

Social posts containing headlines and URLs could initially result in:

```text
CLAIMS FOUND: 0
```

The claim extraction pipeline was improved to better handle article-linked posts and headline-style factual claims.

### 4. Evidence Retrieval

Not every search result is necessarily useful evidence. Therefore, VeritasAI uses:

```text
Retrieval
    ↓
Reranking
    ↓
Filtering
    ↓
Verification
```

### 5. Mastodon Authentication

The live-monitoring feature requires a Mastodon access token.

```env
MASTODON_INSTANCE=https://mastodon.social
MASTODON_ACCESS_TOKEN=YOUR_TOKEN
```

### 6. WebSocket Disconnections

Temporary network interruptions can disconnect the WebSocket stream. Reconnect logic is used to restore monitoring.

---

## 🔐 Security

Never commit API keys, access tokens, passwords, or other secrets to GitHub. Use environment variables.

```env
GROQ_API_KEY=your_groq_api_key

MASTODON_INSTANCE=https://mastodon.social
MASTODON_ACCESS_TOKEN=YOUR_MASTODON_ACCESS_TOKEN

NEWS_API_KEY=YOUR_NEWS_API_KEY
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
```

For Hugging Face Spaces and other cloud deployments, configure secrets through the platform's **Secrets / Environment Variables** settings.

Do not commit:

```text
.env
.env.*
```

---

## 📦 Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Full Frontend | Streamlit |
| Public Deployment UI | Gradio |
| Backend | FastAPI |
| API | REST / JSON |
| Deep Learning | PyTorch |
| NLP | Hugging Face Transformers |
| NLI Model | DeBERTa-v3 |
| Claim Detection | Hugging Face Zero-Shot Pipeline |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Vector Search | FAISS |
| Knowledge Sources | Wikipedia + Wikidata |
| Social Platform | Mastodon |
| Social API | Mastodon REST API |
| Real-Time Streaming | Mastodon WebSocket API |
| Database Layer | SQLAlchemy |
| Explanation | Groq API |
| Public Deployment | Hugging Face Spaces |

---

## 📁 Project Structure

```text
VeritasAI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── verification.py
│   │   │   │   ├── retrieval.py
│   │   │   │   ├── claims.py
│   │   │   │   └── entity.py
│   │   │   └── router.py
│   │   │
│   │   ├── verification/
│   │   │   ├── pipeline.py
│   │   │   ├── verifier.py
│   │   │   ├── model.py
│   │   │   ├── schemas.py
│   │   │   └── response_schema.py
│   │   │
│   │   ├── claim_detection/
│   │   ├── entity_recognition/
│   │   ├── retrieval/
│   │   ├── ranking/
│   │   ├── filtering/
│   │   ├── preprocessing/
│   │   ├── credibility/
│   │   ├── explanation/
│   │   ├── social/
│   │   │   ├── mastodon_client.py
│   │   │   ├── mastodon_stream.py
│   │   │   ├── post_extractor.py
│   │   │   ├── live_monitor.py
│   │   │   └── service.py
│   │   ├── analytics/
│   │   ├── database/
│   │   ├── url/
│   │   ├── pdf/
│   │   ├── image/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── components/
│   ├── assets/
│   ├── utils/
│   ├── styles.css
│   └── app.py
│
├── docs/
│   └── Veritas_AI_Architecture_Flow.png
│
├── hf-deploy/
│   ├── app.py
│   ├── backend/
│   ├── requirements.txt
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🐍 Installation

### Prerequisites

Recommended:

- Python 3.10+
- Git
- Internet connection
- Sufficient RAM for Transformer inference

A dedicated GPU is not mandatory for the current implementation because CPU inference is supported. Additional compute resources can improve inference latency and scalability.

### Clone the Repository

```bash
git clone https://github.com/deepika8mandakala/AI_Fact_tool_VeritasAI.git
cd AI_Fact_tool_VeritasAI
```

### Create a Virtual Environment

**Windows**

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

For local development, configure the required environment variables:

```env
GROQ_API_KEY=your_groq_api_key

PORT=8000

MASTODON_INSTANCE=https://mastodon.social
MASTODON_ACCESS_TOKEN=YOUR_MASTODON_ACCESS_TOKEN

NEWS_API_KEY=YOUR_NEWS_API_KEY
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
```

Never commit real credentials.

---

## ▶️ Run the FastAPI Backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

- Backend: `http://127.0.0.1:8000`
- Swagger documentation: `http://127.0.0.1:8000/docs`

---

## ▶️ Run the Streamlit Frontend

Open another terminal.

```bash
cd frontend
python -m streamlit run app.py
```

- Frontend: `http://localhost:8501`

---

## ▶️ Run the Gradio Deployment

The Hugging Face deployment uses:

```text
Gradio
   ↓
VeritasAI Verification Pipeline
   ↓
Evidence Retrieval
   ↓
DeBERTa NLI
   ↓
Verdict
   ↓
Explanation
```

The public deployment is available at: https://huggingface.co/spaces/deepika-mandakala/Veritas_AI

---

## ☁️ Hugging Face Spaces Deployment

The Gradio application is deployed using Hugging Face Spaces. The deployment uses a dedicated deployment directory:

```text
hf-deploy/
```

The Space configuration is defined in its `README.md` front matter:

```yaml
---
title: VeritasAI
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "6.25.0"
python_version: "3.12"
app_file: app.py
pinned: false
---
```

Sensitive values such as `GROQ_API_KEY` are configured through Hugging Face Space Secrets rather than committed to the repository.

---

## 🧪 Recommended Demo Flow

A complete demonstration can follow this sequence:

1. Start FastAPI.
2. Start Streamlit.
3. Open the VeritasAI dashboard.
4. Demonstrate manual claim verification.
5. Show evidence and verdict.
6. Demonstrate Mastodon URL verification.
7. Show extracted claim.
8. Show retrieved evidence.
9. Start live monitoring.
10. Select a hashtag.
11. Publish or wait for a test claim on Mastodon.
12. WebSocket receives the post.
13. Claim detection runs.
14. Evidence retrieval runs.
15. NLI verification runs.
16. Live verdict appears.
17. Show live statistics.
18. Stop monitoring.

### 🎬 Recommended Demo Claims

**Movie Claim**

```text
The movie Titanic was directed by James Cameron and released in 1997.
```

Expected: `🟢 SUPPORTED`

**Contradictory Claim**

```text
Titanic was directed by Christopher Nolan and released in 2010.
```

Expected behavior: `🔴 CONTRADICTED`, depending on the retrieved evidence.

**Insufficient Evidence**

Use an intentionally obscure or unsupported claim where the available evidence sources do not contain enough relevant information.

Expected: `🟡 INSUFFICIENT EVIDENCE`

---

## ⚠️ Limitations

VeritasAI is an evidence-grounded prototype. It does not guarantee absolute truth. Verification depends on:

- Evidence availability
- Evidence quality
- Retrieval relevance
- Evidence filtering
- Model behavior
- Model confidence
- Knowledge-source coverage

### Insufficient Evidence

```text
INSUFFICIENT EVIDENCE ≠ FALSE
```

It means the available evidence was not sufficient to establish support or contradiction.

### Live Monitoring

The current live feature monitors **Mastodon post events** through WebSockets. It does not currently process live video, live audio, or video/audio broadcasts.

---

## 🎥 Future Video Livestream Verification

A future version could extend VeritasAI to live video platforms. Possible architecture:

```text
LIVE VIDEO
    ↓
Audio Extraction
    ↓
Speech-to-Text
    ↓
Claim Detection
    ↓
Evidence Retrieval
    ↓
FAISS
    ↓
DeBERTa NLI
    ↓
Real-Time Verdict
    ↓
User Alert
```

This would require additional infrastructure for video ingestion, audio extraction, automatic speech recognition, streaming infrastructure, low-latency inference, GPU acceleration, and real-time event processing.

---

## 🚀 Future Roadmap

### Phase 1 — Current Prototype

- ✅ Claim Verification
- ✅ Social Post Verification
- ✅ Evidence Retrieval
- ✅ FAISS Search
- ✅ Wikipedia/Wikidata
- ✅ DeBERTa NLI
- ✅ Source Metadata
- ✅ Explainability
- ✅ Mastodon WebSocket Monitoring
- ✅ Streamlit Dashboard
- ✅ Gradio Hugging Face Deployment

### Phase 2 — More Evidence Sources

Reuters, Associated Press, government databases, scientific publications, news APIs, domain-specific trusted sources.

### Phase 3 — More Social Platforms

X, Reddit, YouTube, news feeds, other federated social platforms.

### Phase 4 — Video Livestream Verification

```text
Video → Audio → Speech-to-Text → Claim Detection → Evidence Retrieval → NLI → Real-Time Alert
```

### Phase 5 — Production Infrastructure

Docker, cloud deployment, GPU inference, Redis, Kafka, authentication, multi-user support, monitoring, logging, distributed workers.

### Phase 6 — Advanced Reasoning

Claim decomposition, multi-hop reasoning, cross-source consensus, temporal reasoning, source reputation learning, evidence graph construction, improved contradiction detection, better confidence calibration.

---

## 🧩 Core Components

| Component | Description |
|---|---|
| Claim Detection | Identifies factual-looking claims |
| Entity Identification | Identifies important entities used for retrieval |
| Evidence Retrieval | Searches available knowledge sources |
| FAISS | Performs vector similarity retrieval |
| Evidence Ranking | Ranks candidate evidence |
| Evidence Filtering | Removes insufficiently relevant evidence |
| DeBERTa NLI | Evaluates evidence–claim relationships |
| Source Evaluation | Provides source-level metadata |
| Explanation | Generates human-readable reasoning |
| Mastodon Integration | Retrieves public Mastodon posts |
| Live Monitoring | Processes Mastodon post events in real time |
| Analytics | Provides verification history and statistics |
| Streamlit | Full-featured project frontend |
| Gradio | Public lightweight verification interface |

---

## 💡 Why VeritasAI?

**Traditional misinformation detection:**

```text
Social Post → ML Classifier → FAKE / REAL
```

**VeritasAI:**

```text
Social Post → Claim Detection → Entity Identification → Evidence Retrieval →
Vector Search → Evidence Ranking → Evidence Filtering → NLI Verification →
SUPPORTED / CONTRADICTED / INSUFFICIENT → Confidence → Source Quality → Explanation
```

The key differentiator is:

> **VeritasAI provides an evidence-grounded assessment rather than only a black-box classification label.**

---

## 🧠 Core Verification Philosophy

VeritasAI follows:

```text
RETRIEVE → COMPARE → VERIFY → EXPLAIN
```

rather than:

```text
CLASSIFY → TRUE / FALSE
```

This design makes the verification process more transparent and useful for applications where evidence, source quality, and explainability matter.

---

## 🏆 Project Outcome

The VeritasAI prototype demonstrates an integrated AI verification system combining Natural Language Processing, Natural Language Inference, Transformer models, zero-shot classification, sentence embeddings, FAISS vector search, evidence retrieval/ranking/filtering, source evaluation, explainability, FastAPI, Streamlit, Gradio, Mastodon REST API, Mastodon WebSocket streaming, and database persistence.

The system supports:

- Manual claim verification
- Social-media post verification
- Supported, contradicted, and insufficient-evidence scenarios
- Evidence retrieval and source display
- Mastodon integration
- Real-time hashtag monitoring
- Live claim detection and verification
- WebSocket reconnection
- Analytics and verification history
- Public Hugging Face deployment

---

## 📌 Final Architecture Summary

```text
                         VERITASAI
                             │
              ┌──────────────┴──────────────┐
              │                             │
       NORMAL VERIFICATION            LIVE MONITORING
              │                             │
              ▼                             ▼
         User Claim                      Mastodon
              │                          WebSocket
              │                             │
              ▼                             ▼
       Claim Detection                   New Post
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    Entity Identification
                             │
                             ▼
                    Evidence Retrieval
                             │
                             ▼
                           FAISS
                             │
                             ▼
                    Wikipedia / Wikidata
                             │
                             ▼
                    Evidence Filtering
                             │
                             ▼
                       DeBERTa NLI
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
          SUPPORTED     CONTRADICTED   INSUFFICIENT
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    Confidence + Evidence
                             │
                             ▼
                      Source Evaluation
                             │
                             ▼
                         Explanation
                             │
                             ▼
                    Streamlit / Gradio
```

---

## 📋 Key Takeaways

1. **Evidence-Grounded** — Claims are evaluated against retrieved evidence.
2. **NLI-Based** — DeBERTa evaluates the relationship between evidence and claim.
3. **Explainable** — Evidence, sources, confidence, reasoning, and explanations are exposed.
4. **Domain-Flexible** — Zero-shot classification supports multiple topics.
5. **Real-Time** — Mastodon WebSocket streaming enables continuous post-event monitoring.
6. **Resource-Conscious** — Shared model loading and CPU inference reduce local resource requirements.
7. **Dual Frontend** — Streamlit provides the full project dashboard while Gradio provides the public Hugging Face interface.
8. **Extensible** — The architecture can be extended with additional evidence sources, social platforms, video streams, cloud infrastructure, and advanced reasoning.

---

## 🛡️ VeritasAI

### From Social-Media Claims to Evidence-Backed Verdicts.

✓ Claim Detection · ✓ Evidence Retrieval · ✓ NLI Verification · ✓ Explainability · ✓ Real-Time Social Monitoring
=======
# 🛡️ VeritasAI

## AI-Powered Claim Verification & Real-Time Social Media Monitoring

> **From social-media claims to evidence-backed verdicts.**

VeritasAI is an evidence-grounded claim verification platform designed to identify factual claims, retrieve relevant evidence, evaluate claim–evidence relationships using Natural Language Inference (NLI), and present explainable verification results.

Unlike a simple fake-news classifier that produces only a `TRUE` or `FALSE` prediction, VeritasAI provides:

- 🟢 **SUPPORTED**
- 🔴 **CONTRADICTED**
- 🟡 **INSUFFICIENT EVIDENCE**
- Confidence score
- Retrieved evidence
- Evidence agreement
- Majority verdict
- Source credibility
- Evidence quality
- Freshness
- Reliability
- Bias
- Source category
- AI reasoning
- AI explanation
- Original source links

VeritasAI also supports **real-time monitoring of public Mastodon posts through Mastodon's WebSocket Streaming API**.

# 🎯 Project Objective

The objective of VeritasAI is to move beyond simple misinformation classification and build an **evidence-grounded claim verification pipeline**.

Instead of:

```text
Social Media Post
       ↓
Fake / Real
````

VeritasAI follows:

```text
Social Media Post
       ↓
Claim Detection
       ↓
Entity Identification
       ↓
Evidence Retrieval
       ↓
Evidence Ranking
       ↓
Evidence Filtering
       ↓
Natural Language Inference
       ↓
SUPPORTED / CONTRADICTED / INSUFFICIENT
       ↓
Confidence + Evidence + Explanation
```

The central idea is:

> **A claim should be evaluated against retrieved evidence rather than classified in isolation.**

---

# 🚀 Key Features

## 1. Manual Claim Verification

Users can directly enter a factual claim through the Streamlit interface.

Example:

```text
The movie Titanic was directed by James Cameron and released in 1997.
```

The system:

1. Processes the claim.
2. Identifies relevant entities.
3. Retrieves relevant evidence.
4. Ranks the retrieved evidence.
5. Filters irrelevant evidence.
6. Compares the claim with evidence using DeBERTa NLI.
7. Produces a final verdict.

Example:

```text
🟢 SUPPORTED

Confidence: 99.5%
```

---

# 2. Social Media Post Verification

Users can paste a public Mastodon post URL.

The system automatically:

```text
Mastodon URL
     ↓
Mastodon API
     ↓
Post Extraction
     ↓
Claim Extraction
     ↓
Evidence Retrieval
     ↓
Evidence Ranking
     ↓
Evidence Filtering
     ↓
DeBERTa NLI
     ↓
Verification Result
```

Example claim detected from a Mastodon post:

```text
A rare tidal disruption event exposed a massive wandering
black hole about 30,000 light-years from its galaxy’s center.
```

The system can retrieve the linked article and use it as evidence for verification.

---

# 3. 🟢 Supported Claims

When the retrieved evidence supports the claim, VeritasAI produces:

```text
🟢 SUPPORTED
```

The result includes:

* Confidence
* Evidence
* Source
* Retrieval score
* Rerank score
* Source credibility
* Freshness
* Quality
* Reliability
* Bias
* Explanation

---

# 4. 🔴 Contradicted Claims

When retrieved evidence explicitly conflicts with a claim, VeritasAI can produce:

```text
🔴 CONTRADICTED
```

For example:

```text
Claim:

Titanic was directed by Christopher Nolan and released in 2010.
```

Relevant evidence:

```text
Titanic was directed by James Cameron and released in 1997.
```

The evidence contradicts the claim.

---

# 5. 🟡 Insufficient Evidence

VeritasAI does not force every claim into TRUE or FALSE.

If:

* relevant evidence cannot be retrieved,
* evidence is filtered out,
* the available evidence is insufficient,
* or model confidence is below the configured threshold,

the system returns:

```text
🟡 INSUFFICIENT EVIDENCE
```

This distinction is important:

```text
INSUFFICIENT EVIDENCE
        ≠
FALSE
```

It means that the available evidence was not sufficient to establish either support or contradiction.

---

# 6. ⚡ Real-Time Mastodon Monitoring

VeritasAI supports real-time monitoring of public Mastodon posts through Mastodon's WebSocket Streaming API.

Users can monitor hashtags such as:

```text
#sports
#movies
#science
#love
#technology
```

The system continuously receives new posts and processes them automatically.

Architecture:

```text
                    MASTODON
                       │
                       │ WebSocket
                       ▼
                HASHTAG STREAM
                       │
                       ▼
                   NEW POST
                       │
                       ▼
                CLAIM DETECTION
                       │
                       ▼
              EVIDENCE RETRIEVAL
                       │
                       ▼
                  DeBERTa NLI
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      SUPPORTED    CONTRADICTED   INSUFFICIENT
          │            │            │
          └────────────┼────────────┘
                       ▼
              STREAMLIT DASHBOARD
```

### Important clarification

The current VeritasAI live-monitoring feature is a:

> **Real-time social-media post event stream**

using Mastodon's WebSocket API.

It is **not a video livestream verification system**.

Video/audio livestream verification is future scope.

---

# 🧠 AI / NLP Model

VeritasAI uses the pretrained model:

```text
MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli
```

The model is used primarily for **Natural Language Inference**.

The verification problem is formulated as:

```text
Evidence + Claim
      ↓
   DeBERTa
      ↓
Entailment / Neutral / Contradiction
      ↓
Supported / Insufficient / Contradicted
```

---

# 🔬 Why DeBERTa?

The core problem in VeritasAI is not simply:

> "Is this text fake?"

It is:

> "Does the retrieved evidence support, contradict, or fail to establish this claim?"

This is fundamentally a Natural Language Inference problem.

Therefore, an NLI-oriented pretrained Transformer was more appropriate than a generic binary fake-news classifier.

The selected checkpoint was already fine-tuned using:

* MultiNLI
* FEVER-NLI
* ANLI

This allowed the project to leverage an existing NLI model instead of training a large Transformer from scratch.

---

# 📊 DeBERTa Technical Specifications

| Specification                    | Details                                        |
| -------------------------------- | ---------------------------------------------- |
| Model                            | `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` |
| Architecture                     | DeBERTa-v3 Base                                |
| Parameters                       | ~183M                                          |
| Transformer Layers               | 12                                             |
| Hidden Size                      | 768                                            |
| Attention Heads                  | 12                                             |
| Intermediate Size                | 3,072                                          |
| Maximum Sequence Length          | 512 tokens                                     |
| Vocabulary                       | ~128K                                          |
| Framework                        | PyTorch                                        |
| NLP Framework                    | Hugging Face Transformers                      |
| NLI Training                     | MultiNLI + FEVER-NLI + ANLI                    |
| NLI Pairs                        | ~763,913                                       |
| Current Inference                | CPU                                            |
| Model Loading                    | `low_cpu_mem_usage=True`                       |
| Application Confidence Threshold | 0.60                                           |

---

# 📚 Model Training Background

The selected checkpoint was trained/fine-tuned using multiple NLI datasets.

## MultiNLI

Provides broad natural-language inference examples across multiple domains.

## FEVER-NLI

Provides fact-verification-oriented inference examples.

## ANLI

Provides adversarial NLI examples designed to make inference models more robust.

The combined training data provides a strong foundation for the evidence-versus-claim verification task.

---

# 🔄 Model Selection Journey

The project initially explored an ML-based/custom model approach.

However, the available development environment introduced practical constraints:

* Limited laptop specifications
* GPU limitations
* Limited GPU memory
* Training time
* System memory limitations
* Local model experimentation constraints

Training a large Transformer model from scratch was therefore not practical for the available environment.

The project shifted toward a pretrained NLI model.

The final model selection was based on:

```text
Task suitability
       +
NLI capability
       +
Fact-verification training
       +
Zero-shot capability
       +
Local inference feasibility
       ↓
DeBERTa-v3-base
```

This allowed the project to focus engineering effort on the unique parts of VeritasAI:

* Claim extraction
* Entity identification
* Evidence retrieval
* Vector search
* Evidence ranking
* Evidence filtering
* Source evaluation
* Social-media integration
* Real-time monitoring
* Explainability

---

# 💾 Memory / OOM Challenge

Even after switching to a pretrained DeBERTa model, the project encountered memory and OOM issues.

The local environment had to handle:

* Transformer model weights
* PyTorch runtime
* Tokenizer
* FAISS
* FastAPI
* Streamlit
* Other Python dependencies

This created significant memory pressure.

---

# 🛠️ Memory Optimization

Several practical optimizations were performed.

### 1. Environment Cleanup

Unnecessary files and resources were removed from the C drive to free system resources.

### 2. Memory-Conscious Model Loading

The model is loaded using:

```python
AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    low_cpu_mem_usage=True
)
```

### 3. Shared Model Instance

Instead of loading the model for every request:

```python
_tokenizer = None
_model = None
_classifier = None
```

The model is initialized once and reused.

Conceptually:

```text
First Request
     ↓
Load Model
     ↓
Keep Model in Memory
     ↓
Next Request
     ↓
Reuse Model
```

### 4. CPU Inference

The current zero-shot pipeline uses:

```python
device=-1
```

which means CPU inference.

---

# 🎯 Why Pretrained Instead of Training From Scratch?

The decision was an engineering tradeoff.

The objective was not simply to train a new language model.

The objective was to build a working evidence-grounded verification platform.

Using a pretrained NLI model allowed development effort to be redirected toward:

```text
Evidence Retrieval
       +
Claim Detection
       +
Social Integration
       +
Real-Time Monitoring
       +
Explainability
```

The model choice was therefore driven by:

> **Task suitability + available compute + deployment practicality.**

---

# 🤖 Zero-Shot Classification

The DeBERTa model is also used through a Hugging Face zero-shot classification pipeline.

The implementation uses:

```python
pipeline(
    "zero-shot-classification",
    model=get_model(),
    tokenizer=get_tokenizer(),
    device=-1
)
```

Zero-shot classification helps the system remain flexible across multiple domains.

For example:

```text
#sports
#movies
#science
#love
#technology
#politics
```

The project does not require a separate supervised classifier for every topic.

---

# 🔎 Two Roles of the NLP Model

The project uses the model in two related stages.

## Role 1 — Claim Detection

The zero-shot classification capability helps identify factual-looking content.

```text
Social Post
     ↓
Text Extraction
     ↓
Claim Detection
```

## Role 2 — Evidence Verification

The NLI classifier compares:

```text
Evidence
   +
Claim
```

and determines:

```text
Entailment
Neutral
Contradiction
```

which are mapped to:

```text
SUPPORTED
INSUFFICIENT_EVIDENCE
CONTRADICTED
```

---

# 🔍 NLI Verification Configuration

The verifier processes evidence and claim using:

```python
inputs = tokenizer(
    evidence,
    claim,
    return_tensors="pt",
    truncation=True,
    padding=True,
    max_length=512
)
```

Therefore:

```text
Premise    = Evidence
Hypothesis = Claim
```

The model produces logits.

These are converted into probabilities using:

```python
probabilities = softmax(
    outputs.logits,
    dim=1
)
```

The highest probability class becomes the predicted NLI relationship.

---

# 🏷️ Label Mapping

The model output is mapped to application-level verification labels.

```text
Entailment
     ↓
SUPPORTED

Neutral
     ↓
INSUFFICIENT_EVIDENCE

Contradiction
     ↓
CONTRADICTED
```

This mapping allows the frontend and backend to work with understandable verification terminology.

---

# 📈 Confidence Threshold

VeritasAI applies an application-level confidence threshold:

```text
0.60
```

Conceptually:

```python
if confidence < 0.60:
    label = "INSUFFICIENT_EVIDENCE"
```

This prevents low-confidence predictions from being presented as definitive verification.

### Important interpretation

A result such as:

```text
97.7% confidence
```

means:

> The verification model assigned approximately 97.7% confidence to the selected verification class for the retrieved evidence.

It should not be interpreted as an objectively calibrated 97.7% probability that the claim is true.

---

# 🔎 Evidence Retrieval Architecture

VeritasAI uses an evidence-first architecture.

Instead of directly predicting whether a claim is true, the system first retrieves relevant evidence.

```text
Claim
 ↓
Entity Extraction
 ↓
Query Generation
 ↓
Vector Retrieval
 ↓
FAISS
 ↓
Wikipedia / Wikidata
 ↓
Candidate Evidence
 ↓
Reranking
 ↓
Filtering
 ↓
DeBERTa NLI
 ↓
Final Verdict
```

---

# 🧮 FAISS Vector Search

FAISS is used as the vector similarity search layer.

Its responsibility is retrieval.

```text
Claim / Query
      ↓
Vector Representation
      ↓
FAISS Similarity Search
      ↓
Candidate Evidence
      ↓
Reranking
      ↓
Filtering
```

FAISS does **not** determine whether a claim is true.

It retrieves candidate evidence.

The NLI model is responsible for evaluating the relationship between the evidence and the claim.

---

# 📦 Current Evidence Index

During runtime, the system successfully loaded:

```text
Loaded FAISS index with 449 vectors
Loaded 449 metadata records
```

Therefore, the current prototype operates using:

```text
449 vectors
449 metadata records
```

---

# 📚 Knowledge Sources

The current prototype uses:

* Wikipedia
* Wikidata

as knowledge/evidence sources.

These sources form part of the retrieval layer.

The system can use retrieved content to provide evidence for NLI verification.

---

# 🧾 Evidence Metadata

Each evidence item can contain:

* Document ID
* Chunk ID
* Title
* Source
* URL
* Published date
* Chunk text
* Retrieval score
* Rerank score
* Source score
* Freshness score
* Quality score
* Quality label
* Stars
* Bias
* Reliability
* Category
* Highlight
* Verdict
* Confidence

---

# ⭐ Evidence Quality

The frontend presents evidence quality information such as:

```text
Credibility
Freshness
Quality Score
Quality Label
Reliability
Bias
Category
Published Date
```

This makes the verification process more transparent.

The system does not simply show:

```text
SUPPORTED
```

It also shows:

```text
WHY?
WHERE DID THE EVIDENCE COME FROM?
HOW RELEVANT WAS IT?
WHAT IS THE SOURCE QUALITY?
```

---

# 📊 Verification Metrics

The dashboard can display:

```text
Evidence
Filtered
Confidence
```

It can also display:

```text
Evidence Agreement
Majority Verdict
Supported Count
Contradicted Count
Insufficient Count
```

Example:

```text
Evidence Agreement: 100%

Supported: 1
Contradicted: 0
Insufficient: 0
```

---

# 🧠 Explainability

Explainability is a core design principle.

Traditional approach:

```text
POST
 ↓
FAKE
```

VeritasAI:

```text
POST
 ↓
CLAIM
 ↓
EVIDENCE
 ↓
VERDICT
 ↓
CONFIDENCE
 ↓
SOURCE
 ↓
EXPLANATION
```

The system provides an evidence-backed reasoning trail rather than only a classification label.

---

# 🌐 Why Mastodon?

Mastodon was selected for the social-media integration prototype because it provides:

1. A developer-friendly API.
2. Public post retrieval.
3. Hashtag-based streams.
4. WebSocket streaming.
5. Programmatic access to post events.
6. A suitable environment for prototyping real-time social-media monitoring.

The streaming interface allows VeritasAI to receive new post events programmatically.

---

# 🔗 Mastodon URL Verification

The social verification pipeline follows:

```text
Public Mastodon URL
        ↓
Mastodon REST API
        ↓
Post Content
        ↓
HTML/Text Extraction
        ↓
Claim Detection
        ↓
Evidence Retrieval
        ↓
DeBERTa NLI
        ↓
Verdict
```

The post extractor handles Mastodon's HTML-formatted content and extracts usable text.

---

# ⚡ Mastodon WebSocket Streaming

The live stream implementation:

1. Retrieves the Mastodon streaming host.
2. Creates a WebSocket connection.
3. Authenticates using an access token.
4. Subscribes to a hashtag.
5. Receives update events.
6. Parses the event payload.
7. Extracts the post.
8. Sends it for claim detection and verification.
9. Continues processing subsequent posts.
10. Reconnects when the connection is lost.

Example runtime:

```text
Connecting to Mastodon...
Connected successfully.
Waiting for new #sports posts...
```

---

# 🔄 WebSocket Reconnection

Real-time connections can be interrupted.

The implementation handles this using reconnect logic.

```text
WebSocket Connected
       ↓
Receive Posts
       ↓
Connection Lost
       ↓
Wait
       ↓
Reconnect
       ↓
Resume Monitoring
```

This prevents a temporary network/WebSocket failure from permanently stopping the monitoring process.

---

# 📱 Streamlit Frontend

The frontend is implemented using:

```text
Streamlit
```

The application provides:

## Verification

* Manual claim verification
* Mastodon post verification

## Live Monitoring

* Hashtag monitoring
* Start monitoring
* Stop monitoring
* Live claim detection
* Live verdicts
* Live confidence

## Evidence

* Evidence cards
* Source badge
* Credibility
* Freshness
* Quality
* Reliability
* Bias
* Category
* Evidence highlight
* Original source link

## Analytics

* Posts
* Claims
* Supported
* Contradicted
* Insufficient
* Verification history
* Live statistics

---

# 📊 Live Dashboard

The live dashboard displays statistics such as:

```text
Posts
Claims
Supported
Contradicted
Insufficient
```

Individual live claims are displayed with:

```text
Author
Timestamp
Detected Claim
Verdict
Confidence
Explanation
Evidence
```

---

# ⚙️ FastAPI Backend

The backend is implemented using:

```text
FastAPI
```

Responsibilities include:

* Claim verification
* Social post verification
* Batch verification
* Evidence retrieval
* NLI inference
* Database persistence
* Mastodon integration
* Live monitoring
* Analytics

---

# 🔌 API Endpoints

## Claim Verification

```http
POST /verification/verify
```

## Social Media Verification

```http
POST /verification/social/verify
```

## Batch Verification

```http
POST /verification/verify-batch
```

## Start Live Monitoring

```http
POST /social/live/start
```

## Stop Live Monitoring

```http
POST /social/live/stop
```

## Live Monitoring Status

```http
GET /social/live/status
```

## Live Results

```http
GET /social/live/results
```

## Analytics Statistics

```http
GET /analytics/stats
```

## Verification History

```http
GET /analytics/history
```

---

# 🗄️ Database

The backend uses SQLAlchemy for database interaction.

Verification information can be persisted, including:

* Claim
* Verdict
* Confidence
* Explanation

This supports:

* Verification history
* Analytics
* Dashboard statistics

---

# 🏗️ High-Level Architecture

```text
                         ┌───────────────────┐
                         │       USER        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    STREAMLIT      │
                         │    FRONTEND       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │      FASTAPI      │
                         │      BACKEND      │
                         └─────────┬─────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
     Claim Verification    Social Verification    Live Monitoring
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   ▼
                         ┌───────────────────┐
                         │  CLAIM DETECTION  │
                         └─────────┬─────────┘
                                   ▼
                         ┌───────────────────┐
                         │ ENTITY EXTRACTION │
                         └─────────┬─────────┘
                                   ▼
                         ┌───────────────────┐
                         │ EVIDENCE RETRIEVAL│
                         └─────────┬─────────┘
                                   ▼
                         ┌───────────────────┐
                         │       FAISS       │
                         └─────────┬─────────┘
                                   ▼
                  ┌─────────────────────────────┐
                  │ Wikipedia / Wikidata        │
                  └──────────────┬──────────────┘
                                 ▼
                         ┌───────────────────┐
                         │ EVIDENCE FILTERING│
                         └─────────┬─────────┘
                                   ▼
                         ┌───────────────────┐
                         │   DeBERTa NLI     │
                         └─────────┬─────────┘
                                   ▼
                 ┌─────────────────┼─────────────────┐
                 ▼                 ▼                 ▼
             SUPPORTED       CONTRADICTED     INSUFFICIENT
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   ▼
                         ┌───────────────────┐
                         │ EXPLANATION +     │
                         │ CONFIDENCE        │
                         └─────────┬─────────┘
                                   ▼
                         ┌───────────────────┐
                         │    STREAMLIT      │
                         └───────────────────┘
```

---

# ⚡ Real-Time Architecture

```text
                   MASTODON
                      │
                      │ WebSocket
                      ▼
                HASHTAG STREAM
                      │
                      ▼
                  NEW POST
                      │
                      ▼
              POST EXTRACTION
                      │
                      ▼
              CLAIM DETECTION
                      │
                      ▼
             EVIDENCE RETRIEVAL
                      │
                      ▼
                 FAISS
                      │
                      ▼
             Wikipedia/Wikidata
                      │
                      ▼
               EVIDENCE FILTER
                      │
                      ▼
                DeBERTa NLI
                      │
                      ▼
              VERIFICATION RESULT
                      │
                      ▼
             STREAMLIT DASHBOARD
```

---

# 🧪 Example Demo — Movie Claim

A test claim used during live monitoring:

```text
The movie Titanic was directed by James Cameron and released in 1997.
```

VeritasAI detected the claim and retrieved relevant Wikipedia evidence.

Example result:

```text
🟢 SUPPORTED

Confidence: ~99.5%
```

The system also displayed an explanation stating that the evidence from Wikipedia supports the claim.

---

# 🧪 Example Demo — Science Claim

Example social-media claim:

```text
A rare tidal disruption event exposed a massive wandering black hole
about 30,000 light-years from its galaxy’s center.
```

The system:

```text
Mastodon Post
      ↓
Claim Detection
      ↓
Article Retrieval
      ↓
Evidence
      ↓
DeBERTa NLI
      ↓
SUPPORTED
```

Example tested result:

```text
🟢 SUPPORTED

Confidence: ~97.7%
```

---

# 🧪 Example Demo — Insufficient Evidence

The system was also tested with claims for which relevant evidence was unavailable.

Example behavior:

```text
🟡 INSUFFICIENT EVIDENCE

Confidence: 0.0%

Evidence: 0
Filtered: 0
```

Reason:

```text
No relevant evidence was retrieved.
```

This demonstrates that VeritasAI does not force unsupported claims into a binary true/false decision.

---

# 🛠️ Engineering Challenges

## 1. Initial ML Approach

The project initially explored a custom ML-based approach.

The available laptop/GPU environment made large-scale model training and repeated experimentation difficult.

### Challenge

* Limited GPU resources
* Limited VRAM
* Limited laptop specifications
* Memory pressure
* Training time

### Decision

Move to a pretrained NLI Transformer.

---

# 2. DeBERTa OOM Issues

Even after selecting a pretrained model, DeBERTa caused memory pressure/OOM problems.

### Causes

The development environment had to simultaneously handle:

```text
PyTorch
+
Transformer Model
+
Tokenizer
+
FAISS
+
FastAPI
+
Streamlit
+
Other Dependencies
```

### Solution

* Cleaned unnecessary files from the C drive.
* Freed system resources.
* Restarted the development environment.
* Used `low_cpu_mem_usage=True`.
* Implemented shared model loading.
* Avoided repeated model initialization.
* Used CPU inference where necessary.

---

# 3. Claim Extraction Issues

At an early stage, social posts containing article headlines and URLs were sometimes processed as having:

```text
CLAIMS FOUND: 0
```

The extraction pipeline was improved to handle article-linked posts and headline-style factual claims.

Example successful extraction:

```text
A rare tidal disruption event exposed a massive wandering black hole
about 30,000 light-years from its galaxy’s center.
```

---

# 4. Evidence Retrieval Issues

Not every retrieved search result is necessarily relevant.

For example, a query could return a Wikipedia result that is semantically related but not actually useful for the claim.

Therefore the pipeline includes:

```text
Retrieval
   ↓
Reranking
   ↓
Filtering
   ↓
Verification
```

This reduces the possibility of irrelevant documents being treated as evidence.

---

# 5. Mastodon Authentication

The live monitoring feature initially failed because the Mastodon access token was not configured.

Initial error:

```text
MASTODON_ACCESS_TOKEN is not set.
```

After configuring the required token:

```text
Connected successfully.
Waiting for new #sports posts...
```

The live monitoring pipeline then successfully processed new posts.

---

# 6. WebSocket Disconnections

During testing, the Mastodon WebSocket occasionally disconnected.

Example:

```text
WebSocketConnectionClosedException
Connection to remote host was lost.
```

The streaming implementation includes reconnect behavior:

```text
Disconnected
    ↓
Wait
    ↓
Reconnect
    ↓
Continue monitoring
```

---

# 7. Frontend / Backend Integration

During development, frontend imports and backend utility organization caused errors such as:

```text
ImportError:
cannot import name 'get_stats' from 'utils'
```

The project was progressively reorganized into clearer modules for:

* API utilities
* frontend components
* analytics
* verification
* social services

---

# 🔐 Security Considerations

Credentials should never be hard-coded into the repository.

Sensitive configuration should be stored in environment variables.

Example:

```env
MASTODON_INSTANCE=https://mastodon.social
MASTODON_ACCESS_TOKEN=YOUR_TOKEN
```

The actual access token should never be committed to GitHub.

---

# 📦 Technology Stack

| Layer                    | Technology                 |
| ------------------------ | -------------------------- |
| Programming Language     | Python                     |
| Frontend                 | Streamlit                  |
| Backend                  | FastAPI                    |
| API                      | REST / JSON                |
| Deep Learning            | PyTorch                    |
| NLP                      | Hugging Face Transformers  |
| NLI Model                | DeBERTa-v3-base            |
| Zero-Shot Classification | Hugging Face Pipeline      |
| Vector Search            | FAISS                      |
| Knowledge Sources        | Wikipedia + Wikidata       |
| Social Platform          | Mastodon                   |
| Social API               | Mastodon REST API          |
| Real-Time Streaming      | Mastodon WebSocket API     |
| Database Layer           | SQLAlchemy                 |
| Environment              | Python Virtual Environment |

---

# 📁 Project Structure

```text
VeritasAI/
│
├── backend/
│   │
│   └── app/
│       │
│       ├── api/
│       │   ├── routes/
│       │   │   ├── verification.py
│       │   │   ├── retrieval.py
│       │   │   ├── claims.py
│       │   │   ├── entity.py
│       │   │   └── ...
│       │   │
│       │   └── router.py
│       │
│       ├── verification/
│       │   ├── pipeline.py
│       │   ├── verifier.py
│       │   ├── model.py
│       │   ├── schemas.py
│       │   └── response_schema.py
│       │
│       ├── models/
│       │   └── deberta.py
│       │
│       ├── retrieval/
│       │   └── vector_store.py
│       │
│       ├── social/
│       │   ├── mastodon_client.py
│       │   ├── mastodon_stream.py
│       │   ├── post_extractor.py
│       │   ├── service.py
│       │   ├── router.py
│       │   └── ...
│       │
│       ├── analytics/
│       │
│       ├── database/
│       │
│       ├── url/
│       │
│       ├── pdf/
│       │
│       ├── image/
│       │
│       └── main.py
│
├── frontend/
│   │
│   ├── components/
│   │   ├── analytics.py
│   │   ├── single_verification.py
│   │   ├── verdict_card.py
│   │   ├── metrics.py
│   │   ├── explanation_card.py
│   │   ├── evidence_card.py
│   │   ├── source_badge.py
│   │   ├── trust_gauge.py
│   │   └── ...
│   │
│   ├── utils/
│   │
│   ├── assets/
│   │
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🐍 Installation

## Prerequisites

Recommended environment:

* Python 3.10+
* Git
* Internet connection
* Sufficient RAM for Transformer inference

A dedicated GPU is **not mandatory** for the current implementation because CPU inference is supported.

However, additional compute resources would improve inference latency and scalability.

---

# 📥 Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd VeritasAI
```

---

# 🐍 Create Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 📦 Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file where required.

Example:

```env
MASTODON_INSTANCE=https://mastodon.social
MASTODON_ACCESS_TOKEN=YOUR_MASTODON_ACCESS_TOKEN
```

Never commit real credentials.

Add the following to `.gitignore`:

```text
.env
.env.*
```

---

# ▶️ Run Backend

Open a terminal and navigate to:

```powershell
cd backend
```

Activate the environment if necessary:

```powershell
..\venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Run Frontend

Open another terminal.

Navigate to:

```powershell
cd frontend
```

Activate the environment:

```powershell
..\venv\Scripts\Activate.ps1
```

Run Streamlit:

```powershell
python -m streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

---

# 🧪 Demo Flow

The recommended demonstration sequence is:

```text
1. Start FastAPI
        ↓
2. Start Streamlit
        ↓
3. Open VeritasAI Dashboard
        ↓
4. Demonstrate Manual Claim Verification
        ↓
5. Show Evidence + Verdict
        ↓
6. Demonstrate Mastodon URL Verification
        ↓
7. Show Detected Claim
        ↓
8. Show Evidence + Source
        ↓
9. Start Live Monitoring
        ↓
10. Select Hashtag
        ↓
11. Post a Test Claim on Mastodon
        ↓
12. WebSocket Receives New Post
        ↓
13. Automatic Claim Detection
        ↓
14. Automatic Evidence Retrieval
        ↓
15. Automatic NLI Verification
        ↓
16. Live Verdict Appears
        ↓
17. Show Live Statistics
        ↓
18. Stop Monitoring
```

---

# 🎬 Recommended Demo Claims

## Movie

```text
The movie Titanic was directed by James Cameron and released in 1997.
```

Expected:

```text
🟢 SUPPORTED
```

---

## Contradiction

```text
Titanic was directed by Christopher Nolan and released in 2010.
```

Expected behavior:

```text
🔴 CONTRADICTED
```

depending on the retrieved evidence.

---

## Insufficient Evidence

Use an intentionally obscure or unsupported claim where the current evidence sources do not contain sufficient relevant information.

Expected:

```text
🟡 INSUFFICIENT EVIDENCE
```

---

# 📈 Example Live Statistics

During live monitoring, the dashboard can show:

```text
Posts
1

Claims
1

🟢 Supported
1

🔴 Contradicted
0

🟡 Insufficient
0
```

Individual claims are displayed with:

```text
Author
Timestamp
Detected Claim
Verdict
Confidence
Explanation
Evidence
```

---

# ⚠️ Current Scope & Limitations

VeritasAI is an evidence-grounded prototype.

It does not guarantee absolute truth.

Verification depends on:

* Availability of evidence
* Quality of retrieved sources
* Retrieval relevance
* Evidence filtering
* Model behavior
* Model confidence
* Knowledge-source coverage

---

## Important Limitation: Insufficient Evidence

```text
INSUFFICIENT EVIDENCE
```

does not mean:

```text
FALSE
```

It means:

> The available evidence was not sufficient to establish support or contradiction.

---

## Important Limitation: Live Monitoring

The current live feature monitors:

```text
Mastodon POST EVENTS
```

through WebSockets.

It does not currently process:

```text
VIDEO
AUDIO
LIVE BROADCAST VIDEO
```

---

# 🎥 Future Video Livestream Verification

A future version could extend the system to live video platforms.

Possible architecture:

```text
             LIVE VIDEO
                 │
                 ▼
          AUDIO EXTRACTION
                 │
                 ▼
          SPEECH-TO-TEXT
                 │
                 ▼
          CLAIM DETECTION
                 │
                 ▼
        EVIDENCE RETRIEVAL
                 │
                 ▼
              FAISS
                 │
                 ▼
          DeBERTa NLI
                 │
                 ▼
       REAL-TIME VERDICT
                 │
                 ▼
          USER ALERT
```

This would require additional infrastructure for:

* Video ingestion
* Audio extraction
* Automatic Speech Recognition
* Streaming infrastructure
* Low-latency inference
* GPU acceleration
* Real-time event processing

---

# 🚀 Future Roadmap

## Phase 1 — Current Prototype

```text
✓ Claim Verification
✓ Social Post Verification
✓ Evidence Retrieval
✓ FAISS Search
✓ Wikipedia/Wikidata
✓ DeBERTa NLI
✓ Source Metadata
✓ Explainability
✓ Mastodon WebSocket Monitoring
✓ Live Dashboard
```

---

## Phase 2 — More Evidence Sources

Potential integrations:

* Reuters
* Associated Press
* Government databases
* Scientific publications
* News APIs
* Domain-specific trusted sources

---

## Phase 3 — More Social Platforms

Potential integrations:

* X
* Reddit
* YouTube
* News feeds
* Other federated social platforms

---

## Phase 4 — Video Livestream Verification

Potential pipeline:

```text
Video
 ↓
Audio
 ↓
Speech-to-Text
 ↓
Claim Detection
 ↓
Evidence Retrieval
 ↓
NLI
 ↓
Real-Time Alert
```

---

## Phase 5 — Production Infrastructure

Potential technologies:

* Docker
* Cloud deployment
* GPU inference
* Redis
* Kafka
* Authentication
* Multi-user support
* Monitoring
* Logging
* Distributed workers

---

## Phase 6 — Advanced Reasoning

Potential improvements:

* Claim decomposition
* Multi-hop reasoning
* Cross-source consensus
* Temporal reasoning
* Source reputation learning
* Evidence graph construction
* Better contradiction detection
* Improved confidence calibration

---

# 🔒 Production Considerations

For production deployment, the system could be extended with:

```text
Authentication
       +
API Gateway
       +
Distributed Workers
       +
Message Queue
       +
Vector Database
       +
GPU Inference
       +
Monitoring
       +
Logging
       +
Source Reputation
```

This would allow the prototype architecture to evolve toward high-volume real-time verification.

---

# 💡 Why VeritasAI?

Traditional misinformation detection:

```text
Social Post
     ↓
ML Classifier
     ↓
FAKE / REAL
```

VeritasAI:

```text
Social Post
     ↓
Claim Detection
     ↓
Entity Identification
     ↓
Evidence Retrieval
     ↓
Vector Search
     ↓
Evidence Ranking
     ↓
Evidence Filtering
     ↓
NLI
     ↓
SUPPORTED
CONTRADICTED
INSUFFICIENT
     ↓
Confidence
     ↓
Source Quality
     ↓
Explanation
```

The key differentiator is:

> **VeritasAI provides an evidence-grounded assessment instead of only a black-box classification label.**

---

# 🧩 Core Components

## Claim Detection

Identifies factual-looking claims from user input and social-media posts.

## Entity Identification

Identifies important entities that can be used to retrieve relevant evidence.

## Evidence Retrieval

Searches available knowledge sources for potentially relevant information.

## FAISS

Performs vector similarity retrieval.

## Evidence Ranking

Ranks candidate evidence based on relevance.

## Evidence Filtering

Removes evidence that does not meet the required relevance criteria.

## DeBERTa NLI

Evaluates whether evidence supports or contradicts the claim.

## Source Evaluation

Displays source-level credibility and quality metadata.

## Explanation

Provides human-readable verification reasoning.

## Mastodon Integration

Retrieves and verifies public Mastodon posts.

## Live Monitoring

Processes new Mastodon posts in real time through WebSocket streaming.

## Analytics

Provides verification history and live monitoring statistics.

---

# 🧠 Core Verification Philosophy

VeritasAI follows:

```text
RETRIEVE
   ↓
COMPARE
   ↓
VERIFY
   ↓
EXPLAIN
```

rather than:

```text
CLASSIFY
   ↓
TRUE / FALSE
```

This design makes the system more transparent and useful for applications where evidence and explainability matter.

---

# 🏆 Project Outcome

The final prototype demonstrates an integrated AI verification pipeline combining:

```text
Natural Language Processing
        +
Natural Language Inference
        +
Vector Search
        +
Knowledge Retrieval
        +
Evidence Ranking
        +
Source Evaluation
        +
Social Media APIs
        +
WebSocket Streaming
        +
FastAPI
        +
Streamlit
        +
Database Persistence
```

The system has been tested for:

* Manual claim verification
* Social-media post verification
* Supported claims
* Contradicted/insufficient evidence scenarios
* Evidence retrieval
* Source display
* Mastodon integration
* Real-time hashtag monitoring
* Live claim detection
* Live verification
* WebSocket reconnection behavior
* Analytics
* Verification history

---

# 📌 Final Architecture Summary

```text
                         VERITASAI
                             │
             ┌───────────────┴───────────────┐
             │                               │
       NORMAL VERIFICATION              LIVE MONITORING
             │                               │
             ▼                               ▼
       User Claim                       Mastodon
             │                         WebSocket
             │                               │
             ▼                               ▼
      Claim Detection                    New Post
             │                               │
             └───────────────┬───────────────┘
                             ▼
                    Entity Identification
                             │
                             ▼
                    Evidence Retrieval
                             │
                             ▼
                           FAISS
                             │
                             ▼
                   Wikipedia / Wikidata
                             │
                             ▼
                    Evidence Filtering
                             │
                             ▼
                       DeBERTa NLI
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
         SUPPORTED      CONTRADICTED    INSUFFICIENT
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                   Confidence + Evidence
                             │
                             ▼
                    Source Evaluation
                             │
                             ▼
                       Explanation
                             │
                             ▼
                    Streamlit Dashboard
```

---

# 📋 Key Takeaways

### 1. Evidence-Grounded

Claims are evaluated against retrieved evidence.

### 2. NLI-Based

DeBERTa evaluates the relationship between evidence and claim.

### 3. Explainable

The system exposes evidence, source information, confidence and reasoning.

### 4. Domain-Flexible

Zero-shot classification supports different topics without requiring a dedicated classifier for every domain.

### 5. Real-Time

Mastodon WebSocket streaming enables continuous monitoring of new public posts.

### 6. Resource-Conscious

The system was optimized to run within local hardware constraints using shared model loading, CPU inference and memory-conscious model initialization.

### 7. Extensible

The architecture can be extended with additional evidence sources, social platforms, video streams, cloud infrastructure and advanced reasoning.

---

# 🛡️ VeritasAI

## From Social-Media Claims to Evidence-Backed Verdicts.

```text
✓ Claim Detection
✓ Evidence Retrieval
✓ NLI Verification
✓ Explainability
✓ Real-Time Social Monitoring
``` 
=======
**Claim Detection · Evidence Retrieval · NLI Verification · Explainability · Real-Time Social Monitoring**
