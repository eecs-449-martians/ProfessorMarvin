from collections.abc import Iterable
from operator import truediv
import fitz
import re
from typing import Dict, List, Tuple
from collections import Counter 


def get_style_name(span,
            use_feats :bool = False,
            use_rgb   :bool = False,
            italic_feats:bool = False) -> str:
    """
    reads document, and counts the frequencies of different fonts 
    :param doc: the pdf document, read by pymupdf 
    :param use_feats: whether or not to consider bold/italic-ness of text 
    :param use_rgb: whether or not to consider the color of text 
    :param italic_feats: whether or not italic is considered a feature by use_feats. False by default. 
    :returns: 
    """
 
    name = f"{span['size']}_pt_{span['font'][:6]}"
    if use_feats: 
        if span['flags'] & (2**4): 
            name += "_BOLD"
        # if span['flags'] & (2**3):
        #     name += "_MONO"
        if italic_feats and span['flags'] & (2**1): 
            name += "_ITALIC"
    if use_rgb: 
        name += f"_rgb_{span['rgb']:#x}"
    return name

def get_font_size(fontname:str)->float : 
    """
    given a font-name generated by :func get_style_name:, returns the font size 
    :param fontname: the name of the font generated by `get_style_name`
    :returns: the size of the font, as a float 
    """
    # possible change, switch to int, for consiseness
    return float(fontname.split('_')[0])

def get_font_boldness(fontname:str)-> bool:
    """
    given a font-name generated by :func get_style_name:, returns if the font is bold 
    :param fontname: the name of the font generated by `get_style_name`
    :returns: whether the font is bold. 
            Note, if get_style_name had `use_feats`= False, this will always be False
    """
    return bool(re.match("\d\.\d.+(_BOLD)(_MONO)?(_ITALIC)?$",fontname))

    

def get_font_italic(fontname:str)->bool:
    """
    given a font-name generated by :func get_style_name:, returns if the font is bold 
    :param fontname: the name of the font generated by `get_style_name`
    :returns: whether the font is bold. 
            Note, if get_style_name had `use_feats` or `italic_feats` == False, this will always be False
    """
    return bool(re.match("\d\.\d.+(_BOLD)?(_MONO)?(_ITALIC)$",fontname))

def get_font_freqs(
            doc: fitz.Document,
            use_feats : bool = False,
            use_rgb   : bool = False,
            italic_feats: bool =False
            ) -> Counter:
    """
    reads document, and counts the frequencies of different fonts 
    :param doc: the pdf document, read by pymupdf 
    :param use_feats: whether or not to consider bold/italic-ness of text 
    :param use_rgb: whether or not to consider the color of text 
    :param italic_feats: whether or not italic is considered a feature by use_feats. False by default. 
    :returns: a Counter object (superset of dict) with the frequencies of each style
    """
    freqs = Counter()

    for page in doc:
        for block in page.get_text('dict')["blocks"]:
            # print(block)
            if block['type'] == 0:# only continue on text blocks
                # then look at  text spans 
                freqs.update(
                    get_style_name(span,use_feats=use_feats,use_rgb=use_rgb,italic_feats=italic_feats)
                    for line in block['lines'] 
                    for span in line['spans']
                    )
    return freqs

def tag_fonts(font_counts:Counter)->Dict[str,str]:
    """
    Creates header and footer tags for each font type 
    :param font_counts: a Counter object relating the frequencies of each font style 
            with each in the format used by `get_style_name`
    """
    freqs = font_counts.most_common()
    base_font = freqs[0]
    # define a custom comparator that prioritizes 
    def key(font):
        base_val = int(get_font_size(font[0])*10)
        if get_font_boldness(font[0]):
            base_val += 5
        if get_font_italic(font[0]): 
            base_val += 2 
        return base_val
    # now use it 

    # sort key low-to-high
    freqs.sort(key=key)

    size_tags = {}
    footer_offset = 0 
    for n,font in enumerate(freqs): 
        if font[0] == base_font[0]:           # paragraph text
            footer_offset = n
            size_tags[font[0]] = '<p>'
        elif key(base_font)< key(font): # header text 
            size_tags[font[0]] = f'<h{n}>'
        else:                           # sub-text
            size_tags[font[0]] = f'<s{n-footer_offset -1}>'
    return size_tags

def gather_texts(
        doc:fitz.Document, 
        imp_tag     :Dict[str,str], 
        use_feats   :bool = False,
        use_rgb     :bool = False,
        italic_feats:bool = False,
        combine_consc_blocks=True
            )->List[Tuple[str,str]]:
    """
    Grabs text and headers and footers from pdf document, and returns them together with tags 
    :param doc: document to be scraped
    :param imp_tag: a dictionay mapping text to 'importance' tag
    :param use_feats: whether or not to consider bold/italic-ness of text. 
        Should be the same value as used for `font_tags` 
    :param use_rgb: whether or not to consider the color of text 
        Should be the same value as used for `font_tags` 
    :param italic_feats: whether or not italic is considered a feature by use_feats. False by default. 
        Should be the same value as used for `font_tags` 

    :return: a list of (text chunk, importance tag) strings
    """
    doc_paras = []

    if combine_consc_blocks: #if we're combining irrespective of blocks, do that 
        last_style = None 
        sequence_text = []

    for page in doc: 
        for block in page.get_text('dict')['blocks']: 
            if block['type'] == 0: # if text block 
                # treat each block as a seperate paragraph 
                # then within blocks separate out by font type 
                # for now we will only use font size 
                if not combine_consc_blocks:
                    last_style = None 
                    last_
                    sequence_text = []
                spans = (span for line in block['lines'] for span in line['spans'] if span['text'].strip())
                for span in spans: 
                    # generate style name
                    style = get_style_name(span,use_feats=use_feats,use_rgb=use_rgb,italic_feats=italic_feats)
                    # if we have a new, style reset our running counter
                    if last_style is not None and last_style != style:
                        doc_paras.append((' '.join(sequence_text),imp_tag[last_style]))
                        last_style = style
                        sequence_text = []

                    if last_style is None:   # side case: first span in block
                        last_style = style
                    # invariant: style == last_style 
                    sequence_text.append(span['text'])
                # at end of block, add the last subsection to the paragraphs 
                if last_style is not None and not combine_consc_blocks:
                    doc_paras.append((' '.join(sequence_text),imp_tag[last_style]))
    # add the last block if we're combining blocks
    if last_style is not None and combine_consc_blocks: 
        doc_paras.append((' '.join(sequence_text),imp_tag[last_style]))

    return doc_paras


def segment_document(filepath,use_feats=False,use_rgb=False,italic_feats=False,combine_blocks=True): 
    # read document 
    document = fitz.open(filepath)
    # get different font sizes and types
    font_freqs = get_font_freqs(document,use_feats=use_feats,use_rgb=use_rgb,italic_feats=italic_feats)
    # create tags by feat 
    font_tags = tag_fonts(font_freqs)
    # then gather paragraphs 
    text_chunks = gather_texts(document,font_tags,use_feats,use_rgb,italic_feats,combine_blocks)
    
    # use a custom filter lambda that only takes text chunks that:
    #   1.  Have > 6 characters
    # And either 
    #   2.  Are normal text 
    # Or 
    #   3. Are one of the first 10 subscript sizes 

    filter_text = lambda text,tag: len(text) > 6 and (tag[:2] != "<s" or int(tag[2:-1]) <10)
    filtered = [text for text,tag in text_chunks if filter_text(text,tag)]
    return filtered


def test_func(): 
    print("hi there")
    print('this works! ')