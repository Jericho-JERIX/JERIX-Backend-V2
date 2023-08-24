from django.forms import model_to_dict
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os

datasets = [{'homework_id': 90, 'file_id': 8, 'is_active': True, 'date': 1, 'month': 1, 'year': 2024, 'timestamp': 1704128399, 'day_name': 'Monday', 'type': 'ASSIGNMENT', 'label': '23', 'no_deadline': 
False, 'is_checked': False}, {'homework_id': 116, 'file_id': 8, 'is_active': True, 'date': 8, 'month': 8, 'year': 2023, 'timestamp': 9999999999, 'day_name': 'Tuesday', 'type': 'ASSIGNMENT', 
'label': '11111', 'no_deadline': True, 'is_checked': False}, {'homework_id': 117, 'file_id': 8, 'is_active': True, 'date': 5, 'month': 7, 'year': 2024, 'timestamp': 9999999999, 'day_name': 'Friday', 'type': 'ASSIGNMENT', 'label': '1235555', 'no_deadline': True, 'is_checked': True}]

def fetchSearchedHomeworkId(homeworks,keyword):

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)

    writer = ix.writer()

    for homeworkFile in homeworks:
        writer.add_document(
            title = homeworkFile['label'],
            content=str(homeworkFile)[1:-1],
            path = str(homeworkFile['homework_id'])
        )
    
    writer.commit()

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(keyword)
        results = searcher.search(query)
        return [int(result['path']) for result in results]