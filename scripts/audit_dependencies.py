"""Audit direct PE imports in the executables/libraries used by the judge toolchains."""
import argparse, json, pathlib, struct, os

SYSTEM=set('kernel32.dll ntdll.dll user32.dll advapi32.dll ole32.dll oleaut32.dll shell32.dll shlwapi.dll ws2_32.dll msvcrt.dll ucrtbase.dll gdi32.dll comdlg32.dll comctl32.dll secur32.dll crypt32.dll bcrypt.dll bcryptprimitives.dll winmm.dll version.dll winhttp.dll wininet.dll normaliz.dll psapi.dll dbghelp.dll iphlpapi.dll netapi32.dll userenv.dll profapi.dll powrprof.dll setupapi.dll imm32.dll uxtheme.dll dwmapi.dll dwrite.dll d2d1.dll opengl32.dll glu32.dll usp10.dll msimg32.dll winscard.dll dnsapi.dll cabinet.dll mpr.dll rpcrt4.dll wtsapi32.dll winspool.drv mswsock.dll cryptbase.dll ncrypt.dll sensapi.dll wevtapi.dll authz.dll wldap32.dll rasapi32.dll wintrust.dll dwmapi.dll hid.dll msasn1.dll d3d9.dll d3d11.dll dxgi.dll windowscodecs.dll oleacc.dll dsound.dll avrt.dll win32u.dll msacm32.dll dwmapi.dll pdh.dll dbgeng.dll urlmon.dll propsys.dll winrnr.dll d3dcompiler_47.dll dhcpcsvc.dll dhcpcsvc6.dll nsi.dll winbrand.dll'.split())
SYSTEM.add('msi.dll')

def imports(path):
    b=path.read_bytes()
    if b[:2]!=b'MZ':return []
    pe=struct.unpack_from('<I',b,0x3c)[0]
    if b[pe:pe+4]!=b'PE\0\0':return []
    sections=struct.unpack_from('<H',b,pe+6)[0];size=struct.unpack_from('<H',b,pe+20)[0];opt=pe+24
    magic=struct.unpack_from('<H',b,opt)[0];directory=opt+(112 if magic==0x20b else 96)
    import_rva=struct.unpack_from('<I',b,directory+8)[0]
    if not import_rva:return []
    table=opt+size
    def offset(rva):
        for i in range(sections):
            vs,va,raw_size,raw=struct.unpack_from('<IIII',b,table+i*40+8)
            if va<=rva<va+max(vs,raw_size):return raw+rva-va
        raise ValueError('Invalid import RVA in '+str(path))
    pos=offset(import_rva);result=[]
    while any(b[pos:pos+20]):
        name=offset(struct.unpack_from('<I',b,pos+12)[0]);end=b.index(0,name)
        result.append(b[name:end].decode('ascii').lower());pos+=20
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=pathlib.Path);ap.add_argument('--report',type=pathlib.Path,required=True);a=ap.parse_args();root=a.directory.resolve();rt=root/'runtimes'
    groups={
        'gcc':list((rt/'gcc').rglob('*.exe'))+list((rt/'gcc').rglob('*.dll')),
        'python':[f for f in (rt/'python').rglob('*') if f.suffix.lower() in ('.exe','.dll','.pyd')],
        'jdk':[f for f in (rt/'jdk/bin').rglob('*') if f.suffix.lower() in ('.exe','.dll')],
        'cangjie':[f for folder in ['bin','runtime','lib'] for f in (rt/'cangjie'/folder).rglob('*') if f.suffix.lower() in ('.exe','.dll')],
        'app':[root/'JudgeBox.exe']}
    for name in ['llc.exe','ld.lld.exe','lld-link.exe','lld.exe']:
        p=rt/'cangjie/third_party/llvm/bin'/name
        if p.exists():groups['cangjie'].append(p)
    report={'scope':'Direct PE imports for judge-used components; optional SDK developer tools and dynamic LoadLibrary paths are not a clean-VM proof.','checked':0,'missing':[]}
    for group,files in groups.items():
        search=[rt/group/'bin']
        if group=='jdk':search.append(rt/'jdk/bin/server') # JVM launcher loads this explicitly before java.dll.
        if group=='python':search=[rt/'python']
        if group=='cangjie':search=[rt/'cangjie'/p for p in ['bin','lib/windows_x86_64_cjnative','runtime/lib/windows_x86_64_cjnative','tools/bin','tools/lib','third_party/llvm/bin']]
        for path in files:
            available={f.name.lower() for folder in [path.parent,*search] if folder.exists() for f in folder.iterdir() if f.is_file()}
            report['checked']+=1
            for dll in imports(path):
                if dll in available or dll.startswith(('api-ms-win-','ext-ms-win-')) or dll in SYSTEM:continue
                report['missing'].append({'file':str(path.relative_to(root)),'dependency':dll})
    report['passed']=not report['missing'];a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
