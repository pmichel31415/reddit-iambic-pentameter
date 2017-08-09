# RIP: a Reddit Iambic Pentameter bot

RIP is a bot that scans new comment on the popular message board [reddit](https://www.reddit.com/r/all/) to detect iambic pentameter, one of the most famous types of verses in english poetry.

## Iambic pentameters?

From wikipedia:

> An iambic foot is an unstressed syllable followed by a stressed syllable. [...] A standard line of iambic pentameter is five iambic feet in a row

Here's an example of a iambic pentameter that you would typically encounter on reddit:

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
