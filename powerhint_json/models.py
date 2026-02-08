from typing import Callable, List, OrderedDict


Node = OrderedDict[str, str | List[str]]
Action = OrderedDict[str, str | int]

# Creates a node given the name, path and set of values
NodeFactory = Callable[[str, str, set[str]], Node]

# Gets the default value given the path and set of values
DefaultGetter = Callable[[str, set[str]], str]
