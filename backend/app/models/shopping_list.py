from dataclasses import dataclass, field

from models.shopping_item import (
    ShoppingItem
)


@dataclass
class ShoppingList:

    items: list[
        ShoppingItem
    ] = field(default_factory=list)