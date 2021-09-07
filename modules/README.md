## This is the guide on how to develop modules for Warlord

Step 1:
    Create a folder with an appropriate name under the modules dir

Step 2:
    Write your python code, it must be contained in a class or have an exportible function

Step 3:
    Create a file in the module directory called __init__.py and paste the following code 

    ```python
    import pkgutil

        __path__ = pkgutil.extend_path(__path__, __name__)
        for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
            __import__(modname)
    ```

Step 4:
    Modify the __init__.py in the modules folder, import your module based on the example, then add it to the __all__ array.

Step 5:
    The module should now load into the GUI on launch.