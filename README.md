# Photoroom interview assignment

## Set up
Prerequisites: Python 3.12 or newer

1. Install the dependencies

    Tip: Use a virtual env.

    ```
    pip install -r requirements-dev.txt
    ```

2. Run the web server

    ```
    python manage.py runserver
    ```

3. Browse the API documentation

    ```
    http://localhost:8000/api/docs/
    ```

### Shortcuts for formatting/linting/type-checking
Lint: `poe lint`

Format: `poe format`

Type-check: `poe lint_types`

Run all checks in fix/format mode: `poe fix`

Validate all checks: `poe verify`

## Assignment specific choices
### No personal color palletes
In order to keep the database model and API simple/predictable I decided that each user gets a default/personal team upon registration.

This simplifies the data model as we can just deal with teams as owners of color palletes. This also makes it easy for a user to share their personal palletes with other users.

### No pagination
I deprioritized this as it is dead easy to tack on. Getting the feature to work was a priority.

Usually it's wise to launch new list APIs with some form  of pagination or limit so that in the future, users don't end up fetching massive lists of teams/palletes.

### Basic auth
Since there were no specific requirements about authentication, I went with just basic auth. Obviously there are much better ways to handle this depending on the client requirements.

### Re-using `django.contrib.auth` models
I decided to use Django's `Group` model for teams to avoid having to create it myself. In a real-world system it might be wise to create a separate team model to get clearer naming and flexibility.

### Lacking tests
I deprioritized writing exhaustive tests. I wrote some that cover the most basic cases to proof that I can write a unit test, but it's not exhaustive by any means.

I've included a list of non-exhaustive additions that could've been made.

### No CI
Although the repository has a linter, formatter, type checking and tests. I did not get around to setting up a CI pipeline.

If I had to do it quickly, I would set up a simple Github Actions pipeline that verifies the code has no linter errors, is formatted and the tests pass.

When you're working in a team, this is critical to prevent basic regressions and enforce a consistent style.

### No package manager
I wanted to be sure that the reviewers of this assignment could get my project up and running. Sticking to just pip with requirements files accomplishes that.

For a productionized setup, a package manager with lock files should be used to ensure that what get installed is exactly as we expected and there are no surprise upgrades of downstream dependencies.

## Technical thoughts
### Module/directory structure
The layout as is as simple, predictable and familiar as possible. It follows the layout presented in the [Django Rest Framework "Quick start guide"](https://www.django-rest-framework.org/tutorial/quickstart/).

In a larger code base, I tend to split code by functionality or domain as I've found that it scales better. Sticking to the pseudo standard defined by Django of splitting code by "type" (views, models, serializers etc) tends not to scale well in large code bases.

For this interview assignment, I did not apply such splitting because it was my intention to make the code base recognizable and familiar, which is also worth something.

It's all about trade offs.

### Scaling the database
One of the biggest bottle necks in scaling an application is often the database. Although I've applied some good practices when it comes to scaling a PostgreSQL database, a productionized set up would also include:

- A connection pooler (PgBouncer, Supavisor etc) with transaction pooling enabled.
- TLS setup
- Do not use binary builds of Psycopg3
- Disable `ATOMIC_REQUESTS` for read-only views, use async views.

### API versioning
I went with a header versioning scheme. This builds on top the HTTP standard and is found in other well known APIs such as the Github API.

This allows for standard HTTP content negotiation in the future. Unfortunately, it does make it a little trickier to handle caching since the `Accept` header has to be included in the cache key (`Vary`).

### Deploying
Couple of things that are left to do before deploying this to production:

- Set up integration with a ASGI/WSGI web server.
- Set up request logging
- Set up error tracking (Sentry?)
- Integrate OpenTelemetry logs & metrics SDK
- Set up and configure Django settings for running a TLS web server (secure cookies, HSTS etc).
- Put it behind some kind of load balancer (Nginx, AWS ALB, CLB, Cloudflare, whatever) and have it terminate TLS.
