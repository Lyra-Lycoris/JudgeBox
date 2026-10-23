"""Create the release file inventory and copy the verification evidence."""
import argparse, hashlib, importlib.metadata, json, pathlib, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('stage',type=pathlib.Path);a=p.parse_args();stage=a.stage.resolve();rt=stage/'runtimes'
    packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions(path=[str(rt/'python/Lib/site-packages')])}
    expected={'cyaron':'0.7.0','colorful':'0.5.8','colorama':'0.4.6','xeger':'0.4.0'}
    if any(packages.get(k)!=v for k,v in expected.items()):raise RuntimeError('Python package lock mismatch: '+str(packages))
    manifest=json.loads((rt/'manifest.json').read_text(encoding='utf-8'));manifest['pythonPackages']=packages
    for key,rel in manifest['tools'].items():
        manifest.setdefault('entrypointSha256',{})[key]=hashlib.sha256((rt/rel).read_bytes()).hexdigest()
    (rt/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    validation=stage/'validation';validation.mkdir(exist_ok=True)
    required=['toolchain-local-report.json','toolchain-bundled-report.json','pe-dependencies-report.json']
    optional=['toolchain-installed-unicode-report.json']
    for name in required+optional:
        report_path=ROOT/'build'/name
        if name in optional and not report_path.is_file():
            continue
        report=json.loads(report_path.read_text(encoding='utf-8'))
        if not report.get('passed'):raise RuntimeError('Cannot release with failed report '+name)
        shutil.copy2(report_path,validation/name)
    files={}
    for file in sorted(stage.rglob('*')):
        if not file.is_file() or file.suffix=='.pyc' or file.name in ('file-sha256.json','.judgebox-stage-owner'):continue
        files[file.relative_to(stage).as_posix()]={'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'bytes':file.stat().st_size}
    (rt/'file-sha256.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
    print('Release inventory:',len(files),'files,',round(sum(x['bytes'] for x in files.values())/1048576,1),'MiB')
if __name__=='__main__':main()
