# Web app Client TCP Socket

## Introduction

---

The App works as a very simple socket client that just receives messages from a socket server and display the messages on the webpage in real time.

I've tried 2 versions:

- the fist I failed and include the files app.py and socket_client.py.

- the second use just one file main.py, then it works.

## Dependencies and Installation

---

To install the application, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

## Usage

---

To use the applicaton, follow these steps:

1. Ensure that you have installed the required dependencies.

2. Run the ` main.py` file using the Streamlit CLI. Execute the following command:

   ```
   streamlit run main.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

## Notes

---

I choose use PyVenv to create virtual envorioment for my Python project, to ensure to use the Python version 3.11

First, make sure install Python 3.11 in your computer.

Make sure create your virtual envionment:

To create the virtual environment, run:

```
python3.11 -m venv name_of_virtual_env
```

For example: python3.11 -m venv venv

To activate your new virtual environment, run:

```
.\name_of_virtual_env\Scripts\Activate.ps1
```

For example: .\venv\Scripts\Activate.ps1

To deactivate your virtual environment, just run:
deactivate

## Requirements.txt commands

---

Install the required dependencies by running the following command:

```
pip install -r requirements.txt
```

Update all dependencies to last version by running the following command:

```
pip install --upgrade -r requirements.txt
```

If you install dependencies manually, to generate the file requirements.txt run the following command:
Para gerar o arquivo requirements.txt com as dependencias instaladas no ambiente virtual usar o comando:

```
pip freeze > requirements.txt
```

## Contributing

---

This repository is intended for educational purposes and does not accept further contributions. It serves as supporting material for a YouTube tutorial that demonstrates how to build this project. Feel free to utilize and enhance the app based on your own requirements.

## License

---

The application is released under the [MIT License](https://opensource.org/licenses/MIT).
