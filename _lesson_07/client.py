g = 'module attribute (module-global variable)'
"""Это документация переменной g."""


class AClass:
    c = 'class attribute'
    """Это документация атрибута AClass.c."""

    def __init__(self):
        """Документация метода ``__init__``"""
        self.i = 'instance attribute'
        """Документация атрибута self.i."""


def f(x):
    """Документация функции f."""
    return x ** 2


f.a = 1
"""Документация атрибута функции f."""
