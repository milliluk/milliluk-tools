import os
import filecmp
from subprocess import check_output
from tempfile import NamedTemporaryFile


HELP_OUTPUT = (
    b"""usage: max2png [-h] [--color] [--swap] infile outfile"""
    b"""\n\nConvert CoCo Max images to PNG\n\npositional arguments:\n  """
    b"""infile      input .max file\n  outfile     output .png file\n\n"""
    b"""optional arguments:\n  -h, --help  show this help message and """
    b"""exit\n  --color     generate an artifact color image\n  --swap """
    b"""     swap blue/orange\n\nCopyright 2016 Erik Gavriluk. Released """
    b"""under the Artistic License 2.0.\n"""
)


def test_help_message():
    assert check_output("max2png", shell=True) == HELP_OUTPUT


def test_bw_output():
    generic_test_output("EYE4.MAX", "EYE4.MAX.PNG", "")


def test_color_output():
    generic_test_output("EYE4.MAX", "EYE4.MAX.COLOR.PNG", "--color")


def test_swap_output():
    generic_test_output("EYE4.MAX", "EYE4.MAX.SWAP.PNG", "--color --swap")


def generic_test_output(infile, expected_outfile, args):
    infile = os.path.join(os.path.dirname(__file__), "samples", infile)
    expected_outfile = os.path.join(
        os.path.dirname(__file__), "samples", expected_outfile
    )
    outfile = NamedTemporaryFile()
    outfile.close()
    assert (
        check_output(
            "max2png {} {} {}".format(args, infile, outfile.name), shell=True
        )
        == b""
    )
    assert filecmp.cmp(outfile.name, expected_outfile)
    os.remove(outfile.name)
