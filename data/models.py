from typing import Optional, List
from attr import dataclass


class Node:
    def __init__(self, name: str, isRoot: bool, documentation: Optional[str] = "",
                 attributes: Optional[List['Node_Attribute']] = None,
                 parent: Optional['Node'] = None,
                 multiplicity: Optional['Aggr_Multi'] = None,
                 children: Optional[List['Node']] = None):
        self.name = name
        self.isRoot = bool(isRoot.lower() == "true")
        self.documentation = documentation
        self.attributes = attributes

        self.parent = parent
        self.multiplicity = multiplicity
        self.children = children if children is not None else []

    def add_child(self, child: 'Node'):
        self.children.append(child)

    def set_parent(self, parent: 'Node', multiplicity: 'Aggr_Multi'):
        self.parent = parent
        self.multiplicity = multiplicity

    def __repr__(self):
        return f"Node({self.name=},{self.isRoot=}, children={self.children})"

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child.__iter__()


@dataclass(frozen=True)
class Node_Attribute:
    name: str
    type: str


class Aggr_Multi:
    min: int
    max: int

    def __init__(self, multiplicity: str):
        if '..' in multiplicity:
            minv, maxv = multiplicity.split('..')
            minv, maxv = int(minv), int(maxv)
        else:
            minv, maxv = int(multiplicity), int(multiplicity)
        if minv < 0 or maxv < 0:
            raise ValueError("Multiplicity values must be non-negative")
        if minv > maxv:
            raise ValueError(
                "Minimum multiplicity cannot be greater than maximum multiplicity")

        self.min = minv
        self.max = maxv
