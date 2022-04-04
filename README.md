# EXCEL to ICES Dome Conversion Tool

## Installation
If no Python version is yet installed, please install miniconda, following the instructions here:
https://docs.conda.io/en/latest/miniconda.html

Clone this repository in any local directory.

Next, create and setup a new environment, using the *Anconda Prompt* App (Just search for it in the Windows Start Menu):
* In the command prompt run:
````
conda install --name=domeconverter python=3.9
````
* Activate the environment with: 
````
conda activate domeconverter
````
* navigate into the DomeXLSConverter folder
* run: 
```` 
pip install -r requirements.txt
````

The following screenshot shows the procedure (note, that the environment in my case was just named *domeconv*).
![](images/01_activate_and_configure.png)

This installs all required python packages.

## Launch the tool
In the _Anaconda Prompt_ run (having activated the domeconverter environment) run the command:
````python
python main.py
````

Then follow the instructions in the user ui.

## Code Structure
to be continued..