from fastapi import FastAPI, UploadFile, File, Form
from chains import DocumentSyncChain, ingest_docs
import tempfile
import os

app = FastAPI()

@app.post("/sync_doc/")
def sync_doc(file: UploadFile = File(...), collection: str = Form("doc_vectors"), mysql_host: str = Form("127.0.0.1"), mysql_user: str = Form("root"), mysql_password: str = Form("yourpass"), mysql_db: str = Form("yyc3_GenerativeAI")):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    vector_db_config = {"collection_name": collection}
    mysql_config = {
        "host": mysql_host,
        "user": mysql_user,
        "password": mysql_password,
        "database": mysql_db
    }
    chain = DocumentSyncChain(vector_db_config, mysql_config)
    docs = ingest_docs(tmp_path)
    chain.process_and_store(docs)
    os.remove(tmp_path)
    return {"msg": f"已同步文档: {file.filename}", "count": len(docs)}
