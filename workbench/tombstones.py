def get_tombstones():
  return [("/data/tombstones/"+fn, int(os.stat("/data/tombstones/"+fn).st_ctime) )
          for fn in os.listdir("/data/tombstones") if fn.startswith("tombstone")]

def get_tombstone(fn):
  mtime = os.path.getmtime(fn)
  with open(fn, "r") as f:
    dat = f.read()

  # see system/core/debuggerd/tombstone.cpp
  parsed = re.match(r"[* ]*\n"
                    r"(?P<header>CM Version:[\s\S]*?ABI:.*\n)"
                    r"(?P<thread>pid:.*\n)"
                    r"(?P<signal>signal.*\n)?"
                    r"(?P<abort>Abort.*\n)?"
                    r"(?P<registers>\s+x0[\s\S]*?\n)\n"
                    r"(?:backtrace:\n"
                      r"(?P<backtrace>[\s\S]*?\n)\n"
                      r"stack:\n"
                      r"(?P<stack>[\s\S]*?\n)\n"
                    r")?", dat)

  # logtail = re.search(r"--------- tail end of.*\n([\s\S]*?\n)---", dat)
  # logtail = logtail and logtail.group(1)

  if parsed:
    parsedict = parsed.groupdict()
    message = parsedict.get('thread') or ''
    message += parsedict.get('signal') or  ''
    message += parsedict.get('abort') or ''
  else:
    parsedict = {}
    message = fn+"\n"+dat[:1024]

  return parsedict