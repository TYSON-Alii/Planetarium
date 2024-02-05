import os, io, time
from PIL import Image, ImageDraw
import discord
from random import *
api = "your bot api is here"
# produce continuously
create_everytime = True
guild_id = 0 # your guild id
channel_id = 0 # channel id
seed(time.time())
from math import *
from colorsys import hsv_to_rgb
def mul3(c1, c2): return (c1[0] * c2[0], c1[1] * c2[1], c1[2] * c2[2])
def col(c): return (c, c, c, c)
def cast3(c): return (int(c[0]), int(c[1]), int(c[2]))
def alpha(c, a): return (c[0], c[1], c[2], a)
def to_rgb(c): return cast3((c[0]*255, c[1]*255, c[2]*255))
def limit(c): return ((c+1) if c < 0 else ((c-1) if c > 1 else c)) 
def r_color(): return to_rgb(hsv_to_rgb(uniform(0,1), 1, 1))
def prob(p): return randint(0,100) < p
uf = uniform
rint = randint
def create_pla(yem=None):
  if yem == None: yem = time.time()
  seed(yem)
  #init pla
  w, h = 32, 32
  ow, oh = w*3, h*3
  out = Image.new("RGBA", (ow, oh), (0,0,0,0))
  #colors
  bc1 = uf(0,1)
  bc2 = limit(bc1+choice([uf(1/16,1/2), uf(-1/2,-1/16)])) 
  rl = rint(1,7) + uf(0,1)
  rb = uf(-0.2,0.2)
  cw, cb = uf(0.4,0.95), uf(0.6,0.95)
  #planet
  im = Image.new('RGBA', (w, h), (0,0,0,0)) 
  pix = im.load()
  t = 0
  for x in range(0,w):
    t = x/rl
    for y in range(0,h):
      rc = uf(-0.1,0.1) 
      c1 = to_rgb(
        hsv_to_rgb(
          limit(bc1+rc),cw,cb)) 
      c2 = to_rgb(
        hsv_to_rgb(
          limit(bc2+rc),cw,cb)) 
      s = sin(t)
      ds = (s+1)/2 *100
      pix[x,y] = c2 if prob(ds+10)else c1
      t += 0.5 + rb
  mask = Image.new('L', (w, h), 0)
  draw = ImageDraw.Draw(mask)
  ekx, eky = rint(0,3),rint(0,3)
  draw.ellipse((0, 0, w, h), fill=255)
  pla = Image.new('RGBA',(w+ekx,h+eky),(0,0,0,0))
  pla.paste(im, (0, 0), mask)
  #rings
  cr = uf(0, 1)
  cw, cb = uf(0.4,0.95), uf(0.4,0.95)
  rot = rint(0,360) 
  r = rint(0,3)
  qs = []
  for n in range(r):
    rs = rint(300,500)
    sx, sy = uf(0.5,1), uf(1.5,2)
    acr = uf(-0.1, 0.1) 
    q = Image.new('RGBA', (ow, oh), (0,0,0,0)) 
    hpix = q.load()
    mw, mh = w/2,h/2
    fr = sqrt(mw**2+mh**2) 
    for x in range(0,ow):
      for y in range(0,oh):
        dx = abs(x-ow//2)*sx
        dy = abs(y-oh//2)*sy
        dr = sqrt(dx**2+dy**2)
        if not prob((abs(fr-dr)**1/fr**1) *rs):
          rc = uf(-0.1,0.1)
          hpix[x, y] = to_rgb(
            hsv_to_rgb(
              limit(cr+acr+rc), cw, cb))
    ai = Image.new('RGBA', (ow, oh//2), (0,0,0,0))
    ro = rint(1,10)
    q1, q2 = q.copy(), q.copy()
    q1.paste(ai, (0,0))
    q2.paste(ai, (0,oh//2))
    qs.append([q1.rotate(rot*n/r+ro), q2.rotate(rot*n/r+ro)])
  for q in qs:
    out.paste(q[0], (0,0), q[0])
  out.paste(pla, (ow//2-w//2, oh//2-h//2), pla)
  for q in qs:
    out.paste(q[1], (0,0), q[1]) 
  #flag
  def to_t(c):
    return to_rgb(hsv_to_rgb(c, 0.9, 0.9))
  colors = [to_t(bc1), to_t(bc2)]
  colors += [(0,0,0,255)]*rint(0,5)
  size = 8
  fim = Image.new('RGBA', (size, size), (255, 255, 255, 255))
  pix = fim.load()
  for x in range(size):
    for y in range(size):
      pix[x,y] = choice(colors)
  nim = Image.new('RGBA', (size*2, size), (255, 255, 255, 255)) 
  nim.paste(fim, (0,0))
  fim = fim.transpose(Image.FLIP_LEFT_RIGHT) 
  nim.paste(fim, (size,0))
  #falan
  out = out.resize((500,500), resample=Image.NEAREST)
  im = im.resize((500,500), resample=Image.NEAREST) 
  nim = nim.resize((1000,500), resample=Image.NEAREST) 
  fim = Image.new('RGBA', (1000, 1000), (0, 0, 0, 255))
  fim.paste(out, (0,0), out)
  fim.paste(im, (500,0))
  fim.paste(nim, (0,500))
  return [out,im,nim,yem,fim]  
  
def save_im(im, fn="anan"):
  with io.BytesIO() as bin:
    im.save(bin, "PNG", quality=90, optimize=True, progressive=True)
    bin.seek(0)
    return discord.File(fp=bin, filename=fn+'.png')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
def wait(): time.sleep(0.5)

@client.event
async def on_ready():
  print("basladi")
  g = client.get_guild(guild_id)
  c = g.get_channel(channel_id)
  while create_everytime:
    pla = create_pla()
    await c.send(file=save_im(pla[1]))
    await c.send(file=save_im(pla[0]))
    await c.send(file=save_im(pla[2]))
    await c.send(pla[3],file=save_im(pla[4]))
    wait()

@client.event 
async def on_message(messages):
  mes = messages
  user = messages.author
  ch = messages.channel
  mess = mes.content.lower()
  mesl = mess.split()
  pla = None
  if len(mesl) == 2 and mesl[0] == 'qf':
    pla = create_pla(float(mess[2:]))
  elif len(mesl) >= 2 and mesl[0] == 'q':
    pla = create_pla(mess[2:])
  if pla:
    await ch.send(file=save_im(pla[1]))
    await ch.send(file=save_im(pla[0]))
    await ch.send(file=save_im(pla[2]))
    await ch.send(file=save_im(pla[4], pla[3])) 
client.run(api)
