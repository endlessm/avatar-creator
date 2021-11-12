## Update pot files from source files:
cd po
intltool-update --maintain
cd ..
find avatar-creator -iname "*.py" | xargs xgettext --from-code=UTF-8 --output=po/avatar-creator-python.pot
find data -iname "*.ui" | xargs xgettext --from-code=UTF-8 --output=po/avatar-creator-glade.pot -L Glade
msgcat --use-first po/avatar-creator-glade.pot po/avatar-creator-python.pot > po/avatar-creator.pot
rm po/avatar-creator-glade.pot po/avatar-creator-python.pot

## Generate po file for language
cd po
msginit --locale=xx --input=avatar-creator.pot

