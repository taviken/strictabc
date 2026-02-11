Repository of python package strictabc

The strict abc package implements a subclass of the builtin ABCMeta and ABC classes. Its behavior checks
that all marked methods are implemented and have the correct function signature. This is done at creation
of the class, before any instatiation attempts. It allows for developers of abstract classes and interfaces 
to enforce implementation earlier.


Example
-------

The classic interface example, Animal.

.. code-block:: python

    from strictabc import StrictABC, strictabstract


    class Animal(StrictABC):
        
        @strictabstract
        def speak(self)->str:
            pass
Later implementing concrete classes
.. code-block:: python
    class A10Warthog(Animal):
        
        def speak(self)->str:
            return "Brrrrrrrrrt!"
    
    class Warthog(Animal):
        pass

The concrete class 'A10Warthog' will pass the checks that 'StrictABC' performs. The other 'Warthog' class 
will not pass, and a 'StrictAbstractError' will be thrown'

.. code-block:: console
    >>> from concrete import *
    . strictabc.strict.StrictAbstractError: Errors in <StrictABCMeta>
    . Missing methods: ['speak']
    . Missmatched signatures detected: []
    >>>

Or, if the 'speak' signature doesn't match, a similar exception will be thrown.
.. code-block:: python
    class Warthog(Animal):
        def speak(cls)->str:
            return 'oh the shame ... And I got downhearted, everytime....!'

.. code-block:: console
    . strictabc.strict.StrictAbstractError: Errors in <StrictABCMeta>
    . Missing methods: []
    . Missmatched signatures detected: [miss_matched_sigs(method_name='Warthog', good_sig=<Signature (self) -> str>, bad_sig=<Signature (cls) -> str>)]
    >>>




License
-------

Licensed under the `MIT License`_.

.. _MIT License: https://github.com/taviken/strictabc/blob/main/LICENSE

