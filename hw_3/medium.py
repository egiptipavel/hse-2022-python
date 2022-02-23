import numpy as np


class Setter:
    def __setitem__(self, key, value):
        self.value[key] = value


class Getter:
    def __getitem__(self, item):
        return self.value[item]


class ToFile:
    def to_file(self, file_name):
        file = open(file_name, "w+")
        file.write(self.__str__())
        file.close()


class ToStr:
    def __str__(self):
        return "[" + "\n".join([line.tolist().__str__() for line in self.value]) + "]"


class Creator(np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, value):
        self.value = np.asarray(value)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())

        inputs = tuple(x.value if isinstance(x, Creator) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.value if isinstance(x, Creator) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


class Matrix(Creator, ToFile, Getter, Setter, ToStr):
    pass
