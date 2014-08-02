# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Header Adder.
Usage:
  add_header [options] [-nl] -h <header> <file>...
  add_header --help

Options:
-n, --no-append-newline			Do not append a newline at the end of the \
current line.
-l <language>, --lang <langauge>	Set the language to force for all files
-h <header>, --header <header>		Sets the header file to be read.
"""

import os

from docopt import docopt


# Indentation functions
def c_style_block_comment(lines):
    yield '/*'
    for line in lines:
        yield ' * ' + line
    yield '*/'


def python_comment(lines):
    for line in lines:
        yield '# ' + line


COMMENT_FUNCS = {".cpp": c_style_block_comment, ".c": c_style_block_comment,
                 ".py": python_comment}


def main():
    arguments = docopt(__doc__, version='testing')

    files = arguments['<file>']
    skip_nl = arguments['--no-append-newline']
    header_filename = arguments['--header']

    try:
        with open(header_filename, 'r') as f:
            header = f.readlines()
    except IOError as e:
        print('Cannot open header file {}: {}'.format(header_filename, str(e)))
        exit(1)

    # Do a first pass to make sure that all the files exist and are files
    # (try to avoid partial jobs)
    for filename in files:
        if not os.path.isfile(filename):
            print('{} doesn\'t exist or isn\'t a file. Exiting.')
            exit(1)

    for filename in files:
        try:
            with open(filename, 'r') as f:
                contents = f.read()

                extsplit = os.path.splitext(filename)
                if len(extsplit) != 2:
                    print(('Unable to detect file type for file {}: '
                           'No extension.').format(filename))
                    exit(1)

                extension = extsplit[1]

                # Look up the extension in the dict
                comment_func = COMMENT_FUNCS.get(extension)

                if not comment_func:
                    print('Unknown extension: ' + extension)
                    exit(1)

                contents = ''.join(comment_func(header)) + '\n' + ('' if skip_nl else '\n') + contents

            with open(filename, 'w') as f:
                print('Write: {}'.format(filename))
                f.write(contents)
        except IOError as e:
            print('An error occurred while writing/reading {}: {}'
                  .format(filename, str(e)))
            exit(1)


if __name__ == '__main__':
    main()
