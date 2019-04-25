
# slack-bot
Application for easy make slack bot


## Getting Started:

### Installing:

```bash
pip install slack-bot
```

### Usage:

```python
import os

from slack_bot import Application, Response


app = Application(token=os.getenv('SLACK_TOKEN'))


@app.route('hello')
def main(request):
    return Response(request=request, text=f'Hi! {request.user}')


@app.route('deploy {app:w}')
def deploy_staging(request):
    current_app = request.match_info["app"]
    # body for deploy staging ...
    return Response(request=request, text=f'Start deploy {current_app}')


if __name__ == '__main__':
    app.run()
```

![chat example](./chat_example.png)

### Examples:

 - [init routes in app as decorator](example/first_example.py) 
 - [init routes in table](example/second_example.py) 
 - [init routes in app](example/third_example.py) 

## Authors:

 - Denis Korytkin

## License:

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Dependencies:

*base*

```bash
pip==19.0.3
setuptools==41.0.0
```

*application dependencies*

```bash
slackclient==1.3.1
```

*slackclient dependencies*

```bash
certifi==2019.3.9
chardet==3.0.4
idna==2.8
requests==2.21.0
six==1.12.0
urllib3==1.24.2
websocket-client==0.47.0
```
