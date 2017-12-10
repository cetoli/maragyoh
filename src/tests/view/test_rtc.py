import unittest
from . import Base, Item, log


class TestCaseRtc(unittest.TestCase):
    """Testing client module

    """
    def setUp(self):
        Item.item = {}
        self.baser = Base(0, "NOD%02d", )
        Item.conn.send = lambda data=0: self._send(data)

    def _send(self, data):
        self.data = data

    def test_create_base(self):
        """Creating a base instance."""
        tester = self.baser
        props = [tester.parent, tester.node_id, tester.rgb, tester.size]
        cprops = [Item.prefix, Item.item]
        csets = ['NOD%02d', {(): tester.no_item, (0,): tester}]
        sets = [tester.no_item, (0,), (50, 50, 50), (404, 788)]
        assert Item.conn is not None
        assert tester.container == [], tester.container
        assert props == sets, props
        assert cprops == csets, cprops

    def test_create_item(self):
        """Creating a item instance."""
        itemer = self.baser
        tester = itemer.create((9, 8, 7))
        tester.send()
        props = [tester.parent, tester.node_id, tester.rgb, tester.size]
        cprops = [Item.prefix, Item.item]
        csets = ['NOD%02d', {(0, 0): tester, (): itemer.no_item, (0,): itemer}]
        sets = [itemer, (0, 0), (9, 8, 7), (386.0, 770.0)]
        assert Item.conn is not None
        assert itemer.container == [tester], itemer.container
        assert tester.container == [], tester.container
        assert props == sets, props
        assert cprops == csets, cprops
        assert self.data == [list(arg) for arg in sets[1:]], self.data

    def test_create_second_item(self):
        """Creating a second item instance."""
        itemer = self.baser
        first = itemer.create((6, 5, 4))
        tester = itemer.create((9, 8, 7))
        tester.send()
        props = [tester.parent, tester.node_id, tester.rgb, tester.size]
        cprops = [Item.prefix, Item.item]
        csets = ['NOD%02d', {(0, 1): tester, (0, 0): first, (): itemer.no_item, (0,): itemer}]
        sets = [itemer, (0, 1), (9, 8, 7), (386.0, 376.5)]
        assert Item.conn is not None
        assert itemer.container == [first, tester], itemer.container
        assert tester.container == [], tester.container
        assert props == sets, props
        assert cprops == csets, cprops
        assert self.data == [list(arg) for arg in sets[1:]], self.data

    def test_create_sub_item(self):
        """Creating a sub item instance."""
        itemer = self.baser
        first = itemer.create((6, 5, 4))
        second = itemer.create((9, 8, 7))
        tester = Item.item[(0, 1)].create((3, 2, 1))
        tester.send()
        props = [tester.parent, tester.node_id, tester.rgb, tester.size]
        cprops = [Item.prefix, Item.item]
        csets = ['NOD%02d', {(0, 1): second, (0, 0): first, (0, 1, 0): tester, (): itemer.no_item, (0,): itemer}]
        sets = [second, (0, 1, 0), (3, 2, 1), (368.0, 358.5)]
        assert Item.conn is not None
        assert itemer.container == [first, second], itemer.container
        assert tester.container == [], tester.container
        assert second.container == [tester], second.container
        assert props == sets, props
        assert cprops == csets, cprops
        assert self.data == [list(arg) for arg in sets[1:]], self.data

    def test_create_remote_item(self):
        """Creating a remote item instance."""

        def _add_item(data):
            log.debug("XXXXXXX>>>> _add_item(data) >%s<", data)
            _rgb, _node_id, _size = tuple(data[0]), tuple(data[1]), tuple(data[2])
            log.debug("XXXXXXX>>>> Item.item >%s<", Item.item.keys())
            return Item.item[tuple(data[1][:-1])].create(_rgb, node_id=_node_id, size=_size)
        itemer = self.baser
        first = itemer.create((6, 5, 4))
        second = itemer.create((9, 8, 7))
        tester = _add_item([[3, 2, 1], [0, 1, 0], [384, 374]])
        props = [tester.parent, tester.node_id, tester.rgb, tester.size]
        cprops = [Item.prefix, Item.item]
        csets = ['NOD%02d', {(0, 1): second, (0, 0): first, (0, 1, 0): tester, (): itemer.no_item, (0,): itemer}]
        sets = [second, (0, 1, 0), (3, 2, 1), (368.0, 358.5)]
        assert Item.conn is not None
        assert itemer.container == [first, second], itemer.container
        assert tester.container == [], tester.container
        assert second.container == [tester], second.container
        assert props == sets, props
        assert cprops == csets, cprops

if __name__ == '__main__':
    unittest.main()
