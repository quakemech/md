# Overview 

MD is a Markdown processing tool that compiles markdown files into multiple 
output formats. Essentially it is a wrapper around pandoc with a more 
convenient user interface. 

# Installation 

MD uses template files to implement some formatting choices. The repo includes 
two template files: mdtemplate.css (for epub outputs) and mdtemplate.tex for 
pdf outputs. These files need to be placed in the users ~/bin directory. 
Alternatively, the user can use a command line flag to specify an alternative 
location of the template .tex file. 

# Dependencies 

MD requires pandoc to be installed in the system. It can be installed using the 
system package manager such as 

```bash
apt install pandoc 
```

```bash 
brew install pandoc
```

# Usage 

To compile a document into a pdf use the following command: 

```bash
md.py -p README.md
```
