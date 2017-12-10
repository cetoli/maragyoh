#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Marayho
# Copyright 2014-2017 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# Marayho é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""Recursiv Item List.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

try:
    from browser import document, html, window
    from connector import Connect
    NODOM = html.DIV()
except ImportError:
    from maragyoh.views.browser import document, html, window, NODOM
    from maragyoh.views.connector import Connect
"""
from . import log, document, html, window, NODOM
from .connector import Connect


from random import randint

TEXT_MARGIN = 16

SIZE = (50, 50)
GRAY = (250, 250, 250)
PAD = 2
MAR = 6

"""*##########################################*.

"""


class Item:
    """ An Item in the outline.

    :param node_id: Id for remote connection
    :param rgb: Color for the item
    :param size: Size for the item
    :param parent: Parent for the Item
    """
    conn = None
    item = {}
    prefix = "S_N_O_D_E_%03x" % randint(0x111, 0xfff) + "-%02d"

    def __init__(self, node_id, rgb, size=SIZE, parent=NODOM, text="-enter text-"):
        self.container = []
        self.capacity = self.item_count = self.rows = self.cols = 1
        self.base = self.content = NODOM
        self.parent, self.node_id, self.rgb, self.size, self.text = self.init_(node_id, rgb, size, parent, text)
        self.parent = parent

    def init_(self, node_id, rgb, size, parent, text):
        """
        >>> print(item.init_(2, (0, 0, 0), (15, 15), NODOM)[1:])
        (2, (0, 0, 0), (15, 15))

        :param text:
        :param node_id: Id for remote connection
        :param rgb: Color for the item
        :param size: Size for the item
        :param parent: the node from wich this stems
        :return: parent, node_id, rgb, size
        """
        # print("XXXXXXX>>>> _init", ">%s<" % [node_id, rgb, size])
        height, width = size
        brgb = tuple([max(0, k-randint(30, 100)) for k in rgb])
        span = 100*(width-TEXT_MARGIN)/width
        self.base = html.DIV(style={
            "background-color": "rgb(%d, %d, %d)" % rgb, "border": "2px solid rgb(%d, %d, %d)" % brgb, "padding": "2px",
            "margin": "2px", "border-radius": "8px", "overflow": "hidden",
            "height": "%dpx" % height, "width": "%dpx" % width, "float": "left"})
        self.content = content = html.DIV(
            text, style={"position": "relative", "float": "left", "left": "-4px", "width": "%d%%" % span})
        adder = html.SPAN(
            "◉", style={"position": "relative", "float": "left", "left": "-5px", "top": "-8px", "cursor": "crosshair"})
        fixer = html.SPAN("❌", style={"position": "relative", "float": "right", "top": "-4px"})
        self.base <= adder
        self.base <= content
        # self.base <= fixer
        fixer.onclick = self.fix_item
        adder.onclick = self.add_item
        content.onclick = self.edit_item
        content.onresize = self.compute_grid
        content.addEventListener("change", self.compute_grid)
        content.bind("DOMSubtreeModified",self.compute_grid)
        parent <= self
        return parent, node_id, rgb, size, text

    def create(self, rgb=None, node_id=None, size=None):
        """Create an Item instance.

        :param node_id: Id for remote connection
        :param rgb: Color for the item
        :param size: Size for the item
        :return: An instance of Item
        """
        nodeid = node_id if node_id else self.node_id + (len(self.container),)
        rgb = rgb or (randint(235, 255), randint(235, 255), randint(235, 255))
        size = size if size else self.compute_grid()
        item = Item(node_id=nodeid, rgb=rgb, size=size, parent=self)
        Item.item[nodeid] = item
        size = self.compute_grid()
        [it.resize(size) for it in self.container]
        return item

    def compute_grid(self, *_):
        def compute_size():
            return (height - 1 * PAD + - 2 * MAR * self.rows) / self.rows, \
                                 (width - 1 * PAD - 2 * MAR * self.cols) / self.cols
        height, width = self.size
        txth = self.content.getBoundingClientRect().height
        txth = txth if isinstance(txth, int) else int(txth[:-2])
        # print("compute_grid", height, txth, type(height), type(txth))
        height -= txth
        cheight, cwidth = size = compute_size()
        self.capacity = self.cols = self.rows = 1
        while len(self.container) > self.capacity:
            if(3*width / (self.rows + 1) >= height / (self.cols + 1)) and (cheight > 48):
                self.rows = self.rows + 1
            else:
                self.cols = self.cols + 1
                self.rows = max(1, self.rows // self.cols)
            self.capacity = self.rows * self.cols
            # size = height / self.rows-10, width / self.cols-10
            cheight, cwidth = size = compute_size()
        [item.resize(size) for item in self.container]
        return size

    def resize(self, size):
        height, width = self.size = size
        self.base.style.width = "%dpx" % width
        self.content.style.width = "%d%%" % (100*(width-TEXT_MARGIN)/width)
        self.base.style.height = "%d%s" % (height, "px")
        # self.size = height, width
        self.compute_grid()
        # size = (height-4*self.rows+2)/self.rows, (width-4*self.cols+2)/self.cols
        # [item.resize(size) for item in self.container]

    def __le__(self, square):
        self.container.append(square)
        self.base <= square.base

    @staticmethod
    def fix_item(ev=None):
        ev.stopPropagation()
        ev.target.contentEditable = False

    @staticmethod
    def edit_item(ev=None):
        ev.stopPropagation()
        ev.target.contentEditable = True
        # self.create().send()

    def add_item(self, ev=None):
        ev.stopPropagation()
        log.debug("XXXXXXX>>>> Item.add_item(ev) = >%s<", [list(self.node_id), list(self.rgb), list(self.size)])
        self.create().send()
        # Item(self, self.compute_grid())

    def send(self):
        data = [list(self.node_id), list(self.rgb), list(self.size)]
        Item.conn.send(data)


"""*##########################################*.

"""


class Base(Item):
    """ The Base Item of the outline.

    :param node_id: Id for remote connection
    :param rgb: Color for the item
    :param last: index for the item
    """
    def __init__(self, last, node_id, rgb=GRAY):
        self.base = canvas = document["pydiv"]
        canvas.text = ""

        def resize(_):
            self.resize([window.innerHeight - 20, window.innerWidth - 30])

        def _add_item(data):
            log.debug("XXXXXXX>>>> Base._add_item(data) = >%s<", data)
            _node_id, _rgb, _size = tuple(data[0]), tuple(data[1]), tuple(data[2])
            log.debug("XXXXXXX>>>> Base.Item.item = >%s<", Item.item.keys())
            log.debug("XXXXXXX>>>> type(_node_id) = >%s<, _node_id = >%s<", type(_node_id), _node_id)
            Item.item[_node_id[:-1]].create(_rgb, _node_id, _size)

        class NoItem:
            def __init__(self):
                self.container = []

            def __le__(self, square):
                canvas <= square.base

        Item.prefix = node_id
        self.no_item = NoItem()
        size = window.innerHeight - 20, window.innerWidth - 30
        window.onresize = resize
        Item.item[()], Item.item[(0,)] = self.no_item, self
        Item.__init__(self, (0,), rgb, size, self.no_item)
        Item.conn = self   # Connect(last, node_id, _add_item)
        self.base.style.left = 2
        self.base.style.top = -2
        self.base.style.position = "absolute"

    def send(self, *_):
        pass


"""*##########################################*.

"""


def main(last, nodeid):
    Base(last, nodeid)


if __name__ == "__main__":
    import doctest

    doctest.testmod(globs=dict(
        item=Item(12, GRAY),
        NODOM=NODOM
    ))
