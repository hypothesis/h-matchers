# Matching numbers

## Type comparisons

You can compare to various types of numbers. This will account for edge cases
like booleans appearing as ints.

```python
Any.number()  # Any real valued number (not complex)
Any.int()
Any.float()
Any.complex()
Any.decimal()
```

## Conditions

There are various unitary tests: 

```python
Any.int.even()
Any.int.odd()
Any.int.truthy()
Any.int.falsy()
```

And comparisons with values:

```python
Any.number.not_equal_to(4)
Any.number.less_than(6)
Any.number.less_than_or_equal_to(1)
Any.number.greater_than(6)
Any.number.greater_than_or_equal_to(5)
Any.number.multiple_of(5)
Any.float.approximately(5.01, error_factor=0.05)
```

## Comparisons with values using operators

You can also use operators to express your conditions instead of the slightly
wordier methods. Some care needs to be taken with ordering and parens to get 
the correct result.

This does not work with `!=` as this would clash with the basic matching 
functionality.

```python
assert my_value == (Any.number() < 4)

Any.number() <= 5
Any.number() > 4
Any.number() >= 4
```

## Fluent chaining

You can chain together many conditions:

```python
Any.number.greater_than(4).less_than(100).odd()
((Any.number() > 4) < 100).odd()
```