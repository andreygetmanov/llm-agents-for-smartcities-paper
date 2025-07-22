# llm-agents-for-smartcities-paper

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?style={0}&logo=FastAPI&logoColor=white)
![git](https://img.shields.io/badge/Git-F05032.svg?style={0}&logo=Git&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style={0}&logo=Pydantic&logoColor=white)
![pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style={0}&logo=Pytest&logoColor=white)

## Overview

Leveraging recent advances in large language models, this project pioneers a multi-agent AI system designed to transform smart city management. By orchestrating specialized LLM agents, the system bridges unstructured user questions with curated urban data to provide rapid, reliable decision support for city planners and administrators. Its modular architecture facilitates intelligent query analysis, real-time data integration, and fact-based answer generation using both Retrieval-Augmented Generation (RAG) and advanced analytic workflows. Demonstrating remarkable gains in both response accuracy and speed, the research advances scalable, agent-driven approaches to urban planning and highlights the possibilities of automated reasoning in addressing complex city management challenges, ultimately enabling more informed and timely decisions in dynamic urban environments.

## Table of Contents

- [Content](#content)
- [Algorithms](#algorithms)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Documentation](#documentation)
- [Citation](#citation)

## Content

This project presents a modular, multi-agent AI system designed to enhance smart city management through advanced decision support. Central to its architecture are distributed language model agents, each specializing in tasks such as tool selection, context retrieval, and answer validation. The system integrates user-facing chatbot interfaces, an orchestration layer for intelligent query routing, and Retrieval-Augmented Generation pipelines coupled with vector databases to ensure factual and context-aware responses. It leverages configurable connectors for diverse language models and data sources, supporting workflows that combine real-time urban APIs with structured document resources. Datasets of expert-validated urban queries and comprehensive analytics modules underpin its evaluation, collectively enabling dynamic, scalable, and accurate urban analysis essential for research and informed city planning.

## Algorithms

The project employs a multi-agent system orchestrated by large language models (LLMs) to process urban queries and support smart city management. Key computational methods include dynamic agent orchestration for query routing, Retrieval-Augmented Generation (RAG) for factually accurate responses, and hierarchical decision pipelines that integrate real-time city APIs with curated document databases. Specialized agents select, validate, and synthesize relevant data using both open and closed-source LLMs. Batched document transformation and embedding enable efficient knowledge retrieval. These methods collectively automate complex data extraction and reasoning, dramatically improving response time and accuracy for urban analytics—facilitating scalable, reliable, and rapid decision support in dynamic smart city environments.

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

## Getting Started

1. **Clone the repository and switch to the required branch:**

```bash
cd /var/essdata/llm/project/BIAM-Urb
git checkout <required_branch>
git pull
```

2. **Set up configuration:**

Create a `config.env` file in the root directory with the following content, replacing `<url>` with your endpoints:

```env
LLAMA_URL=<url>
LLAMA_FC_URL=<url>
ENDPOINT_LISTINGS_URL=<url>
ENDPOINT_CITY_URL=<url>
ENDPOINT_METRICS_URL=<url>
ENDPOINT_PROVISION_URL=<url>
ENDPOINT_TABLES_URL=<url>
```

3. **Build and run the Docker container:**

```bash
docker container stop llm_city_app-container
docker container rm llm_city_app-container
# Use --no-cache if dependencies have changed
docker build -t llm_city_app --build-arg NSS_NPA_TOKEN=$NSS_NPA_TOKEN -f docker/app/Dockerfile --no-cache .
docker run -d --restart always -p <port>:80 --name llm_city_app-container llm_city_app
```

4. **(Optional) Set up ChromaDB and the embedding model:**

Copy the `docker/chroma/compose.yaml` file to your server and run:

```bash
docker compose up
```

5. **Test the API:**

- Send a question to the running application:

```bash
curl -v POST http://<ip>:<port>/question -H 'Content-Type: application/json' -d '{"question_body": "What are the problems of demographic development of St. Petersburg?"}'
```

- Or, visit the API documentation:

```
http://<ip>:<port>/docs/
```

- View application logs:

```bash
docker logs --follow --timestamps llm_city_app-container
```

6. **Test API locally:**

- Start the server locally:

```bash
fastapi run main.py --proxy-headers --port 80
```

- Send a query from your terminal:

```bash
curl -v POST http://0.0.0.0:80/question -H 'Content-Type: application/json' -d '{"question_body": "What are the problems of demographic development of St. Petersburg?"}'
```

- Visit local API docs in your browser:

```
http://localhost/docs#/
```

## Examples

Examples of how this should work and how it should be used are available [here](https://github.com/andreygetmanov/llm-agents-for-smartcities-paper/tree/main/experiments/llama-notebook.ipynb).

## Documentation

A detailed llm-agents-for-smartcities-paper description is available [here](https://github.com/andreygetmanov/llm-agents-for-smartcities-paper/tree/main/chroma_rag/docs).

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