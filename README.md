# Ragtranscript

To use this tool you need to have API keys to [FMP](https://site.financialmodelingprep.com/), and a Google Gemini1.5flash API key.

Copy .env-example to .env and update with your keys.

Use 'poetry lock; poetry install; poetry run rt' to run it.

This project uses chromadb to create a vectordb of the embeddings of the documents retreived from fmp.