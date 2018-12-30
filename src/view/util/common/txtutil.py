
__all__ = [ 'IsUnicode', 'DecodeString']

#-----------------------------------------------------------------------------#
# Imports
import types

#-----------------------------------------------------------------------------#



def DecodeString(txt, enc):
    """Decode the given string with the given encoding,
    only attempts to decode if the given txt is not already Unicode
    @param txt: string
    @param enc: encoding 'utf-8'
    @return: unicode

    """
    return txt.decode(enc)
