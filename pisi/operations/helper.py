# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi
import pisi.context as ctx
import pisi.util as util
import pisi.ui as ui
import pisi.conflict
import pisi.db

def reorder_base_packages(order):

    componentdb = pisi.db.componentdb.ComponentDB()
    
    """system.base packages must be first in order"""
    systembase = componentdb.get_union_component('system.base').packages

    systembase_order = []
    nonbase_order = []
    for pkg in order:
        if pkg in systembase:
            systembase_order.append(pkg)
        else:
            nonbase_order.append(pkg)

    # bug #5 force baselayout to be first 
    if "baselayout" in systembase_order:
        systembase_order.remove("baselayout")
        systembase_order.insert(0, "baselayout")

    return systembase_order + nonbase_order

def check_conflicts(order, packagedb):
    """check if upgrading to the latest versions will cause havoc
    done in a simple minded way without regard for dependencies of
    conflicts, etc."""

    (C, D, pkg_conflicts) = pisi.conflict.calculate_conflicts(order, packagedb)

    if D:
        raise Exception(_("Selected packages [%s] are in conflict with each other.") %
                    util.strlist(list(D)))

    if pkg_conflicts:
        conflicts = ""
        for pkg in pkg_conflicts.keys():
            conflicts += _("[%s conflicts with: %s]\n") % (pkg, util.strlist(pkg_conflicts[pkg]))

        ctx.ui.info(_("The following packages have conflicts:\n%s") %
                    conflicts)

        if not ctx.ui.confirm(_('Remove the following conflicting packages?')):
            raise Exception(_("Conflicting packages should be removed to continue"))

    return list(C)

def expand_src_components(A):
    componentdb = pisi.db.componentdb.ComponentDB()
    Ap = set()
    for x in A:
        if componentdb.has_component(x):
            Ap = Ap.union(componentdb.get_union_component(x).sources)
        else:
            Ap.add(x)
    return Ap

def calculate_download_sizes(order):
    total_size = cached_size = 0

    installdb = pisi.db.installdb.InstallDB()
    packagedb = pisi.db.packagedb.PackageDB()

    try:
        cached_packages_dir = ctx.config.cached_packages_dir()
    except OSError:
        # happens when cached_packages_dir tried to be created by an unpriviledged user
        cached_packages_dir = None

    for pkg in [packagedb.get_package(name) for name in order]:

        delta = None
        if installdb.has_package(pkg.name):
            (version, release, build, distro, distro_release) = installdb.get_version_and_distro_release(pkg.name)
            if distro_release == pkg.distributionRelease:
                delta = pkg.get_delta(release)

        ignore_delta = ctx.config.values.general.ignore_delta

        if delta and not ignore_delta:
            fn = os.path.basename(delta.packageURI)
            pkg_hash = delta.packageHash
            pkg_size = delta.packageSize
        else:
            fn = os.path.basename(pkg.packageURI)
            pkg_hash = pkg.packageHash
            pkg_size = pkg.packageSize

        if cached_packages_dir:
            path = util.join_path(cached_packages_dir, fn)
            # check the file and sha1sum to be sure it _is_ the cached package
            if os.path.exists(path) and util.sha1_file(path) == pkg_hash:
                cached_size += pkg_size
            elif os.path.exists("%s.part" % path):
                cached_size += os.stat("%s.part" % path).st_size

        total_size += pkg_size

    ctx.ui.notify(ui.cached, total=total_size, cached=cached_size)
    return total_size, cached_size
