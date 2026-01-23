# amr-resource-search
A domain-specific search engine for antimicrobial resistance databases and computational tools

## Overview

AMR Resource Search is a domain-specific search engine for discovering antimicrobial resistance (AMR) databases and computational tools. It is designed to help researchers quickly identify relevant AMR resources based on functionality and user intent, rather than relying on generic web search.

## Motivation

AMR databases and tools are scattered across publications, websites, and repositories, making discovery time-consuming and inefficient. This project addresses that gap by providing a curated, searchable metadata layer focused exclusively on AMR resources.

## Dataset

The core dataset is provided as a curated Excel file containing 30 AMR databases and tools.

The Excel file consists of three sheets:
1. AMR_Databases_and_Tools – main indexed dataset
2. Controlled_Vocabulary – standardized values for selected categorical fields  to enable consistent filtering and indexing
3. Column_Definitions – metadata describing each column

The dataset was manually curated to ensure accuracy, relevance, and consistency.

## Search Logic

Search is performed using keyword-based matching across selected fields, including:
- database/tool name
- primary_use
- description
- tags

All text is normalized during search (lowercasing, whitespace trimming) to ensure consistent matching.

## Ranking Strategy

Search results are ranked using a simple weighted matching strategy:
- Matches in the database/tool name are prioritized
- Matches in primary_use receive intermediate weight
- Tag matches receive intermediate weight
- Description matches receive lower weight

This approach balances precision and recall while keeping the system interpretable.

## Filtering

Filterable attributes include:
- category
- data_type
- methodology
- access_type
- interface
- target_user

Species coverage is displayed for informational purposes and is not used for filtering or ranking.

## Implementation

- Language: Python  
- Libraries: pandas, Streamlit  
- Data source: Excel (.xlsx)  

Standard parsing libraries are used; no custom CSV string splitting is performed.

## Future Work

Planned extensions include:
- Improved web-based user interface
- Expanded AMR resource coverage
- Ontology-based tagging
- Automated updates and validation






