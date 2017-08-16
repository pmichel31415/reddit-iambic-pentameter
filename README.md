<div align="center">
  <a href="https://pmichel31415.github.io/reddit-iambic-pentameter/">
    <img src="https://github.com/pmichel31415/reddit-iambic-pentameter/raw/master/logo.gif" width="100px">
  </a>
</div>

#  [RIP: Reddit Iambic Pentameters](https://pmichel31415.github.io/reddit-iambic-pentameter/)

RIP is a bot that scans new comment on the popular message board [reddit](https://www.reddit.com/r/all/) to detect iambic pentameter, one of the most famous types of verses in english poetry.>
9
> 

Here are some funny quartains it composed

    And half the toilet paper in the building.
    Was at that final. It was a good day.
    Can you? It would be pretty interesting.
    The Maya are alive and well today.
    ---
    and pirates do a LOT of gambling!
    Its not that hard to recognize a door.
    That dive into the quarry looks amazing.
    Are people even trying anymore?

RIP tweets an Iambic pentameter found on twitter every hour, follow him:

<a class="twitter-timeline" href="https://twitter.com/R_I_P_bot">Tweets by @R_I_P_bot</a> 

## Iambic pentameters?

From wikipedia:

> An iambic foot is an unstressed syllable followed by a stressed syllable. [...] A standard line of iambic pentameter is five iambic feet in a row

Here's an example of a iambic pentameter that you would typically encounter on reddit:
>
9
> 
> this post has been removed for breaking rule 

This line follows the ``0101010101`` stress pattern, here's a breakdown

	this | post | has | been | re | moved | for | brea | king | rule
	 0   |  1   |  0  |  1   | 0  |   1   |  0  |  1   |  0   |  1   
	 
## Requirements

This project requires 3 packages to function, ``praw`` for the reddit API, ``pyyaml`` to read the yaml config file and ``pronouncing`` to get the stress pattern of words.

    PyYAML>=3.12
    praw>=5.0.1
    pronouncing>=0.1.5

## Usage

Modify the config file to set your bot's details. Then just run

```bash
python rip.py config.yaml
```
