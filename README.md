# antlr4_tex2sym

antlr4_tex2sym parses LaTeX math expressions and converts it into the equivalent SymPy form by using antlr4.  

Author:Akira Hakuta,  Date: 2019/04/09 

## Installation (windows)

Python3 : <https://www.python.org/downloads/windows/>  
SymPy : <http://www.sympy.org/en/index.html>  
ANTLR : <http://www.antlr.org>  (antlr4-python3-runtime 4.7.2)
```
> pip install sympy
> pip install antlr4-python3-runtime 
```


## Usage  
Open Command Prompt
```
> python.exe antlr4_tex2sym.py
```

```
tex2sym: LaTeX math expression --> SymPy form
-2-3+4 --> (-1)*2-3+4
2\\times3^4 --> 2*3**4
0.5 \\times 3 \\div 5a\\cdot 4 --> nsimplify(0.5)*3*5**(-1)*a*4
2\\times3! --> 2*factorial(3)
2ab^2(x+y)^3 --> 2*a*b**2*(x+y)**3
\\sqrt{3x} --> sqrt(3*x)
\\frac{2}{3}a --> (2)*(3)**(-1)*a
\\sin {\\ppi x} --> sin(S.Pi*x)
\\log{\\ee^3} --> log(S.Exp1**3)
\\frac{d}{dx}{x^5} --> diff(x**5,x)
\\int{\\sin^{2}{\\theta} d\\theta} --> integrate((sin(ttheta))**(2),ttheta)
\\sum_{k=1}^{n}{k^3} --> summation(k**3,(k,1,n))
2x^2+3x+4=0 --> Eq(2*x**2+3*x+4,0)
3x^2-4x+5 \\geqq 0 --> 3*x**2-4*x+5>=0
\\frac{d^{2}}{dx^{2}}{f(x)}=-f(x) --> Eq(diff(f(x),x,2),(-1)*f(x))
\\alpha\\beta\\gamma...\\omega\\ppi --> aalpha*bbeta*ggamma*...*oomega*S.Pi
...
```

### latex_example/example.tex  
**Installation**  
TeX Live:  <http://www.tug.org/texlive/acquire-netinstall.html>  
pygments: `> pip install pygments`  

```
> pdflatex.exe -synctex=1 -interaction=nonstopmode example.tex  
> pythontex.exe example.tex  
> pdflatex.exe -synctex=1 -interaction=nonstopmode example.tex
```
### ls_calc.py  
LaTeX SymPy Caluculator (calculator with LaTeX expression Form by using SymPy)   
&nbsp;   
**Installation**    
PyQt4: `> pip install PyQt4‑4.11.4‑cp37‑cp37m‑win_amd64.whl`  
matplotlib: `> pip install matplotlib`   
&nbsp;  
`> pythonw.exe ls_calc.p`  
File -> Open -> DEMO.slc  
&nbsp;  
If it does not work, download Microsoft Visual C\+\+ 2015 Redistributable.  
&nbsp;  
If you want to convert ls_calc.py to .exe files,  
`> pip install cx_Freeze `   
`> python.exe setup.py `   

### ChangeLog  

#### 2019-04-09  
##### Added
- TeX2Sym.g4  
`LATEX_SP  :   ('\\!'|'\\,'|'\\:'|'\\;'|'~') -> skip ;`  


----------------------------
### in Japanese

#### antlr4_tex2sym は LaTeX の数式コードを解析して、SymPy のコード変換する Python のプログラムです。  
すでに、 
LaTeX2SymPy <https://github.com/augustt198/latex2sympy> があります。  
今回、 antlr4 で生成される Visitor.py を用いて作ってみました。  


#### 各ソフトのインスツール   

##### Python3 (+ SymPy,ANTLR4)
まず、<https://www.python.org/downloads/windows/> に入って、  
Python3 をインスツールして下さい。  
コマンドプロンプトで  
pip install sympy  
pip install antlr4-python3-runtime  
と打ち込む。Successfully installed ...　と表示されればOK!   
\Python37\Lib\site-packagesのなかにパッケージのフォルダができる。   
ANTLR4 は antlr4-python3-runtime 4.7.2 です。  



#### 使い方  
`> python.exe antlr4_tex2sym.py`  
を実行。出力を見て下さい。  

※ LaTeX の数式コード texexpr は  
```
# variable : a,b,...,z, A,B,..,Z, \\alpha, \\beta,..,\pi,... , \\omega (except E, I, N, O, S, zeta, omicron)
# math constant : pi; --> \\ppi, i --> \\ii, e --> \\ee
# LaTeX Code Style: \\sin{x},  \\log\_{2}{8}, \\sum\_{k=1}\^{n}{k(k+1)\^2},...
```
の形で入力。  

  

#### LaTeX SymPy Caluculator (ls_calc.py) について   
LaTeX SymPy Caluculator は入出力が LaTeX 数式コード の電卓です。  
試用版です。不具合等はお許しください！   

LaTeX 数式コード入力 の数式処理としては、  
wolframalpha: <https://www.wolframalpha.com> があります。  
Mathematica でもできる筈です。  

PyQt4, matplotlib を pip でインストールし、  
`> pythonw.exe ls_calc.py`     
「LaTeX SymPy Caluculator」の青い画面が出る筈です。   

( 何も画面に表示されない場合は、  
ImportError: DLL load failed: 指定されたモジュールが見つかりません、かもしれません。  
「Visual Studio 2015 の Visual C++ 再頒布可能パッケージ」をインストールしてみてください。 )  

Input に(2x+3y)^4 と入力、  
Calculation の項目 expand を click、  
Output にSymPy で数式処理した結果が表示されます。  
処理できないコードの場合は、原則として「None」が表示されます。  

File Open で DEMO.slc を開いてみて下さい。  
view mode ON にして、 LaTeX Expression Table の各項目をclick すると、  
各行が Input, Calculation, Output に表示されます。  

 

**SymPy について**  
SymPy は漸化式については error ではなく、誤答を出力することがあります。  
 a_{n+1}=2a_{n}+n-1 & a_1=1  --> a_n=\frac{2^{n}}{2} + \frac{n}{2} - \frac{1}{2}  
正解は、a_n= 2^n - n です。  
何か変だ、と思ったら、Maxima で確認を！  

**.exe file の作成**  
cx_Freeze をインストール(pip install cx_Freeze)し、  
`> python.exe setup.py `   
ls_calc.exe を含む、フォルダー `ls_calc` ができます。  

**matplotlib のLaTeX表示について**  
```
matplotlib.rcParams['mathtext.fontset'] = 'cm' # to revert to old style (matplotlib 1.5)
matplotlib.rcParams['mathtext.rm'] = 'serif' # to revert to old style (matplotlib 1.5)
```  
とすると、matplotlib 1.5 style の綺麗なLaTeX の表示になります！  

