eopkg(1) -- Solus package manager
=================================


## SYNOPSIS

`eopkg [options] <command> [arguments]`


## DESCRIPTION

`eopkg` is the package manager for the Solus operating system. It is used to
manage installed software packages, search for available software and to apply
updates to the system.

## OPTIONS

The following options are applicable to `eopkg(1)`.

 * `-D`, `--destdir`

   Change the system root for eopkg commands

 * `-y`, `--yes-all`

   Assume yes in all yes/no queries

 * `-u`, `--username`

   Set username used when connecting to Basic-Auth repositories. Rarely required.

 * `-p`, `--password`

   Set password used when connecting to Basic-Auth repositories. Rarely required.

 * `-L`, `--bandwidth-limit`

   Keep bandwidth usage under the specified (numeric) KBs

 * `-v`, `--verbose`

   Detailed output

 * `-d`, `--debug`

   Enable full debug information and backtraces

 * `-h`, `--help`

   Print the command line options for `eopkg(1)` and exit.

 * `--version`

   Print the `eopkg(1)` version and exit.

 * `-N`, `--no-color`

   Disable the use of ANSI escape sequences for colourisation by eopkg.

## SUBCOMMANDS

All available subcommands are listed below by their primary name and their
alias, if available. Most commands in eopkg support a short form.

`add-repo (ar) <repo-name> <repo URI>`

    Add a new repository to the system with the given name and URI. Note
    that a valid eopkg index file will start with `eopkg-index.xml` and
    typically is compressed with `.xz` or similar.

 * `--ignore-check`:
 
        Ignore checking metadata for a valid distribution specifier.

 * `--no-fetch`:

        Do not download index, just register the new repository and add
        it to the system.

 * `--at`:

        Insert the new repository at the given index position.
        The default is `0`

`autoremove (rmf) <package1> <package2> ...`

    Remove a package from the system, along with reverse dependencies and
    any automatically installed packages related to this package that are
    now no longer required. This ensures a full removal for direct
    runtime dependencies instead of just reverse dependencies.

 * `--ignore-dependency`:

        Do not attempt the removal/validation of reverse dependencies that
        would otherwise be removed.

 * `--ignore-comar`:

        Bypass system configuration. Deprecated in favour of `usysconf(1)`

 * `--ignore-safety`:

        Ignore safety switch on `system.base` component - highly dangerous.

 * `-n`, `--dry-run`:

        Only show what would happen, do not actually perform changes.

 * `-p`, `--purge`:

        Remove files tagged as configuration files too. This primarily
        applies to any files in `/etc/`.

`blame (bl) <packagename>`

    Show history entry for a given package to show the packages
    changelog. This will integrate automatically with `solbuild(1)`
    git changelog support for official Solus packages, and allow
    inspecting each change.

    By default `blame` will show the information on the highest available
    release.

 * `-r`, `--release`:

        Only show blame for the given release number

 * `-a`, `--all`:

        Show blame for the entire history of the package

`build (bi) <path to pspec.xml>`

    Consult `eopkg ? bi` for further details. The legacy `eopkg` format
    is no longer supported by Solus and is only currently used behind
    the scenes in the third party mechanism. New packages should only
    use `package.yml(5)` via `ypkg(1)` and `solbuild(1)`

`check <package?>`

    Check the installation status (corruption, etc) of all packages,
    or the provided package names. This subcommand will check the hashes
    for all installed packages to ensure integrity.

 * `-c`, `--component`:

        Check installed packages under the given component

 * `--config`:

        Only check the status of configuration files (i.e. `/etc/`)

`clean`

    Forcibly delete any stale file locks held by previous instances
    of eopkg. This should only be used if the package manager refuses
    to operate due to a stale lockfile, perhaps caused by a previous
    power failure.

`configure-pending (cp)`

    Perform any system configuration if any packages are in a pending
    state. This will only invoke `usysconf(1)` and clear the pending
    state. It is also safe to invoke `usysconf run` directly as root.

`delete-cache (dc)`

    Clear out any temporary caches still held by `eopkg` for downloads
    and package files. These are automatically cleared when using the
    Software Centre but you must manually invoke `dc` if you only use
    the CLI approach to software management.

`delta (dt) <oldpackage1> <newpackage>`

    Construct a delta package between the given packages. Delta packages
    are used to create smaller updates and reduce bandwidth consumption
    for users. Typically deltas are constructed by `ferryd(1)` - however
    for manual repo management you can use this command. A `.delta.eopkg`
    will be constructed in the current working directory.

 * `-t`, `--newest-package`:

        Override the "new" package detection for explicit control
        of the process.

 * `-O`, `--output-dir`:

        Override the output directory for the `.delta.eopkg`
        instead of using the current working directory.

 * `-F`, `--package-format`:

        Override the eopkg internal format. Expert option only,
        consult `-F help` for further details.

`disable-repo (dr) <name>`

    Disable a system repository. It will no longer be accounted for
    in any operation, including search, install, and updates.

`emerge (em) <name>`

    Consult `eopkg ? em` for further details. The legacy `eopkg` format
    is no longer supported by Solus and is only currently used behind
    the scenes in the third party mechanism. New packages should only
    use `package.yml(5)` via `ypkg(1)` and `solbuild(1)`

`enable-repo (er) <name>`

    Enable a previously disabled repository by name. This will allow
    the repo to be accounted for in all operations (search,
    updates, etc.)

`fetch (fc) <name>`

    Download the package file for the named package, into the current
    working directory.

 * `-o`, `--output-dir`:

        Override the output directory for the `.eopkg` instead of
        using the current working directory.

`help (?) <subcommand?>`

    Display help topics, or help for the given subcommand. Without
    any arguments the main help topic will be displayed, along with
    an overview for all subcommands.

`history (hs)`

    Manage the eopkg transaction history. Every operation via `eopkg`
    will cause a new transaction to be recorded, which can be replayed
    through the log or rolled back to.

    Note that rolling back to older snapshots has a limited shelflive
    due to the rolling nature of Solus, and that old packages may
    disappear that were previously installed as part of an older
    transaction.

    Without arguments, this command will just emit the history into the
    `less(1)` pager.

 * `-l`, `--last`:

        Only output the last `<n>` operations.

 * `-s`, `--snapshot`:

        Create a new snapshot transaction to record the current system
        state for later rollback operations.

 * `-t`, `--takeback`:

        Given a transaction ID, this command will attempt to roll the
        system state back to the state of that transaction.

`index (ix) <directory>`

    Produce an `eopkg-index` repository in the given directory
    containing information on all discovered `eokpg` files living
    recursively under that directory.

    For more advanced repository management, please see `ferryd(1)`

 * `-a`, `--absolute-urls`:

        Use absolute URLs in the index instead of relative ones. Useful for
        locally added `file://` protocol repositories.

 * `-o`, `--output`:

        Override path to the output file

 * `--compression-types`:

        Comma separated list of compression types to use when producing the
        index, such as `bz2`, `xz`, for additional compressed index files
        for client systems to add.

 * `--skip-sources`:

        Do not include `pspec.xml` legacy format eopkg definitions in
        the index. It is highly recommended to not use the legacy
        format.

 * `--skip-signing`:

        Do not attempt to GPG sign the index.

`info`

    Show information about the given package name or package file.

 * `-f`, `--files`:

        Show a list of the package's files if available.

 * `-c`, `--component`:

        Show information about a component instead of a package.

 * `-F`, `--files-path`:

        Only show the files, and no other information about the package.

 * `-s`, `--short`:

        Compact information about each package.

 * `--xml`:

        Emit the original XML metadata for the package.

`install (it) <name>`

    Install a named package or local `.eopkg` directly onto the system.

 * `--ignore-dependency`:

        Do not attempt the installation/validation of dependencies that
        would otherwise be installed.

 * `--ignore-comar`:

        Bypass system configuration. Deprecated in favour of `usysconf(1)`

 * `--ignore-safety`:

        Ignore safety switch on `system.base` component - highly dangerous.

 * `-n`, `--dry-run`:

        Only show what would happen, do not actually perform changes.

 * `--reinstall`:

        Reinstall an already installed package.

 * `--ignore-check`:

        Do not check if this package is intended for use with the current
        distribution.

 * `--ignore-file-conflicts`:

        Allow the package to install even if it conflicts with another
        package's files. Not recommended.

 * `--ignore-package-conflicts`:

        Forcibly install a package even though it is marked as conflicting
        with another package on system. Not recommended.

 * `-c`, `--component`:

        Install an entire component by name, instead of just a package.

 * `-r`, `--repository`:

        Specify which repository to pull the component from.

 * `-f`, `--fetch-only`:

        Download the required packages but don't actually install them.

 * `-x`, `--exclude`:

        Ignore packages and components that match the specified basename
        here when installing components and packages. Use this as a filter
        to install a component while deliberately not installing one or
        more of its packages.

 * `--exclude-from <filename>`:

        Just like `--exclude`, except the package/component list is
        specified in the given filename.

`list-available <la> <repo name?>`

    List all available packages in all repositories, or just in the
    repositories specified.

 * `-l`, `--long`:

        Use long output instead of brief one line descriptions.

 * `-c`, `--component`:

        List available packages under the given component.

 * `-U`, `--uninstalled`:

        Only show uninstalled packages, i.e. packages that are available
        but not currently installed on the system.

`list-components (lc)`

    Show all available components in the combined indexes of all
    installed repositories. Each package may belong to only one
    component, and these are the enforced level of categorisation
    within a Solus repository.

 * `l`, `--long`:

        Show full details on each component instead of just listing
        the names.

 * `r`, `--repository`:

        Only list components in the specified repository.

`list-installed (li)`:

    Show a list of all installed packages.

 * `-a`, `--automatic`:

        Show a list of all packages that have been automatically
        installed as a dependency of other packages, along with
        the package they are still associated with. Orphaned
        packages with no relationship will be clearly listed.

 * `-b`, `--build-host`:

        Only show packages that come from a particular build host.
        Useful for finding packages that have been built and installed
        locally, as opposed to from an official repository.

 * `-l`, `--long`:

        Show full details of each package instead of one line
        summaries.

 * `-c`, `--component`:

        Only show installed packages from the specified component.

 * `-i`, `--install-info`:

        Show detailed installation information for each package.

`list-newest (ln) <repo?>`

    List the newest packages in the repository. With no arguments,
    this will show the newest packages in all configured
    repositories.

 * `-s`, `--since`:

        Show the newest since the specified date (YYYY-MM-DD)

 * `-l`, `--last`:

        Only show the newest packages since the nth (specified) repository
        update.

`list-pending (lp)`

    Show all packages currently in a state of required configuration.
    This is rarely the case and is nowadays only reserved for the
    building of images, where `configure-pending` is invoked after
    all required packages are installed, due to the incremental nature
    of `usysconf(1)`.

`list-repo (lr)`

    List all currently tracked repositories, and emit their
    status (enabled or not)

`list-sources (ls)`

    This is only supported with source repositories using the
    legacy `pspec.xml` ormat and is no longer recommeneded or
    supported. When invoked, this will output all source packages
    available for `emerge` operations.

 * `-l`, `--long`:

        Show detailed information on each source package.

`list-upgrades (lu)`

    List all package upgrades that are currently available.

 * `-l`, `--long`:

        Show detailed information on each package to be updated.

 * `-c`, `--component`:

        Only show upgrades from the given component

 * `-i`, `--install-info`:

        Show detailed installation information on each
        available upgrade

`rebuild-db (rdb)`

    Rebuild all `eopkg` databases. This may be required if eopkg
    is interrupted or killed during an operation, and complains
    that database recovery is required (DB5 errors). Running this
    command will reassemble the database from all the installed
    packages.

 * `-f`, `--files`:

        Only rebuild the files database
        
`remove (rm) <package1> <package2> ...`

    Remove packages from the system. Unless `--ignore-dependency`
    is specified, any reverse dependencies will also be removed
    from the system. This does not remove packages that are
    dependencies of the package being removed, however. For those
    packages, use `rmf` or later invoke `rmo`.

    
 * `--ignore-comar`:

        Bypass system configuration. Deprecated in favour
        of `usysconf(1)`

 * `--ignore-safety`:

        Ignore safety switch on `system.base` component -
        highly dangerous.

 * `-n`, `--dry-run`:

        Only show what would happen, do not actually perform
        changes.

 * `-p`, `--purge`:

        Remove files tagged as configuration files too. This
        primarily applies to any files in `/etc/`.

 * `-c`, `--component`:

        Remove any packages under the given component, and any
        child component. This is used to recursively remove
        components and their packages from the system and should
        be used with great care.

`remove-orphans (rmo)`

    Remove any packages that were automatically installed and
    no longer have any dependency relationship with non
    automatically installed packages on the system.

    Note that in Solus terminology an orphan is a proveable
    concept, not an automatic heuristic. Thus, the only
    candidates in the algorithm are those packages that
    were marked automatic as dependencies of another operation,
    and are no longer required by other packages on the system
    that aren't automatically installed.

 * `--ignore-comar`:

        Bypass system configuration. Deprecated in favour
        of `usysconf(1)`

 * `--ignore-safety`:

        Ignore safety switch on `system.base` component -
        highly dangerous.

 * `-n`, `--dry-run`:

        Only show what would happen, do not actually perform changes.

 * `-p`, `--purge`:

        Remove files tagged as configuration files too.
        This primarily applies to any files in `/etc/`.

`search (sr) <term>`

    Finds packages using the specified search term, which can
    be a regular expression when quoted.

 * `-l`, `--language`:

        Only search for summaries/descriptions with the matching
        language code. The default language code is `en`
        
 * `-r`, `--repository`:

        Only search within the specified repository.

 * `-i`, `--installdb`:

        Only search installed packages, ignoring repository
        candidates.

 * `-s`, `--sourcedb`:

        Only search source repositories. Note that source
        repositores are no longer supported and are now deprecated.

 * `--name`:

        Only search in the name field of packages

 * `--summary`:

        Only search in the summary field of packages

 * `--description`:

        Only search in the description field of packages

`search-file (sf) <path>`

    Locate the package which is considered to be the owner of
    the specified path on disk. Currently only locally installed
    packages are supported.

 * `-l`, `--long`:

        Show detailed information about matching packages

 * `-q`, `--quiet`:

        Terse output only showing the package name, most useful
        in scripts.

`update-repo (ur) <reponame?>`

    With no arguments this command will update all repository
    indexes by fetching them from their origin if a change
    has occurred. This will then synchronise the remote
    data with the local data so that changes to the repository
    are now visible to eopkg.

    You may optionally specify a repository name to only
    update that repository.

 * `-f`, `--force`:

    Forcibly update the repository indexes, even if the
    checksum file for the index hasn't been changed.
    Typically the checksum file is first consulted before
    downloading the larger index itself.

`upgrade (up) <package-name?>`

    With no arguments this command will perform a full system
    upgrade, otherwise it will update the specified packages
    along with any resulting dependencies.
    Initially the remote repositories will be updated to ensure
    all metadata is up to date.

    During an upgrade, any packages marked as `Obsolete` will
    automatically be removed from the system. Any package
    replacements for packages that have been replaced with
    different upstreams, or indeed name changes, will
    be applied too. Thus, package removals are a normal
    part of the upgrade experience.

 * `--ignore-comar`:

        Bypass system configuration. Deprecated in favou
         of `usysconf(1)`

 * `--ignore-safety`:

        Ignore safety switch on `system.base` component -
        highly dangerous.

 * `-n`, `--dry-run`:

        Only show what would happen, do not actually
        perform changes.

 * `--security-only`:

        Only apply updates that have been marked as
        security updates.

 * `-b`, `--bypass-update-repo`:

        Do not update the repositories first

 * `--ignore-file-conflicts`:

        Allow completing the update even if file conflicts
        would occur.

 * `--ignore-package-conflicts`:

        Allow completing the upgrade even if package conflicts
        would occur. This is not recommended and indicates a
        problem with the upgrade path in the remote repository.
        You should file a bug if this happens.

 * `-c`, `--component`:

        Only upgrade packages from the given component.

 * `-r`, `--repository`:

        Only upgrade packages from the given repository.

 * `-f`, `--fetch-only`:

        Only download the packages, but do not apply any
        upgrade operations.

 * `-x`, `--exclude`:

        Ignore packages and components that match the specified
        basename here when upgrading. Use this to block an update
        from happening whilst updating all other possible updates.

 * `--exclude-from <filename>`:

        Just like `--exclude`, except the package/component
        list is specified in the given filename.

## EXIT STATUS

On success, 0 is returned. A non-zero return code signals a failure.


## COPYRIGHT

 * This documentation is Copyright © 2018 Ikey Doherty, License: CC-BY-SA-3.0


## SEE ALSO

`usysconf(1)`, `solbuild(1)`, `ferryd(1)`, `ypkg(1)`, `package.yml(5)`

 * https://getsol.us/articles/package-management/
 * https://getsol.us/articles/packaging/

## NOTES

Creative Commons Attribution-ShareAlike 3.0 Unported

 * http://creativecommons.org/licenses/by-sa/3.0/
