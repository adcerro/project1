import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        return default_storage.open(f"entries/{title}.md").read().decode("utf-8")
    except FileNotFoundError:
        return None
    
def entry2html(title):
    try:
        lines = get_entry(title).splitlines()
    except:
        return None
    
    html:str = []
    lastline:str = ""
    for line in lines:
        text = md2html(line)
        if (not lastline.startswith("* ")) and line.startswith("* "):
            text = "<ul>\n"+text
        elif (lastline.startswith("* ") and (not line.startswith("* "))):
            text = "</ul>\n"+text
        html.append(text)
        lastline = line 
    return html

def md2html(line:str):
    if line=="":
        return "<br>"
    else:
        text = headerDetector(line)
        text = boldfaceDetector(text)
        text = ulistDetector(text)
        text = linkDetector(text)
        if text.startswith("<h") or text.startswith("<li>"):
            return text
        else:
            return "<p>" + text+ "</p>"

def linkDetector(text:str):
    """
    text: string to be analized

    The function checks if the string contains links, replacing the \[]() with the <a href=""> tag in each instance
    """
    matches = re.finditer(r"\[[^\]]*\]"+r"\([^\)]*\)",text)
    for match in matches:
        visible = re.search(r"\[(.*)\]",match.group(0))
        link = re.search(r"\(.*\)",match.group(0))
        text = text.replace(match.group(0),f'<a href="{link.group(0)[1:-1]}">{visible.group(0)[1:-1]}</a>')
    return text

def ulistDetector(text:str):
    """
    text: string to be analized

    The function checks if the string is a list item, removes the * and wraps the text in the <li> tag\n
    """
    match = re.match(r"\* (.*)",text)
    if match != None:
        text ="<li>"+match.group(0)[2:]+"</li>"
    return text
    
def boldfaceDetector(text:str):
    """
    text: string to be analized

    The function checks if the string contains bold text and replaces each ** with the <b>|</b> tag
    """
    matches = re.finditer(r"\*\*([^\*]*)\*\*",text)
    for match in matches:
        text =text.replace(match.group(0),"<b>"+match.group(0)[2:-2]+"</b>")
    return text

def headerDetector(text:str):
    """
    text: string to be analized

    The function checks if the string is a header and returns the html equivalent using the <h> tag\n
    The number of # in the beginning of the string determines the level of the header
    """
    match = re.match(r"^#+ (.*)",text)
    if match != None:
        text = match.group(0)
        level = headerCount(text)
        return f"<h{level}>{text[level+1:]}</h{level}>"
    return text

def headerCount(text:str):
    """
    text: string to be counted

    The function calls returns the number of # in the beginning of the string
    """
    return countCall(text.strip(),0)

def countCall(text:str,index:int):
    """
    text: string to be counted
    index: index of the string

    The function is a recursive call that counts the number of # in the beginning of the string
    """
    if text[index] == "#":
       return 1 + countCall(text,index+1)
    else:
        return 0
