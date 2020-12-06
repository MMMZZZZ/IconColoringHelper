# IconColoringHelper

IconColoringHelper is simple a Python command line tool that quickly allows you to recolor a set of icons. 

## Requirements

This script has been written with [Python 3.9](https://www.python.org/downloads/). I don't know to what extend it will work with previous Python versions.

In addition you need to instal the [Pillow library](https://pypi.org/project/Pillow/). Should be straight-forward.

## Usage

You can get a full description of all options using

```
python IconColoringHelper.py -h
```

There are three ways of using / features. In all cases you need to specify an input and an output folder:

```
python IconColoringHelper.py -i INPUT_FOLDER -o OUTPUT_FOLDER
```

In addition you need to specify how the images are processed:

* Use the flag `-g` to convert the input files to grayscale images.
* Use the flag `-n` to convert the input files to grayscale images and map the grayscale values to the full range of 0-255.
* Specify colors with `-c FORMAT DARK_COLOR LIGHT_COLOR`. This colorizes the (grayscale) images with the specified colors. `FORMAT` indicates whether you specified the colors as 24 bit RGB (8/8/8) or 16 bit RGB (5/6/5). The colors can be entered as normal integers or as hex values.

## Example

The following graphic is from a set I created for a microcontroller project. I wanted to create a "dark mode" set.

![Original Button](/Example%20Pictures/Original.png)

First I created the mapped grayscale images (same button as example):

![Mapped Grayscale Button](/Example%20Pictures/MappedGrayscale.png)

Then I recolored them with the dark mode colors I wanted. Note this does not look as because the background around is missing.

![Dark Mode Button](/Example%20Pictures/ColoredDark.png)

And for fun, here's the same button with random colors:

![Randomly colored Button](/Example%20Pictures/ColoredRandom.png)
