import sys, base64, subprocess, os
# usage: jsup.py FILE MIME  -> injects file into the first matching <input type=file accept*=png> on the current Safari tab
path, mime = sys.argv[1], sys.argv[2]
b = base64.b64encode(open(path,'rb').read()).decode()
def js(code):
    r = subprocess.run(['/tmp/claude-501/sj.sh', code], capture_output=True, text=True); return r.stdout.strip()
js('window.__b=""; "reset"')
N=150000
for i in range(0,len(b),N):
    js(f'window.__b+="{b[i:i+N]}"; window.__b.length')
print('len', js('window.__b.length'), 'expected', len(b))
name=os.path.basename(path)
print(js(f'''(function(){{var bin=atob(window.__b); var u=new Uint8Array(bin.length); for(var i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
var f=new File([u],"{name}",{{type:"{mime}"}}); var inp=[...document.querySelectorAll("input[type=file]")].find(x=>(x.accept||"").indexOf("png")>=0);
var dt=new DataTransfer(); dt.items.add(f); inp.files=dt.files; inp.dispatchEvent(new Event("input",{{bubbles:true}})); inp.dispatchEvent(new Event("change",{{bubbles:true}})); return "set "+inp.files.length+" "+f.size}})()'''))
