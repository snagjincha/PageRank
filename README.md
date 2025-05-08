# PageRank with Power Iteration

This project implements the **PageRank algorithm** using the **Power Iteration method** on the [web-Google graph dataset](https://snap.stanford.edu/data/web-Google.html).  
It efficiently computes the relative importance of each node (webpage) in a directed graph.

## Overview

PageRank is an algorithm developed by Google to rank web pages based on their link structure.  
This implementation:
- Loads and parses a large-scale graph (`web-Google.txt.gz`)
- Converts it to **Compressed Row Storage (CRS)** format for memory-efficient representation
- Applies **Power Iteration** to compute PageRank scores
- Outputs the top 10 most influential nodes

## How to Run

python pagerank.py
