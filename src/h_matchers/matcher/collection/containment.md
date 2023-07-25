# Matching items in any order

This method uses a constraint satisfaction algorithm to match items
together, or to prove they can't be matched. The idea is to work out
all the possible things each item could match against, and then 
whittle down the possibilities until a solution is found or all options
have been explored.

## The setup - creating a constraint set

Let's say we have the following container, and a matching target to try
and find a match for:

    container = [1, "string", 45, None, 45]
    items_to_match = [45, Any(), Any.int()]

We can take each matching target and list every item it matches:

    45 - {45, 45}
    Any() - {1, "string", 45, None, 45}
    Any.int() - {1, 45, 45}

To make storage simpler, object agnostic, and to avoid the confusion about
the same item at different indexes we cat use the indices of the items instead 
of their raw values:

    0: {2, 4}
    1: {0, 1, 2, 3, 4}
    2: {0, 2, 4}

These are our constraints:

 * Each item on the left must match one of the items on the right
 * No two items can match the same item

## The search - Finding a solution

The key observation to finding a solution quickly is that items which have
fewer choices should be chosen first as they have less room for manouver. As
you search, items with a high degree of freedom are more likely to "work out".
In the extreme case when there is only one choice there is no search.

To apply this heuristic, we will sort our items by the most constrained first:

    0: {2, 4}
    2: {0, 2, 4}
    1: {0, 1, 2, 3, 4}
    
We will pick the first item to match (index: 0) and then try each of its 
possibilities recursively to search for a match. We will only follow one
branch here where we choose "0 = 2". As we are matching 0 to 2, we know
nothing else can be, so we will remove it from the other sets:

    0 = 2
    2: {0, 4}
    1: {0, 1, 3, 4}

We then, sort again (which results in no change in this case) and go again
and pick the most constrained unresolved item (index: 2). This time we will 
first try "2 = 0":

    0 = 2
    2 = 0
    1: {1, 3, 4}

As we have no conflict, we continue recursing, sorting again (no change)
and picking the most constrained unresolved item (index: 1). We will pick
"1 = 1":

    0 = 2
    2 = 0
    1 = 1

We have no unresolved items left, and so a solution is found. 

If at any point any set of possibilities becomes zero we have failed one 
of our conditions (every item must have a match), so we would abort and
recurse up picking the next available possibility for the item before.
