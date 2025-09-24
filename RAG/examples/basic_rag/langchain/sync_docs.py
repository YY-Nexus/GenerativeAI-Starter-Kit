import argparse
from chains import DocumentSyncChain, ingest_docs


def main():
    parser = argparse.ArgumentParser(description="批量文档同步到向量数据库和 MySQL")
    parser.add_argument("--file", type=str, help="待处理文档路径")
    parser.add_argument(
        "--collection", type=str, default="doc_vectors", help="向量数据库集合名"
    )
    parser.add_argument("--mysql_host", type=str, default="127.0.0.1")
    parser.add_argument("--mysql_user", type=str, default="root")
    parser.add_argument("--mysql_password", type=str, default="yourpass")
    parser.add_argument("--mysql_db", type=str, default="yyc3_GenerativeAI")
    args = parser.parse_args()

    vector_db_config = {"collection_name": args.collection}
    mysql_config = {
        "host": args.mysql_host,
        "user": args.mysql_user,
        "password": args.mysql_password,
        "database": args.mysql_db,
    }
    chain = DocumentSyncChain(vector_db_config, mysql_config)
    docs = ingest_docs(args.file)
    chain.process_and_store(docs)
    print(f"已同步文档: {args.file}")


if __name__ == "__main__":
    main()
