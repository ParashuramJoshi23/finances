# finances
Input:
Transcript file as input via the /api/upload endpoint

Process:
separation of each sentence into one of these categories.
1. Asset
2. Income
3. Expenditure.

Endpoints:

/api/upload -> returns the transcriptId object that is created
/api/financial-data/transcript_id -> returns the separation of each of the sentences with categories.

Validation to check if the file is less than 10kb or more than 10 MB.

Breaking the conversation into sentences and running it with langchain chain and a prompt.

Few other approaches can be 
1. Providing each conversation line with prompt
2. Providing entire transcript as context against each sentence.

I have gone with first approach as it is simpler and can be iterated against.

Setup required.
1. Clone the repo
2. pip install requirements.txt
3. create db.sqlite3 file
4. create /media/transcript folder where uploaded file can sit.

Further improvements that can be done.
1. Spin off process_transcription as a task.
2. Move uploaded file to s3.
3. Check if the same file is uploaded don't reprocess.
