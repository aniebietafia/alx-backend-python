# Python - Async

# Requirements

## General

> - Allowed editors: vi, vim, emacs
> - All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)(version 3.4.3)
> - All your files should end with a new line
> - The first line of all your files should be exactly #!/usr/bin/env python3
> - A README.md file, at the root of the folder of the project, is mandatory
> - Your code should use the pycodestyle style (version 2.5.)
> - All your files must be executable
> - The length of your files will be tested using wc
> - All your modules should have a documentation (python3 -c 'print(__import__("my_module").__doc__)')
> - All your classes should have a documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)')
> - All your functions (inside and outside a class) should have a documentation (python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')

## Task

**0. The basics of async**

File: [0-main.py](0-main.py/) - [0-basic_async_syntax.py](0-basic_async_syntax.py/)

Write an asynchronous coroutine that takes in an integer argument (max_delay, with a default value of 10) named wait_random that waits for a random delay between 0 and max_delay (included and float value) seconds and eventually returns it.

Use the random module.

```sh
#!/usr/bin/env python3
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random
print(asyncio.run(wait_random()))
print(asyncio.run(wait_random(5)))
print(asyncio.run(wait_random(15)))
vagrant@ubuntu-bionic:/vagrant/holberton_development/curriculum-specialization-backend/0x01-Python_async_function$ ./0-0-main.py
9.034261504534394
1.6216525464615306
10.634589756751769
```
