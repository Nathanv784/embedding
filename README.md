#   Building a Chat Conversation using LangChain and OpenAI 



## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: Download and install Python from [here](https://www.python.org/downloads/).
- **Postman**: Download and install Postman from [here](https://www.postman.com/downloads/).
- **pgAdmin4**: Download and install pgAdmin4 from [here](https://www.pgadmin.org/download/).
- **PostgreSQL Database**: Install PostgreSQL from [here](https://www.postgresql.org/download/).
- **OpenAI API Key**: Create an OpenAI API Key from [here](https://openai.com/blog/openai-api).

## Getting Started

To get a local copy up and running, follow these simple steps:

1. **Clone the repository:**

    ```bash
    git clone [repository_url]
    ```

2. **Setting up Virtual Environment:**

    - **Install Virtual Environment:**

        For Linux/Mac:

        ```bash
        sudo apt install python3.8-venv
        ```

    - **Create a Virtual Environment:**

        For Linux/Mac:

        ```bash
        python3 -m venv envname
        ```

        For Windows:

        ```bash
        python -m venv envname
        ```

        Example:

        ```bash
        python3 -m venv env1
        ```

    - **Activate the Virtual Environment:**

        For Linux/Mac:

        ```bash
        source envname/bin/activate
        ```

        For Windows:

        ```bash
        .\envname\Scripts\activate
        ```

    - **Install Dependencies:**

        ```bash
        pip install -r requirements.txt
        ```

3. **Create a Database and Install the Vector Extension:**

    - **For Linux/Ubuntu:**

        ```bash
        sudo -u postgres psql
        ```

        ```sql
        CREATE DATABASE databasename;
        \c databasename
        CREATE EXTENSION vector;
        ```

    - **For Mac:**

        ```bash
        psql postgres -c "CREATE DATABASE database_name"
        ```

        ```bash
        psql postgres -U username -d database_name -c "CREATE EXTENSION vector" databasename;
        ```

4. **Create .env file:**

    ```bash
    touch sample.env
    ```

5. **Run the Application:**

    ```bash
    python3 app.py
    ```

6. **Deactivate the Virtual Environment:**

    ```bash
    deactivate
    ```


