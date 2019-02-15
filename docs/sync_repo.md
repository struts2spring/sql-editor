# this is to sync code in different repository.

git remote show origin

(venv) c:\1\sql_editor>git remote -v
origin  https://gitlab.com/struts2spring/sql_editor.git (fetch)
origin  https://gitlab.com/struts2spring/sql_editor.git (push)

git remote set-url origin https://github.com/struts2spring/sql-editor.git

sudo python3 setup.py install
sudo python3 -m twine upload --skip-existing  dist/*

# command to create windows executable
pyinstaller src\TheEclipse.py -w -F -i "C:\1\sql_editor\src\images\Opal_database.ico"


pyinstaller sql_editor.spec

