from functools import wraps
from pandas import DatetimeIndex,Series



class TypeChecker(object):
    
    @staticmethod
    def type_check(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查位置参数的类型
            for arg, arg_type in zip(args, func.__annotations__.values()):
                if not isinstance(arg, arg_type):
                    raise TypeError(
                        f"Invalid argument type, expected {arg_type} but got {type(arg)}")

            # 检查关键字参数的类型
            for kwarg, kwarg_type in func.__annotations__.items():
                if kwarg in kwargs and not isinstance(kwargs[kwarg], kwarg_type):
                    raise TypeError(
                        f"Invalid argument type, expected {kwarg_type} but got {type(kwargs[kwarg])}")

            return func(*args, **kwargs)

        return wrapper
    
    @staticmethod
    def datetime_index_check(func):
        """
        检查实例方法的位置参数是否为series，参数的index是否是pandas.DatetimeIndex类型
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查位置参数的类型
            for arg, arg_name in zip(args[1:], func.__annotations__.keys()):
                if isinstance(arg, Series):
                    if not isinstance(arg.index, DatetimeIndex):
                        raise TypeError(
                            f"{arg_name}的index类型必须为pandas.DatetimeIndex")
                else:
                    raise TypeError(
                            f"{arg_name}的类型必须为pandas.Series")
            return func(*args, **kwargs)
        
        return wrapper