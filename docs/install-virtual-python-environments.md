<small>Copyright (c) 2018 - 2019 Jolle Jolles<br/>
Last updated: 31 Jan 2019</small>

<h2>Installing virtual python environments</h2>

When you start working with Python it is great practice to create isolated Python environments to work on your specific projects. The standard python environment is used by a large number of system scripts and therefore best to leave alone. In addition, when working on different projects, those projects may have different and conflicting dependencies and therefore should ideally be installed in their own python environments. The ability to create different python environments can also be really beneficial when developing your own python packages and thereby test its installation and performance in different versions of python.

<h3>Installing virtualenv and virtualenvwrapper</h3>

To create different virtual environments we will use the `virtualenv` and accompanying `virtualenvwrapper` packages. To do so, enter the following commands in terminal:

```
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip
```

Now, to finish the installation and make it easy to use this functionality we need to update the `~/.profile` file. Simply run the following bash commands:

```
echo -e "\n# Virtual python environments" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
```

*Note 1: Make sure that the python version you are using is correctly specified in the third line, e.g. for python2.7 the end of the line would look like `/usr/bin/python2" >> ~/.profile`.*

*Note 2: Different systems make use of different shell startup files `~/.bash_profile` and `~/.bashrc`. Make sure which file your system uses.*

Next, source the profile file:

```
source ~/.profile
```

<h3>Create and work with a virtual environment</h3>

Now we are ready to create a virtual environment.

```
mkvirtualenv py2 -p python
```

With this command "py2" is the name we give our virtual environment and "python" is the version of python we want to use for the virtual environment. So if we would like to create a different virtual environment for python 3 with opencv support for example, the command could like like: `mkvirtualenv py3cv -p python3`.

Now to use the new virtual environment simply type "workon" followed by the name of the environment, e.g. 

```
workon py2
```

The newly created virtual environment is basically a folder which contains all the necessary executables to use the packages that a Python project would need. So the moment you have created your fresh virtual environment it contains no packages yet, even when other virtual environments or the global environment does. To install packages, simply use apt-get or pip, e.g.:

```
pip install numpy
``` 

When you are ready and want to exit your python environment, simply type:

```
deactivate
```

To list all environments enter:

```
lsvirtualenv
```

And to delete a virtual environment:

```
rmvirtualenv py2
```

<h3>Copy a (virtual) environment</h3>

It may be helpful to copy an existing (virtual) environment, such as to ensure consistency across installations and deployments. To do so, enter the current environment and get a list of all installed packages and their version by typing:

```
pip freeze > requirements.txt
```

Now enter your new virtual environment and install all the same packages using the same versions:

```
workon py2
pip install -r requirements.txt
```

That's it!