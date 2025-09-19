#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate


try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)

except (BrokenPipeError, OSError):
    sys.stderr.close()
    sys.stdout.close()
    sys.exit(0)