import os
import filecmp
from subprocess import check_output
from tempfile import NamedTemporaryFile
from ...util import unix_only


HELP_OUTPUT = (
    b"""usage: cgp220 [-h] [-c] [-m] [-y] [-k] [-d D] infile """
    b"""outfile\n\nConvert CGP-220 printer output to a PNG\n\npositional """
    b"""arguments:\n  infile      input file containing raw printer dump\n  """
    b"""outfile     output filename for PNG\n\noptional arguments:\n  -h, """
    b"""--help  show this help message and exit\n  -c          block cyan\n """
    b""" -m          block magenta\n  -y          block yellow\n  -k        """
    b"""  block black\n  -d D        desaturate (0-100)\n\nCopyright 2015 """
    b"""Erik Gavriluk. Released under the Artistic License 2.0.\n"""
)


@unix_only
def test_help_message():
    assert check_output("cgp220", shell=True) == HELP_OUTPUT


def test_output():
    infile = os.path.join(os.path.dirname(__file__), "data", "cgp220.prn")
    expected_outfile = os.path.join(
        os.path.dirname(__file__), "data", "cgp220.prn.png"
    )
    outfile = NamedTemporaryFile()
    outfile.close()
    assert (
        check_output("cgp220 {} {}".format(infile, outfile.name), shell=True)
        == b""
    )
    assert filecmp.cmp(outfile.name, expected_outfile)
    os.remove(outfile.name)
