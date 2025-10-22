# __init__.py
"""
Resolution Theorem Prover Package
"""

from .clause import Term, Literal, Clause
from .unification import Unifier
from .resolution import ResolutionProver

__all__ = ['Term', 'Literal', 'Clause', 'Unifier', 'ResolutionProver']