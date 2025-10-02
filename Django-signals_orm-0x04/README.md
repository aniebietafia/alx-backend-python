## Event Listeners (Signals), ORM & Advanced ORM Techniques
In modern web applications, performance, modularity, and clean architecture are essential. Django provides powerful tools that help developers build robust and maintainable backend systems. Three core concepts that support these goals are:

1. Event Listeners using Django Signals:
Signals allow decoupled parts of an application to communicate by emitting and listening to events. This enables actions like sending confirmation emails or logging activities whenever a specific model action (like saving or deleting) occurs—without tightly coupling that logic to your views or models.

2. Django ORM & Advanced ORM Techniques:
Django’s Object-Relational Mapper (ORM) enables developers to interact with the database using Python code instead of SQL. It also provides advanced tools to optimize performance—like select_related, prefetch_related, and query annotations—helping avoid common issues like the N+1 query problem.

3. Basic Caching:
Caching stores frequently accessed data so it can be retrieved faster. Django supports various caching strategies (view-level, template fragment, low-level caching), which can drastically reduce page load time and database load.

Together, these techniques improve application responsiveness, database efficiency, and code scalability, making them crucial tools for Django backend developers.

## Task 0: Implement Signals for User Notifications
**Objective**: Automatically notify users when they receive a new message.

**Instructions**:

* Create a Message model with fields like sender, receiver, content, and timestamp.

* Use Django signals (e.g., post_save) to trigger a notification when a new Message instance is created.

* Create a Notification model to store notifications, linking it to the User and Message models.

* Write a signal that listens for new messages and automatically creates a notification for the receiving user.

## Task 1: Create a Signal for Logging Message Edits
**Objective**: Log when a user edits a message and save the old content before the edit.

**Instructions**:

* Add an edited field to the Message model to track if a message has been edited.

* Use the pre_save signal to log the old content of a message into a separate MessageHistory model before it’s updated.

* Display the message edit history in the user interface, allowing users to view previous versions of their messages.

## Task 2: Use Signals for Deleting User-Related Data
**Objective**: Automatically clean up related data when a user deletes their account.

**Instructions**:

* Create a `delete_user` view that allows a user to delete their account.

* Implement a `post_delete` signal on the User model to delete all messages, notifications, and message histories associated with the user.

* Ensure that foreign key constraints are respected during the deletion process by using CASCADE or custom signal logic.

## Task 3: Leverage Advanced ORM Techniques for Threaded Conversations
**Objective**: Implement threaded conversations where users can reply to specific messages, and retrieve conversations efficiently.

**Instructions**:

* Modify the Message model to include a parent_message field (self-referential foreign key) to represent replies.

* Use prefetchrelated and selectrelated to optimize querying of messages and their replies, reducing the number of database queries.

* Implement a recursive query using Django’s ORM to fetch all replies to a message and display them in a threaded format in the user interface.

## Task 4: Custom ORM Manager for Unread Messages
**Objective**: Create a custom manager to filter unread messages for a user.

**Instructions**:

* Add a read boolean field to the Message model to indicate whether a message has been read.

* Implement a custom manager (e.g., UnreadMessagesManager) that filters unread messages for a specific user.

* Use this manager in your views to display only unread messages in a user’s inbox.

* Optimize this query with .only() to retrieve only necessary fields.

## Task 5: implement basic view cache
**Objective**: Set up basic caching for a view that retrieves messages in the messaging app.

**Instructions**:

* Update your settings.py in your `messagingapp/messagingapp/settings.py` with the default cache i.e django.core.cache.backends.locmem.LocMemCache as follows:

```bash
CACHES = { 'default': { 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'unique-snowflake', } }
```

* Use cache-page in your views to cache the view that displays a list of messages in a conversation. Learn more about cache-page here

* Set a 60 seconds cache timeout on the view.