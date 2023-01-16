# little bit of code to help me get a printout of cProfile stats
import pstats
from pstats import SortKey
p = pstats.Stats('profile.dat')
p.strip_dirs().sort_stats('cumulative').print_stats()