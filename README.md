<h1 align="center">catcalc</h1>

<p align="center"><b> Submit bulk patient data to multiple intraocular lens power calculation formulas.</b></p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/1383561/151686011-7a40c115-f0fc-43ce-9e9c-7e456ff77cfe.png" alt="stock image of a cat wearing glasses" width="300">
</p>

## About ##
For research purposes only!

## Installation ##
Written for Python 3, requires 2 libraries.  In case your IDE doesn't pull them down, here are the two dependendies you need:
* `pip3 install selenium`
* `pip3 install chromedriver-binary-auto`

`chromedriver-binary-auto` (as opposed to `chromedriver-binary`) will automatically detects the latest chromedriver version required for your local installation of Chrome.  Considering most Chrome installs automatically update, you could probably just use `chromedriver-binary`; the import statement doesn't need to change as far as I know.

## How to Run ##
* Just invoke via the command line, like so:
`python3 name_of_calculator.py`
* Both scripts are currently set to "headless" mode -- comment out the line `opts.add_argument("headless")` near the top of the file to see the calculator actually spawn a browser window and run through it *(although it runs fast so it's hard to watch)*. 
* The model names from the dropdown you'll need are listed in a comment above the select_IOL_model() function.  
* Other info about what functions return is usually in a comment above the function, or near the function call.
* You will see a `DeprecationWarning` complaining about `executable_path` -- you can ignore this.
