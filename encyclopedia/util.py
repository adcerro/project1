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
        f = default_storage.open(f"entries/{title}.md")
        lines = f.read().decode("utf-8").splitlines()
    except FileNotFoundError:
        return None
    
    html:str = []
    lastline:str = ""
    for line in lines:
        text = md2html(line)
        if (not lastline.startswith("<li>")) and text.startswith("<li>"):
            text = "<ul>"+text
        elif (lastline.startswith("<li>") and (not text.startswith("<li>"))):
            text = "</ul>"+text
        html.append(text)
        lastline = text
    return html

def md2html(line:str):
    if line=="":
        return "<br>"
    else:
        text = boldfaceDetector(line)
        text = headerDetector(text)
        text = ulistDetector(text)
        if text.startswith("<h") or text.startswith("<li"):
            return text
        else:
            return "<p>" + text+ "</p>"

def ulistDetector(text:str):
    match = re.match(r"\* (.*)",text)
    if match != None:
        text ="<li>"+match.group(0)[2:]+"</li>"
    return text
    
def boldfaceDetector(text:str):
    matches = re.finditer(r"\*\*([^\*]*)\*\*",text)
    for match in matches:
        text =text.replace(match.group(0),"<b>"+match.group(0)[2:-2]+"</b>")
    return text

def headerDetector(text:str):
    match = re.match(r"^#+ (.*)",text)
    if match != None:
        text = match.group(0)
        level = headerCount(text)
        return f"<h{level}>{text[level+1:]}</h{level}>"
    return text

def headerCount(text:str):
    return countCall(text.strip(),0)

def countCall(text:str,index:int):
    if text[index] == "#":
       return 1 + countCall(text,index+1)
    else:
        return 0