
# slack_bot
Template app for make slack bot


## Getting Started:

### Installing:

```bash
pip install slack_bot
```

### Usage:

```python
import os

from slack_bot.bot import Application


app = Application(token=os.getenv('SLACK_TOKEN'))


@app.route('hello')
def main():
    return 'Hi!'


if __name__ == '__main__':
    app.run()
```

### Examples:

 - [init routes in app as decorator](example/first_example.py) 
 - [init routes in table](example/second_example.py) 
 - [init routes in app](example/third_example.py) 

## Authors:

 - Denis Korytkin

## License:

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
