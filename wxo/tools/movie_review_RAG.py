from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from langchain_astradb import AstraDBVectorStore
from langchain_ibm import WatsonxEmbeddings
from graph_retriever.strategies import Eager
from langchain_graph_retriever import GraphRetriever



@tool(name="MovieReviewRAG", 
      permission=ToolPermission.READ_ONLY,
      expected_credentials=[
          ExpectedCredentials(
            app_id = "astraDB",
            type = ConnectionType.KEY_VALUE),
          ExpectedCredentials(
            app_id = "watsonx",
            type = ConnectionType.KEY_VALUE)
        ]
)
def movie_review_rag(question:str) -> str:
    """
    Retrieve data for answer to question using RAG.
    
    Args:
        question (str): The question to find answers for.

    Returns:
        str: The candidate data for the answer.

    """

    astraDB_conn = connections.key_value("astraDB")
    watsonx_conn = connections.key_value("watsonx")

    ASTRA_DB_API_ENDPOINT = astraDB_conn['ASTRA_DB_API_ENDPOINT']
    ASTRA_DB_APPLICATION_TOKEN = astraDB_conn['ASTRA_DB_APPLICATION_TOKEN']
    WATSONX_APIKEY = watsonx_conn['WATSONX_APIKEY']
    WATSONX_PROJECT_ID = watsonx_conn['WATSONX_PROJECT_ID']
    
    embeddings = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr",
        url="https://us-south.ml.cloud.ibm.com",
        apikey=WATSONX_APIKEY,
        project_id=WATSONX_PROJECT_ID
    )

    COLLECTION = "movie_reviews_rotten_tomatoes"
    vectorstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=COLLECTION,
        pre_delete_collection=False,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN
    )
    
    retriever = GraphRetriever(
        store=vectorstore,
        edges=[("reviewed_movie_id", "movie_id")],
        strategy=Eager(start_k=10, adjacent_k=10, select_k=100, max_depth=1),
    )
    
    # invoke the query
    query_results = retriever.invoke(question)
    
    # collect the movie info for each film retrieved
    compiled_results = {}
    for result in query_results:
        if result.metadata["doc_type"] == "movie_info":
            movie_id = result.metadata["movie_id"]
            movie_title = result.metadata["title"]
            compiled_results[movie_id] = {
                "movie_id": movie_id,
                "movie_title": movie_title,
                "reviews": {},
            }

    # go through the results a second time, collecting the retreived reviews for
    # each of the movies
    for result in query_results:
        if result.metadata["doc_type"] == "movie_review":
            reviewed_movie_id = result.metadata["reviewed_movie_id"]
            review_id = result.metadata["reviewId"]
            review_text = result.page_content
            compiled_results[reviewed_movie_id]["reviews"][review_id] = review_text


    # compile the retrieved movies and reviews into a string that we can pass to an
    # LLM in an augmented prompt
    formatted_text = ""
    for movie_id, review_list in compiled_results.items():
        formatted_text += "\n\n Movie Title: "
        formatted_text += review_list["movie_title"]
        formatted_text += "\n Movie ID: "
        formatted_text += review_list["movie_id"]
        for review_id, review_text in review_list["reviews"].items():
            formatted_text += "\n Review: "
            formatted_text += review_text

    return formatted_text
