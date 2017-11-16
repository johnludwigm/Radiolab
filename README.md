# Radiolab

Downloads episodes of Radiolab from radiolab.org.



If you find any errors or have any suggestions for improvement, please let me know!

To download specific episodes, simply run:

 `python3 -m radiolab -dl <Episodes-that-you-want-to-download> -dest <path-to-download-destination>`
 
 
To download all episodes, run:

`python3 -m radiolab -dlall -dest <path-to-download-destination>`


---

Ex:


`python3 -m radiolab -dl "The Ceremony" Colors "Radiolab Presents: Ponzi Supernova" -dest /Users/John/Desktop`


This will download the episodes "The Ceremony", "Colors", and 'Radiolab Presents: Ponzi Supernova" to the directory "/Users/John/Desktop".


Bear in mind that if any string has a space in it (e.g. `"The Ceremony"`), then you will have to put quotes around it when entering it in the command line so that it is interpreted as one string rather than two (e.g. `"The Ceremony"` is interpreted as `The Ceremony` whereas `The Ceremony` is interpreted as `The` `Ceremony`).



Even for episodes with weird titles, (e.g. "12: Proof", "(So-Called) Life") you have to enter the exact title name in order to download that specific episode. The exception is when there is a character that is not UTF-8 (e.g. "≤ kg"). I changed those to the intuitive substitutes (in this case, "<= kg").


