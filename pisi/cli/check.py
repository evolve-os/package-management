# -*- coding:utf-8 -*-
#
# Copyright (C) 2005-2011, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import optparse

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.api
import pisi.cli.command as command
import pisi.context as ctx
import pisi.util as util
import pisi.db


usage = _("""Verify installation

Usage: check [<package1> <package2> ... <packagen>]
       check -c <component>

<packagei>: package name

A cryptographic checksum is stored for each installed
file. Check command uses the checksums to verify a package.
Just give the names of packages.

If no packages are given, checks all installed packages.
""")


class Check(command.Command):

    __doc__ = usage
    __metaclass__ = command.autocommand

    def __init__(self, args):
        super(Check, self).__init__(args)
        self.installdb = pisi.db.installdb.InstallDB()
        self.componentdb = pisi.db.componentdb.ComponentDB()

    name = ("check", None)

    def options(self):
        group = optparse.OptionGroup(self.parser, _("check options"))

        group.add_option("-c", "--component",
                         action="store",
                         default=None,
                         help=_("Check installed packages under "
                                "given component"))

        group.add_option("--config",
                         action="store_true",
                         default=False,
                         help=_("Checks only changed config files of "
                                "the packages"))

        self.parser.add_option_group(group)

    def run(self):
        self.init(database=True, write=False)

        component = ctx.get_option('component')
        if component:
            installed = pisi.api.list_installed()
            component_pkgs = self.componentdb.get_union_packages(component,
                                                                 walk=True)
            pkgs = list(set(installed) & set(component_pkgs))
        elif self.args:
            pkgs = self.args
        else:
            ctx.ui.info(_('Checking all installed packages') + '\n')
            pkgs = pisi.api.list_installed()

        necessary_permissions = True

        broken_packages = []

        # True if we should also check the configuration files
        check_config = ctx.get_option('config')

        # Line prefix
        prefix = _('Checking integrity of %s')

        # Determine maximum length of messages for proper formatting
        maxpkglen = max([len(_p) for _p in pkgs])

        for pkg in pkgs:
            if self.installdb.has_package(pkg):
                check_results = pisi.api.check(pkg, check_config)
                ctx.ui.info("%s    %s" % ((prefix % pkg),
                                          ' ' * (maxpkglen - len(pkg))),
                            noln=True)

                if check_results['missing'] or check_results['corrupted'] \
                        or check_results['config']:
                    ctx.ui.info(util.colorize(_("Broken"), 'brightred'))
                    broken_packages.append(pkg)
                elif check_results['denied']:
                    # We can't deduce a result when some files
                    # can't be accessed
                    necessary_permissions = False
                    ctx.ui.info(util.colorize(_("Unknown"), 'yellow'))
                else:
                    ctx.ui.info(util.colorize(_("OK"), 'green'))
                    continue

                # Dump per file stuff
                for fpath in check_results['missing']:
                    ctx.ui.info(util.colorize(
                        _("Missing file: /%s") % fpath, 'brightred'))

                for fpath in check_results['denied']:
                    ctx.ui.info(util.colorize(
                        _("Access denied: /%s") % fpath, 'yellow'))

                for fpath in check_results['corrupted']:
                    ctx.ui.info(util.colorize(
                        _("Corrupted file: /%s") % fpath, 'brightyellow'))

                for fpath in check_results['config']:
                    ctx.ui.info(util.colorize(
                        _("Modified configuration file: /%s") % fpath,
                        'brightyellow'))

            else:
                # Package is not installed
                ctx.ui.info(_('Package %s not installed') % pkg)

        if len(broken_packages) > 0:
            broken_packages_str = ' '.join(broken_packages)

            ctx.ui.info("")
            ctx.ui.warning(_("Some packages are reported as broken, you may "
                             "want to repair these packages by running:"))
            ctx.ui.warning("sudo eopkg it --reinstall %s" % broken_packages_str)

        if not necessary_permissions:
            ctx.ui.info("")
            ctx.ui.warning(_("Pisi was unable to check the integrity of "
                             "packages which contain files that you don't "
                             "have read access.\n"
                             "Running the check under a privileged user "
                             "may help fixing this problem."))
