# Crawlx
An Intelligent Targeted Web Crawler Written in Python

## Use Cases
CrawlX was orginally designed for use in pentesting engagements or bug bounty programs as a way to scope out a site through the use of crawling and light directory brute-forcing. Apart from its orginal use cases, CrawlX can used or modified to be helpful in other use cases.

## CLI Usage
`usage: crawlx.py [-h] -u URL [-o OUTPUT] [-d DEPTH] [-t TIMEOUT] [-l LOG] [-j JSON] [-v] [-q] [--delay DELAY]`

## Examples
`./crawlx.py -u http://example.com`

## Q&A
Q. What do you mean by "Targeted" web crawler

A. This script was orginally designed for security audits, rather than crawling the entire internet. Thus when finding links we only look for "in-scope" links (matching the orginal domain or its subdomains in the --URL param)
