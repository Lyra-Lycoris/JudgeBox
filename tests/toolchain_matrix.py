"""Real toolchain matrix; no missing-language skips. Works on staged or installed JudgeBox."""
import argparse, json, os, pathlib, subprocess, tempfile, time, urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')

SOURCES = {
    'cpp': {
        'io': '#include <iostream>\n#include <string>\nint main(){std::string s;std::getline(std::cin,s);std::cout<<s;}',
        'library': '#include <bits/stdc++.h>\nint main(){std::vector<int> a={4,1,3,2};std::sort(a.begin(),a.end());std::cout<<std::accumulate(a.begin(),a.end(),0);}',
        'ce': 'int main(){ invalid syntax }', 're': 'int main(){return 7;}',
        'tle': 'int main(){for(;;){}}',
        'ole': '#include <cstdio>\nint main(){for(;;)puts("xxxxxxxxxxxxxxxxxxxxxxxx");}'},
    'python': {
        'io': 'import sys;print(sys.stdin.readline().strip())',
        'library': 'import sqlite3,ssl,decimal,hashlib,ctypes,json\nc=sqlite3.connect(":memory:");print(sum(sorted([4,1,3,2])))',
        'ce': 'def broken(: pass', 're': 'raise RuntimeError("expected test exception")',
        'tle': 'while True: pass', 'ole': 'while True: print("xxxxxxxxxxxxxxxxxxxxxxxx")'},
    'java': {
        'io': 'import java.io.*;public class Main{public static void main(String[] a)throws Exception{System.out.println(new BufferedReader(new InputStreamReader(System.in,"UTF-8")).readLine());}}',
        'library': 'import java.util.*;public class Main{public static void main(String[] a){System.out.println(Arrays.stream(new int[]{4,1,3,2}).sorted().sum());}}',
        'ce': 'public class Main{broken syntax}',
        're': 'public class Main{public static void main(String[] a){throw new RuntimeException("expected");}}',
        'tle': 'public class Main{public static void main(String[] a){while(true){}}}',
        'ole': 'public class Main{public static void main(String[] a){while(true)System.out.println("xxxxxxxxxxxxxxxxxxxxxxxx");}}'},
    'cangjie': {
        'io': 'import std.console.*\nmain(){let s=Console.stdIn.readln();println(s ?? "")}',
        'library': 'main(){var sum:Int64=0;for(x in [1,2,3,4]){sum+=x};println(sum)}',
        'ce': 'main(){ invalid syntax }', 're': 'main():Int64{return 7}',
        'tle': 'main(){while(true){}}', 'ole': 'main(){while(true){println("xxxxxxxxxxxxxxxxxxxxxxxx")}}'}
}

class Client:
    def __init__(self,exe,data,clean=False):
        env=dict(os.environ)
        if clean:
            env['PATH']=str(pathlib.Path(env.get('SystemRoot',r'C:\Windows'))/'System32')
            for key in list(env):
                if key.upper().startswith(('PYTHON','CANGJIE','CJNATIVE','JAVA_HOME','JDK_HOME','CLASSPATH','JAVA_TOOL_OPTIONS','JDK_JAVA_OPTIONS','_JAVA_OPTIONS','GCC_EXEC_PREFIX','COMPILER_PATH','LIBRARY_PATH','CPATH','CPLUS_INCLUDE_PATH','C_INCLUDE_PATH')): env.pop(key,None)
        self.proc=subprocess.Popen([str(exe),'--no-browser','--data-dir',str(data)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
        line=self.proc.stdout.readline().strip()
        if not line.startswith('http://127.0.0.1:'): raise RuntimeError('startup failed: '+line)
        self.base,self.token=line.split('/#')
    def api(self,path,body=None):
        req=urllib.request.Request(self.base+path,data=None if body is None else json.dumps(body).encode(),headers={'Content-Type':'application/json','X-JudgeBox-Token':self.token})
        with urllib.request.urlopen(req,timeout=15) as r:return json.load(r)
    def run(self,lang,source,expected='10',input='',wanted='AC',time_ms=2000,output_kb=1024,**extra):
        self.api('/api/run',{'source':source,'language':lang,'mode':'manual','cases':[{'input':input,'expected':expected}], 'timeMs':time_ms,'memoryMb':1024,'outputKb':output_kb,**extra})
        end=time.monotonic()+100
        while time.monotonic()<end:
            r=self.api('/api/status')
            if r['done']:
                ok=r['verdict']==wanted
                result={'passed':ok,'expected':wanted,'actual':r['verdict'],'message':r['message'],'compileLog':r.get('compileLog',''),'directory':r.get('directory','')}
                if not ok and r.get('cases'):result['detail']=self.api('/api/case?index=0')
                return result
            time.sleep(.08)
        raise TimeoutError('job did not complete')
    def close(self):
        try:self.api('/api/shutdown',{});self.proc.wait(timeout=15)
        finally:
            if self.proc.poll() is None:self.proc.terminate();self.proc.wait(timeout=10)
            self.proc.stdout.close();self.proc.stderr.close()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('exe',type=pathlib.Path);ap.add_argument('--clean',action='store_true');ap.add_argument('--bundled',action='store_true');ap.add_argument('--report',type=pathlib.Path,default=pathlib.Path('build/toolchain-report.json'));args=ap.parse_args()
    exe=args.exe.resolve();args.report.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='JudgeBox matrix 中文 ') as temp:
        client=Client(exe,pathlib.Path(temp),args.clean);report={'exe':str(exe),'cleanEnvironment':args.clean,'tools':{},'checks':[]}
        try:
            report['tools']=client.api('/api/config')['tools']
            for lang,programs in SOURCES.items():
                for kind,source in programs.items():
                    options={'wanted':{'ce':'CE','re':'RE','tle':'TLE','ole':'OLE'}.get(kind,'AC')}
                    if kind=='io':options.update(input='JudgeBox 中文 123\n',expected='JudgeBox 中文 123')
                    if kind=='tle':options['time_ms']=300
                    if kind=='ole':options.update(output_kb=8,time_ms=5000)
                    result=client.run(lang,source,**options);result.update(language=lang,test=kind);report['checks'].append(result)
                    print(lang,kind,'PASS' if result['passed'] else 'FAIL',result['actual'],flush=True)
                    if not result['passed']: print(result['message'],result['compileLog'][-3000:],flush=True)
            if args.bundled:
                prefix=str(exe.parent/'runtimes').lower()
                for key,path in report['tools'].items():
                    ok=str(pathlib.Path(path).resolve()).lower().startswith(prefix+os.sep.lower())
                    report['checks'].append({'language':key,'test':'bundled-path','passed':ok,'path':path})
                source='import sys,random\nfrom cyaron import Graph\nrandom.seed(int(sys.argv[1])+int(sys.argv[2]));print(4);print(Graph.tree(4))'
                r=client.run('python','print(input())',wanted='RUN',generatorMode='python',generatorSource=source,mode='generated',count=2)
                r.update(language='python',test='cyaron-generator');report['checks'].append(r)
        finally:client.close()
        report['passed']=all(x['passed'] for x in report['checks']);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print('Report:',args.report,'PASS' if report['passed'] else 'FAIL')
        return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
