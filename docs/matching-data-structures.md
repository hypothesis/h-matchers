# Matching data structures

## Comparing with simple objects

```python
Any.object.of_type(User).with_attrs({"username": "name", "id": 4})
Any.object(User, {"username": "name", "id": 4})
```

## Comparing to collections
You can make basic comparisons to collections as follows:

```python
Any.iterable()
Any.list()
Any.set()
```

You can specify a custom class with:

```python
Any.iterable.of_type(MyCustomList)
```

#### Specifying size

You can also chain on to add requirements for the size.

```python
Any.iterable.of_size(4)
Any.list.of_size(at_least=3)
Any.set.of_size(at_most=5)
Any.set.of_size(at_least=3, at_most=5)
```

#### Specifying specific content

You can require an iterable to have a minimum number of items, with repetitions
, optionally in order:

```python
Any.iterable.containing([1])
Any.list.containing([1, 2, 2])
Any.list.containing([1, 2, 2]).in_order()
```

This will match if the sequence is found any where in the iterable.

You can also say that there cannot be any extra items in the iterable:

```python
Any.set.containing({2, 3, 4}).only()
Any.list.containing([1, 2, 2, 3]).only().in_order()
```

All of this should work with non-hashable items too as long as the items test
as equal:

```python
Any.set.containing([{'a': 1}, {'b': 2}])
```

#### Specifying every item must match something

You can specify that every item in the collection must match a certain item.
You can also pass matchers to this:

```python
Any.list.comprised_of(Any.string).of_size(6)
Any.iterable.comprised_of(True)
```

## Comparing to dicts

Basic comparisons are available:

```python
Any.iterable()
Any.mapping()
Any.dict()
```

### Most things for collections go for dicts too

```python
Any.dict.of_size(at_most=4)
Any.dict.containing(['key_1', 'key_2']).only()
```

### You can test for key value pairs

```python
Any.dict.containing({'a': 5, 'b': 6})
Any.dict.containing({'a': 5, 'b': 6}).only()
```

### You can compare against any mappable including multi-value dicts

This is useful for dict-like objects which may have different behavior and
semantics to regular dicts. For example: objects which support multiple values
for the same key.

```python
Any.mapping.containing(MultiDict(['a', 1], ['a', 2]))
```
