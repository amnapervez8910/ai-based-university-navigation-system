# 🧠 AI-Based University Navigation System

An AI-powered university campus navigation system developed in **Python** using **Speech Recognition**, **Natural Language Processing (NLP)**, and **Text-to-Speech (TTS)** technologies.  
The system helps users navigate through campus locations using voice commands and spoken directions.

---

## ✨ Features

- ✅ Voice-based user interaction
- ✅ Speech-to-text conversion
- ✅ Natural language query processing
- ✅ AI-based pathfinding system
- ✅ Text-to-speech navigation guidance
- ✅ Graph-based campus representation
- ✅ Multiple route exploration using DFS
- ✅ Hands-free navigation assistance

---

## 🛠 Technologies Used

- **Programming Language:** Python
- **Speech Recognition:** SpeechRecognition
- **Natural Language Processing:** spaCy
- **Text-to-Speech:** pyttsx3
- **Search Algorithm:** Depth-First Search (DFS)
- **Concepts:** Artificial Intelligence, Graph Traversal, NLP

---

## 📚 Python Libraries Used

### 🔹 SpeechRecognition
Used for converting speech into text.

### 🔹 spaCy
Used for natural language processing and extracting locations from user queries.

### 🔹 pyttsx3
Used for converting text directions into spoken audio output.

---

## ⚙️ System Working

1. User speaks a navigation query through the microphone
2. Speech Recognition converts speech into text
3. NLP processes the query and extracts locations
4. The graph-based system searches for paths using DFS
5. The system generates navigation directions
6. Text-to-Speech reads the directions aloud

---

## 🧭 Search Technique Used

### Depth-First Search (DFS)

The system uses DFS to explore all possible paths between locations on the campus graph.

Features of DFS in this project:
- Explores all possible routes
- Handles multiple paths
- Efficient for smaller graph structures
- Uses recursion for traversal

---

## 🔗 Graph Representation

The campus is represented as an undirected weighted graph where:

- Nodes represent campus locations
- Edges represent pathways between locations
- Weights represent distance or travel cost
---

## 🎯 AI Functionalities

### 🗣 Speech Recognition
Converts spoken user commands into text.

### 🧠 Natural Language Processing
Extracts source and destination locations from natural language queries.

### 🛣 Pathfinding
Finds routes between locations using graph traversal algorithms.

### 🔊 Text-to-Speech
Provides spoken navigation directions to the user.

---

## ⚠️ Challenges Addressed

- Speech recognition accuracy
- Handling natural language variations
- Pathfinding complexity in graph traversal
- User-friendly voice interaction

---

## ⚠️ Requirements

Install the following Python libraries before running the project:

```bash
pip install SpeechRecognition
pip install pyttsx3
pip install spacy
```

Download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

Make sure Python and a working microphone are installed on the system.

---

## 📄 Project Report

The complete project report is included in this repository.

---

## 👨‍💻 Author

**Amna Pervez**

---
