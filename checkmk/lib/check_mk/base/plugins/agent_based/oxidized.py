#!/usr/bin/env python3
# Part of check_oxidized
# Copyright (C) 2021, Jan-Philipp Litza <jpl@plutex.de>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from datetime import datetime, timedelta
from .agent_based_api.v1 import register, Service, Result, State


THRESHOLD = timedelta(hours=12)


def discover_oxidized(section):
    yield Service()


def check_oxidized(section):
    status, time = section[0]

    if status == "never":
        yield Result(state=State.WARN, summary="No backup tries since startup")
    elif status != "success":
        yield Result(state=State.CRIT, summary=f"status={status}, time={time}")
    else:
        time_parsed = datetime.strptime(time, "%Y-%m-%d %H:%M:%S %Z")
        if datetime.now() - time_parsed >= THRESHOLD:
            yield Result(state=State.WARN, summary=f"Backup older than {THRESHOLD} (last run: {time})")
        else:
            yield Result(state=State.OK, summary=f"Last backup at {time} was successful")


register.check_plugin(
    name="oxidized",
    service_name="Config Backup",
    discovery_function=discover_oxidized,
    check_function=check_oxidized,
)
