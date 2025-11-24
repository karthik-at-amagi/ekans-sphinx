# EKANS - Eka Knowledge & Answers

- This repository holds the website for EKANS, a central knowledge base for the data science team at Amagi.
- The website is deployed using sphinx and is in a one-way sync with Confluence (Sphinx -> Confluence).
  - The sync is done using the `sphinxcontrib-confluencebuilder` extension.
  - This way we can have a good version controlled knowledge base along with the search and discovery features of Confluence.
- To add or update content, please make changes here and submit a pull request with review.
- The content of the website can be written in Markdown (preferred) or RST format under the source directory.
