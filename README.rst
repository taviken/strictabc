Repository of python package strictabc

The strict abc package implements a subclass of the builtin ABCMeta and ABC classes. It's behavior checks
that all marked methods are implemented and have the correct function signature. This is done at creation
of the class, before any instatiation attempts. It allows for developers of abstract classes and interfaces 
to enforce implementation earlier.


Example
-------

The classic interface example, Animal.

.. code-block:: python

    from strictabc import StrictABC, strictabstract


    class Animal(StrictABC):

        def speak(self)->str:
            pass

License
-------

Licensed under the `MIT License`_.

.. _MIT License: https://github.com/taviken/strictabc/blob/main/LICENSE

