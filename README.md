# EmailMonitor
Screening emails &amp; summarizing with LLM agents

Stage 1: POC
Stage 2: Full fledged
Stage 3: Full fledged backend with a frontend interface

Current stage: Stage 1 complete

### Stage 1
Proof of concept. Program was written to see if this works with a singular email (it does).

### Stage 2
For this stage, the data issue will be solved. The problem is finding a way to process multiple emails (10-15 at least) and screen them. Given the limited context window, the emails cannot be passed all at once.

Currently thinking of solutions. Might use another agent to screen based on the 'Subject' or 'From' fields. Another option is ingesting the data into a data table (Postgres or MongoDB) and querying it. This would then be a RAG system.

### Stage 3
In this stage, the program will be interactive with a frontend interface. The idea is for this to run as a CRON job or to trigger it with a button. Leaning more towards the button.

## Architecture

- Emails are read from Gmail inbox using IMAP
- Email content is cleaned
- Emails are passed to a Screener agent
- Screener returns list of emails marked as important and not important
- Important emails are passed to the Summarizer agent
- The Summarizer summarizes all the important emails and returns an output
