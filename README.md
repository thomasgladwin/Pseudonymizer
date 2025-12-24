# Pseudonymizer
Practice attempt at pseudonymizing documents, e.g., prior to use of gen-AI tools.

Usage: python Pseudonymizer.py. This opens the GUI.

Pseudonymizing requires a list of txt or docx documents to be processed, with outputs (including a mapping file, linking pseudonym-codes to the replaced text) saved in a Pseudon subdirectory. Depseudonymizing requires a list of txt files and the associated mapping file.

The program also outputs a prompt for gen-AI analysis using the pseudonymized documents which are assumed to be interview transcripts. This can, e.g., be uploaded to a Copilot prompt and then run via the prompt (it may be too large to be copy-pasted).
