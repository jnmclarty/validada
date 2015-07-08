from checks import none_missing
from slicers import iloc, ix

import pandas as pd

# Create some data...
ind = pd.date_range('2010', '2015', freq='A')
adf = pd.DataFrame({'one' : range(5), 'two' : [ i ** 2 for i in range(5)]}, index=ind)
adf.ix[4,'two'] = pd.np.NaN

"""
            one  two
2010-12-31    0    0
2011-12-31    1    1
2012-12-31    2    4
2013-12-31    3    9
2014-12-31    4  NaN
"""

# Basic call...
try:
    none_missing(adf)
except AssertionError:
    print "Some values are missing!"

# Using arguments explicitly
try:
    none_missing(adf, columns='one')
    print "No problem here!"
except:
    pass

# Or implicitly using arguments...
try:
    none_missing(adf, 'two')
    print "Shouldn't see this!"
except:
    print "There's a problem, in the second column"


try:
    none_missing(adf, iloc[-2:])
except AssertionError:
    print "Some values are missing in the last two rows"

try:
    # iloc stores the :-2 slice, so this works until iloc is changed
    none_missing(adf, iloc)
except AssertionError:
    print "Some values are still missing in the last two rows"


try:
    none_missing(adf, ix[:'2013'])
    print "There are no problems looking at data before 2013"
except:
    pass

# Did you notice the type detection between passing 'two', and the slicers?
# Look ma, args only - kwargs not mandatory!

# Now for some real fun...

from core import RaiseSet

rs = RaiseSet(IOError, "IO error makes no sense, but why not?")
none_missing = rs.none_missing

try:
    none_missing(adf, ix['2013':])
except IOError as e:
    print e.message

#This is only needed, since the user has added a custom exception message...
none_missing = rs.decorator_maker('none_missing')

@none_missing(ix['2013':])
def somefunc(anydf):
    soln = anydf + 1.0
    return soln

try:
    somefunc(adf)
except IOError as e:
    print "Second time the charm?"
    print e.message

from core import ReturnSet

rs = ReturnSet(('bool', 'obj'))
none_missing = rs.none_missing

print "Since we specified 'bool' and 'obj':"
a_bool, an_obj = none_missing(adf, ix['2013':], columns='one')
#a_bool, is the result of the check
print a_bool
#an_obj, is a none_missing specific object, it's a way to get other information out of the check.
print an_obj



