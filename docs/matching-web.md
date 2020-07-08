# Matching web objects

## Comparing to URLs

The URL matcher provides a both a kwargs interface and a fluent style interface which is a little
more verbose but provides more readable results.

You can construct matchers directly from URLs:

```python
Any.url("http://example.com/path?a=b#anchor")
Any.url.matching("http://example.com/path?a=b#anchor")
```

You can also construct URL matchers manually:

```python
Any.url(host='www.example.com', path='/path')
Any.url.matching('www.example.com').with_path('/path')

Any.url(scheme=Any.string.containing('http'), query={'a': 'b'}, fragment='anchor')
Any.url.with_scheme(Any.string.containing('http')).with_query({'a': 'b'}).with_fragment('anchor')
```

Or mix and match, here the separate `host=Any()` argument overrides the `example.com` in the URL and allows URLs with any host to match:
```python
Any.url("http://example.com/path?a=b#anchor", host=Any())  
Any.url.matching("http://example.com/path?a=b#anchor").with_host(Any()) 
```

#### Matching URL queries

You can specify the query in a number of different ways:

```python
Any.url(query='a=1&a=2&b=2')
Any.url.with_query('a=1&a=2&b=2')

Any.url(query={'a': '1', 'b': '2'})
Any.url.with_query({'a': '1', 'b': '2'})

Any.url(query=[('a', '1'), ('a', '2'), ('b', '2')])
Any.url.with_query([('a', '1'), ('a', '2'), ('b', '2')])

Any.url(query=Any.mapping.containing({'a': '1'}))
Any.url.containing_query({'a': '1'})
```

#### Specify that a component must be present

With the fluent interface you can specify that a URL must contain a certain 
part without specifying what that part has to be:

```python
AnyURL.with_scheme()
AnyURL.with_host()
AnyURL.with_path()
AnyURL.with_query()
AnyURL.with_fragment()
```

## Matching request objects

The request matcher will match a number of request objects from different
libraries with a common interface. For details see:
[h_matchers.matcher.web.request](../src/h_matchers/matcher/web/request.py).

This allows you to make assertions about objects like `requests.Request`:

```python
Any.request()

Any.request(url="http://example.com")
Any.request.with_url("http://example.com")

Any.request(method="GET")
Any.request.with_method("GET")

Any.request(headers={"Content-Type": "application/json"})
Any.request.with_headers({"Content-Type": "application/json"})

Any.request.containing_headers({"Content-Type": "application/json"})
```

### Header matching takes exact rows

At the moment even though two sets of headers might be equivalent:

```
Cache-Control: max-age=0
Cache-Control: no-cache

# vs.

Cache-Control: max-age=0; no-cache
```

We currently only match exact row values. No parsing of the header values is
performed.

### You can use any of these in combination

```python
Any.request(
    method="GET",
    url="http://example.com",
    headers={
        "Content-Type": "application/json"
    }
)

Any.request("GET", "http://example.com", {
    "Content-Type": "application/json"
})

Any.request.with_method("GET").with_url("http://example.com").with_headers({
    "Content-Type": "application/json"
})
```

### All methods accept other matchers as options

```python
Any.request(
    method=Any.of(["POST", "PATCH"]),
    url=Any.url.with_scheme("https"),
    headers=Any.mapping.of_size(at_least=3)
)
```