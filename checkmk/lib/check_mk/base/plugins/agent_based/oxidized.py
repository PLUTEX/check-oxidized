#!/usr/bin/env python3
# 2021, Jan-Philipp Litza <jpl@plutex.de>.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this list of
#   conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this list
#   of conditions and the following disclaimer in the documentation and/or other materials
#   provided with the distribution.
#
# * The names of its contributors may not be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
# AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


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
        if time_parsed - datetime.now() >= THRESHOLD:
            yield Result(state=State.WARN, summary=f"Backup older than {THRESHOLD} (last run: {time})")
        else:
            yield Result(state=State.OK, summary=f"Last backup at {time} was successful")


register.check_plugin(
    name="oxidized",
    service_name="Config Backup",
    discovery_function=discover_oxidized,
    check_function=check_oxidized,
)
