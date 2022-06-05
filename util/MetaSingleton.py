
class MetaSingleton(type):
    """
    All classes that implement this class as metaclass will be defined as singleton only,
    and calling the constructor multiple times will assing to the same instance.
    """
    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in MetaSingleton.__instances:
            MetaSingleton.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        # print(MetaSingleton.__instances)
        return MetaSingleton.__instances[cls]