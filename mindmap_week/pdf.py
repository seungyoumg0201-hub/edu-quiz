from playwright.sync_api import sync_playwright
import subprocess,pathlib,re
D=['월','화','수','목','금'];res={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_page()
    for d in D:
        pg.goto(pathlib.Path(f'day_{d}.html').resolve().as_uri());pg.emulate_media(media='print')
        fs=11.5
        while fs>6.4:
            pg.evaluate(f"document.body.style.setProperty('--fs','{fs}pt')")
            out=f'{d}요일_위계도.pdf';pg.pdf(path=out,format='A4',landscape=True,print_background=True,margin={'top':'8mm','bottom':'8mm','left':'8mm','right':'8mm'})
            n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',out],capture_output=True,text=True).stdout).group(1))
            if n==1:break
            fs=round(fs-0.3,1)
        res[d]=(fs,n)
    pg.goto(pathlib.Path('교육학_위계도_요일별.html').resolve().as_uri());pg.set_viewport_size({'width':390,'height':844});pg.emulate_media(media='screen')
    pg.screenshot(path='미리보기_모바일.png')
    b.close()
print(res)
