# Imports
import os

#-----------------------------------------------------------------------------#


class FileTypeChecker(object):
    """File type checker and recognizer"""
    TXTCHARS = ''.join(map(chr, [7, 8, 9, 10, 12, 13, 27] + [i for i in range(32,255 ) ]))
    ALLBYTES = ''.join(map(chr,  [i for i in range(256)]))

    def __init__(self, preread=4096):
        """Create the FileTypeChecker
        @keyword preread: number of bytes to read for checking file type

        """
        super().__init__()

        # Attributes
        self._preread = preread

    @staticmethod
    def _GetHandle(fname):
        """Get a file handle for reading
        @param fname: filename
        @return: file object or None

        """
        try:
            handle = open(fname, 'rb')
        except:
            handle = None
        return handle

    def IsBinary(self, fname):
        """Is the file made up of binary data
        @param fname: filename to check
        @return: bool

        """
        handle = self._GetHandle(fname)
        if handle is not None:
            bytesData = handle.read(self._preread)
            handle.close()
            return self.IsBinaryBytes(bytesData)
        else:
            return False

    def IsBinaryBytes(self, bytesData):
        """Check if the given string is composed of binary bytes
        @param bytesData: string

        """
        nontext = bytesData.translate(FileTypeChecker.ALLBYTES,
                                  FileTypeChecker.TXTCHARS)
        return bool(nontext)

    def IsReadableText(self, fname):
        """Is the given path readable as text. Will return True if the
        file is accessable by current user and is plain text.
        @param fname: filename
        @return: bool

        """
        f_ok = False
        if os.access(fname, os.R_OK):
            f_ok = not self.IsBinary(fname)
        return f_ok
