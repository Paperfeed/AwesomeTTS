AwesomeTTS [unofficial update v11]
==========

A TTS plugin for Anki

Changelog:

== BETA v11 == 
*Fixed the MP3 Generation when using Google with Chinese/special characters.

*Changed the way the files are being pulled from Google Translate (urllib2)

*Filenames are now being hashed from the input string. 
This way we can locally check if the file exists already, before generating a new file it from Google.
