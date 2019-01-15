# What is this?
A simple code that attempts to automatically generate a character network from a given movie or tv script.

# How does it work?
Character names are obtained from the script using the fact that standard scripts follow the convention of preceeding each character line with 'CHARACTER NAME:' in uppercase.
A list of characters is formed and used to build a character matrix.
The script is then analysed to find every time two character names appear within a specified distance. If such an instance occurs we add one to the associated position in the character matrix.
The network is then built and analysed using the networkx library.

# Caveats
The script has to be formatted so that every character line is preceeded by 'CHARACTER NAME:', so this is only appropriate for 
screenplays/ tv scripts/ plays, and not for example a novel.
# Output
The code outputs the network where each node represents a character, and are coloured according to which community the character belongs to. Edge weight and color between a character represent how often the character names appear close to one another in the script.

This example is for season 1 episode 1 of game of thrones, you can find the script here: https://genius.com/Game-of-thrones-winter-is-coming-annotated

The output of the code:

<img src="https://github.com/scottgilmartin/Auto_Network/blob/master/images/1.png" alt="alt text" width="60%" height="50%">

A closer look at the main community:

<img src="https://github.com/scottgilmartin/Auto_Network/blob/master/images/2.png" alt="alt text" width="60%" height="50%">

