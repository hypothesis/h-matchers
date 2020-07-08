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