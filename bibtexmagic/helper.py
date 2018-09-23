def get_parentheses(s, stop_on_closing=False):
    """
    Looks up opening/closing parentheses pairs in a string.

    Positional arguments:
    s -- input string.

    Keyword arguments:
    stop_on_closing -- if True, parsing stops upon reaching
        a closing parenthesis of the first opening one. If False,
        the parser continues until the end of the string.

    Return value:
    A dictionary of parentheses positions in a string containing
        entries of the form "opening: closing".
    """
    to_return = {}
    pstack = []

    for i, c in enumerate(s):
        if c == '{':
            pstack.append(i)
        elif c == '}':
            if not pstack:
                raise IndexError("No matching opening parenthesis for " + str(i))
            to_return[pstack.pop()] = i

            #If all brackets closed, return?
            if stop_on_closing and not pstack:
                return to_return

    if pstack:
        raise IndexError("No matching closing parenthesis for " + str(pstack.pop()))

    return to_return


