"""Build the offline runtime tree from explicit, versioned local distributions."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, sys, zipfile
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
ROOT=pathlib.Path(__file__).resolve().parents[1]

def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.is_file() and source.stat().st_size==target.stat().st_size and source.stat().st_mtime_ns==target.stat().st_mtime_ns:return
    shutil.copy2(source,target)

def tree(source,target):
    for base,dirs,files in os.walk(source):
        dirs[:]=[d for d in dirs if d!='__pycache__']
        for name in files:copy(pathlib.Path(base)/name,target/pathlib.Path(base).relative_to(source)/name)

def fields(path):
    parts=re.split(r'%([A-Z_]+)%\n',path.read_text(encoding='utf-8'))
    return {parts[i]:parts[i+1].strip().splitlines() for i in range(1,len(parts)-1,2)}

def gcc_distribution(msys,target,notices):
    packages={};providers={}
    for folder in (msys/'var/lib/pacman/local').iterdir():
        if not (folder/'desc').exists():continue
        meta=fields(folder/'desc');name=meta['NAME'][0];packages[name]=(folder,meta)
        for provide in meta.get('PROVIDES',[]):providers[re.split('[<>=]',provide)[0]]=name
    selected=set()
    def visit(name):
        name=providers.get(name,name) if name not in packages else name
        if name in selected:return
        if name not in packages:raise RuntimeError('Missing GCC dependency: '+name)
        selected.add(name)
        for dep in packages[name][1].get('DEPENDS',[]):visit(re.split('[<>=]',dep)[0])
    visit('mingw-w64-ucrt-x86_64-gcc')
    inventory=[]
    for name in sorted(selected):
        folder,meta=packages[name]
        for raw in fields(folder/'files').get('FILES',[]):
            rel=pathlib.PurePosixPath(raw)
            if not rel.parts or rel.parts[0]!='ucrt64' or '..' in rel.parts:raise RuntimeError('Unexpected package path: '+raw)
            source=msys/pathlib.Path(*rel.parts)
            if source.is_file():copy(source,target/pathlib.Path(*rel.parts[1:]))
        copy(folder/'desc',notices/'msys2-packages'/name/'desc')
        copy(folder/'files',notices/'msys2-packages'/name/'files')
        inventory.append({'name':name,'version':meta['VERSION'][0],'licenses':meta.get('LICENSE',[]),'upstream':meta.get('URL',[]),'sourcePackage':'https://repo.msys2.org/mingw/sources/'+meta.get('BASE',[name])[0]+'-'+meta['VERSION'][0]+'.src.tar.zst'})
    return inventory

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,default=ROOT/'.runtime/release/JudgeBox');p.add_argument('--msys',type=pathlib.Path,default=pathlib.Path(r'C:\msys64'));p.add_argument('--jdk',type=pathlib.Path,default=pathlib.Path(r'C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot'));p.add_argument('--cangjie',type=pathlib.Path,default=pathlib.Path(r'D:\Cangjie\cangjie'));p.add_argument('--python-zip',type=pathlib.Path,default=ROOT/'.runtime/downloads/python-3.14.9-embed-amd64.zip');a=p.parse_args()
    out=a.output.resolve();rt=out/'runtimes';notices=out/'notices'
    for path in [a.msys/'ucrt64/bin/g++.exe',a.jdk/'bin/javac.exe',a.cangjie/'bin/cjc.exe',a.python_zip]:
        if not path.is_file():raise RuntimeError('Missing required distribution input: '+str(path))
    for source in [ROOT,a.msys.resolve(),a.jdk.resolve(),a.cangjie.resolve(),a.python_zip.resolve()]:
        if source==out or source.is_relative_to(out):raise RuntimeError('Stage output must not contain a source directory: '+str(out))
    python_hash=hashlib.sha256(a.python_zip.read_bytes()).hexdigest()
    if python_hash!='3c01d7cfc666f746a6f064f60fb2156ab0ec464d3d738ab796371a46a9bb24a2':raise RuntimeError('Python archive SHA-256 does not match the official release')
    env=dict(os.environ);env['PATH']=str(a.msys/'ucrt64/bin')+os.pathsep+env.get('PATH','')
    gcc_version=subprocess.check_output([str(a.msys/'ucrt64/bin/g++.exe'),'-dumpfullversion'],env=env,text=True).strip()
    if gcc_version!='16.1.0':raise RuntimeError('Expected GCC 16.1.0, got '+gcc_version)
    if 'JAVA_VERSION="21.0.11"' not in (a.jdk/'release').read_text():raise RuntimeError('Expected Temurin JDK 21.0.11')
    cangjie_version=subprocess.check_output([str(a.cangjie/'bin/cjc.exe'),'--version'],text=True,errors='replace')
    if '1.2.0' not in cangjie_version:raise RuntimeError('Expected Cangjie 1.2.0, got '+cangjie_version)
    stage_owner=out/'.judgebox-stage-owner'
    if out.exists() and any(out.iterdir()):
        if not stage_owner.is_file() or stage_owner.read_text()!='JudgeBox stage v1':raise RuntimeError('Existing output is not a JudgeBox-owned stage; select an empty --output directory')
        # Resolved absolute output is marker-verified, and cannot contain any source path.
        shutil.rmtree(out)
    rt.mkdir(parents=True,exist_ok=True);stage_owner.write_text('JudgeBox stage v1')
    (rt/'bundle-owner.txt').write_text('JudgeBox.OfflineToolchains',encoding='ascii')
    print('Staging GCC and transitive dependencies',flush=True)
    gcc=gcc_distribution(a.msys.resolve(),rt/'gcc',notices)
    print('Staging Temurin JDK',flush=True);tree(a.jdk.resolve(),rt/'jdk')
    print('Staging Cangjie SDK',flush=True);tree(a.cangjie.resolve(),rt/'cangjie')
    print('Staging embedded Python',flush=True)
    with zipfile.ZipFile(a.python_zip) as archive:archive.extractall(rt/'python')
    (rt/'python/Lib/site-packages').mkdir(parents=True,exist_ok=True)
    (rt/'python/python314._pth').write_text('python314.zip\n.\nLib\\site-packages\nimport site\n',encoding='utf-8')
    copy(ROOT/'build/JudgeBox.exe',out/'JudgeBox.exe')
    copy(ROOT/'README.md',out/'README.md');copy(ROOT/'docs/输入生成规则.md',out/'docs/输入生成规则.md')
    copy(ROOT/'third_party/json.LICENSE.MIT',notices/'json.LICENSE.MIT')
    copy(ROOT/'tests/toolchain_matrix.py',out/'diagnostics/toolchain_matrix.py')
    (out/'Check-Toolchains.cmd').write_text('@echo off\r\n"%~dp0JudgeBox.exe" --self-test\r\npause\r\n',encoding='ascii')
    manifest={'format':1,'platform':'Windows 11 x64','tools':{'cpp':'gcc/bin/g++.exe','python':'python/python.exe','java':'jdk/bin/java.exe','javac':'jdk/bin/javac.exe','cangjie':'cangjie/bin/cjc.exe'},'versions':{'gcc':'16.1.0','python':'3.14.9','java':'Temurin 21.0.11+10','cangjie':'1.2.0'},'gccPackages':gcc,'sources':{'python':'https://www.python.org/downloads/release/python-3149/','java':'https://github.com/adoptium/temurin21-binaries/releases/tag/jdk-21.0.11%2B10','cangjie':'https://cangjie-lang.cn/download','gcc':'https://packages.msys2.org/package/mingw-w64-ucrt-x86_64-gcc'}}
    (rt/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (notices/'THIRD-PARTY.txt').write_text('JudgeBox invokes unmodified third-party tools as separate processes.\n\nGCC and dependencies: original licenses are under runtimes/gcc/share/licenses and package descriptions under notices/msys2-packages. Exact source package locations and versions are recorded in runtimes/manifest.json. When redistributing binaries, also provide corresponding sources as required by each license; source locations alone do not replace those obligations.\n\nTemurin OpenJDK: legal notices under runtimes/jdk/legal; source archive runtimes/jdk/lib/src.zip.\nCangjie: runtimes/cangjie/LICENSE and Open_Source_Software_Notice.docx.\nPython: runtimes/python/LICENSE.txt.\nPython packages: license metadata under runtimes/python/Lib/site-packages/*.dist-info.\n',encoding='utf-8')
    total=sum(f.stat().st_size for f in out.rglob('*') if f.is_file())
    print('Staged',out,'size MiB',round(total/1048576,1),'GCC packages',len(gcc),flush=True)

if __name__=='__main__':main()
