# Setup development system

Use this guide to setup your local system to develop for the project.
We provide scripts for setting up Mac and Linux based systems. While Windows
based systems might also be used for development, the setup is not straightforward
and we do not provide a script to set it up. 

## Prerequisites
1. Install Anaconda or a preferred Python environment manager. We use [Anaconda](https://www.anaconda.com/products/individual)
2. Create a new environment with **Python 3.7**. This is important, since we support only Python 3.7. Other version of Python will not work.
    - Example conda environment creation command: `conda create --name covid python=3.7`
3. Activate your virtual environment
4. If your system is Mac, run the `setup_mac.sh` script, and if your system is Linux based, run the `setup_linux.sh` script.


## Error while setting up system

If you come across an error while setting up your system, or if you had to perform
additional steps, please either raise an issue or put in a pull request with the fix.
