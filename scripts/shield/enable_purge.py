#!/usr/bin/env python3
import json
from pathlib import Path
p = Path.home() / '.artifact_shield' / 'purge_config.json'
print('Config path:', p)
if not p.exists():
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{}')
conf = json.loads(p.read_text())
conf['enabled'] = True
conf['keep_commits'] = 5
conf['backup_enabled'] = True
conf['fail_safe'] = False
p.write_text(json.dumps(conf, indent=2))
print('Updated config:', json.dumps(conf, indent=2))
