"""End-to-end tests against the real compiled Windows executable."""
import json, subprocess, tempfile, time, urllib.request, urllib.error, pathlib, unittest, sys, os
EXE = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'build/JudgeBox.exe').resolve()
sys.argv = sys.argv[:1]
class API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='JudgeBox 测试 ')
        env = dict(os.environ)
        env['PATH'] = ';'.join(p for p in env['PATH'].split(';') if 'msys64' not in p.lower() and 'cangjie' not in p.lower())
        cls.proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', cls.temp.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8',env=env)
        line = cls.proc.stdout.readline().strip()
        if not line.startswith('http://127.0.0.1:'):
            cls.proc.terminate()
            raise RuntimeError('Server did not announce URL: '+line)
        cls.url, cls.token = line.split('/#')
    @classmethod
    def tearDownClass(cls):
        try: cls.call('/api/shutdown',{})
        finally:
            cls.proc.wait(timeout=10)
            cls.proc.stdout.close(); cls.proc.stderr.close(); cls.temp.cleanup()
    @classmethod
    def call(cls, path, obj=None, token=True):
        req=urllib.request.Request(cls.url+path, data=None if obj is None else json.dumps(obj).encode(), headers={'Content-Type':'application/json','X-JudgeBox-Token':cls.token if token else ''})
        with urllib.request.urlopen(req,timeout=10) as r: return json.load(r)
    def job(self, code, lang='cpp', **extra):
        payload={'source':code,'language':lang,'mode':'manual','cases':[{'input':'2 3\n','expected':'5'}], 'timeMs':1000,'memoryMb':256,**extra}
        self.call('/api/run',payload)
        deadline=time.monotonic()+90
        while time.monotonic()<deadline:
            result=self.call('/api/status')
            if result['done']: return result
            time.sleep(.05)
        self.fail('job timeout')
    def test_01_auth(self):
        with self.assertRaises(urllib.error.HTTPError) as c: self.call('/api/config',token=False)
        self.assertEqual(c.exception.code,403)
        c.exception.close()
        request=urllib.request.Request(self.url+'/api/config',headers={'X-JudgeBox-Token':self.token,'Origin':'https://example.com'})
        with self.assertRaises(urllib.error.HTTPError) as c: urllib.request.urlopen(request)
        self.assertEqual(c.exception.code,403); c.exception.close()
    def test_02_verdicts(self):
        cpp='#include <iostream>\nint main(){long long a,b;std::cin>>a>>b;std::cout<<a+b;}'
        for code, expected, options in [
            (cpp,'AC',{}),(cpp,'WA',{'cases':[{'input':'2 3','expected':'6'}]}),
            ('int main(){broken syntax}','CE',{}),('int main(){for(;;){}}','TLE',{'timeMs':80}),
            ('int main(){return 7;}','RE',{}),
            ('#include <cstdio>\nint main(){for(;;) puts("xxxxxxxxxxxxxxxx");}','OLE',{'outputKb':8}),
            (cpp,'RUN',{'cases':[{'input':'1 4','expected':None}]}),
        ]:
            with self.subTest(expected=expected):
                result=self.job(code,**options)
                self.assertEqual(result['verdict'],expected,str(result))
    def test_03_stress(self):
        rule={'steps':[{'type':'line','items':[{'min':1,'max':10},{'min':1,'max':10}]}]}
        cpp='#include <iostream>\nint main(){int a,b;std::cin>>a>>b;std::cout<<a+b;}'
        r=self.job('print(0)','python',mode='stress',reference=cpp,referenceLanguage='cpp',generator=rule,count=10,seed=42)
        self.assertEqual(r['verdict'],'WA'); self.assertEqual(r['completed'],1)
        detail=self.call('/api/case?index=0'); self.assertTrue(detail['input']); self.assertNotEqual(detail['stdout'].strip(),detail['expected'].strip())
        r=self.job(cpp,mode='stress',reference='raise RuntimeError("reference bad")',referenceLanguage='python',generator=rule,count=2)
        self.assertEqual(r['verdict'],'JE'); self.assertIn('参考',r['message'])
    def test_04_languages(self):
        config=self.call('/api/config')
        examples={
            'python':('print(sum(map(int,input().split())))','5'),
            'java':('import java.util.*; public class Main{public static void main(String[] a){Scanner s=new Scanner(System.in);System.out.println(s.nextInt()+s.nextInt());}}','5'),
            'cangjie':('main() { println("5") }','5')}
        for lang,(source,expected) in examples.items():
            if config['tools'].get(lang):
                with self.subTest(lang=lang):
                    result=self.job(source,lang,memoryMb=1024)
                    self.assertEqual(result['verdict'],'AC',str(result))
    def test_05_generator(self):
        spec={'generator':{'steps':[{'type':'int','min':1,'max':10}]},'seed':42,'index':0}
        self.assertEqual(self.call('/api/generate',spec),self.call('/api/generate',spec))
        r=self.job('print(input())','python',mode='generated',generator=spec['generator'],count=3)
        self.assertEqual(r['verdict'],'RUN'); self.assertEqual(r['completed'],3)
    def test_06_cancel(self):
        self.call('/api/run',{'language':'python','source':'while True: pass','mode':'manual','timeMs':30000,'cases':[{'input':'','expected':'0'}]})
        time.sleep(.2); self.call('/api/cancel',{})
        for _ in range(100):
            r=self.call('/api/status')
            if r['done']: break
            time.sleep(.05)
        self.assertEqual(r['verdict'],'CANCELLED')
    def test_07_python_generator(self):
        r=self.job('print(input())','python',mode='generated',generatorMode='python',generatorSource='import sys,random\nr=random.Random(int(sys.argv[1])+int(sys.argv[2]));print(r.randint(1,10))',count=2)
        self.assertEqual(r['verdict'],'RUN')
        r=self.job('print(1)','python',mode='generated',generatorMode='python',generatorSource='raise ValueError("bad gen")',count=1)
        self.assertEqual(r['verdict'],'JE')
    def test_08_mle(self):
        code='#include <windows.h>\nint main(){for(;;){void* p=VirtualAlloc(0,4194304,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);if(!p)return 9;}}'
        self.assertEqual(self.job(code,memoryMb=32)['verdict'],'MLE')
    def test_09_java_heap(self):
        if not self.call('/api/config')['tools'].get('java'): self.skipTest('Java unavailable')
        code='public class Main{public static void main(String[] a){byte[] x=new byte[300*1024*1024];System.out.println(x.length);}}'
        r=self.job(code,'java',memoryMb=1024,cases=[{'input':'','expected':str(300*1024*1024)}])
        self.assertEqual(r['verdict'],'AC',str(r))
    def test_10_edge_cases(self):
        for code,expected,options in [
            ('import sys;print("debug",file=sys.stderr);print(5)','AC',{}),
            ('pass','AC',{'cases':[{'input':'','expected':''}]}),
            ('print(5)','WA',{'cases':[{'input':'','expected':''}]}),
            ('print("1.00000001")','AC',{'checker':'float','cases':[{'input':'','expected':'1'}]}),
            ('print("5 ")','WA',{'checker':'exact','cases':[{'input':'','expected':'5'}]}),
            ('print(5)','WA',{'cases':[{'input':'','expected':'0'},{'input':'','expected':'5'}]}),
        ]:
            with self.subTest(code=code,expected=expected):
                r=self.job(code,'python',**options); self.assertEqual(r['verdict'],expected,str(r))
                if len(options.get('cases',[]))==2: self.assertEqual(r['completed'],2)
        r=self.job('print(5)','python',tools={'python':r'Z:\missing_python.exe'})
        self.assertEqual(r['verdict'],'JE')
        rule={'steps':[{'type':'line','items':[1,2]}]}
        r=self.job('print(5)','python',mode='stress',reference='bad source',referenceLanguage='cpp',generator=rule,count=1)
        self.assertEqual(r['verdict'],'JE'); self.assertIn('参考程序 CE',r['message'])
        r=self.job('print(5)','python',mode='generated',generator={'steps':[{'type':'graph','nodes':2,'edges':99}]},count=1)
        self.assertEqual(r['verdict'],'JE')
if __name__=='__main__': unittest.main(verbosity=2)
