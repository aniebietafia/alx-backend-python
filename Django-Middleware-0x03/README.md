## Middleware Best Practices
* Keep middleware functions small and focused — avoid bloating a single middleware with multiple responsibilities.
* Chain logic properly — always call `get_response(request)` unless rejecting the request early.
* Use Django’s `request.user`, `request.path`, and `request.method` for clean conditional logic.
* Avoid database-heavy logic in middleware to maintain performance.
* Use logging middleware responsibly — log minimal and relevant data to avoid clutter.
* Write unit tests for middleware behavior and edge cases.
* Document each middleware clearly — what it does, why it exists, and where it sits in the stack.

## Task 1: Logging User Requests(Basic Middleware)
**Objective**: Create a middleware that logs each user’s requests to a file, including the timestamp, user and the request path.

**Instructions**: - create a file `middleware.py` and Create the middleware class `RequestLoggingMiddleware` with two methods, `__init__`and `__call__`.

* In the `__call__` implement a logger that log’s the following information `f"{datetime.now()} - User: {user} - Path: {request.path}“`

* Configure the Middleware section in the `settings.py` with your newly created middleware

* Run the server to test it out. python manage.py runserver

## Task 2: Restrict Chat Access by time
**Objective**: implement a middleware that restricts access to the messaging up during certain hours of the day

**Instructions**:

* Create a middleware class RestrictAccessByTimeMiddleware with two methods, __init__and__call__. that check the current server time and deny access by returning an error 403 Forbidden

    * if a user accesses the chat outside 9PM and 6PM.
* Update the settings.py with the middleware.