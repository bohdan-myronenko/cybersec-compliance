ECS_MIN = [
    "@ts",      # timestamp (string or datetime upstream)
    "user",     # user / principal / account id
    "src_ip",   # source ip (if any)
    "dst_ip",   # destination ip (if any)
    "action",   # action verb (login, access, get, sudo, etc.)
    "status",   # status / result (success, fail, denied, ...)
    "resource", # target resource (path, service, db, etc.)
    "msg",      # short message
    "raw"       # raw line, truncated
]