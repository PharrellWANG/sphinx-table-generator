import string
import argparse
import pyperclip
from data import data


def as_rest_table(arg_data, full=False):
    """
    >>> data = [('what', 'how', 'who'),
    ...         ('lorem', 'that is a long value', 3.1415),
    ...         ('ipsum', 89798, 0.2)]
    >>> print(as_rest_table(data, full=True))
    +-------+----------------------+--------+
    | what  | how                  | who    |
    +=======+======================+========+
    | lorem | that is a long value | 3.1415 |
    +-------+----------------------+--------+
    | ipsum |                89798 |    0.2 |
    +-------+----------------------+--------+

    >>> print(as_rest_table(data))
    =====  ====================  ======
    what   how                   who
    =====  ====================  ======
    lorem  that is a long value  3.1415
    ipsum                 89798     0.2
    =====  ====================  ======

    """
    arg_data = arg_data if arg_data else [['No Data']]
    table = []
    # max size of each column
    zipped = zip(*[[len(str(elt)) for elt in member]
                   for member in arg_data])
    sizes = list(map(max, list(zipped)))
    num_elts = len(sizes)

    if full:
        start_of_line = '| '
        vertical_separator = ' | '
        end_of_line = ' |'
        line_marker = '-'
    else:
        start_of_line = ''
        vertical_separator = '  '
        end_of_line = ''
        line_marker = '='

    meta_template = vertical_separator.join(['{{{{{0}:{{{0}}}}}}}'.format(i)
                                             for i in range(num_elts)])
    template = '{0}{1}{2}'.format(start_of_line,
                                  meta_template.format(*sizes),
                                  end_of_line)
    # determine top/bottom borders
    if full:
        to_separator = bytes.maketrans(b'| ', b'+-')
    else:
        to_separator = bytes.maketrans(b'|', b'+')
    start_of_line = start_of_line.translate(to_separator)
    vertical_separator = vertical_separator.translate(to_separator)
    end_of_line = end_of_line.translate(to_separator)
    separator = '{0}{1}{2}'.format(start_of_line,
                                   vertical_separator.join([x * line_marker for x in sizes]),
                                   end_of_line)
    # determine header separator
    th_separator_tr = bytes.maketrans(b'-', b'=')
    start_of_line = start_of_line.translate(th_separator_tr)
    line_marker = line_marker.translate(th_separator_tr)
    vertical_separator = vertical_separator.translate(th_separator_tr)
    end_of_line = end_of_line.translate(th_separator_tr)
    th_separator = '{0}{1}{2}'.format(start_of_line,
                                      vertical_separator.join([x * line_marker for x in sizes]),
                                      end_of_line)
    # prepare result
    table.append(separator)
    # set table header
    titles = arg_data[0]
    table.append(template.format(*titles))
    table.append(th_separator)

    for d in arg_data[1:-1]:
        table.append(template.format(*d))
        if full:
            table.append(separator)
    table.append(template.format(*arg_data[-1]))
    table.append(separator)
    table = ['\t' + table_line for table_line in table]
    return '\n'.join(table)


def main(table_data, flags):
    table_with_title = '.. table:: ' + flags.table_title + '\n\n' + as_rest_table(table_data, full=flags.is_full)
    print(table_with_title)
    pyperclip.copy(table_with_title)
    print('\n Copied to clipboard already, feel free to paste.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate formatted sphinx table.")
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument("--is_full", type=bool,
                        default=True,
                        help="Toggle this to see diff")
    parser.add_argument("--table_title", "-t", type=str,
                        default='YOUR TABLE TITLE',
                        help="Your table title")
    parsed_flags = parser.parse_args()
    main(data, parsed_flags)
