## Introduction

If you're reading this, is because either you love Slack, or just need to work with its API somehow. Recently I had 
to start implementing a bot in Slack which content was more complex than usual. Then, I found that Slack API was quite 
easy to use but.... its views, those contents in json can be soooo huge and complex, that I realized I spent most of my 
time designing templates instead of coding the logic of the bot.
This is when I started to look around searching for some library that would allow me to code my views in Python easily, 
unfortunately, I didn't found any (hey, if it does exist, please let me know, I had no idea about it) so I decided to
write this one.
The lib, includes "almost" all Block types, I just left out those that I was not gonna use for sure, but once you see 
the source code you'll realize it can be extended to include those pretty easily.

## Documentation

Check included Readme.md or latest doc at [Slackviews Readme.md](https://github.com/escamez/slackviews/blob/master/README.md)
