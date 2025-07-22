# llm-agents-for-smartcities-paper

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?style={0}&logo=FastAPI&logoColor=white)
![git](https://img.shields.io/badge/Git-F05032.svg?style={0}&logo=Git&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style={0}&logo=Pydantic&logoColor=white)
![pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style={0}&logo=Pytest&logoColor=white)

## Overview

Harnessing the power of large language models (LLMs) and multi-agent AI systems, the initiative pioneers a novel framework for smart city management by enabling advanced, interpretable decision support. By orchestrating specialized language agents and integrating both real-time urban data and semantic document retrieval, the system delivers rapid, context-aware insights for complex urban planning and governance challenges. Addressing key barriers such as fragmented data, decision inconsistency, and automation gaps, the approach reflects cutting-edge research in leveraging AI for actionable, auditable urban intelligence. Validated within real-world city contexts, the solution markedly improves the speed, accuracy, and relevance of policy and strategy recommendations, exemplifying the transformative role of multi-agent LLM systems in fostering data-driven urban innovation.

## Table of Contents

- [Content](#content)
- [Algorithms](#algorithms)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Documentation](#documentation)
- [Citation](#citation)

## Content

This project centers on a modular, multi-agent AI framework tailored for smart city management and decision support. Large language models (LLMs) serve as the core reasoning engines, integrated with retrieval-augmented generation for contextual information access. Specialized agents collaborate to process user queries, dynamically directing them through data validation, reasoning pipelines, and external urban data sources. Supporting modules manage natural language processing, semantic search, and real-time API interactions, with ChromaDB facilitating efficient document retrieval. The system’s configuration allows adaptation to diverse city environments and applications, exemplified by its deployment in St. Petersburg. Collectively, these components enable interpretable, scalable, and auditable insights for urban planning, demographic analysis, and policy evaluation, significantly improving the speed and relevance of smart city decisions.

## Algorithms

The project implements a modular multi-agent system leveraging Large Language Models (LLMs) for smart city management. Central to its approach is an agent-based orchestration algorithm, where specialized LLM agents dynamically route user queries, identify relevant analytical tools, and coordinate information retrieval. Retrieval-Augmented Generation (RAG) techniques combine real-time city API data with document-based knowledge via dense vector semantic search. The pipeline employs function-calling LLMs for automated tool selection and validation logic, ensuring accurate context extraction and response synthesis. Additional validation agents review and adjust tool choices to maximize relevance. These computational strategies enable rapid, context-aware decision support, streamlining urban planning tasks and enhancing response accuracy over standalone LLMs, while integrating both structured and unstructured urban data sources.

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

To start using this project, follow these steps:

1. Check out the required branch and update the repository:

```bash
cd /var/essdata/llm/project/BIAM-Urb
git checkout <required_branch>
git pull
```

2. Create a `config.env` file in the root of the project with your configuration. Example:

```bash
LLAMA_URL=<url>
LLAMA_FC_URL=<url>
ENDPOINT_LISTINGS_URL=<url>
ENDPOINT_CITY_URL=<url>
ENDPOINT_METRICS_URL=<url>
ENDPOINT_PROVISION_URL=<url>
ENDPOINT_TABLES_URL=<url>
```

3. (Optional, if you're using the RAG pipelines in Docker) Build and run the Docker container:

```bash
docker container stop llm_city_app-container
docker container rm llm_city_app-container
docker build -t llm_city_app --build-arg NSS_NPA_TOKEN=$NSS_NPA_TOKEN -f docker/app/Dockerfile --no-cache .
docker run -d --restart always -p <port>:80 --name llm_city_app-container llm_city_app
```

4. Test the pipeline by sending a request:

```bash
curl -v POST http://<ip>:<port>/question -H 'Content-Type: application/json' -d '{"question_body": "What are the problems of demographic development of St. Petersburg?"}'
```

Or access the API documentation in your browser:

```
http://<ip>:<port>/docs/
```

The application logs can be checked on the server:

```bash
docker logs --follow --timestamps llm_city_app-container
```

5. To run the API locally:

```bash
fastapi run main.py --proxy-headers --port 80
```

Send a test request:

```bash
curl -v POST http://0.0.0.0:80/question -H 'Content-Type: application/json' -d '{"question_body": "What are the problems of demographic development of St. Petersburg?"}'
```

Then open the local docs:

```
http://localhost/docs#/
```

6. (Optional) To set up ChromaDB and the embedding model, copy the provided Docker Compose file and run:

```bash
# Copy the file docker/chroma/compose.yaml to your server if needed

docker compose up
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