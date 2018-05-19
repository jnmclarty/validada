Validada 
========

(Pronounced "Valid-Data")

This project started as a fork of [engarde v0.0.2](https://github.com/TomAugspurger/engarde)

Validada differentiates from engarde under the hood, substantially, in order to implement a richer
feature set including custom-exceptions, universal slicing API, check object-return.  All, 
with a focus on code brevity.  

All of the basics are the same as engarde, with likely a minor hit to speed.  Although,
in many cases engarde raises on the first problem it finds.  Validada's policy is
to raise only after checking everything.

As of 7/7/2015,  validada passes all of the unit tests of engarde.

Slicing?
========
All checks slice the dataframe internally, so users of validada never have to pass in a sliced dataframe.
Instead, users can pass in a slice-like object as an argument.  

How do I pass a slice?

```python
from validada.slicers import iloc, loc, ix

some_check(adf, iloc[-7:], iloc[:-7])

# or...

@some_check(ix[-1], iloc[:-1])
def somefunc(adf):
	return adf + 1.0

```

All checks can take up to two slice-like arguments.  The first, is the slice which will be checked. 
The second, is a slice for calculating constants to use during the check.  Both are optional.
So, say you have a dataframe coming from a source of data, with known "good" data 
(for instance, before last week), and want to check that the data for just this week is within
two standard deviations of the data, excluding the latest week of data, you would pass in 
```iloc[-7:]``` and ```iloc[:-7]`` as arguments to the check.

```
#To use the same functionality of engarde, one would use...
from validada.functions.raising import none_missing, is_shape, unique_index
#or
from validada.decorators.raising import none_missing, is_shape, unique_index
```

```
#But with validada you get more out of the box...
from validada.functions.returning import none_missing, is_shape, unique_index
#or
from validada.decorators.returning import none_missing, is_shape, unique_index
```

Custom Return-Objects?
======================
Depending on the check, there might be some useful information to pass back out, or maybe you
want to perform a bunch of checks and just collect the boolean results for each?

``` python
from validada.core import ReturnSet

rs = ReturnSet(('bool', 'obj'))
none_missing = rs.none_missing

print "Since we specified 'bool' and 'obj', in that order:"
a_bool, an_obj = none_missing(adf, ix['2013':], columns='one')
#a_bool, is the result of the check
print a_bool
#an_obj, is a none_missing specific object, it's a way to 
#get other information out of the check.
print an_obj
```


Custom Exceptions?
==================
To use the advance features instantiate your own ```CheckSet``` (or child of, eg. ```RaiseSet```,```ReturnSet```) via...

``` python
from validada.core import RaiseSet
rs = RaiseSet(IOError, "IO error makes no sense, but why not?")
none_missing = rs.none_missing

#ready...
none_missing(adf, ix['2013':])

#or make a decorator
none_missing = rs.decorator_maker('none_missing')
```

Dependencies
============

- pandas

Supports python 2.7+  ...would be easy to do 3.4.  Just, lower priority.


Overall Design
==============

Every check has a return-function and raise-function created all sharing a common signature.
These two functions are used to create one staticfunction, for every check, of the CheckSet.
A CheckSet object stores custom-exception, custom-object return, and default slicing settings.
A CheckSet object has a generic way to turn any check, into a decorator using one line.  
An instance of RaiseSet and ReturnSet is used to declare function.*.checks and decorators.*.checks.

See Also
========

[assertr](https://github.com/tonyfischetti/assertr)
[engarde](https://github.com/TomAugspurger/engarde)

