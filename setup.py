from setuptools import setup, find_packages


def long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setup(
    name="slack_bot",
    version='0.0.7',
    author='Denis Korytkin',
    author_email='dkorytkin@gmail.com',
    url='https://github.com/DKorytkin/slack-bot',
    description='Simple application for make slack bot',
    long_description=long_description(),
    long_description_content_type="text/markdown",
    keywords=['bot', 'slack', 'app', 'slack_bot', 'app', 'application'],
    platforms=['linux'],
    packages=find_packages(exclude=['tests', 'tests.*', 'example']),
    py_modules=[
        'slack_bot.bot',
        'slack_bot.models',
        'slack_bot.routes',
    ],
    python_requires='>=3.6',
    install_requires=[
        # base
        'pip>=19.0.3',
        'setuptools>=41.0.0',
        # for slackclient
        'certifi==2019.3.9',
        'chardet==3.0.4',
        'idna==2.8',
        'requests>=2.21.0,<3',
        'six>=1.12.0',
        'urllib3>=1.24.2,<1.25.0',
        'websocket-client==0.47.0',
        # for application
        'slackclient==1.3.1,<2.0.0',
        'parse>=1.12.0<2.0.0',
    ],
    license='MIT license',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
