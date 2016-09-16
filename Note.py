""" The note class

	This class represents a single note(-file)
    
"""

import yaml

class Note:
    title = ""
    notebook = ""
    tags = []
    content = ""

    def __init__(self):
        pass

    def __str__(self):
        return self.notebook + ": " + self.title + self.content[:10]

    @staticmethod
    def load(filename):
        result = Note()

        with open(filename, 'r') as file:
            if(file.readline() != "---\n"):
                raise NoteFileMalformedError("Doesn't start with metadata")
            
            metadata_block = ""
            content_block = ""
            reading_metadata = True
            
            for line in file:
                if(line == "---\n"):
                    reading_metadata = False
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
                    result.title = metadata["title"]
                except KeyError as e:
                    raise NoteFileMalformedError("Missing title in metadata")

                # Interpret NOTEBOOK
                try:
                    result.notebook = metadata["notebook"]
                except KeyError as e:
                    raise NoteFileMalformedError("Missing notebook in metadata")

                # Interpret TAGS
                if(len(metadata["tags"]) != 0):
                    result.tags = metadata["tags"].split(" ")
            if len(content_block) is not 0:
                result.content = content_block
        return result

class NoteFileMalformedError(Exception):
    pass
