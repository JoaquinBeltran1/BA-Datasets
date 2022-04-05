# Business Analysis Datasets

This repo contains the datasets used for my projects (you can read more about them here --> joaquinbeltran.github.io/blog), as well as the Jupyter notebooks with the code to generate them.

Persistence layer -> Business logic layer -> Presentation layer

Database module, commands, module

### Classes

- Database-Manager -> manipulating data in the database

```python
class DatabaseManager:

    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)
        
    def __del__(self):
        self.connection.close()
```