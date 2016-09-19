""" The note class
        This class represents a single note(-file)

"""

import yaml
from collections import namedtuple

Note = namedtuple("Note", ["title", "tags", "content"])
Notebook = namedtuple("Notebook", ["title", "parent"])
def load_note(filename, only_metadata=False):
    result_title = ""
    result_tags = ""
    result_content = ""
    with open(filename, 'r') as file:
        if(file.readline() != "---\n"):
            raise NoteFileMalformedError("Doesn't start with metadata")

        metadata_block = ""
        content_block = ""
        reading_metadata = True

        for line in file:
            if(line == "---\n"):
                reading_metadata = False
                if only_metadata:
                    break
            else:
                if(reading_metadata):
                    metadata_block += line
                else:
                    content_block += line

        if len(metadata_block) is 0:
            raise NoteFileMalformedError("Reached EOF. Metadata block seems damaged")
        else:
            metadata = yaml.load(metadata_block)
            # Interpret TITLE
            try:
                result_title = metadata["title"]
            except KeyError as e:
                raise NoteFileMalformedError("Missing title in metadata")
            # Interpret TAGS
            if(len(metadata["tags"]) != 0):
                result_tags = metadata["tags"]
    if len(content_block) is not 0:
        result_content = content_block
    return Note(result_title, result_tags, result_content)

class NoteFileMalformedError(Exception):
    pass
