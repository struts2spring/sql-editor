import codecs




def GetFileReader(file_name, enc='utf-8'):
    """Returns a file stream reader object for reading the
    supplied file name. It returns a file reader using the encoding
    (enc) which defaults to utf-8. If lookup of the reader fails on
    the host system it will return an ascii reader.
    If there is an error in creating the file reader the function
    will return a negative number.
    @param file_name: name of file to get a reader for
    @keyword enc: encoding to use for reading the file
    @return file reader, or int if error.

    """
    try:
        file_h = open(file_name, "rb")
    except (IOError, OSError):
#         dev_tool.DEBUGP("[file_reader] Failed to open file %s" % file_name)
        return -1

    try:
        reader = codecs.getreader(enc)(file_h)
    except (LookupError, IndexError, ValueError):
#         dev_tool.DEBUGP('[file_reader] Failed to get %s Reader' % enc)
        reader = file_h
    return reader

def GetFileWriter(file_name, enc='utf-8'):
    """Returns a file stream writer object for reading the
    supplied file name. It returns a file writer in the supplied
    encoding if the host system supports it other wise it will return
    an ascii reader. The default will try and return a utf-8 reader.
    If there is an error in creating the file reader the function
    will return a negative number.
    @param file_name: path of file to get writer for
    @keyword enc: encoding to write text to file with

    """
    try:
        file_h = open(file_name, "wb")
    except IOError:
#         dev_tool.DEBUGP("[file_writer][err] Failed to open file %s" % file_name)
        return -1
    try:
        writer = codecs.getwriter(enc)(file_h)
    except (LookupError, IndexError, ValueError):
#         dev_tool.DEBUGP('[file_writer][err] Failed to get %s Writer' % enc)
        writer = file_h
    return writer

