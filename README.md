# Pseudonymizer
Practice attempt at pseudonymizing documents, e.g., prior to use of gen-AI tools.

Usage: python Pseudonymizer.py. This opens the GUI.

Pseudonymizing requires a list of txt, docx or xlsx documents to be processed, with outputs (including a mapping file, linking pseudonym-codes to the replaced text) saved in a Pseudon subdirectory. Uses parts-of-speech tagging. Optional additional input for specific, direct string replacements, via an Excel file with old (column 1) to new (column 2) replacements per row.

Depseudonymizing requires a list of pseudonymized files and the associated mapping file.

The program also outputs a prompt for gen-AI analysis using the pseudonymized documents which are assumed to be interview transcripts. This can, e.g., be uploaded to a Copilot prompt and then run via the prompt (it may be too large to be copy-pasted).
