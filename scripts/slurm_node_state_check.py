#!/usr/bin/env python3
# Created: 2023-03-20 20:04
# Copyright (C) 2022-now, RPL, KTH Royal Institute of Technology
# Author: Qingwen Zhang  (https://kin-zhang.github.io/)

# Test only on our rplgpu cluster, may not work on other clusters.
# run: `curl -s https://raw.githubusercontent.com/Kin-Zhang/Kin-Zhang/main/scripts/slurm_node_state_check.py | python3 -`

# NOTE: part of code is from tabulate!!!
# Please check their origin: https://github.com/gregbanks/python-tabulate
# from tabulate import tabulate
# since we don't want to install anything, so I copy the tabulate here:

# -*- coding: utf-8 -*-

"""==================> Pretty-print tabular data."""
from __future__ import print_function
from __future__ import unicode_literals
from collections import namedtuple
import re

DataRow = namedtuple("DataRow", ["begin", "sep", "end"])
Line = namedtuple("Line", ["begin", "hline", "sep", "end"])
TableFormat = namedtuple("TableFormat", ["lineabove", "linebelowheader",
                                         "linebetweenrows", "linebelow",
                                         "headerrow", "datarow",
                                         "padding", "with_header_hide"])

from itertools import zip_longest as izip_longest
from functools import reduce, partial
_none_type = type(None)
_int_type = int
_float_type = float
_text_type = str
_binary_type = bytes

def _pipe_segment_with_colons(align, colwidth):
    """Return a segment of a horizontal line with optional colons which
    indicate column's alignment (as in `pipe` output format)."""
    w = colwidth
    if align in ["right", "decimal"]:
        return ('-' * (w - 1)) + ":"
    elif align == "center":
        return ":" + ('-' * (w - 2)) + ":"
    elif align == "left":
        return ":" + ('-' * (w - 1))
    else:
        return '-' * w


def _pipe_line_with_colons(colwidths, colaligns):
    """Return a horizontal line with optional colons to indicate column's
    alignment (as in `pipe` output format)."""
    segments = [_pipe_segment_with_colons(a, w) for a, w in zip(colaligns, colwidths)]
    return "|" + "|".join(segments) + "|"


def _mediawiki_row_with_attrs(separator, cell_values, colwidths, colaligns):
    alignment = { "left":    '',
                  "right":   'align="right"| ',
                  "center":  'align="center"| ',
                  "decimal": 'align="right"| ' }
    # hard-coded padding _around_ align attribute and value together
    # rather than padding parameter which affects only the value
    values_with_attrs = [' ' + alignment.get(a, '') + c + ' '
                         for c, a in zip(cell_values, colaligns)]
    colsep = separator*2
    return (separator + colsep.join(values_with_attrs)).rstrip()


def _latex_line_begin_tabular(colwidths, colaligns):
    alignment = { "left": "l", "right": "r", "center": "c", "decimal": "r" }
    tabular_columns_fmt = "".join([alignment.get(a, "l") for a in colaligns])
    return "\\begin{tabular}{" + tabular_columns_fmt + "}\n\hline"


_table_formats = {"simple":
                  TableFormat(lineabove=Line("", "-", "  ", ""),
                              linebelowheader=Line("", "-", "  ", ""),
                              linebetweenrows=None,
                              linebelow=Line("", "-", "  ", ""),
                              headerrow=DataRow("", "  ", ""),
                              datarow=DataRow("", "  ", ""),
                              padding=0,
                              with_header_hide=["lineabove", "linebelow"]),
                  "plain":
                  TableFormat(lineabove=None, linebelowheader=None,
                              linebetweenrows=None, linebelow=None,
                              headerrow=DataRow("", "  ", ""),
                              datarow=DataRow("", "  ", ""),
                              padding=0, with_header_hide=None),
                  "grid":
                  TableFormat(lineabove=Line("+", "-", "+", "+"),
                              linebelowheader=Line("+", "=", "+", "+"),
                              linebetweenrows=Line("+", "-", "+", "+"),
                              linebelow=Line("+", "-", "+", "+"),
                              headerrow=DataRow("|", "|", "|"),
                              datarow=DataRow("|", "|", "|"),
                              padding=1, with_header_hide=None),
                  "pipe":
                  TableFormat(lineabove=_pipe_line_with_colons,
                              linebelowheader=_pipe_line_with_colons,
                              linebetweenrows=None,
                              linebelow=None,
                              headerrow=DataRow("|", "|", "|"),
                              datarow=DataRow("|", "|", "|"),
                              padding=1,
                              with_header_hide=["lineabove"]),
                  "orgtbl":
                  TableFormat(lineabove=None,
                              linebelowheader=Line("|", "-", "+", "|"),
                              linebetweenrows=None,
                              linebelow=None,
                              headerrow=DataRow("|", "|", "|"),
                              datarow=DataRow("|", "|", "|"),
                              padding=1, with_header_hide=None),
                  "rst":
                  TableFormat(lineabove=Line("", "=", "  ", ""),
                              linebelowheader=Line("", "=", "  ", ""),
                              linebetweenrows=None,
                              linebelow=Line("", "=", "  ", ""),
                              headerrow=DataRow("", "  ", ""),
                              datarow=DataRow("", "  ", ""),
                              padding=0, with_header_hide=None),
                  "mediawiki":
                  TableFormat(lineabove=Line("{| class=\"wikitable\" style=\"text-align: left;\"",
                                             "", "", "\n|+ <!-- caption -->\n|-"),
                              linebelowheader=Line("|-", "", "", ""),
                              linebetweenrows=Line("|-", "", "", ""),
                              linebelow=Line("|}", "", "", ""),
                              headerrow=partial(_mediawiki_row_with_attrs, "!"),
                              datarow=partial(_mediawiki_row_with_attrs, "|"),
                              padding=0, with_header_hide=None),
                  "latex":
                  TableFormat(lineabove=_latex_line_begin_tabular,
                              linebelowheader=Line("\\hline", "", "", ""),
                              linebetweenrows=None,
                              linebelow=Line("\\hline\n\\end{tabular}", "", "", ""),
                              headerrow=DataRow("", "&", "\\\\"),
                              datarow=DataRow("", "&", "\\\\"),
                              padding=1, with_header_hide=None),
                  "tsv":
                  TableFormat(lineabove=None, linebelowheader=None,
                              linebetweenrows=None, linebelow=None,
                              headerrow=DataRow("", "\t", ""),
                              datarow=DataRow("", "\t", ""),
                              padding=0, with_header_hide=None)}


tabulate_formats = list(sorted(_table_formats.keys()))


_invisible_codes = re.compile("\x1b\[\d*m")  # ANSI color codes
_invisible_codes_bytes = re.compile(b"\x1b\[\d*m")  # ANSI color codes


def simple_separated_format(separator):
    """Construct a simple TableFormat with columns separated by a separator.
    >>> tsv = simple_separated_format("\\t") ; \
        tabulate([["foo", 1], ["spam", 23]], tablefmt=tsv) == 'foo \\t 1\\nspam\\t23'
    True
    """
    return TableFormat(None, None, None, None,
                       headerrow=DataRow('', separator, ''),
                       datarow=DataRow('', separator, ''),
                       padding=0, with_header_hide=None)


def _isconvertible(conv, string):
    try:
        n = conv(string)
        return True
    except ValueError:
        return False


def _isnumber(string):
    """
    >>> _isnumber("123.45")
    True
    >>> _isnumber("123")
    True
    >>> _isnumber("spam")
    False
    """
    return _isconvertible(float, string)


def _isint(string):
    """
    >>> _isint("123")
    True
    >>> _isint("123.45")
    False
    """
    return type(string) is int or \
           (isinstance(string, _binary_type) or isinstance(string, _text_type)) and \
           _isconvertible(int, string)


def _type(string, has_invisible=True):
    """The least generic type (type(None), int, float, str, unicode).
    >>> _type(None) is type(None)
    True
    >>> _type("foo") is type("")
    True
    >>> _type("1") is type(1)
    True
    >>> _type('\x1b[31m42\x1b[0m') is type(42)
    True
    >>> _type('\x1b[31m42\x1b[0m') is type(42)
    True
    """

    if has_invisible and \
       (isinstance(string, _text_type) or isinstance(string, _binary_type)):
        string = _strip_invisible(string)

    if string is None:
        return _none_type
    elif hasattr(string, "isoformat"):  # datetime.datetime, date, and time
        return _text_type
    elif _isint(string):
        return int
    elif _isnumber(string):
        return float
    elif isinstance(string, _binary_type):
        return _binary_type
    else:
        return _text_type


def _afterpoint(string):
    """Symbols after a decimal point, -1 if the string lacks the decimal point.
    >>> _afterpoint("123.45")
    2
    >>> _afterpoint("1001")
    -1
    >>> _afterpoint("eggs")
    -1
    >>> _afterpoint("123e45")
    2
    """
    if _isnumber(string):
        if _isint(string):
            return -1
        else:
            pos = string.rfind(".")
            pos = string.lower().rfind("e") if pos < 0 else pos
            if pos >= 0:
                return len(string) - pos - 1
            else:
                return -1  # no point
    else:
        return -1  # not a number


def _padleft(width, s, has_invisible=True):
    """Flush right.
    >>> _padleft(6, '\u044f\u0439\u0446\u0430') == '  \u044f\u0439\u0446\u0430'
    True
    """
    iwidth = width + len(s) - len(_strip_invisible(s)) if has_invisible else width
    fmt = "{0:>%ds}" % iwidth
    return fmt.format(s)


def _padright(width, s, has_invisible=True):
    """Flush left.
    >>> _padright(6, '\u044f\u0439\u0446\u0430') == '\u044f\u0439\u0446\u0430  '
    True
    """
    iwidth = width + len(s) - len(_strip_invisible(s)) if has_invisible else width
    fmt = "{0:<%ds}" % iwidth
    return fmt.format(s)


def _padboth(width, s, has_invisible=True):
    """Center string.
    >>> _padboth(6, '\u044f\u0439\u0446\u0430') == ' \u044f\u0439\u0446\u0430 '
    True
    """
    iwidth = width + len(s) - len(_strip_invisible(s)) if has_invisible else width
    fmt = "{0:^%ds}" % iwidth
    return fmt.format(s)


def _strip_invisible(s):
    "Remove invisible ANSI color codes."
    if isinstance(s, _text_type):
        return re.sub(_invisible_codes, "", s)
    else:  # a bytestring
        return re.sub(_invisible_codes_bytes, "", s)


def _visible_width(s):
    """Visible width of a printed string. ANSI color codes are removed.
    >>> _visible_width('\x1b[31mhello\x1b[0m'), _visible_width("world")
    (5, 5)
    """
    if isinstance(s, _text_type) or isinstance(s, _binary_type):
        return len(_strip_invisible(s))
    else:
        return len(_text_type(s))


def _align_column(strings, alignment, minwidth=0, has_invisible=True):
    """[string] -> [padded_string]
    >>> list(map(str,_align_column(["12.345", "-1234.5", "1.23", "1234.5", "1e+234", "1.0e234"], "decimal")))
    ['   12.345  ', '-1234.5    ', '    1.23   ', ' 1234.5    ', '    1e+234 ', '    1.0e234']
    >>> list(map(str,_align_column(['123.4', '56.7890'], None)))
    ['123.4', '56.7890']
    """
    if alignment == "right":
        strings = [s.strip() for s in strings]
        padfn = _padleft
    elif alignment == "center":
        strings = [s.strip() for s in strings]
        padfn = _padboth
    elif alignment == "decimal":
        decimals = [_afterpoint(s) for s in strings]
        maxdecimals = max(decimals)
        strings = [s + (maxdecimals - decs) * " "
                   for s, decs in zip(strings, decimals)]
        padfn = _padleft
    elif not alignment:
        return strings
    else:
        strings = [s.strip() for s in strings]
        padfn = _padright

    if has_invisible:
        width_fn = _visible_width
    else:
        width_fn = len

    maxwidth = max(max(map(width_fn, strings)), minwidth)
    padded_strings = [padfn(maxwidth, s, has_invisible) for s in strings]
    return padded_strings


def _more_generic(type1, type2):
    types = { _none_type: 0, int: 1, float: 2, _binary_type: 3, _text_type: 4 }
    invtypes = { 4: _text_type, 3: _binary_type, 2: float, 1: int, 0: _none_type }
    moregeneric = max(types.get(type1, 4), types.get(type2, 4))
    return invtypes[moregeneric]


def _column_type(strings, has_invisible=True):
    """The least generic type all column values are convertible to.
    >>> _column_type(["1", "2"]) is _int_type
    True
    >>> _column_type(["1", "2.3"]) is _float_type
    True
    >>> _column_type(["1", "2.3", "four"]) is _text_type
    True
    >>> _column_type(["four", '\u043f\u044f\u0442\u044c']) is _text_type
    True
    >>> _column_type([None, "brux"]) is _text_type
    True
    >>> _column_type([1, 2, None]) is _int_type
    True
    >>> import datetime as dt
    >>> _column_type([dt.datetime(1991,2,19), dt.time(17,35)]) is _text_type
    True
    """
    types = [_type(s, has_invisible) for s in strings ]
    return reduce(_more_generic, types, int)


def _format(val, valtype, floatfmt, missingval=""):
    """Format a value accoding to its type.
    Unicode is supported:
    >>> hrow = ['\u0431\u0443\u043a\u0432\u0430', '\u0446\u0438\u0444\u0440\u0430'] ; \
        tbl = [['\u0430\u0437', 2], ['\u0431\u0443\u043a\u0438', 4]] ; \
        good_result = '\\u0431\\u0443\\u043a\\u0432\\u0430      \\u0446\\u0438\\u0444\\u0440\\u0430\\n-------  -------\\n\\u0430\\u0437             2\\n\\u0431\\u0443\\u043a\\u0438           4' ; \
        tabulate(tbl, headers=hrow) == good_result
    True
    """
    if val is None:
        return missingval

    if valtype in [int, _text_type]:
        return "{0}".format(val)
    elif valtype is _binary_type:
        try:
            return _text_type(val, "ascii")
        except TypeError:
            return _text_type(val)
    elif valtype is float:
        return format(float(val), floatfmt)
    else:
        return "{0}".format(val)


def _align_header(header, alignment, width):
    if alignment == "left":
        return _padright(width, header)
    elif alignment == "center":
        return _padboth(width, header)
    elif not alignment:
        return "{0}".format(header)
    else:
        return _padleft(width, header)


def _normalize_tabular_data(tabular_data, headers):

    if hasattr(tabular_data, "keys") and hasattr(tabular_data, "values"):
        # dict-like and pandas.DataFrame?
        if hasattr(tabular_data.values, "__call__"):
            # likely a conventional dict
            keys = tabular_data.keys()
            rows = list(izip_longest(*tabular_data.values()))  # columns have to be transposed
        elif hasattr(tabular_data, "index"):
            # values is a property, has .index => it's likely a pandas.DataFrame (pandas 0.11.0)
            keys = tabular_data.keys()
            vals = tabular_data.values  # values matrix doesn't need to be transposed
            names = tabular_data.index
            rows = [[v]+list(row) for v,row in zip(names, vals)]
        else:
            raise ValueError("tabular data doesn't appear to be a dict or a DataFrame")

        if headers == "keys":
            headers = list(map(_text_type,keys))  # headers should be strings

    else:  # it's a usual an iterable of iterables, or a NumPy array
        rows = list(tabular_data)

        if (headers == "keys" and
            hasattr(tabular_data, "dtype") and
            getattr(tabular_data.dtype, "names")):
            # numpy record array
            headers = tabular_data.dtype.names
        elif (headers == "keys"
              and len(rows) > 0
              and isinstance(rows[0], tuple)
              and hasattr(rows[0], "_fields")):
            # namedtuple
            headers = list(map(_text_type, rows[0]._fields))
        elif (len(rows) > 0
              and isinstance(rows[0], dict)):
            # dict or OrderedDict
            uniq_keys = set() # implements hashed lookup
            keys = [] # storage for set
            if headers == "firstrow":
                firstdict = rows[0] if len(rows) > 0 else {}
                keys.extend(firstdict.keys())
                uniq_keys.update(keys)
                rows = rows[1:]
            for row in rows:
                for k in row.keys():
                    #Save unique items in input order
                    if k not in uniq_keys:
                        keys.append(k)
                        uniq_keys.add(k)
            if headers == 'keys':
                headers = keys
            elif headers == "firstrow" and len(rows) > 0:
                headers = [firstdict.get(k, k) for k in keys]
                headers = list(map(_text_type, headers))
            rows = [[row.get(k) for k in keys] for row in rows]
        elif headers == "keys" and len(rows) > 0:
            # keys are column indices
            headers = list(map(_text_type, range(len(rows[0]))))

    # take headers from the first row if necessary
    if headers == "firstrow" and len(rows) > 0:
        headers = list(map(_text_type, rows[0])) # headers should be strings
        rows = rows[1:]

    headers = list(map(_text_type,headers))
    rows = list(map(list,rows))

    # pad with empty headers for initial columns if necessary
    if headers and len(rows) > 0:
       nhs = len(headers)
       ncols = len(rows[0])
       if nhs < ncols:
           headers = [""]*(ncols - nhs) + headers

    return rows, headers


def tabulate(tabular_data, headers=[], tablefmt="simple",
             floatfmt="g", numalign="decimal", stralign="left",
             missingval=""):
    list_of_lists, headers = _normalize_tabular_data(tabular_data, headers)

    # optimization: look for ANSI control codes once,
    # enable smart width functions only if a control code is found
    plain_text = '\n'.join(['\t'.join(map(_text_type, headers))] + \
                            ['\t'.join(map(_text_type, row)) for row in list_of_lists])
    has_invisible = re.search(_invisible_codes, plain_text)
    if has_invisible:
        width_fn = _visible_width
    else:
        width_fn = len

    # format rows and columns, convert numeric values to strings
    cols = list(zip(*list_of_lists))
    coltypes = list(map(_column_type, cols))
    cols = [[_format(v, ct, floatfmt, missingval) for v in c]
             for c,ct in zip(cols, coltypes)]

    # align columns
    aligns = [numalign if ct in [int,float] else stralign for ct in coltypes]
    minwidths = [width_fn(h)+2 for h in headers] if headers else [0]*len(cols)
    cols = [_align_column(c, a, minw, has_invisible)
            for c, a, minw in zip(cols, aligns, minwidths)]

    if headers:
        # align headers and add headers
        minwidths = [max(minw, width_fn(c[0])) for minw, c in zip(minwidths, cols)]
        headers = [_align_header(h, a, minw)
                   for h, a, minw in zip(headers, aligns, minwidths)]
        rows = list(zip(*cols))
    else:
        minwidths = [width_fn(c[0]) for c in cols]
        rows = list(zip(*cols))

    if not isinstance(tablefmt, TableFormat):
        tablefmt = _table_formats.get(tablefmt, _table_formats["simple"])

    return _format_table(tablefmt, headers, rows, minwidths, aligns)


def _build_simple_row(padded_cells, rowfmt):
    "Format row according to DataRow format without padding."
    begin, sep, end = rowfmt
    return (begin + sep.join(padded_cells) + end).rstrip()


def _build_row(padded_cells, colwidths, colaligns, rowfmt):
    "Return a string which represents a row of data cells."
    if not rowfmt:
        return None
    if hasattr(rowfmt, "__call__"):
        return rowfmt(padded_cells, colwidths, colaligns)
    else:
        return _build_simple_row(padded_cells, rowfmt)


def _build_line(colwidths, colaligns, linefmt):
    "Return a string which represents a horizontal line."
    if not linefmt:
        return None
    if hasattr(linefmt, "__call__"):
        return linefmt(colwidths, colaligns)
    else:
        begin, fill, sep,  end = linefmt
        cells = [fill*w for w in colwidths]
        return _build_simple_row(cells, (begin, sep, end))


def _pad_row(cells, padding):
    if cells:
        pad = " "*padding
        padded_cells = [pad + cell + pad for cell in cells]
        return padded_cells
    else:
        return cells


def _format_table(fmt, headers, rows, colwidths, colaligns):
    """Produce a plain-text representation of the table."""
    lines = []
    hidden = fmt.with_header_hide if (headers and fmt.with_header_hide) else []
    pad = fmt.padding
    headerrow = fmt.headerrow

    padded_widths = [(w + 2*pad) for w in colwidths]
    padded_headers = _pad_row(headers, pad)
    padded_rows = [_pad_row(row, pad) for row in rows]

    if fmt.lineabove and "lineabove" not in hidden:
        lines.append(_build_line(padded_widths, colaligns, fmt.lineabove))

    if padded_headers:
        lines.append(_build_row(padded_headers, padded_widths, colaligns, headerrow))
        if fmt.linebelowheader and "linebelowheader" not in hidden:
            lines.append(_build_line(padded_widths, colaligns, fmt.linebelowheader))

    if padded_rows and fmt.linebetweenrows and "linebetweenrows" not in hidden:
        # initial rows with a line below
        for row in padded_rows[:-1]:
            lines.append(_build_row(row, padded_widths, colaligns, fmt.datarow))
            lines.append(_build_line(padded_widths, colaligns, fmt.linebetweenrows))
        # the last row without a line below
        lines.append(_build_row(padded_rows[-1], padded_widths, colaligns, fmt.datarow))
    else:
        for row in padded_rows:
            lines.append(_build_row(row, padded_widths, colaligns, fmt.datarow))

    if fmt.linebelow and "linebelow" not in hidden:
        lines.append(_build_line(padded_widths, colaligns, fmt.linebelow))

    return "\n".join(lines)

"""==================> Pretty-print tabular data."""

import subprocess, argparse

def parse_cmd(cmd, split=True):
    """Parse the output of a shell command...
     and if split set to true: split into a list of strings, one per line of output.

    Args:
        cmd (str): the shell command to be executed.
        split (bool): whether to split the output per line
    Returns:
        (list[str]): the strings from each output line.
    """
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
    if split:
        output = [x for x in output.split("\n") if x]
    return output

def node_info(filetxt=None):
    # node info running this command: sinfo -o '%N|%G|%m|%C' --noheader -N
    if filetxt:
        output = open(filetxt, 'r').read()
        output_cmd = [x for x in output.split("\n") if x]
    else:
        output_cmd = parse_cmd("sinfo -o '%N|%G|%m|%C|%t' --noheader -N")

    # key: node_name, value: [gpu_type, gpu_num, RAM_total, CPU_total, state]
    node_infos = dict()
    for row in output_cmd:
        lists_as = row.split('|')
        node_name = lists_as[0]

        gpu_type = lists_as[1].split(':')[1]
        gpu_num = int(lists_as[1].split(':')[2].split('(')[0])
        
        RAM_total = int(int(lists_as[2])/1000)
        CPU_total = int(lists_as[3].split('/')[-1])

        if lists_as[4] not in ['mix', 'idle', 'alloc']:
            continue
        node_infos[node_name] = [gpu_type, gpu_num, RAM_total, CPU_total, lists_as[4]]
    return node_infos

def node_usage(node_infos, filetxt=None, alloc_nodes=False):
    raw_nodeinfos = node_infos.copy()
    # node usage running this command: squeue -o "%N|%b|%m|%C" --noheader
    # %i for job id, %u for user, %b for gpu type, %N for node name
    if filetxt:
        output = open(filetxt, 'r').read()
        output_cmd = [x for x in output.split("\n") if x]
    else:
        output_cmd = parse_cmd("squeue -o '%N|%b|%m|%C' --noheader")
    
    # node_name, gpu_type, gpu_AT, cpu_AT, ram_AT
    final = []
    
    for row in output_cmd:
        used_resourced = row.split('|')
        node_name = used_resourced[0]

        if node_name not in node_infos.keys():
            continue
        used_gpu_num = used_resourced[1]
        if used_gpu_num == '(null)':
            used_gpu_num = 0
        else:
            used_gpu_num = int(used_resourced[1].split(':')[-1])

        # compute the RAM usage
        if 'G' in used_resourced[2]:
            used_ram = int(used_resourced[2].split('G')[0].split('.')[0])
        elif 'M' in used_resourced[2]:
            used_ram = int(used_resourced[2].split('M')[0].split('.')[0])/1000
        
        used_cpucore = int(used_resourced[3])
        node_infos[node_name] = [
            node_infos[node_name][0], \
            node_infos[node_name][1] - used_gpu_num, \
            node_infos[node_name][2] - used_ram, \
            node_infos[node_name][3] - used_cpucore]
        
    # info_states: [gpu_type, gpu_num, RAM_total, CPU_total, state]
    for node_name, info_states in node_infos.items():
        if info_states[1] == 0 and not alloc_nodes:
            continue
        gpu_AT = f'{int(info_states[1])}/{raw_nodeinfos[node_name][1]}'
        ram_AT = f'{int(info_states[2])}/{raw_nodeinfos[node_name][2]}'
        cpu_AT = f'{int(info_states[3])}/{raw_nodeinfos[node_name][3]}'
        final.append([node_name, info_states[0], gpu_AT, cpu_AT, ram_AT])
    return final

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check node usage, show available resources.")
    parser.add_argument("--show-alloc", action="store_true", help="Print alloc node also, mainly for admin to check.")
    args = parser.parse_args()
    print()
    node_infos = node_info()
    final = node_usage(node_infos, alloc_nodes=args.show_alloc)
    print("The list sort by available resource at this moment.")
    print("##: [A/T] means *Available* num to use and *Total* num in the node.\n")
    # sort final by CPU usage
    final.sort(key=lambda x: int(x[2].split('/')[0]), reverse=True)
    res = tabulate(final, headers=(["Node", "GPU Type", "GPU [A/T]", "CPU [A/T]", "RAM [A/T]"]))
    print(res)
    print()
