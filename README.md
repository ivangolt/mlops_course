Repository of the course "MLOps and production in DS research 3.0"

## Tools and Usage

For details see [CONTRIBUTING.md](CONTRIBUTING.md)

## Repository management methodology


This repository follows a specific development and code maintenance methodology. Below are the main principles and guidelines for working with it.

### Branching

We use the following branching strategy:

- `main`: The `main` branch is only for stable, production-ready code. Direct changes to it are prohibited.
- if you want to make changes or new features use separate branch (bash: git branch `feature/*`)
- before push new commit use pre-commit!


### Pull Requests

- To merge code from `feature/*` branches into `develop` or from `develop` into `main`, a Pull Request must be created.
- Each Pull Request must be reviewed by at least one colleague before merging.
- Clear comments and a description of what has been done are required in the Pull Request.

### Code Commenting

- All code must be adequately commented.
- Long functions or complex code sections require detailed comments.

### Testing

- Each new feature must be covered by tests.
- Special attention should be paid to regression testing during feature development.

### Running a Local Server

- Instructions for running a local server or development environment must be provided in README.md.
- README.md should contain information about environment requirements, dependencies installation, and application startup.


## Docker

To get started with the project, follow these steps:

1. Clone the repository to your computer using the following command:
    ```bash
    git clone https://gitlab.com/ivan_ds/mlops_course
    ```
2. Navigate to the project directory:
    ```bash
    cd repository_name
    ```
3.  Build the Docker image
    ```bash
    docker build -t mlops_course
    ```
4. Running the container
    ```bash
    docker run -it mlops_course /bin/bash
    ```

## CI\CD stages

1. **linting** 

2. Build and publish your project as a package to the **gitlab pypi registry** (https://gitlab.com/ivan_ds/mlops_course/-/packages).

3. **DinD** build of a Docker image. Image published [Gitlab Docker Registry](https://gitlab.com/ivan_ds/mlops_course/container_registry).

4. **EDA**  [mlops_course](mlops_course/tree_data.ipynb)

5. **pages** add documentation of project in Gitlab Pages

## Contacts

If you have any questions or suggestions regarding the development methodology in this repository, please contact us at:
- Email: milovidov.999@gmail.com
- telegram: @ivan_golt
