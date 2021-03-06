# -*- coding: utf-8 -*-
import logging

from lib.netgraph.net_distribution import DrawDistribution

_NODES = (0, 1, 2, 3, 4, 5, 6, 7)
_EDGES = [
    (0, 1, 0.01),
    (1, 2, 1),
    (1, 3, 1),
    (1, 4, 1),
    (2, 3, 1),
    (2, 4, 1),
    (3, 5, 1),
    (5, 6, 1),
    (5, 7, 1),
    (6, 7, 1)
]


def test_non_existent_measure():
    catch_except = False
    try:
        DrawDistribution(_EDGES, measure='non_existent_measure')
    except Exception:
        catch_except = True
    finally:
        assert catch_except


def test_filter_none():
    drawer = DrawDistribution(_EDGES)
    drawer.filter_ranks(0)
    nodes = drawer.get_nodes()
    assert len(nodes) == len(_NODES)
    drawer.filter_ranks(None)
    nodes = drawer.get_nodes()
    assert len(nodes) == len(_NODES)
    drawer.filter_ranks(0.6)
    nodes = drawer.get_nodes()
    assert len(nodes) < len(_NODES)


def test_distribute():
    logging.info('Loading edges to graph ...')
    drawer = DrawDistribution(_EDGES)
    logging.info('Friends distribution analysis ...')
    drawer.plot_networkx(with_label=True, block=False)
    drawer.get_measures()
    drawer.plot_rank_pdf_cdf(block=False)
    logging.info('Plot closed.')


if __name__ == '__main__':
    test_non_existent_measure()
    test_filter_none()
    test_distribute()
