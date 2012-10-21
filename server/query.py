import itertools
import math
import pprint
import sys

class AttrObj(object):
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


def query(data, headway_torelance=300):
    grouped = []
    data = sorted(data, key=lambda x: x.stop_id)
    for k,g in itertools.groupby(data, key=lambda x: x.stop_id):
        grouped.append((k, list(g)))
    grouped.sort()

    result = []
    for k, lst in grouped:
        item0 = lst[0]
        summary = summary_for_stop(lst, headway_torelance)
        st = dict(
            stop_id = item0.stop_id,
            stop_name = item0.stop_name,
            lat = item0.lat,
            lon = item0.lon,
            expected_frequency = dict(
                value = int(round(float(summary.expected_frequency/60.0))),
                rank = 3,
            ),
            headway_index = dict(
                value = "%.2f" % summary.headway_index,
                rank = 3,
            ),
            percent_tolerable_headway= dict(
                value = int(round(summary.percent_tolerable_headway*100)),
                rank = 3,
            ),
            std_dev_headway = dict(
                value = "%.2f" % float(summary.std_dev_headway/60.0),
                rank = 3,
            ),
        )

        result.append(st)

    rank(result, 'expected_frequency')
    rank(result, 'headway_index')
    rank(result, 'percent_tolerable_headway')
    rank(result, 'std_dev_headway')

    # summary for all
    summary = summary_for_stop(data, headway_torelance)

    return {
      "route_aggregate": dict(
        expected_frequency = dict(
            value = summary.expected_frequency,
        ),
        headway_index = dict(
            value = summary.headway_index,
        ),
        percent_tolerable_headway= dict(
            value = summary.percent_tolerable_headway,
        ),
        std_dev_headway = dict(
            value = summary.std_dev_headway,
        ),
      ),
      "stop_stats": result,
      }

def summary_for_stop(lst, headway_torelance):
    H = [x.headway for x in lst]
    N = len(H)
    ef = expected_frequency=effective_frequency(H)
    mean = float(sum(H)) / N
    hi = ef / mean
    pth = sum(1 for h in H if h <= headway_torelance) / float(N)
    sd = std_dev(H)

    return AttrObj(
        expected_frequency        = ef,
        headway_index             = hi,
        percent_tolerable_headway = pth,
        std_dev_headway           = sd,
    )


def effective_frequency(times):
    h2 = sum(t*t for t in times)
    T = sum(times)
    return float(h2)/T


def std_dev(times):
    N = len(times)
    s2 = sum(t*t for t in times)
    s = sum(times)
    variance = (s2 - s*s/N) / N
    return math.sqrt(variance)


def rank(result, metric):
    """ Assign rank sorted by the value of metric """
    sr = sorted(result, key=lambda r: r[metric]['value'])
    for i,r in enumerate(sr):
        r[metric]['rank'] = i+1




#------------------------------------------------------------------------
# Testing

SAMPLE = [
AttrObj(route="10",stop_id=1,stop_name="brannan",lat=1,lon=2,arrival=1349997242,headway=100),
AttrObj(route="10",stop_id=1,stop_name="brannan",lat=1,lon=2,arrival=1349997342,headway=200),
AttrObj(route="10",stop_id=1,stop_name="brannan",lat=1,lon=2,arrival=1349997342,headway=100),
AttrObj(route="10",stop_id=2,stop_name="townsend",lat=1,lon=2,arrival=1349997542,headway=100),
AttrObj(route="10",stop_id=2,stop_name="townsend",lat=1,lon=2,arrival=1349997642,headway=100),
AttrObj(route="10",stop_id=2,stop_name="townsend",lat=1,lon=2,arrival=1349997542,headway=150),
]

def test(argv):
    pprint.pprint(query(SAMPLE))

if __name__ =='__main__':
    test(sys.argv)

