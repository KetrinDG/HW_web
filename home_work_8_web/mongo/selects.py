from mongo import Authors, Quotes
from redis_cache import cache, r_cache


# @cache
@r_cache(3)
def fetch_authors(name):
    print("\033[035mFETCH AUTHOR\033[0m")
    author = Authors.objects(fullname__iregex=name)
    result = []
    for el in author:
        result.append(el.to_mongo().to_dict())
    return result


# @cache
@r_cache(3)
def fetch_quotes(tags):
    print("\033[035mFETCH QUOTE\033[0m")
    quote = Quotes.objects(tags__iregex=tags)
    result = []
    for el in quote:
        author = el.author.fullname
        res = el.to_mongo().to_dict()
        res["author"] = author
        result.append(res)
    return result
