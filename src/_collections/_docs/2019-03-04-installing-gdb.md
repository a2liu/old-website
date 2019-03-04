---
title: Installing GDB on MacOS
author: Albert Liu
categories: [coding]
tags: [gdb, debugging]
---
So MacOS has quite a few *interesting* things that prevent GDB from working. This
guide doesn't promise that you'll be able to use it, just that you'll be able to figure
out the solution faster.

##### Shortcut
If the below steps make you confused, unhappy, or discouraged, just remember that
MacOS comes with a debugger already installed called [LLDB][lldb-tutorial]! To
use it, just type in

```shell
lldb <program name>
```

...similar to how you'd use GDB.

[lldb-tutorial]: https://lldb.llvm.org/tutorial.html

### Downloading
First, please use a package manager. Generally this isn't always necessary, but
in this case, there are so many problems with the installation process anyways,
that you might as well have the *first part* handled for you.

More specifically, please use [Homebrew][homebrew] to install GDB. From there you
can run

```shell
brew install gdb
```

[homebrew]: https://brew.sh/

### Setting Permissions
Usually, the above is all you need to do. However, because Mac security features prevent
a program from arbitrary taking control of another one, we also need to configure
the mac security features to allow for GDB to work. If we run `gdb <program>` right now,
we get something like this:

```shell
Unable to find Mach task port for process-id 57573: (os/kern) failure (0x5).
(please check gdb is codesigned - see taskgated(8))
```

To fix this, we need to create a certificate and sign GDB with it. You can follow
multiple tutorials to do this:

* [Github Gist](https://gist.github.com/hlissner/898b7dfc0a3b63824a70e15cd0180154)
* [Stack Overflow Answer](https://stackoverflow.com/questions/18423124/please-check-gdb-is-codesigned-see-taskgated8-how-to-get-gdb-installed-w)
* [GDB Wiki](https://sourceware.org/gdb/wiki/PermissionsDarwin)

> **TLDR;** You go to Keychain Access, create a new self-signed certificate, and set
> its permissions to always trust.

That still might not fix it though. If it doesn't work, you need to
[create a permissions file][perm-file]. The following should probably be fine:

[perm-file]: https://stackoverflow.com/questions/52699661/macos-mojave-how-to-achieve-codesign-to-enable-debugging-gdb

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.debugger</key>
    <true/>
</dict>
</plist>
```

Then you need to sign GDB with you newly created file. Assuming the above file
is named `gdb.xml`, and the certificate you made earlier is named `gdbcert`, you would write:

```shell
codesign --entitlements gdb.xml -fs gdbcert /usr/local/bin/gdb
```

This *should* get Mac to allow GDB to function; it will not, however, guarrantee
that GDB is usable.

### Ensuring Startup
If you've been doing everything correctly so far, you might still get an error like this:

```shell
During startup program terminated with signal ?, Unknown signal.
```

To fix this, you'll need to [disable GDB from using a shell command to start up
the program that you're debugging][dis-gdb-shell]. Create a file called `.gdbinit` in your user
folder (the path of the file will be `~/.gdbinit`), and add the following line:
[dis-gdb-shell]: https://github.com/Homebrew/homebrew-core/issues/5912

```shell
set startup-with-shell off
```

Then restart gdb, and it should at least start.

### Reducing Latency
The scope of this guide has ended. MacOS doesn't play well with GDB, and it's very
possible that you now have an installation of GDB that opens fine but *is still
completely unusable*. This is because [GDB doesn't work well with MacOS system
instructions][gdb-unusable]. In some cases, this can be fixed by downgrading to
GDB version 8.0.1; on Mojave, [this isn't the case][gdb-mojave-bad].

[gdb-unusable]: https://github.com/Homebrew/homebrew-core/issues/34750
[gdb-mojave-bad]: https://sourceware.org/bugzilla/show_bug.cgi?id=23949
