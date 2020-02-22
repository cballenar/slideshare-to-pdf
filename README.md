# SlideShare to PDF

A python script to help you back up your SlideShare presentations to PDF.


## Requirements

This script has been tested with Vagrant on an **Ubuntu Trusty 64** VM (Vagrantfile included) and requires the following packages:

- [ImageMagick](http://www.imagemagick.org/script/index.php)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [LXML](http://lxml.de/)

They can be installed by running:

````
apt-get update
apt-get install -y imagemagick 
pip install bs4 lxml six requests
````

On Windows, [Windows Binary of ImageMagick](https://imagemagick.org/script/download.php#windows) can be used.
ImageMagick must be added to PATH.
Please check if ImageMagick `magick` command can be executed or not using Command Prompt.

```
> magick -help
Usage: magick tool [ {option} | {image} ... ] {output_image}
```
Remark:
If this script can't find out ImageMagick `magick` command, it will try to use ImageMagick `convert` command.
However, Windows built-in `convert` command(`C:\Windows\System32\convert.exe`) hides it.

The rest of packages can be installed via pip.

````
pip install bs4 lxml six requests
````

## Usage

### Just run it

Simply running the script will prompt you to input the SlideShare URL you'd like to download. By default, this file will be saved in the `downloads` directory created in the root of the script.

````
./grub.py
Input the SlideShare URL you want to convert: [SLIDE URL]
Reading SlideShare page...
Downloading slide 1...
Downloading slide 2...
[...]
Converting to PDF...
Your file has been successfully created at downloads/[SLIDE NAME].pdf
````


### Run it with Arguments

```
./grub.py [-i|--input <url>] [-o|--output <path>] [-j|--jpg] [--use_convert] [-q|--quiet]
```

#### Input
Specify the SlideShare URL you'd like to download with `-i`.

````
./grub.py -i <SLIDESHARE URL>
````


#### Output
You can specify where to save your PDF with `-o`. The script will accept a directory or a file path. If only the directory path is specified, the name of the slide will be used.

````
./grub.py -o <FOLDER OR FILE PATH>

# save in directory
./grub.py -i [...] -o /home/user/documents/

# save to file
./grub.py -i [...] -o /home/user/documents/my-slide.pdf
````


#### Keep JPGs
You can request to keep the JPG files using `-j` or `--jpg`. This will export the PDF file and also a directory with all the JPG files that make up the PDF.

````
/my-slides-by-author.pdf
/my-slides-by-author/01.jpg
/my-slides-by-author/02.jpg
/my-slides-by-author/03.jpg
...
````

#### Force use of `convert`
The script will automatically detect if the command `magick` is available and use it by default. If you require the use of `convert` instead use `--use_convert`


#### Quiet
Don't print status messages to stdout.

````
./grub.py -q
````


#### Help
Show help message and exit.

````
./grub.py -h
````


## Development
This repository includes a Vagrantfile. If you'd like to collaborate, this should help jumpstart the development process.

## Contributors
- [tdrk1980](https://github.com/tdrk1980)
