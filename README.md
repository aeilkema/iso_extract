# iso_extract
NZBget iso extract, simple / basic nzbget post process script to extract iso files after download via 7Zip

[Version 1.0]
* Option to delete it after successful extraction (default: no deletion)
* Option to extract to subdirectory (default: extract to subdirectory)
* Debug messages (default: do not create debug messages)
* Option to disable (default: script is enabled)

[Version 1.1]
* Added: Option to check a list of categories against current download category and not to extract in that case: e.g. 'Video' / 'Movies' / etc will be extracted, but 'Games' and 'Programs' not 

Uses 7zip instead op python, no need to import thirdparty libraries.
Did try patools library, but found 7zip worked easier. 

NOTE:
* Will not delete iso files if iso file(s) are in the base download folder of nzbget (iso is not in own sub directory)
* Will use a sub directory if iso file is in the base download folder of nzbget
* Maybe other scripts can't find iso file if you choose to delete it ;-) (so use this script as the last script?)
* My first pythonscript, so code could be a little weird, but works for me ;-)

Please modify to your own needs.

Joachim Aeilkema
