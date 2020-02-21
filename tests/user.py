def test():
    def out_func(func):
        def in_func():
            print('hello inner')
            return func()
        return in_func

    @out_func
    def fun():
        print('hello world')

    fun()


if __name__ == '__main__':
    test()
