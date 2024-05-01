# Contributing Guidelines

Thank you for wanting to contribute to our project! We welcome any form of help, whether it's fixing bugs, adding new features, improving documentation, or solving issues.

## Getting Started

1. Make sure you have Git installed on your computer.
2. Make sure you have poetry installed on your computer, if not
    ```bash
    pip install poetry
    ```
3. Clone the repository:

    ```bash
    git clone https://gitlab.com/ivan_ds/mlops_course
    ```

3. Create your development branch:

    ```bash
    git checkout -b your_branch_name
    ```

4. Make necessary changes and stage them:

    ```bash
    git add .
    ```
5. Make pre-commit steps(use code linters(ruff, mypy, flake8, black))
    ```bash
    pre-commit run
    ```
If you want to use linters whithout pre-commit stage use next

    ```bash
    poetry run ruff format /path_to_code_file
    poetry run mypy . /path_to_code_file
    poetry run flake8 /path_to_code_file
    poetry run black /path_to_code_file
    ```

6. Commit your changes:

    ```bash
    git commit -m "Description of your change"
    ```

7. Push your changes:

    ```bash
    git push origin your_branch_name
    ```

8. Create a Pull Request (PR) on GitHub.

9. Wait for your PR to be reviewed. We'll try to respond as soon as possible.

## Making Your Contribution Valuable

- **Describe the issue or proposal:** Please provide a detailed description of the issue or proposal in your PR. This will help us understand exactly what you want to change or add.

- **Testing:** Test your changes to ensure they work as expected. This will help avoid errors and simplify the review process.

- **Code style compliance:** Please follow the existing code style in the project. This will make it easier to maintain the code in the future.

- **Updating documentation:** If you're making changes that affect the documentation, please remember to update the relevant sections of the documentation.

- **Respect for others' opinions:** Please be polite and respect the opinions of other project contributors.

## Feedback

If you have any questions or suggestions for improving the contribution process, feel free to contact us by email or create an Issue in the repository.

Thank you for your contribution to the development of our project!
