from serpapi import GoogleSearch

def get_queries(keywords:str, status_type:str):
    if status_type not in ["rising", "top"]:
        status_type = "top"
    params = {
        "engine": "google_trends",
        "q": keywords,
        "data_type": "RELATED_QUERIES",
        "api_key": "f2519cfbe9a6ffed3dd087b4edee2170a8481a92f0092b5a4ccceb818c7e2dd9"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    related_queries = [i["query"] for i in results["related_queries"][status_type]]
    return related_queries
