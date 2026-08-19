def validate_sql(query):
    query_clean = query.strip().lower()

    if not query_clean.startswith("select"):
        return {
            'sucess':False,
            'error':'Only Selected queries are allowed'
        }

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create"
    ]   

    for keyword in forbidden_keywords:
        if  keyword in query_clean:
            return{
                'valid':False,
                'error':f'Forbidden SQL operation:{keyword}'
            }
    return{
        'valid':True
    }    