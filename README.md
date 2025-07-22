# llm-agents-for-smartcities-paper

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?style={0}&logo=FastAPI&logoColor=white)
![git](https://img.shields.io/badge/Git-F05032.svg?style={0}&logo=Git&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style={0}&logo=Pydantic&logoColor=white)
![pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style={0}&logo=Pytest&logoColor=white)

---

## Overview

Enabling smarter urban governance, llm-agents-for-smartcities-paper advances city management by orchestrating multiple AI agents powered by large language models and retrieval-augmented generation techniques. Through a carefully designed multi-agent system, diverse urban data sources are unified and interpreted in real time to answer complex city management queries. Specialized agents collaborate to parse user needs, retrieve context from databases and APIs, synthesize comprehensive responses, and ensure factual accuracy. Demonstrated in the context of St. Petersburg’s Digital Urban Platform, the approach accelerates and enriches decision-making, showing remarkable accuracy and efficiency gains compared to traditional expert analysis. This work lays the foundation for hybrid, AI-driven urban planning, making strategic insights more accessible and operational for city leaders and researchers alike.

---

## Table of Contents

- [Content](#content)
- [Algorithms](#algorithms)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Documentation](#documentation)
- [Citation](#citation)

---

## Content

This project enables intelligent urban management by integrating multi-agent large language model (LLM) systems with retrieval-augmented generation (RAG) pipelines and diverse city data sources. At its core, specialized LLM agents collaboratively parse and route urban management queries, dynamically retrieving relevant context from vector databases and city APIs. A modular backend—supporting both API endpoints and containerized deployment—facilitates seamless query processing, system monitoring, and document retrieval. ChromaDB manages efficient vector-based access to heterogeneous city datasets, while the architecture supports flexible integration of multiple LLM backends. Collectively, these components provide robust analytical and decision-support capabilities, synthesizing real-time, context-rich information to enhance urban analytics and facilitate more effective strategic planning for smart cities.

---

## Algorithms

The project implements a hierarchical multi-agent system powered by large language models for smart city management. Core computational strategies include Retrieval-Augmented Generation (RAG) to enhance question answering with relevant external data, and dynamic function/tool selection by LLM agents to route user queries to specialized analytical pipelines. Agents interact with APIs, databases, and vector stores to extract, process, and synthesize heterogeneous urban data. An agent-based validation step ensures output correctness by verifying generated responses. This workflow enables real-time decision support, context-aware information retrieval, and automation of complex urban management tasks. These algorithms are essential for integrating distributed, task-specialized intelligence, improving accuracy, and accelerating city-scale analysis compared to traditional expert-driven processes.

---

## Installation

Install llm-agents-for-smartcities-paper using one of the following methods:

**Build from source:**

1. Clone the llm-agents-for-smartcities-paper repository:
```sh
git clone https://github.com/andreygetmanov/llm-agents-for-smartcities-paper
```

2. Navigate to the project directory:
```sh
cd llm-agents-for-smartcities-paper
```

3. Install the project dependencies:
```sh
pip install -r requirements.txt
```

---

## Getting Started

To start using the LLM Agents for Smart City Management project, follow these steps:

1. **Set Up Environment Variables**
   - Create the `$NSS_NPA_TOKEN` environment variable on your server.

2. **Clone the Repository and Checkout Branch**
```sh
cd /var/essdata/llm/project/BIAM-Urb
git checkout <required_branch>
git pull
```

3. **Create Configuration File**
   - In the root of the project directory, create a file named `config.env` with the following content (replace placeholder URLs with actual values):
```env
LLAMA_URL=<url>
LLAMA_FC_URL=<url>
ENDPOINT_LISTINGS_URL=<url>
ENDPOINT_CITY_URL=<url>
ENDPOINT_METRICS_URL=<url>
ENDPOINT_PROVISION_URL=<url>
ENDPOINT_TABLES_URL=<url>
```

4. **Build and Run Docker Container**
```sh
docker container stop llm_city_app-container
docker container rm llm_city_app-container
# Use --no-cache if the entire image needs to be rebuilt (e.g., dependencies changed)
docker build -t llm_city_app --build-arg NSS_NPA_TOKEN=$NSS_NPA_TOKEN -f docker/app/Dockerfile --no-cache .
docker run -d --restart always -p <port>:80 --name llm_city_app-container llm_city_app
```

5. **Run ChromaDB and the Embedding Model**
   - Copy `docker/chroma/compose.yaml` to your server, then run:
```sh
docker compose up
```

6. **Testing the Pipeline**
   - To test via terminal:
```sh
curl -v POST http://<ip>:<port>/question -H 'Content-Type: application/json' -d '{"question_body": "What are the problems of demographic development of St. Petersburg?"}'
```
   - To explore the API in the browser, visit:
```
http://<ip>:<port>/docs/
```
   - To check application logs:
```sh
docker logs --follow --timestamps llm_city_app-container
```

7. **Local API Testing**
   - Start the server from the project root:
```sh
fastapi run main.py --proxy-headers --port 80
```
   - Then, test with:
```sh
curl -v POST http://0.0.0.0:80/question -H 'Content-Type: application/json' -d '{"question_body": "What are the problems of demographic development of St. Petersburg?"}'
```
   - Or open in your browser:
```
http://localhost/docs#/
```

---

## Examples

Examples of how this should work and how it should be used are available [here](https://github.com/andreygetmanov/llm-agents-for-smartcities-paper/tree/main/experiments/llama-notebook.ipynb).

---

## Documentation

A detailed llm-agents-for-smartcities-paper description is available [here](https://github.com/andreygetmanov/llm-agents-for-smartcities-paper/tree/main/chroma_rag/docs).

---

## Citation

If you use this software, please cite it as below.

### APA format:

    andreygetmanov (2025). llm-agents-for-smartcities-paper repository [Computer software]. https://github.com/andreygetmanov/llm-agents-for-smartcities-paper

### BibTeX format:

    @misc{llm-agents-for-smartcities-paper,

        author = {andreygetmanov},

        title = {llm-agents-for-smartcities-paper repository},

        year = {2025},

        publisher = {github.com},

        journal = {github.com repository},

        howpublished = {\url{https://github.com/andreygetmanov/llm-agents-for-smartcities-paper.git}},

        url = {https://github.com/andreygetmanov/llm-agents-for-smartcities-paper.git}

    }

---