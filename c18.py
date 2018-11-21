class MyResource:
    # def __enter__(self):
    #     print('connect to resource')
    #     return self

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     print('close resource connect')

    def query(self):
        print('query data')

# with MyResource as r:
#     r.query()

from contextlib import contextmanager

@contextmanager
def make_myresource():
    print('connect to resource')
    yield MyResource()
    print('close resource connect')

# yield 生成器
with make_myresource() as r: # 回去调用make_myresource()函数，yield返回执行r.query()，后执行最后的print()
    r.query()









