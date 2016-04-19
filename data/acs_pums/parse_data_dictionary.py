import re
import json
import csv

class Block(object):
    def __init__(self, text):
        self.text = text

footnotePattern = re.compile("^\*+")

class Footnote(Block):
    def __init__(self, text):
        self.text = text
        match = footnotePattern.search(text)
        self.tag = "FN" + str(len(match.group(0)))
        self.description = self.text[len(self.tag):].strip()
        self.paragraphs = []

    def addParagraph(self, paragraph):
        self.paragraphs.append(paragraph)
        if not self.description.endswith("\n") and len(self.description) > 0:
            self.description += "\n"
        self.description += paragraph.text

    def flatten(self):
        blocks = [self.description]
        blocks += [paragraph.text for paragraph in self.paragraphs]

        return {
            "tag": self.tag,
            "description": self.description
        }

class Note(Block):
    pass

variablePattern = re.compile("^[A-Z0-9]+( +[0-9]+)?( \(.*\))?$")
codePattern = re.compile("^[A-z0-9\\-\\.\\/]+ \\.")
footnoteReferencePattern = re.compile("\\*+$")

class Variable(Block):
    def __init__(self, text):
        self.text = text
        lines = text.split('\n')
        spl = lines[0].split()
        self.name = spl[0]
        if len(spl) > 1:
            self.size = spl[1]
        else:
            self.size = None
        self.codebook = []
        self.footnotes = set()
        descriptionLines = []
        for line in lines[1:]:
            if line.startswith("04.Gulf War:"):
                line = line.replace("04.", "04 .")
            m = footnoteReferencePattern.search(line)
            if m is not None:
                tag = m.group(0)
                tag = "FN" + str(len(tag))
                self.footnotes.add(tag)
                line = re.sub(
                    " *\*+$",
                    "<" + tag + ">",
                    line)
            m = codePattern.search(line)
            if m is None:
                descriptionLines.append(line)
                continue
            code = m.group(0)
            codeDescription = line[len(code):]
            code = re.sub(" \\.$", "", code)
            self.codebook.append([code, codeDescription])
        self.description = "\n".join(descriptionLines)
        self.notes = []

    def addNote(self, note):
        self.notes.append(note)
        if not self.description.endswith("\n") and len(self.description) > 0:
            self.description += "\n"
        self.description += note.text

    def flatten(self):
        return {
            "name": self.name,
            "size": self.size,
            "description": self.description,
            "short_description": self.description.split('\n')[0],
            "codebook": self.codebook,
            "footnotes": list(self.footnotes),
        }


class Header(Block):
    def __init__(self, text):
        self.text = text
        self.variables = []
        if text == "HOUSING RECORD":
            self.tag = 'housing'
        elif text == "PERSON RECORD":
            self.tag = 'person'

    def addVariable(self, variable):
        self.variables.append(variable)

    def flatten(self):
        return [variable.flatten() for variable in self.variables]

class Paragraph(Block):
    pass

def generateElements(blocks):
    elements = []
    state = 'start'
    for block in blocks:
        lines = block.split('\n')
        if state is 'start':
            if block == "HOUSING RECORD":
                state = 'housing'
                elements.append(Header(block))
        elif state == 'housing' or state == 'person':
            if block.startswith("HOUSING RECORD"):
                pass
            elif block.startswith("*"):
                state = 'footnotes'
                elements.append(Footnote(block))
            elif block.lower().startswith('note:'):
                elements.append(Note(block))
            elif len(lines) == 1:
                if block == "PERSON RECORD":
                    state = 'person'
                    elements.append(Header(block))
                elif block.lower().startswith('note'):
                    elements.append(Note(block))
                else:
                    print(block + "\n")
            else:
                if variablePattern.search(lines[0]) is not None:
                    elements.append(Variable(block))
                else:
                    print(block + "\n")
        elif state == 'footnotes':
            if block.startswith("*"):
                elements.append(Footnote(block))
            else:
                elements.append(Paragraph(block))
    return elements

def linkElements(elements):
    headers = []
    footnotes = {}
    currentFootnote = None
    for i, elem in enumerate(elements):
        if isinstance(elem, Header):
            headers.append(elem)
        elif isinstance(elem, Variable):
            headers[-1].addVariable(elem)
        elif isinstance(elem, Note):
            headers[-1].variables[-1].addNote(elem)
        elif isinstance(elem, Footnote):
            footnotes[elem.tag] = elem
            currentFootnote = elem
        elif isinstance(elem, Paragraph):
            currentFootnote.addParagraph(elem)
    headers = dict(((header.tag, header.flatten()) for header in headers))
    footnotes = dict(((footnote.tag, footnote.flatten()) for footnote in footnotes.values()))
    return {
        "categories": headers,
        "footnotes": footnotes
    }

def main():
    fileName = "acs_pums/PUMSDataDict14.txt"
    with open(fileName, encoding='latin-1') as f:
        blocks = re.sub('\n\n+','\n\n', f.read().replace('\r','')).split('\n\n')

    elements = generateElements(blocks)
    tree = linkElements(elements)

    with open("acs_pums/quick_reference.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'Name', 'Description'])
        for category, variables in tree['categories'].items():
            c = category[:1]
            for variable in variables:
                writer.writerow([c, variable['name'], variable['short_description']])


    outFileName = "acs_pums/data-dictionary.json"
    with open(outFileName, "w") as f:
        json.dump(tree, f, sort_keys=True, indent=2)

if __name__ == '__main__':
    main()
