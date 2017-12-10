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

"""Connect two instances.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

.. _modulo_connector:

=========
Connector
=========
try:
    from browser import window
except ImportError:
    from maragyoh.views.browser import document, html, window, NODOM

"""
from . import log, window


class Connect:
    def __init__(self, last, nodeid, remote_action):
        """A WEBRTC connector manager

        :param last: An index referencing this node
        :param nodeid: A string pattern for group address
        :param remote_action: Action called when message is received
        """
        self.last = self.this = last
        self.nid = nodeid
        self.peer = None
        self.conn = []
        self.remote_action = remote_action
        window.addEventListener("beforeunload", self.leave_connection)
        log.debug("XXXXXXX>>>> __init__(self, last=  %s, nodeid=  %s)", last, self.nid % last)
        self.init_peer(last)

    def send(self, data):
        """Send message

        :param data: data for the message
        :return:
        """
        [conn.send(data) for conn in self.conn]

    def _remote_action(self, data=""):
        self.remote_action(data)

    def init_peer(self, last):
        self.peer = peer = window.Peer.new(self.nid % last, {'key': '49rhnah5bore8kt9', 'debug': 0})

        def do_connect(node_id):
            log.debug("XXXXXXX>>>> init_peer.channel.do_connect=  %s", node_id)
            conn = peer.connect(node_id)
            conn.on('data', self.remote_action)
            return conn
        peer.on('connection', self.get_connection)
        self.conn = [do_connect(self.nid % nid) for nid in range(1, last) if nid != self.this]

    def get_connection(self, conn):
        log.debug("XXXXXXX>>>> get_connection(self, a_node)=  %s", str(conn.peer))
        if conn.peer not in [cn.peer for cn in self.conn]:
            log.debug("XXXXXXX>>>> append_connection(self, a_node)=  %s", str(conn.peer))
            self.conn.append(self.peer.connect(str(conn.peer)))
        conn.on('data', self.remote_action)
        conn.send("10 20 30")

    def leave_connection(self, _=0):
        [conn.close() for conn in self.conn]
        log.debug("XXXXXXX>>>> leave_connection conn.close()=  %s", str(self.conn))


def main(last, nodeid, remote_action):
    Connect(last, nodeid, remote_action)
