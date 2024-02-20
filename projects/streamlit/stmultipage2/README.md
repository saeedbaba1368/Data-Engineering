## Code to support the article 
# [3 Ways to Create a Multi-Page Streamlit App](#)

The code files are as follows.

- In the main folder
  - ``mp1.py`` is simple if/else and inline code
  - ``mp2.py`` is like mp1 but with 3.10 pattern matching
  - ``mp3.py`` explicitly imports the modules and uses if/else to run them
  - ``mp4.py`` reads the module names from a library function, loads the modules and runs them by matching the strings in the drop down menu

- ``stlib`` is the library folder which contains:
  - ``__init__.py`` to show that this is a Python package
  - ``libContents.py`` returns a list of modules
  - ``continentDat.py`` is one of the pages to display
  - ``countryData.py`` is the other page to display

- ``stnative`` is a folder with demonstrator files for the Streamlit native implementation of multi-page 