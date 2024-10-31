I'm implementing a web application with front-end and back-end for generating a code base by reading in a requirement spec.

Now I would like you to help me generating the backend for this web application. Your tech stack is python, flask, postgres sql, google cloud user store. You need to deliver a set of REST api as well as their implementations in python.

Here are the definitions of domain entities:
* A user can login and logout the system backed by google cloud user store
* A specification is a text string with a unique numeric ID
* each specification can have 0 or more but less than 10 bullet items. The items are ordered and each of them can be identifiedy by a ID unique in its parent specification.
* A project is a list of specifications with a text title. A project is owned by one user. Only that user can write and update data within a project.
* A specification can only belong to one project.
