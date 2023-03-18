# Allied Mastercomputer

A fun speech to text app, that talks back and helps you do a few things on the web.

## Instructions
1. Clone or download project locally.
2. Run `pipenv install`
3. After installation run `pipenv shell`
4. In the pipenv shell simply run `python main.py`

## Troubleshooting
If you're running into issues with `pyaudio` not installing you may need to run `brew install pyaudio`. This seems to be a common issue on mac OS machines.

## Apple Mac OS X (Homebrew & PyAudio)
Use Homebrew to install the prerequisite portaudio library, then install PyAudio using pip:

`brew install portaudio`
`pip install pyaudio`

Notes:

If not already installed, download Homebrew.
pip will download the PyAudio source and build it for your version of Python.
Homebrew and building PyAudio also require installing the Command Line Tools for Xcode (more information).

[https://people.csail.mit.edu/hubert/pyaudio/](https://people.csail.mit.edu/hubert/pyaudio/)

