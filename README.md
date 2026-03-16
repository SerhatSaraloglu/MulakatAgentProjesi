# AI Interview Agent

AI-powered role-based interview simulation system using RAG and local Large Language Models (LLMs).

## Overview

AI Interview Agent is a project that simulates job interviews using a local Large Language Model. The system generates interview questions, interacts with the user, and evaluates responses in an interview-style conversation.

The project uses a **Retrieval-Augmented Generation (RAG)** architecture to retrieve relevant information from a knowledge base and generate context-aware interview questions. It also supports **role-based interviews**, allowing users to practice interviews for specific positions such as **Sales Consultant**.

## Features

- AI-powered interview simulation
- Role-based interview support (e.g. Sales Consultant)
- Interview question generation
- Answer evaluation with LLM
- Retrieval-Augmented Generation (RAG)
- Local LLM integration using LM Studio
- Streamlit-based user interface
- JSON knowledge base support

## Role-Based Interview Example

The system can simulate interviews for specific roles.

Example role: **Sales Consultant**

Possible interview topics include:

- Customer communication
- Sales strategies
- Handling customer objections
- Product knowledge
- Problem solving in sales scenarios

The AI generates questions related to the selected role and evaluates the user's answers using information retrieved from the knowledge base.

## Technologies Used

- Python
- LM Studio
- RAG (Retrieval-Augmented Generation)
- Chroma Vector Database
- Streamlit
- JSON Knowledge Base

## Installation

Clone the repository:

git clone https://github.com/SerhatSaraloglu/MulakatAgentProjesi.git

Go to the project folder:

cd MulakatAgentProjesi

Install dependencies:

pip install -r requirements.txt

## Running the Project

Make sure **LM Studio** is running with a loaded model.

Then start the Streamlit interface:

streamlit run main.py

## Project Structure

MulakatAgentProjesi  
│  
├── main.py  
├── interview_agent.py  
├── rag_system.py  
├── knowledge_base.json  
├── requirements.txt  
└── README.md  

## Future Improvements

- Support for more job roles
- Improved answer evaluation
- Voice-based interview interaction
- Web deployment

## Author

Serhat Saraloğlu  
Computer Engineering Student  
Süleyman Demirel University

---

## Türkçe Açıklama

AI Interview Agent, kullanıcılarla **rol bazlı mülakat simülasyonu** gerçekleştiren bir yapay zeka sistemidir.

Bu sistem **RAG (Retrieval-Augmented Generation)** mimarisini kullanarak bir bilgi tabanından ilgili bilgileri çekip kullanıcıya mülakat soruları sorar ve verilen cevapları değerlendirir.

Örneğin kullanıcı **Satış Danışmanı (Sales Consultant)** rolü için mülakat simülasyonu yapabilir. Yapay zeka bu role uygun sorular üretir ve verilen cevapları analiz eder.

### Kullanılan Teknolojiler

Python  
LM Studio  
RAG  
Chroma Vector Database  
Streamlit  
JSON Knowledge Base
