# coding: utf-8

# Copyright (C) 2017 Open Path View, Maison Du Libre
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

# Contributors: Benjamin BERNARD <benjamin.bernard@openpathview.fr>
# Email: team@openpathview.fr
# Description: Represent a lot partition, a set a lot with start and end indexes.

from typing import NamedTuple, List
from opv_import.model import Lot

LotPartition = NamedTuple('LotPartition', [
    ('ref_lot', Lot),
    ('lots', List[Lot]),
    ('start_imgset_index', int),
    ('start_meta_index', int),
    ('break_reason', str),
    ('number_of_good_associations', int)
])