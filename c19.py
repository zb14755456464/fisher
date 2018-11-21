
from contextlib import contextmanager
"""
我只是单纯的想要在我要执行的代码，前面和后面个执行一行代码
"""
@contextmanager
def make_myresource():
    print('<<',end='')
    yield  # 没有返回值只是简单的终端而已
    print('>>',end='')

# yield 生成器
with make_myresource():
    print("且将生活饮而进",end="")









