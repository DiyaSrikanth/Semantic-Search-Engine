import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import chromadb

client=chromadb.PersistentClient(path='chroma_1')
collection = client.get_collection("final_embed_data")
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(input_text):
    sentence_embeddings= model.encode(input_text)
    df =pd.DataFrame(sentence_embeddings)
    df_1=pd.read_csv('subtitle_connection.csv')
    # df.to_csv(os.path.join('data-20240401T135418Z-001/test_query/test.txt'), index=False)
    query_embedding = [float(y) for y in df[0]]
    query_ans= collection.query(
    query_embeddings= query_embedding  ,
    n_results=5)
    query_ids= [float(x) for x in query_ans['ids'][0]]
    ids_query = pd.DataFrame({'ids':query_ids})
    your_sub = pd.merge(ids_query, df_1, how='left', on='ids')
    return your_sub