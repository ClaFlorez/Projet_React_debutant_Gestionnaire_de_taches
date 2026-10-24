from pathlib import Path
import math, subprocess, json, textwrap, shutil
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/'tp-react-corrige'
OUT.mkdir(parents=True,exist_ok=True)
QA=OUT/'verification'; QA.mkdir(exist_ok=True)
PROJECT=ROOT
TMP=ROOT/'docs'/'captures'/'originaux'
FONT=Path(r'C:\Windows\Fonts')
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()

def video():
    W,H,FPS=1280,720,20
    fonts={s:ImageFont.truetype(str(FONT/'arial.ttf'),s) for s in [20,22,24,26,28,30,32,38,42]}
    bold={s:ImageFont.truetype(str(FONT/'arialbd.ttf'),s) for s in [22,24,26,28,30,32,38,42]}
    scenes=[
      ('Deux villes qui communiquent', 'React affiche la page. FastAPI traite les demandes.', 'Dans ce TP, les deux villes sont sur le même ordinateur.', 'Deux programmes distincts', 'intro'),
      ('1  React prépare une demande', 'fetch(API_URL) envoie une requête GET /tasks.', 'GET signifie : lire les tâches, sans les modifier.', 'GET /tasks', 'request'),
      ('2  La requête traverse la route HTTP', 'La destination est http://127.0.0.1:8000/tasks.', 'HTTP définit les règles de cet échange.', 'GET /tasks', 'travel'),
      ('3  Uvicorn reçoit la requête', 'Uvicorn transmet la demande à l’application FastAPI.', 'FastAPI exécute la fonction associée à GET /tasks.', 'GET /tasks', 'server'),
      ('4  La réponse revient vers React', 'FastAPI renvoie la liste des tâches au format JSON.', 'Uvicorn envoie la réponse HTTP. Code 200 : réussite.', '200 + JSON', 'return'),
      ('5  React affiche les données', 'await response.json() lit le JSON, puis setTasks(data).', 'React recalcule l’interface et met la page à jour.', 'setTasks(data)', 'render'),
      ('Les autres voyages du CRUD', 'POST crée. GET lit. PATCH modifie. DELETE supprime.', 'Après une réponse réussie, React met son état à jour.', 'POST  GET  PATCH  DELETE', 'crud'),
      ('Où sont conservées les tâches ?', 'La liste Python reste en RAM tant que le serveur fonctionne.', 'Un redémarrage la réinitialise. Une base de données la conserverait.', 'RAM : stockage temporaire', 'memory'),
    ]
    def center(d,y,t,font,fill='#16304c',cx=640):
        d.text((cx,y),t,font=font,fill=fill,anchor='mt')
    def arrow(d,a,b,color,width=7):
        d.line([a,b],fill=color,width=width)
        ang=math.atan2(b[1]-a[1],b[0]-a[0])
        pts=[b,(b[0]-18*math.cos(ang-.5),b[1]-18*math.sin(ang-.5)),(b[0]-18*math.cos(ang+.5),b[1]-18*math.sin(ang+.5))]
        d.polygon(pts,fill=color)
    def truck(d,x,y,label,left=False,color='#087f8c'):
        x=int(x)
        if left:
            d.rounded_rectangle((x,y,x+58,y+67),10,fill=color)
            d.rectangle((x+12,y+8,x+42,y+30),fill='#cceaf8')
            d.rounded_rectangle((x+60,y-22,x+218,y+67),8,fill=color)
        else:
            d.rounded_rectangle((x,y-22,x+158,y+67),8,fill=color)
            d.rounded_rectangle((x+160,y,x+218,y+67),10,fill=color)
            d.rectangle((x+174,y+8,x+204,y+30),fill='#cceaf8')
        for wx in [x+38,x+180]:
            d.ellipse((wx-17,y+49,wx+17,y+83),fill='#20324c')
            d.ellipse((wx-7,y+59,wx+7,y+73),fill='#dbe6ef')
        center(d,y+2,label,fonts[20],'white',x+(139 if left else 79))
    def frame(idx,t):
        title,line1,line2,load,mode=scenes[idx]
        im=Image.new('RGB',(W,H),'#f6f9fc');d=ImageDraw.Draw(im)
        center(d,26,'LE VOYAGE D’UNE REQUÊTE',bold[24],'#087f8c')
        center(d,67,title,bold[38])
        d.rounded_rectangle((42,145,350,387),18,fill='#e1f3f7',outline='#087f8c',width=3)
        d.rounded_rectangle((930,145,1238,387),18,fill='#fff0df',outline='#c87620',width=3)
        center(d,164,'VILLE REACT',bold[28],cx=196)
        center(d,202,'Navigateur · port 5173',fonts[22],cx=196)
        d.rectangle((90,244,302,350),fill='white',outline='#16304c',width=3)
        if mode=='render' or mode=='crud' or mode=='memory':
            d.text((104,259),'Liste des tâches',font=bold[22],fill='#16304c')
            d.text((104,293),'Lire le rapport',font=fonts[20],fill='#16304c')
            d.line((103,306,233,306),fill='#16304c',width=2)
            d.text((104,320),'Vérifier les alertes',font=fonts[20],fill='#16304c')
        else:center(d,278,'Chargement…' if idx>0 else 'Interface',fonts[24],cx=196)
        center(d,164,'VILLE FASTAPI',bold[28],cx=1084)
        center(d,202,'Serveur · port 8000',fonts[22],cx=1084)
        d.rounded_rectangle((958,246,1210,349),10,fill='white',outline='#c87620',width=2)
        center(d,258,'Application FastAPI',bold[22],cx=1084)
        center(d,301,'tasks : liste Python',fonts[22],cx=1084)
        d.rectangle((862,294,922,389),fill='#16304c')
        d.text((892,345),'U',font=bold[32],fill='white',anchor='mm')
        center(d,259,'UVICORN',bold[22],cx=835)
        d.line((835,286,890,310),fill='#16304c',width=2)
        center(d,340,'ROUTE HTTP',bold[24])
        d.rectangle((0,402,1280,540),fill='#3e5065')
        for x in range(-100,1400,95):
            x=int(x-(t*35)%95)
            d.rectangle((x,468,x+48,473),fill='white')
        if mode in ['request','travel']:
            p=min(1,t/7)
            x=160+(660*p if mode=='travel' else 140*p)
            truck(d,x,393,'GET /tasks')
            arrow(d,(410,565),(850,565),'#087f8c')
        elif mode=='return':
            x=820-650*min(1,t/7)
            truck(d,x,450,'200 + JSON',True,'#c87620')
            arrow(d,(850,565),(410,565),'#c87620')
        elif mode=='server':
            truck(d,700,393,'GET /tasks')
            center(d,552,'GET /tasks  →  get_tasks()  →  liste Python',bold[26])
        elif mode=='render':
            truck(d,100,450,'JSON',True,'#c87620')
            center(d,552,'JSON  →  données JavaScript  →  setTasks  →  page',bold[26])
        elif mode=='crud':
            truck(d,280+350*math.sin(t*.45)**2,393,'REQUÊTE')
            truck(d,500-260*math.sin(t*.45)**2,450,'RÉPONSE',True,'#c87620')
        elif mode=='memory':
            center(d,424,'RAM du serveur : les modifications sont temporaires',bold[30],'white')
            center(d,486,'Arrêt / redémarrage → retour à la liste initiale',fonts[28],'white')
        else:
            truck(d,220+450*min(1,t/7),393,'REQUÊTE')
            arrow(d,(400,565),(880,565),'#087f8c')
        center(d,598,line1,bold[26])
        center(d,642,line2,fonts[24])
        d.rectangle((0,710,int(W*(idx*8+t)/64),720),fill='#087f8c')
        d.text((1215,692),f'{idx+1}/8',font=fonts[20],fill='#53667b',anchor='mm')
        return im
    dest=OUT/'Le_voyage_des_requetes.mp4'
    proc=subprocess.Popen([ffmpeg,'-y','-f','rawvideo','-vcodec','rawvideo','-s','1280x720','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE,stderr=(QA/'encodage.log').open('wb'))
    thumbs=[]
    for i in range(8):
        for n in range(8*FPS):
            im=frame(i,n/FPS)
            if n==4*FPS:
                im.save(QA/f'video-{i+1}.png');thumbs.append(im.copy())
            proc.stdin.write(im.tobytes())
        print('Video scene',i+1,flush=True)
    proc.stdin.close()
    if proc.wait()!=0:raise RuntimeError('Encodage échoué')
    sheet=Image.new('RGB',(1280,4*360),'white')
    for i,im in enumerate(thumbs):sheet.paste(im.resize((640,360)),((i%2)*640,(i//2)*360))
    sheet.save(QA/'video-planche.jpg')
    subprocess.run([ffmpeg,'-v','error','-i',str(dest),'-f','null','-'],check=True)
    return scenes

def pdf():
    for name,file in [('Arial','arial.ttf'),('ArialB','arialbd.ttf'),('Mono','consola.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
    P=OUT/'TP_React_corrige.pdf'; c=canvas.Canvas(str(P),pagesize=(612,792))
    c.setTitle('Corrigé du TP React Gestionnaire de tâches')
    c.setAuthor('')
    n=0;y=0
    style=ParagraphStyle('body',fontName='Arial',fontSize=10.5,leading=15,spaceAfter=8,textColor=HexColor('#172435'))
    def page(title,sub=''):
        nonlocal n,y
        if n:c.showPage()
        n+=1;y=722
        c.setFont('Arial',9);c.setFillColor(HexColor('#536477'));c.drawString(44,759,'TP REACT • CORRIGÉ EXPLIQUÉ')
        c.drawRightString(568,28,str(n))
        c.setFillColor(HexColor('#000000'));c.setFont('ArialB',21);c.drawString(44,y,title);y-=30
        if sub:para(sub)
    def para(text):
        nonlocal y
        p=Paragraph(text,style);_,h=p.wrap(524,700)
        if y-h<50:raise ValueError(f'Overflow page {n}: {text[:60]}')
        p.drawOn(c,44,y-h);y-=h+9
    def h(text):
        nonlocal y
        c.setFillColor(HexColor('#000000'));c.setFont('ArialB',12);c.drawString(44,y-5,text);y-=24
    def code(text):
        nonlocal y
        lines=[]
        for line in text.strip('\n').splitlines():
            lines.extend(textwrap.wrap(line,105,replace_whitespace=False,drop_whitespace=False) or [''])
        c.setFillColor(HexColor('#f0f3f6'));c.rect(44,y-len(lines)*11-12,524,len(lines)*11+8,fill=1,stroke=0)
        c.setFillColor(HexColor('#17374e'));c.setFont('Mono',8.4)
        for line in lines:c.drawString(52,y-12,line);y-=11
        y-=22
        if y<45:raise ValueError(f'Code overflow {n}')
    def shot(name,caption,maxh=240,region=None):
        nonlocal y
        file=(PROJECT/'docs'/'captures'/name) if name.endswith('.png') else TMP/f'codex-clipboard-{name}.png'
        im=Image.open(file);iw,ih=im.size
        # Clip in the PDF to show only the relevant response, without altering source captures.
        l,t,r,b=region or (0,0,iw,ih)
        scale=min(524/(r-l),maxh/(b-t)); w=(r-l)*scale; ht=(b-t)*scale
        x=44+(524-w)/2; bottom=y-ht
        c.saveState();p=c.beginPath();p.rect(x,bottom,w,ht);c.clipPath(p,stroke=0)
        c.drawImage(ImageReader(im),x-l*scale,bottom-(ih-b)*scale,width=iw*scale,height=ih*scale)
        c.restoreState();y-=ht+9
        para('<font size="9" color="#536477">'+caption+'</font>')
    REACT='7dfd23f9-c930-49d7-94a5-e877b8c0991f'
    page('Gestionnaire de tâches avec React','Corrigé pédagogique en français • Projet réalisé progressivement • Sans logo')
    para('Ce document reprend les étapes 0 à 9 du sujet « Projet React débutant - Gestionnaire de tâches » (7 pages) et répond à toutes les questions « À expliquer ». Il décrit le projet JavaScript réellement présent dans <b>src/App.jsx</b>, ainsi que son API FastAPI dans <b>api/main.py</b>.')
    h('Ce que le projet permet de comprendre')
    para('Une action dans le navigateur déclenche une requête HTTP. Uvicorn la reçoit et la transmet à FastAPI. FastAPI traite les données et renvoie une réponse JSON. React met alors son état à jour et actualise la page.')
    code('React → fetch → HTTP → Uvicorn → FastAPI\nReact ← response.json() ← réponse HTTP / JSON ← FastAPI\nsetTasks(data) → nouvel affichage')
    h('Comment lire les preuves')
    para('Les captures sont celles fournies pendant les essais. Elles représentent des moments différents du projet : la première interface ne comporte donc pas encore les boutons de suppression. Une capture commune peut illustrer plusieurs notions, sans prouver à elle seule chaque interaction.')
    para('Les quatre opérations de l’API ont été testées dans la documentation interactive. Le cycle final React a ensuite été vérifié dans le navigateur : création, rechargement, changement de statut, filtre et suppression. Quatre nouvelles captures documentent ces essais. Les contrôles de code, de compilation et d’API sont également passés sur GitHub.')
    h('Une différence avec la consigne')
    para('Le sujet initial utilise TypeScript et App.tsx. Le projet utilise JavaScript et App.jsx avec des commentaires JSDoc. Le bon état initial est donc <b>useState([])</b>, sans la syntaxe TypeScript &lt;Task[]&gt;.')
    h('Organisation du corrigé')
    para('Préparation et données • Composants et état • Formulaire • Statut et filtre • Effets • API • Chargement HTTP • CRUD • Mémoire et serveur • Code final en annexe')

    page('0 Préparer le projet','Fichiers concernés : package.json, src/main.jsx, src/App.jsx et environnement Python')
    para('Vite lance le serveur de développement de la page React. Uvicorn lance séparément le serveur de l’API. Les deux terminaux doivent rester actifs pendant les essais.')
    code('cd "C:\\Users\\H0PPR202\\Desktop\\intelligence-artificiel\\_TP1\\REACT\\react-tasks"\nnpm.cmd install\nnpm.cmd run dev')
    para('Dans cette réalisation, .venv a été créé dans le dossier parent REACT. Pour démarrer l’API dans un deuxième terminal :')
    code('cd "C:\\Users\\H0PPR202\\Desktop\\intelligence-artificiel\\_TP1\\REACT"\n.\\.venv\\Scripts\\Activate.ps1\ncd .\\react-tasks\npython -m uvicorn api.main:app --reload')
    shot('30efd50a-7b5a-4822-9016-d76f126b06ba','Capture fournie : installation réussie de FastAPI et Uvicorn dans .venv. La commande d’installation est python -m pip install fastapi "uvicorn[standard]".',160,region=(0,470,1461,633))
    h('Réponse à retenir')
    para('Un serveur est un programme qui reçoit des demandes et renvoie des réponses. Uvicorn est un véritable serveur HTTP. FastAPI définit les routes et les traitements de l’API. Le navigateur affiche React.')

    page('1 Comprendre les données','Fichier : javascript-basics.js')
    code('const tasks = [\n  { id: 1, title: "Lire le rapport", done: true },\n  { id: 2, title: "Vérifier les alertes", done: false },\n];\nconsole.log(tasks[0].title);\nconst remainingTasks = tasks.filter((task) => !task.done);\nconsole.log(remainingTasks.length);')
    h('Réponse expliquée')
    para('Un <b>tableau</b> est une collection ordonnée : ici, tasks contient plusieurs tâches. Un <b>objet</b> regroupe des propriétés nommées : chaque tâche possède id, title et done. tasks[0] est le premier objet du tableau et tasks[0].title est son titre.')
    para('filter conserve les objets pour lesquels la condition est vraie. !task.done signifie « la tâche n’est pas terminée ». Le résultat attendu est <b>Lire le rapport</b>, puis <b>1</b>.')
    para('<b>Vérification proposée :</b> exécuter node javascript-basics.js depuis la racine du projet. Aucune capture de cette exécution n’a été fournie ; les résultats ci-dessus sont calculés à partir du code, et non présentés comme une sortie capturée.')
    shot(REACT,'Capture commune de l’interface : les objets sont affichés sous forme de tâches. Elle illustre le modèle de données, sans remplacer le test de javascript-basics.js.',235)

    page('2 et 3 Composants props et état','Fichier : src/App.jsx')
    h('Un composant')
    para('Un composant est une fonction qui décrit une partie de l’interface en JSX. TaskHeader retourne le titre. App assemble les composants dans main. La majuscule permet à React de distinguer un composant, comme &lt;TaskHeader /&gt;, d’un élément HTML, comme &lt;h1&gt;.')
    code('function TaskHeader() {\n  return <h1>Gestionnaire de tâches</h1>\n}\n// Dans App :\nconst [tasks, setTasks] = useState([])\n// Dans la liste :\n<TaskItem key={task.id} task={task} onToggle={toggleTask}\n  onDelete={deleteTask} />')
    h('Une prop et un état')
    para('Une <b>prop vient du parent</b>. App fournit task à TaskItem. L’enfant la lit et reçoit également des fonctions pour signaler une action. <b>useState</b> conserve une valeur entre les rendus ; son setter demande un nouveau rendu. App possède tasks et TaskForm possède title.')
    para('Au début du parcours, tasks contenait deux tâches dans React. Depuis l’étape 8, tasks commence vide, puis reçoit les données de l’API. Le type Task du sujet devient un commentaire JSDoc dans ce projet JavaScript.')
    shot(REACT,'Capture commune des étapes 2 à 6 : le titre et la liste montrent les composants rendus. Le code explique la circulation des props.',200)

    page('4 Ajouter une tâche','Composants : TaskForm et App')
    para('Le champ est contrôlé : sa valeur vient de title. onChange copie chaque nouvelle saisie dans cet état. onSubmit appelle handleSubmit lorsque le formulaire est validé, y compris avec la touche Entrée.')
    code('const [title, setTitle] = useState(\'\')\n<input value={title}\n  onChange={(event) => setTitle(event.target.value)} />\n\nfunction handleSubmit(event) {\n  event.preventDefault()\n  const trimmedTitle = title.trim()\n  if (!trimmedTitle) return\n  onAdd(trimmedTitle)\n  setTitle(\'\')\n}')
    h('Réponses à expliquer')
    para('<b>onChange</b> réagit à la saisie. <b>onSubmit</b> réagit à la validation du formulaire. <b>event.preventDefault()</b> empêche le comportement HTML habituel qui rechargerait la page. trim enlève les espaces au début et à la fin ; le test suivant refuse un titre vide.')
    para('Flux : saisie → setTitle → validation → onAdd → addTask dans App. À l’étape 4, addTask ajoutait un objet local avec Date.now(). Dans la version finale, il envoie POST et utilise l’objet créé par le serveur.')
    shot(REACT,'Capture commune : le champ et le bouton Ajouter sont visibles. La création finale avec POST est expliquée à l’étape 9.',180)
    para('<b>Limite du code actuel :</b> le champ est vidé dès l’appel à onAdd, même si la requête échoue ensuite. La liste tasks, elle, n’est modifiée qu’après une réponse réussie.')

    page('5 Terminer et filtrer les tâches','États : tasks et remainingOnly')
    code('const visibleTasks = remainingOnly\n  ? tasks.filter((task) => !task.done)\n  : tasks\n\ncurrentTasks.map((t) => t.id === taskId ? updated : t)\n\n<TaskItem key={task.id} task={task}\n  onToggle={toggleTask} onDelete={deleteTask} />')
    h('map et filter')
    para('<b>map</b> produit un résultat pour chaque élément : il sert à créer les éléments JSX, ou à remplacer la tâche modifiée dans une nouvelle liste. <b>filter</b> conserve seulement les éléments qui satisfont une condition : il sélectionne les tâches restantes.')
    para('Cocher le filtre ne supprime aucune tâche. Le code calcule visibleTasks à partir de tasks. Si la liste visible est vide, React affiche « Aucune tâche ».')
    h('Identité et changement de statut')
    para('<b>key={task.id}</b> donne à React une identité stable pour chaque élément entre les rendus. Un changement de statut transmet task.id au parent. Dans la version finale, PATCH modifie done sur le serveur, puis map remplace la tâche dans l’état React.')
    shot(REACT,'Capture commune : Lire le rapport est barré et Vérifier les alertes ne l’est pas. La case de filtre est visible. Cette image ne montre pas encore les boutons de la version finale.',205)

    page('6 Synchroniser le titre de l’onglet','Hook : useEffect')
    code('const remainingCount = tasks.filter((task) => !task.done).length\n\nuseEffect(() => {\n  document.title = `${remainingCount} tâche(s) restante(s)`\n}, [remainingCount])')
    h('Pourquoi utiliser un effet')
    para('document.title appartient au document du navigateur, en dehors du JSX retourné par le composant. useEffect sert ici à synchroniser ce titre avec les données React après le rendu. L’effet s’exécute au montage et lorsque remainingCount change.')
    para('Le tableau [remainingCount] indique la dépendance. Un nouveau rendu où ce nombre reste identique ne demande pas de répéter cet effet. En développement, StrictMode peut provoquer un cycle supplémentaire de vérification des effets.')
    shot(REACT,'Capture : le titre de l’onglet commence par « 1 tâche(s) », ce qui correspond à la seule tâche non terminée affichée.',250)
    h('Flux à expliquer')
    para('tasks → sélection des tâches non terminées → nombre remainingCount → useEffect → document.title. Le filtre d’affichage ne change pas ce compteur, car il est calculé à partir de toutes les tâches.')

    page('7 Créer et tester la petite API','Fichier : api/main.py')
    code('app = FastAPI()\n\n@app.get("/tasks")\ndef get_tasks():\n    return tasks')
    para('React et FastAPI fonctionnent dans <b>deux programmes distincts</b>. Dans ce TP, ils tournent sur le même ordinateur. React est ouvert sur localhost:5173 ; Uvicorn écoute l’API sur 127.0.0.1:8000. CORS autorise le navigateur à lire les réponses de l’API depuis l’origine http://localhost:5173.')
    shot('59ffce10-7bf8-4c4d-b3b5-8a156fb0092a','Capture GET : l’exécution de /tasks renvoie le code 200 et les deux objets JSON. 200 signifie que la requête a réussi.',280,region=(12,440,750,735))
    h('Adresse et route')
    para('<b>127.0.0.1</b> désigne cet ordinateur, <b>8000</b> est le port et <b>/tasks</b> est la route demandée. /docs affiche la documentation interactive. La route / n’étant pas définie, elle renvoie Not Found ; cela ne signifie pas que le serveur est arrêté.')

    page('8 Charger les tâches depuis l’API','Fichier : src/App.jsx')
    code('const API_URL = \'http://127.0.0.1:8000/tasks\'\nconst [tasks, setTasks] = useState([])\nconst [loading, setLoading] = useState(true)\nconst [error, setError] = useState(\'\')\n\n// Dans la fonction asynchrone appelée par useEffect :\nconst response = await fetch(API_URL)\nif (!response.ok) throw new Error(`Erreur HTTP ${response.status}`)\nconst data = await response.json()\nsetTasks(data)')
    h('HTTP JSON et await')
    para('<b>HTTP</b> est le protocole des échanges entre client et serveur. <b>JSON</b> est un format textuel de données. response.json() lit le corps de la réponse et le transforme en données JavaScript. <b>await</b> suspend la suite de la fonction asynchrone jusqu’au résultat, sans bloquer l’interface.')
    para('fetch ne rejette pas automatiquement une réponse HTTP 404 ou 500 : response.ok doit être contrôlé. Le catch renseigne error et le finally termine loading. Le JSX affiche Chargement..., une erreur, ou la liste. Le code complet en annexe évite aussi les mises à jour d’un effet devenu inactif avec cancelled.')
    shot(REACT,'Capture de l’étape 8 : les deux tâches sont affichées après le chargement. Le formulaire et le filtre sont conservés.',190)

    page('9 Créer une tâche avec POST','API et React')
    code('const created = await request(API_URL, {\n  method: \'POST\',\n  headers: { \'Content-Type\': \'application/json\' },\n  body: JSON.stringify({ title }),\n})\nif (created) setTasks((currentTasks) => [...currentTasks, created])')
    para('JSON.stringify transforme l’objet JavaScript en texte JSON pour l’envoi. FastAPI valide le titre avec TaskCreate, construit un identifiant et retourne la tâche créée avec le statut <b>201</b>. React ajoute cet objet à sa liste après réussite.')
    shot('61c63c2f-248b-44b4-a0b9-6a3dd7539993','Capture POST fournie : Préparer le cours a été créé avec id 3 et done false. Le code 201 confirme la création.',315,region=(5,160,505,351))
    para('<b>Validation :</b> POST a été testé dans /docs puis depuis le formulaire React. La tâche de validation reste visible après un rechargement du navigateur, ce qui confirme son retour depuis l’API. Les captures du cycle React figurent après les essais DELETE.')

    page('9 Modifier une tâche avec PATCH','Route : /tasks/{task_id}')
    code('const updated = await request(`${API_URL}/${taskId}`, {\n  method: \'PATCH\',\n  headers: { \'Content-Type\': \'application/json\' },\n  body: JSON.stringify({ done: !task.done }),\n})\nif (updated) {\n  setTasks((currentTasks) =>\n    currentTasks.map((t) => t.id === taskId ? updated : t))\n}')
    para('task_id identifie la tâche à modifier. Le corps contient seulement les propriétés à changer. Le serveur utilise model_dump(exclude_unset=True) pour conserver les propriétés non envoyées, notamment le titre.')
    shot('96bd5770-8d28-4f65-b837-12b2c64fa49f','Capture PATCH : la tâche 3 conserve son titre et passe à done true. Le code 200 confirme la modification.',300,region=(6,164,506,345))
    para('Dans TaskItem, le bouton Changer le statut appelle onToggle(task.id). App transmet toggleTask comme callback. Le texte est barré lorsque task.done est vrai. L’utilisateur a également signalé que ce changement fonctionne dans l’interface React.')

    page('9 Supprimer une tâche avec DELETE','Route : /tasks/{task_id}')
    code('const result = await request(`${API_URL}/${taskId}`, {\n  method: \'DELETE\',\n})\nif (result) {\n  setTasks((currentTasks) =>\n    currentTasks.filter((t) => t.id !== taskId))\n}')
    para('FastAPI retrouve la tâche, la retire de la liste Python et retourne {"deleted": task_id}. Après réussite, filter construit la liste React sans cet identifiant. Le bouton Supprimer et le bouton Changer le statut sont placés dans le même li, sans être imbriqués.')
    shot('ef22c6b4-fa02-4022-a5fd-3e07ee61a7e8','Capture DELETE : le serveur répond 200 avec deleted égal à 3. La tâche de test a été supprimée.',250,region=(3,0,508,182))
    para('La fonction request vérifie response.ok et affiche actionError en cas d’échec. Elle retourne null en cas d’erreur ; les fonctions d’action n’appliquent alors aucun changement à tasks. L’utilisateur a signalé une suppression réussie depuis React.')

    page('9 Vérifier les actions dans React')
    para('Essais réalisés dans le navigateur le 24 octobre 2026. Une seule tâche temporaire a été créée puis supprimée ; la tâche existante Vérifier les alertes a été conservée.')
    shot('13-react-post-apres-rechargement.png','POST depuis React : la tâche de validation reste présente après rechargement.',90,region=(70,0,1210,250))
    shot('14-react-patch-terminee.png','PATCH depuis React : la tâche est barrée et le compteur diminue.',90,region=(70,0,1210,250))
    shot('15-react-filtre-restantes.png','Filtre coché : la tâche terminée est masquée, sans être supprimée.',90,region=(70,0,1210,250))
    shot('16-react-delete-apres-rechargement.png','DELETE puis rechargement : la tâche de validation est absente.',90,region=(70,0,1210,250))

    page('Serveur mémoire et limites du projet')
    h('Où se trouve le serveur')
    para('Uvicorn est installé dans le dossier .venv du projet parent. Son exécutable existe sur le disque ; le serveur en activité est un processus qui utilise la RAM du PC. Il n’a pas de bureau graphique. /docs est une interface de test de l’API fournie par FastAPI.')
    para('La case « Impression élégante » du navigateur sert simplement à présenter le JSON avec des retraits et des retours à la ligne. Elle ne lance aucune impression et ne modifie ni les tâches ni le serveur.')
    h('Ce qui reste après un rechargement')
    para('Recharger React relance le chargement GET : les données encore présentes dans la liste Python reviennent. En revanche, arrêter ou redémarrer le processus de l’API réinitialise cette liste à partir du fichier main.py. --reload peut provoquer ce redémarrage après une modification du code.')
    para('Une base de données permettrait de conserver les changements durablement. Elle n’est pas utilisée dans ce TP. Uvicorn reste un véritable serveur même lorsque le stockage est une simple liste en mémoire.')
    h('Limites de cette version pédagogique')
    para('L’API n’a pas d’authentification. Elle ne rejette pas encore les titres composés uniquement d’espaces côté serveur. TaskUpdate accepte aussi null, même si l’interface normale envoie un booléen pour done. Les requêtes simultanées et les clics répétés ne sont pas gérés comme dans une application complète. Ces points ne bloquent pas les essais demandés, mais doivent être améliorés pour un usage plus large.')
    h('Bilan des vérifications')
    para('GET : capture 200 avec la liste. POST : capture 201 avec la tâche 3. PATCH : capture 200 avec done true. DELETE : capture 200 avec deleted 3. React : création suivie d’un rechargement, changement de statut, filtre et suppression suivie d’un rechargement vérifiés et capturés. Les tests isolés HTTP et les contrôles GitHub ont également réussi.')
    h('Explication orale proposée')
    para('« React est le client. Quand j’effectue une action, il envoie une requête HTTP à l’API. Uvicorn reçoit cette requête et FastAPI exécute la route correspondante. Le serveur renvoie du JSON. Après une réponse réussie, React met son état à jour et actualise la page. Les données du serveur restent ici en mémoire et ne survivent pas à un redémarrage. »')

    # Reproduce the real final files without modifying the user's project.
    srcout=OUT/'code-final';srcout.mkdir(exist_ok=True)
    for rel in ['javascript-basics.js','api/main.py','src/App.jsx','src/main.jsx']:
        text=(PROJECT/rel).read_text(encoding='utf-8')
        dst=srcout/rel;dst.parent.mkdir(exist_ok=True,parents=True);dst.write_text(text,encoding='utf-8')
        lines=text.splitlines()
        # Only reproduce relevant code; comments documenting types are retained.
        chunks=[];chunk=[]
        for lineno,line in enumerate(lines,1):
            wrapped=textwrap.wrap(line,104,replace_whitespace=False,drop_whitespace=False) or ['']
            for j,part in enumerate(wrapped):
                chunk.append((f'{lineno:3} ' if j==0 else '    ')+part)
                if len(chunk)==49:chunks.append(chunk);chunk=[]
        if chunk:chunks.append(chunk)
        for k,part in enumerate(chunks):
            page('Annexe du code final',f'{rel} • partie {k+1} sur {len(chunks)} • Copie du fichier relu')
            c.setFont('Mono',8.2);c.setFillColor(HexColor('#17374e'))
            for line in part:c.drawString(44,y,line);y-=12
    c.save()
    doc=pdfium.PdfDocument(str(P));thumbs=[]
    for i in range(len(doc)):
        im=doc[i].render(scale=1.25).to_pil();im.save(QA/f'page-{i+1:02}.png')
        thumbs.append(im.resize((306,396)))
    sheet=Image.new('RGB',(306*4,396*math.ceil(len(thumbs)/4)),'#d6dce4')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*306,(i//4)*396))
    sheet.save(QA/'pdf-planche.jpg')
    print('PDF pages:',len(doc),flush=True)
    return P

if __name__=='__main__':
    import sys
    if 'pdf' in sys.argv: pdf()
    else: video()
