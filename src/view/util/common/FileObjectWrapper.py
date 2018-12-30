
import wx, time
import re
import codecs
import locale

import logging.config
from src.view.constants import LOG_SETTINGS

from src.view.util.common.FileImpl import FileObjectBaseImpl
from src.view.util.common.FileChecker import FileTypeChecker
from _io import StringIO
import sys
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

#--------------------------------------------------------------------------#
# Globals

# The default fallback encoding
DEFAULT_ENCODING = locale.getpreferredencoding()
try:
    codecs.lookup(DEFAULT_ENCODING)
except (LookupError, TypeError):
    DEFAULT_ENCODING = 'utf-8'

# File Helper Functions
# NOTE: keep in synch with CheckBom function
BOM = { 'utf-8'  : codecs.BOM_UTF8,
        'utf-16' : codecs.BOM,
        'utf-32' : codecs.BOM_UTF32 }

# Regex for extracting magic comments from source files
# i.e *-* coding: utf-8 *-*, encoding=utf-8, ect...
# The first group from this expression will be the encoding.
RE_MAGIC_COMMENT = re.compile("coding[:=]\s*\"*([-\w.]+)\"*")

# File Load States
FL_STATE_START = 0
FL_STATE_READING = 1
FL_STATE_PAUSED = 2
FL_STATE_END = 3
FL_STATE_ABORTED = 4

#--------------------------------------------------------------------------#


class ReadError(Exception):
    """Error happened while trying to read the file"""
    pass


class WriteError(Exception):
    """Error happened while trying to write the file"""
    pass


#--------------------------------------------------------------------------#
class FileObject(FileObjectBaseImpl):
    """Wrapper for representing a file object that stores data
    about the file encoding and path.

    """
    _Checker = FileTypeChecker()
    
    def __init__(self, path=u'', modtime=0):
        """Create the file wrapper object
        @keyword path: the absolute path to the file
        @keyword modtime: file modification time

        """
        super().__init__(path, modtime)

        # Attributes
        self._magic = dict(comment=None, bad=False)
        self.encoding = None
        self.bom = None
        self._mcallback = list()
        self.__buffer = None
        self._raw = False  # Raw bytes?
        self._fuzzy_enc = False
        self._job = None  # async file read job
        
    def _SanitizeBOM(self, bstring):
        """Remove byte order marks that get automatically added by some codecs"""
        for enc in ('utf-8', 'utf-32', 'utf-16'):
            bmark = BOM.get(enc)
            if bstring.startswith(bmark):
                bstring = bstring.lstrip(bmark)
                break
        return bstring

    def _HandleRawBytes(self, bytes_value):
        """Handle prepping raw bytes for return to the buffer
        @param bytes_value: raw read bytes
        @return: string

        """
        logger.debug("[ed_txt][info] HandleRawBytes called")
        if self._magic['comment']:
            self._magic['bad'] = True
        # Return the raw bytes to put into the buffer
        self._raw = True
        return '\0'.join(bytes_value) + '\0'

    def _ResetBuffer(self):
        logger.debug("[ed_txt][info] Resetting buffer")
        if self.__buffer is not None:
            self.__buffer.close()
            del self.__buffer
        self.__buffer = StringIO()

#-----------------------------------------------------------------------------#

class FileReadJob(object):
    """Job for running an async file read in a background thread"""
    def __init__(self, receiver, task, *args, **kwargs):
        """Create the thread
        @param receiver: Window to receive events
        @param task: generator method to call
        @param *args: positional arguments to pass to task
        @param **kwargs: keyword arguments to pass to task

        """
        super(FileReadJob, self).__init__()

        # Attributes
        self.cancel = False
        self._task = task
        self.receiver = receiver
        self._args = args
        self._kwargs = kwargs
        self.pid = receiver.TopLevelParent.Id

    def run(self):
        """Read the text"""
        evt = FileLoadEvent(edEVT_FILE_LOAD, wx.ID_ANY, None, FL_STATE_START)
        wx.PostEvent(self.receiver, evt)
        time.sleep(.75) # give ui a chance to get ready

        count = 1
        for txt in self._task(*self._args, **self._kwargs):
            if self.cancel:
                break

            evt = FileLoadEvent(edEVT_FILE_LOAD, wx.ID_ANY, txt)
            evt.SetProgress(count * self._args[0])
            wx.PostEvent(self.receiver, evt)
            count += 1

        evt = FileLoadEvent(edEVT_FILE_LOAD, wx.ID_ANY, None, FL_STATE_END)
        wx.PostEvent(self.receiver, evt)

    def Cancel(self):
        """Cancel the running task"""
        self.cancel = True

#-----------------------------------------------------------------------------#

edEVT_FILE_LOAD = wx.NewEventType()
EVT_FILE_LOAD = wx.PyEventBinder(edEVT_FILE_LOAD, 1)
class FileLoadEvent(wx.PyEvent):
    """Event to signal that a chunk of text haes been read"""
    def __init__(self, etype, eid, value=None, state=FL_STATE_READING):
        """Creates the event object"""
        super(FileLoadEvent, self).__init__(eid, etype)

        # Attributes
        self._state = state
        self._value = value
        self._prog = 0
    
    def HasText(self):
        """Returns true if the event has text
        @return: bool whether the event contains text

        """
        return self._value is not None

    def GetProgress(self):
        """Get the current progress of the load"""
        return self._prog

    def GetState(self):
        """Get the state of the file load action
        @return: int (FL_STATE_FOO)

        """
        return self._state

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value

    def SetProgress(self, progress):
        """Set the number of bytes that have been read
        @param progress: int

        """
        self._prog = progress

#-----------------------------------------------------------------------------#
# Utility Function
def CheckBom(line):
    """Try to look for a bom byte at the beginning of the given line
    @param line: line (first line) of a file
    @return: encoding or None

    """
    logger.debug("[ed_txt][info] CheckBom called")
    has_bom = None
    # NOTE: MUST check UTF-32 BEFORE utf-16
    for enc in ('utf-8', 'utf-32', 'utf-16'):
        bom = BOM[enc]
        if line.startswith(bom):
            has_bom = enc
            break
    return has_bom

def CheckMagicComment(lines):
    """Try to decode the given text on the basis of a magic
    comment if one is present.
    @param lines: list of lines to check for a magic comment
    @return: encoding or None

    """
    logger.debug("[ed_txt][info] CheckMagicComment: %s" % str(lines))
    enc = None
    for line in lines:
        match = RE_MAGIC_COMMENT.search(line)
        if match:
            enc = match.group(1)
            try:
                codecs.lookup(enc)
            except LookupError:
                enc = None
            break

    logger.debug("[ed_txt][info] MagicComment is %s" % enc)
    return enc

def DecodeString(string, encoding=None):
    """Decode the given string to Unicode using the provided
    encoding or the DEFAULT_ENCODING if None is provided.
    @param string: string to decode
    @keyword encoding: encoding to decode string with

    """
    if encoding is None:
        encoding = DEFAULT_ENCODING

    try:
        rtxt = string.decode(encoding)
    except Exception as msg:
        logger.debug("[ed_txt][err] DecodeString with %s failed" % encoding)
        logger.debug("[ed_txt][err] %s" % msg)
        rtxt = string
    return rtxt


def EncodeString(string, encoding=None):
    """Try and encode a given unicode object to a string
    with the provided encoding returning that string. The
    default encoding will be used if None is given for the
    encoding.
    @param string: unicode object to encode into a string
    @keyword encoding: encoding to use for conversion

    """
    if not encoding:
        encoding = DEFAULT_ENCODING

    try:
        rtxt = string.encode(encoding)
    except LookupError:
        rtxt = string
    return rtxt


def FallbackReader(fname):
    """Guess the encoding of a file by brute force by trying one
    encoding after the next until something succeeds.
    @param fname: file path to read from
    @todo: deprecate this method

    """
    txt = None
    with open(fname, 'rb') as handle:
        byte_str = handle.read()
        for enc in GetEncodings():
            try:
                txt = byte_str.decode(enc)
            except Exception as msg:
                continue
            else:
                return (enc, txt)

    return (None, None)

def GuessEncoding(fname, sample):
    """Attempt to guess an encoding
    @param fname: filename
    @param sample: pre-read amount
    @return: encoding or None

    """
    for enc in GetEncodings():
        try:
            with open(fname, 'rb') as handle:
                with codecs.getreader(enc)(handle) as reader:
                    value = reader.read(sample)
                    if str('\0') in value:
                        continue
                    else:
                        return enc
        except Exception as msg:
            continue
    return None

def GetEncodings():
    """Get a list of possible encodings to try from the locale information
    @return: list of strings

    """
    encodings = list()
#     encodings.append(Profile_Get('ENCODING', None))

    try:
        encodings.append(locale.getpreferredencoding())
    except:
        pass
    
    encodings.append('utf-8')

#     try:
#         if hasattr(locale, 'nl_langinfo'):
#             encodings.append(locale.nl_langinfo(locale.CODESET))
#     except:
#         pass
    try:
        encodings.append(locale.getlocale()[1])
    except:
        pass
    try:
        encodings.append(locale.getdefaultlocale()[1])
    except:
        pass
    encodings.append(sys.getfilesystemencoding())
    encodings.append('utf-16')
    encodings.append('utf-16-le') # for files without BOM...
    encodings.append('latin-1')

    # Normalize all names
    normlist = [ encodings.normalize_encoding(enc) for enc in encodings if enc]

    # Clean the list for duplicates and None values
    rlist = list()
    codec_list = list()
    for enc in normlist:
        if enc is not None and len(enc):
            enc = enc.lower()
            if enc not in rlist:
                # Ascii is useless so ignore it (ascii, us_ascii, ...)
                if 'ascii' in enc:
                    continue

                try:
                    ctmp = codecs.lookup(enc)
                    if ctmp.name not in codec_list:
                        codec_list.append(ctmp.name)
                        rlist.append(enc)
                except LookupError:
                    pass
    return rlist
