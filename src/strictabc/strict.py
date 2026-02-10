"""
This module contains the implementation of Strict ABC classes and decorators
"""

from abc import ABCMeta, abstractmethod, ABC
from typing import Mapping, List, Tuple, Iterable, Callable, Any
from inspect import signature
from collections import namedtuple

_sentinel = object()

miss_matched_sigs = namedtuple(
    "miss_matched_sigs", ["method_name", "good_sig", "bad_sig"]
)

__strict_signature__ = "__strict_signature__"


class StrictAbstractError(AttributeError):
    """Metaclass for defining Strict Abstract Base Classes (ABCs).

    Use this metaclass to create an Strict ABC.  An ABC can be subclassed
    directly, and then acts as a mix-in class.  You can also register
    unrelated concrete classes (even built-in classes) and unrelated
    ABCs as 'virtual subclasses' -- these and their descendants will
    be considered subclasses of the registering ABC by the built-in
    issubclass() function, but the registering ABC won't show up in
    their MRO (Method Resolution Order) nor will method
    implementations defined by the registering ABC be callable (not
    even via super()).

    This Class will throw an Attribute like error upon detecting un implemented
    methods in the Concrete class at compile time.
    """

    def __init__(
        self, name: str, missing: List[str], bad_sigs: List[miss_matched_sigs]
    ):
        missing_methods = f"Missing methods: {missing}"
        missmatch = f"Missmatched signatures detected: {bad_sigs}"
        msg = f"Errors in <{name}>\n{missing_methods}\n{missmatch}"
        super().__init__(msg)


def strictabstract(funcobj: Callable):
    """A decorator indicating strict abstract methods.

    Requires that the metaclass is StrictABCMeta or derived from it.  A
    class that has a metaclass derived from StrictABCMeta cannot be
    compiled unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms.  strictabstract() may be used to declare
    abstract methods for properties and descriptors.

    Usage:

        class C(metaclass=StrictABCMeta):
            @strictabstract
            def my_abstract_method(self, arg1, arg2, argN):
                ...
    """
    sig = signature(funcobj)
    setattr(funcobj, __strict_signature__, sig)
    funcobj.__isabstractmethod__ = True
    return funcobj


class StrictABCMeta(ABCMeta):
    def __new__(
        mcls,
        name: str,
        bases: Tuple[object],
        classdict: Mapping[str, object],
        /,
        **kwargs: Mapping[Any, Any],
    ):

        cls = super().__new__(mcls, name, bases, classdict, **kwargs)

        mcls._check_bases(mcls, bases, classdict)

        return cls

    def _check_bases(
        mcls, bases: Iterable[Tuple[object]], classdict: Mapping[str, object]
    ):
        for base in bases:

            # filter on only methods, and are abstract
            base_methods = dict(
                (method_name, method)
                for method_name, method in vars(base).items()
                if callable(method) and method_name in base.__abstractmethods__
            )

            # check for missing and bad signatures
            mcls._check_missmatch(mcls, base_methods, classdict)

    def _check_missmatch(
        mcls, base_methods: Mapping[str, Callable], classdict: Mapping[str, object]
    ):
        missing = []
        bad_sigs = []
        # loop through base classes
        for method_name, method in base_methods.items():
            # grab corresponding concrete method
            concrete_method = classdict.get(method_name, _sentinel)

            # if no concrete method found, append to missing and continue
            if concrete_method is _sentinel:
                missing.append(method_name)
                continue

            # get base method signature
            base_sig = getattr(method, __strict_signature__)

            # get signature fro concrete method
            if isinstance(concrete_method, classmethod):
                # concrete method is classmethod, handle grab sig differently
                concrete_sig = signature(concrete_method.__func__)
            else:
                concrete_sig = signature(concrete_method)

            # if base and concrete signatures don't match, append to bad sigs
            if concrete_sig != base_sig:
                bad_sig = miss_matched_sigs(
                    method_name=classdict["__qualname__"],
                    good_sig=base_sig,
                    bad_sig=concrete_sig,
                )
                bad_sigs.append(bad_sig)
                continue  # this onctinue added in case of future improvement

        # if either missing or bad sigs found raise exception here
        if missing or bad_sigs:
            raise StrictAbstractError(mcls.__name__, missing, bad_sigs)


class StrictABC(metaclass=StrictABCMeta):
    pass


__all__ = [
    "StrictABC",
    "StrictABCMeta",
    "strictabstract",
    "StrictAbstractError",
    # adding regular abc items from package here
    "ABC",
    "ABCMeta",
    "abstractmethod",
]
