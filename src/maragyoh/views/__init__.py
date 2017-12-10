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

"""Handle http requests.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""


class Log:
    @staticmethod
    def debug(format_string, *values):
        print(format_string % values)


'''
try:
    import browser
    from browser import window, html, window
    from . import connector

    NODOM = html.DIV()

    log = Log()
except ImportError:
    from maragyoh.views.browser import document, html, window, NODOM
    from maragyoh.views import connector
    import logging as logg
    import os

    LOG_LEVEL = logg.DEBUG  # int(os.getenv("LABASELOG", logg.ERROR))

    logg.basicConfig(level=LOG_LEVEL)
    log = logg
'''
import sys
if "Brython" in sys.version:
    from browser import window, html, window
    NODOM = html.DIV()

else:
    from maragyoh.views.browser import document, html, window, NODOM
    import logging as log
    import os

    LOG_LEVEL = log.DEBUG  # int(os.getenv("LABASELOG", logg.ERROR))

    log.basicConfig(level=LOG_LEVEL)
    #log = logg
