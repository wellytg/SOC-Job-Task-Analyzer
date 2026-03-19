# Glossary

## A

**API (Application Programming Interface)**: A set of rules and protocols for accessing a web-based software application or web tool. In this project, refers to SerpAPI for Google Jobs data collection.

**Aggregation**: The process of combining and consolidating similar or duplicate task descriptions from multiple job postings into unified representations.

## B

**Batch Processing**: A method of processing data where a group of transactions or data items are collected and processed together as a single unit, rather than individually.

## C

**Classification**: The process of categorizing job postings into predefined SOC (Standard Occupational Classification) Tier 1 categories based on job titles and descriptions.

**Clustering**: The task of grouping similar items together. In this project, refers to thematic clustering of job tasks into functional categories.

**Cosine Similarity**: A metric used to measure how similar two vectors are, regardless of their size. Used in fuzzy deduplication to compare task similarity.

**CSV (Comma-Separated Values)**: A plain text format for tabular data where each line represents a record and fields are separated by commas.

## D

**Data Pipeline**: A series of data processing steps that transform raw data into actionable insights through collection, processing, storage, and analysis.

**Deduplication**: The process of identifying and removing duplicate or near-duplicate entries from a dataset.

**Difflib**: Python's built-in library for comparing sequences, used in this project for fuzzy string matching in task deduplication.

## E

**ETL (Extract, Transform, Load)**: A data integration process that combines data from multiple sources into a single, consistent data store.

## F

**Fuzzy Matching**: A technique for finding strings that match a pattern approximately rather than exactly. Used for identifying similar but not identical task descriptions.

**Fuzzy Deduplication**: The process of removing near-duplicate entries based on similarity thresholds rather than exact matches.

## G

**Git**: A distributed version control system for tracking changes in source code during software development.

## H

**HTTP (Hypertext Transfer Protocol)**: The foundation of data communication for the World Wide Web, used for API requests to SerpAPI.

## I

**I/O (Input/Output)**: The communication between a computer and the outside world, including reading from and writing to files, networks, and devices.

## J

**Job Posting**: An advertisement created by an employer to attract candidates for a job opening, containing job title, description, requirements, and company information.

**JSON (JavaScript Object Notation)**: A lightweight data-interchange format that is easy for humans to read and write and easy for machines to parse and generate.

**JSON Lines (JSONL)**: A format where each line is a valid JSON object, used for streaming large datasets efficiently.

## K

**Keyword Matching**: A technique for identifying relevant content by searching for specific words or phrases within text data.

## L

**LLM (Large Language Model)**: Advanced AI models trained on vast amounts of text data, capable of understanding and generating human-like text. Referenced in the project for future integration.

**Logging**: The process of recording events, messages, and errors during program execution for debugging and monitoring purposes.

## M

**Memory Management**: The process of controlling and coordinating computer memory, assigning memory to programs when needed and freeing it when no longer needed.

**Multiprocessing**: The ability of a system to run multiple processors simultaneously, used for parallel processing of large datasets.

## N

**Natural Language Processing (NLP)**: A field of AI that focuses on the interaction between computers and humans through natural language, used for text analysis and understanding.

## O

**Ontology**: A formal representation of knowledge within a domain, defining concepts and relationships. Referenced in the context of SOC classification systems.

## P

**Pagination**: The process of dividing content into discrete pages, used in API requests to handle large result sets.

**Parallel Processing**: A computing technique where multiple processors execute different parts of a program simultaneously to improve performance.

**Pipeline Orchestration**: The coordination and management of multiple processing stages in a data pipeline to ensure proper execution order and error handling.

**Preprocessing**: The initial processing of raw data to prepare it for analysis, including cleaning, normalization, and transformation.

## Q

**Query Parameter**: A parameter added to a URL to modify the behavior of a web request, used in API calls to SerpAPI.

## R

**Regex (Regular Expression)**: A sequence of characters that defines a search pattern, used for pattern matching in text processing.

**Responsibility Extraction**: The process of identifying and extracting job responsibilities from job descriptions using text parsing techniques.

**REST API (Representational State Transfer API)**: An architectural style for designing networked applications, used by SerpAPI for data access.

## S

**Scraping**: The automated extraction of data from websites or APIs, used to collect job posting data from Google Jobs.

**Similarity Threshold**: A numerical value that determines how similar two items must be to be considered duplicates or matches.

**SOC (Standard Occupational Classification)**: A system for classifying workers and jobs into occupational categories, developed by the U.S. Bureau of Labor Statistics.

**Streaming**: A method of processing data where data is processed as it arrives rather than loading everything into memory at once.

## T

**Task Aggregation**: The process of consolidating similar job tasks from multiple sources into representative categories.

**TF-IDF (Term Frequency-Inverse Document Frequency)**: A numerical statistic that reflects how important a word is to a document in a collection, used in text similarity calculations.

**Thematic Clustering**: Grouping of job tasks into meaningful categories based on their functional themes or purposes.

**Threading**: A way to achieve parallelism by running multiple threads within a single process.

## U

**Unstructured Data**: Data that doesn't have a predefined data model or is not organized in a predefined manner, such as job descriptions and responsibilities.

## V

**Vectorization**: The process of converting text or other data into numerical vectors that can be processed by machine learning algorithms.

**Virtual Environment**: An isolated Python environment that allows packages to be installed for use by a particular application, rather than being installed system-wide.

## W

**Web Scraping**: See "Scraping".

**Workflow**: A sequence of industrial, administrative, or other processes through which a piece of work passes from initiation to completion.

## X

**XML (eXtensible Markup Language)**: A markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable.

## Y

**YAML (YAML Ain't Markup Language)**: A human-readable data serialization standard, used for configuration files.

## Z

**Zero-Shot Learning**: A machine learning paradigm where a model can make predictions on tasks it hasn't been explicitly trained for, referenced in the context of future LLM integration.

---

## Technical Terms by Category

### Data Processing Terms
- ETL (Extract, Transform, Load)
- Preprocessing
- Batch Processing
- Streaming
- Deduplication
- Fuzzy Matching
- Vectorization

### Machine Learning Terms
- Cosine Similarity
- TF-IDF
- Clustering
- Classification
- Similarity Threshold
- Zero-Shot Learning

### Programming Terms
- API (Application Programming Interface)
- Multiprocessing
- Threading
- Memory Management
- Logging
- Virtual Environment

### Data Formats
- JSON (JavaScript Object Notation)
- JSON Lines (JSONL)
- CSV (Comma-Separated Values)
- YAML (YAML Ain't Markup Language)
- XML (eXtensible Markup Language)

### Web Technologies
- HTTP (Hypertext Transfer Protocol)
- REST API
- Query Parameter
- Pagination
- Web Scraping

### Occupational Classification
- SOC (Standard Occupational Classification)
- Ontology
- Thematic Clustering
- Responsibility Extraction

---

**Last Updated:** December 2024
**Version:** 1.0.0