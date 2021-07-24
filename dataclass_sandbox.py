import dataclasses
from dataclasses import dataclass, field
from dataclasses import asdict


@dataclass(order=True)
class Cats:
    id: int = field(default_factory='int', )
    cats_list: list[str] = field(default_factory=list, compare=False)


if __name__ == '__main__':
    # cats = Cats(['Tom', 'Jerry'])
    cats = Cats(id=5, cats_list=['Tom', 'Jerry'])
    # print(cats)

    cats.cats_list[0] = 'Chonk'
    cats.id = 5

