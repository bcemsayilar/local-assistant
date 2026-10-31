import os, json, time, base64, subprocess, urllib.request, urllib.error, hashlib, re
ENV = {}
# Once kasa (secrets-management.md), yoksa eski yer vidberry/.env
for _f in ('~/.config/parallax/secrets/apple.env', '~/Mac-Projects/vidberry/.env'):
    if not os.path.isfile(os.path.expanduser(_f)): continue
    for l in open(os.path.expanduser(_f)):
        m = re.match(r'^(ASC_[A-Z_]+)=(.*)$', l.strip())
        if m and m.group(1) not in ENV: ENV[m.group(1)] = m.group(2).strip().strip('"').strip("'")
KEY = os.path.expanduser(ENV['ASC_PRIVATE_KEY_PATH'])
def b64(b): return base64.urlsafe_b64encode(b).rstrip(b'=')
def der_to_raw(der):
    assert der[0]==0x30
    i=2 if der[1]<0x80 else 3
    assert der[i]==2; rl=der[i+1]; r=der[i+2:i+2+rl]; i=i+2+rl
    assert der[i]==2; sl=der[i+1]; s=der[i+2:i+2+sl]
    r=r.lstrip(b'\0').rjust(32,b'\0'); s=s.lstrip(b'\0').rjust(32,b'\0'); return r+s
_tok=[0,None]
def token():
    if time.time()-_tok[0] < 900 and _tok[1]: return _tok[1]
    h=b64(json.dumps({'alg':'ES256','kid':ENV['ASC_KEY_ID'],'typ':'JWT'}).encode())
    p=b64(json.dumps({'iss':ENV['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1100,'aud':'appstoreconnect-v1'}).encode())
    si=h+b'.'+p
    der=subprocess.run(['openssl','dgst','-sha256','-sign',KEY],input=si,capture_output=True,check=True).stdout
    _tok[:]=[time.time(), (si+b'.'+b64(der_to_raw(der))).decode()]; return _tok[1]
def api(method, path, body=None, raw_url=False):
    url = path if raw_url else 'https://api.appstoreconnect.apple.com'+path
    req=urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization':'Bearer '+token(),'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            d=r.read(); return json.loads(d) if d else {}
    except urllib.error.HTTPError as e:
        return {'_error':e.code,'_body':e.read().decode()[:1500]}
def upload_ops(ops, data):
    for o in ops:
        chunk=data[o['offset']:o['offset']+o['length']]
        hdr={h['name']:h['value'] for h in o['requestHeaders']}
        req=urllib.request.Request(o['url'], method=o['method'], data=chunk, headers=hdr)
        urllib.request.urlopen(req).read()
def md5(b): return hashlib.md5(b).hexdigest()
