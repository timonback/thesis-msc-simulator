import pstats
import sys


class DmpAnalyzer:
    """
    analyze_dmp.py takes the file INFILEPATH [a pstats dump file] Producing OUTFILEPATH [a human readable python profile]
    Usage:   analyze_dmp.py INFILEPATH  OUTFILEPATH
    Example: analyze_dmp.py stats.dmp   stats.log
    """
    NUM_ARGS = 2

    @staticmethod
    def analyze_dmp(myinfilepath='stats.dmp', myoutfilepath='stats.log'):
        out_stream = open(myoutfilepath, 'w')
        ps = pstats.Stats(myinfilepath, stream=out_stream)
        sortby = 'cumulative'

        ps.strip_dirs().sort_stats(sortby).print_stats(.3)  # plink around with this to get the results you need
        print('Done')

    @staticmethod
    def main():
        args = sys.argv[1:]
        if len(args) != DmpAnalyzer.NUM_ARGS or "-h" in args or "--help" in args:
            print(__doc__)
            s = input('hit return to quit')
            sys.exit(2)
        DmpAnalyzer.analyze_dmp(myinfilepath=args[0], myoutfilepath=args[1])


if __name__ == '__main__':
    DmpAnalyzer.main()
