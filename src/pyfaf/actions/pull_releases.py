# Copyright (C) 2013  ABRT Team
# Copyright (C) 2013  Red Hat, Inc.
#
# This file is part of faf.
#
# faf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# faf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with faf.  If not, see <http://www.gnu.org/licenses/>.

from . import Action
from ..opsys import systems
from ..storage import OpSys, OpSysRelease, OpSysReleaseStatus

class PullReleases(Action):
    name = "pull-releases"

    def __init__(self):
        Action.__init__(self)

    def run(self, cmdline, db):
        if cmdline.opsys is None:
            self.log_error("You need to specify the operating system")
            return 1

        if cmdline.opsys not in systems:
            self.log_error("Operating system '{0}' is not supported"
                           .format(cmdline.opsys))
            return 1

        opsys_plugin = systems[cmdline.opsys]
        opsys = (db.session.query(OpSys)
                           .filter(OpSys.name == opsys_plugin.nice_name)
                           .first())

        if opsys is None:
            self.log_error("Operating system '{0}' is not defined in "
                           "storage.".format(opsys_plugin.nice_name))
            return 1

        self.log_info("Using operating system '{0}'"
                      .format(opsys_plugin.nice_name))

        self.log_info("Loading releases from local storage")
        db_releases = {}
        for db_release in opsys.releases:
            self.log_debug("Loading release '{0}'".format(db_release.version))
            db_releases[db_release.version] = db_release

        self.log_info("Downloading releases from remote database")
        releases = opsys_plugin.get_releases()

        for release, props in releases.items():
            remote_status = OpSysReleaseStatus.enums[props["status"]]
            if release in db_releases:
                if remote_status == db_release.status:
                    self.log_debug("Release '{0}' is up to date"
                                   .format(release))
                    continue

                self.log_info("Updating status for release '{0}': '{1}' "
                              "-> '{2}'".format(release, db_release.status,
                                                remote_status))

                db_release.status = remote_status

            self.log_info("Adding release '{0}' ({1})"
                          .format(release, remote_status))

            new = OpSysRelease()
            new.version = release
            new.opsys = opsys
            new.status = remote_status
            db.session.add(new)

        db.session.flush()

    def tweak_cmdline_parser(self, parser):
        parser.add_opsys()
