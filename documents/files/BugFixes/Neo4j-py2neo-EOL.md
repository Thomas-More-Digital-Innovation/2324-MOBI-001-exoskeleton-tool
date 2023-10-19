# Problem: Neoj4's py2neo service is EOL

## Issue Description
As a Py2neo library user, I've recently confronted difficulties in both the installation and utilization of the library. My suspicion is that these issues stem from Py2neo's recently declared end of life (EOL). This has led to a situation where integrating or installing Py2neo into my Python project, specifically the Sense2Extion exoskeleton tool project, appears to be unattainable. What supports my belief in this association is a sudden inability to execute my app.py file, which arises due to the subsequent error message:
```
Traceback (most recent call last):
  File "C:\repos\DI\2324\sense2exion\code\app.py", line 6, in <module>
    from py2neo import Graph
ModuleNotFoundError: No module named 'py2neo'
```

This error generally signals that the specified library or extension (in this instance, py2neo) has not been incorporated into the project. In an effort to rectify this, I attempted to resolve the issue by deploying the 'pip' command for py2neo installation. Unfortunately, this effort resulted in the subsequent error response:
```
ERROR: Could not find a version that satisfies the requirement py2neo (from versions: none)
ERROR: No matching distribution found for py2neo
```

## py2neo EOL announcement 

> "After many amazing years, the much loved py2neo has come to an end. We are grateful to Nigel Small for the work he put into the project and the ideas that originated there. py2neo elegantly bridged graph thinking with pythonic principles. Well done, Nigel." — ABK, Neo4j Staff

The EOL announcement for Py2neo was posted by ABK, a member of the Neo4j staff, on the Neo4j community forum. You can read the full announcement [here](https://community.neo4j.com/t/farewell-py2neo-what-happens-now/64419).

Additionally, the official documentation, available at [https://store.nige.tech/](https://store.nige.tech/), the Py2neo installation on [PyPI](https://pypi.org/project/py2neo/), and the corresponding GitHub repository [https://github.com/py2neo-org](https://github.com/py2neo-org) have all vanished without prior notice or explanation.

## Short term solution with URL to tar.gz file 

Instead of using the `pip install py2neo` command that no longer works, it is possible to use the URL which goes to the tar.gz file. We can use this URL in our pip install:
```
pip install https://github.com/overhangio/py2neo/releases/download/2021.2.3/py2neo-2021.2.3.tar.gz
``` 

This solves the problem for now but I don't think this fix will keep on working since py2neo is EOL meaning that this solution is far from future proof. As a quick fix it works for now but it's better to keep searching for alternatives.
