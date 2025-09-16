source .env
orchestrate env activate local

# Delete existing

# Agents
orchestrate agents remove -n movie_reviews -k native

# Tools
orchestrate tools remove -n MovieReviewRAG

# Connections
orchestrate connections remove --app-id watsonx
orchestrate connections remove --app-id astraDB

## Create 

# Connections
orchestrate connections import -f wxo/connections/astradb.yaml
orchestrate connections import -f wxo/connections/watsonx.yaml

# Credentials
orchestrate connections set-credentials -a astraDB --environment draft -e ASTRA_DB_API_ENDPOINT=$ASTRA_DB_API_ENDPOINT -e ASTRA_DB_APPLICATION_TOKEN=$ASTRA_DB_APPLICATION_TOKEN
orchestrate connections set-credentials -a watsonx --environment draft -e WATSONX_APIKEY=$WATSONX_APIKEY -e WATSONX_PROJECT_ID=$WATSONX_PROJECT_ID

# Tool
orchestrate tools import -k python -f wxo/tools/movie_review_RAG.py --app-id astraDB --app-id watsonx -r wxo/tools/requirements.txt

# Agent
orchestrate agents import -f wxo/agents/movie_reviews.yaml
