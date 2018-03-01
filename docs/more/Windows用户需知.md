# Windows用户需知

Windows用户在使用PyLf以及其它基于[multiprocessing](https://docs.python.org/3.6/library/multiprocessing.html)的module时，一般须
将代码写成类似于如下形式：

```python
from multiprocessing import freeze_support

def main():
    ...
    
if __name__ == '__main__':
    freeze_support()
    main()

```

更多信息：[17.2. multiprocessing — Process-based parallelism](https://docs.python.org/3.6/library/multiprocessing.html#module-multiprocessing)
