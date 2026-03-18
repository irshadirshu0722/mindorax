| Type     | Purpose                                    |
| -------- | ------------------------------------------ |
| feat     | new feature                                |
| fix      | bug fix                                    |
| refactor | code improvement without changing behavior |
| docs     | documentation                              |
| test     | add/update tests                           |
| style    | formatting, linting                        |
| chore    | maintenance tasks                          |
| perf     | performance improvements                   |
| build    | build system changes                       |
| ci       | CI/CD changes                              |



python -m celery -A core worker -P gevent -c 1000 -l INFO
